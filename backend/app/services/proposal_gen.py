"""
Module 2: AI B2B Proposal Generator

Business logic for generating sustainable product procurement proposals.
Separates AI prompting from data persistence and validation.
"""
import json
from typing import List

from app.database import get_connection, new_id, now_iso
from app.models.proposal import B2BProposalOutput, ProductRecommendation
from app.services.gemini import call_gemini, extract_json


# --------------------------------------------------------------------------- #
#  Prompt builder                                                               #
# --------------------------------------------------------------------------- #

def _build_prompt(
    company_name: str,
    industry: str,
    budget: float,
    preferences: List[str],
    quantity_needed: int,
    use_case: str,
) -> str:
    prefs_str = ", ".join(preferences) if preferences else "no specific preferences"

    return f"""You are an AI sustainable procurement advisor for a B2B e-commerce platform.

Generate a detailed sustainable product procurement proposal with EXACTLY this JSON structure:
{{
  "product_mix": [
    {{
      "product_name": "<string>",
      "category": "<string>",
      "sustainability_attributes": ["<string>", ...],
      "quantity": <integer>,
      "unit_price": <float>,
      "total_price": <float>,
      "reason": "<string — why this fits the company/use-case>"
    }}
  ],
  "budget_allocation": {{
    "<category or product name>": <float — INR amount>
  }},
  "estimated_cost_breakdown": {{
    "subtotal": <float>,
    "packaging": <float>,
    "logistics": <float>,
    "platform_fee": <float>,
    "total": <float>
  }},
  "impact_summary": "<2–3 sentence human-readable sustainability impact statement>"
}}

**Rules:**
- product_mix must contain 3 to 6 products
- The sum of all total_price values in product_mix MUST be within the provided budget
- Each product must have at least one sustainability attribute
- budget_allocation values must sum to the subtotal in estimated_cost_breakdown
- estimated_cost_breakdown.total must not exceed the budget
- quantity values in product_mix must sum to approximately {quantity_needed}
- All monetary values are in INR

**Client Details:**
- Company: {company_name}
- Industry: {industry}
- Total Budget: ₹{budget:,.2f} INR
- Sustainability Preferences: {prefs_str}
- Total Quantity Needed: {quantity_needed} units
- Use Case: {use_case}

**CRITICAL**: Respond with ONLY valid JSON. No markdown code fences, no explanations, no prose before or after. 
The JSON must be complete and properly closed. Ensure all arrays and objects are fully closed.
"""


# --------------------------------------------------------------------------- #
#  Core service function                                                        #
# --------------------------------------------------------------------------- #

def generate_proposal(
    company_name: str,
    industry: str,
    budget: float,
    preferences: List[str],
    quantity_needed: int,
    use_case: str,
) -> B2BProposalOutput:
    """
    AI business logic:
      1. Build structured prompt with budget constraints
      2. Call Gemini (logged automatically)
      3. Parse + validate response
      4. Persist to DB
      5. Return typed output
    """
    prompt = _build_prompt(
        company_name=company_name,
        industry=industry,
        budget=budget,
        preferences=preferences,
        quantity_needed=quantity_needed,
        use_case=use_case,
    )

    raw_response = call_gemini(
        module="module2_proposal_gen",
        prompt=prompt,
        temperature=0.2,
        max_output_tokens=8192,
    )
    try:
        data = extract_json(raw_response)
    except ValueError:
        # One-shot JSON repair fallback: ask Gemini to output corrected JSON only.
        repair_prompt = f"""You are a JSON repair assistant.

Task: Convert the following text into valid JSON that matches EXACTLY this schema:
{{
  "product_mix": [
    {{
      "product_name": "<string>",
      "category": "<string>",
      "sustainability_attributes": ["<string>", ...],
      "quantity": <integer>,
      "unit_price": <float>,
      "total_price": <float>,
      "reason": "<string>"
    }}
  ],
  "budget_allocation": {{
    "<category or product name>": <float>
  }},
  "estimated_cost_breakdown": {{
    "subtotal": <float>,
    "packaging": <float>,
    "logistics": <float>,
    "platform_fee": <float>,
    "total": <float>
  }},
  "impact_summary": "<string>"
}}

Rules:
- Output JSON only (no markdown, no code fences, no commentary).
- Fix missing braces, commas, quotes, and any formatting issues.
- Preserve all values as much as possible; do not invent extra fields.

Text to repair:
{raw_response}
"""
        repaired = call_gemini(
            module="module2_proposal_json_repair",
            prompt=repair_prompt,
            temperature=0.0,
            max_output_tokens=8192,
        )
        data = extract_json(repaired)

    # --- Map product_mix to typed models ---
    product_mix = [
        ProductRecommendation(
            product_name=p.get("product_name", "Unknown"),
            category=p.get("category", "General"),
            sustainability_attributes=p.get("sustainability_attributes", []),
            quantity=int(p.get("quantity", 0)),
            unit_price=float(p.get("unit_price", 0.0)),
            total_price=float(p.get("total_price", 0.0)),
            reason=p.get("reason", ""),
        )
        for p in data.get("product_mix", [])
    ]

    budget_allocation: dict = data.get("budget_allocation", {})
    cost_breakdown: dict = data.get("estimated_cost_breakdown", {})
    impact_summary: str = data.get("impact_summary", "")

    # --- Persist ---
    proposal_id = new_id()
    created_at = now_iso()

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO proposals
                (proposal_id, company_name, industry, total_budget, preferences,
                 quantity_needed, use_case, product_mix, budget_allocation,
                 cost_breakdown, impact_summary, raw_ai_response, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                proposal_id,
                company_name,
                industry,
                budget,
                json.dumps(preferences),
                quantity_needed,
                use_case,
                json.dumps([p.model_dump() for p in product_mix]),
                json.dumps(budget_allocation),
                json.dumps(cost_breakdown),
                impact_summary,
                raw_response,
                created_at,
            ),
        )
        conn.commit()
    finally:
        conn.close()

    return B2BProposalOutput(
        proposal_id=proposal_id,
        company_name=company_name,
        industry=industry,
        total_budget=budget,
        preferences=preferences,
        quantity_needed=quantity_needed,
        use_case=use_case,
        product_mix=product_mix,
        budget_allocation=budget_allocation,
        estimated_cost_breakdown=cost_breakdown,
        impact_summary=impact_summary,
        raw_ai_response=raw_response,
        created_at=created_at,
    )


def get_all_proposals() -> List[B2BProposalOutput]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM proposals ORDER BY created_at DESC"
        ).fetchall()
    finally:
        conn.close()
    return [_row_to_proposal(r) for r in rows]


def get_proposal_by_id(proposal_id: str) -> B2BProposalOutput | None:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM proposals WHERE proposal_id = ?", (proposal_id,)
        ).fetchone()
    finally:
        conn.close()
    return _row_to_proposal(row) if row else None


# --------------------------------------------------------------------------- #
#  Helpers                                                                      #
# --------------------------------------------------------------------------- #

def _row_to_proposal(row) -> B2BProposalOutput:
    product_mix = [ProductRecommendation(**p) for p in json.loads(row["product_mix"])]
    return B2BProposalOutput(
        proposal_id=row["proposal_id"],
        company_name=row["company_name"],
        industry=row["industry"],
        total_budget=row["total_budget"],
        preferences=json.loads(row["preferences"]),
        quantity_needed=row["quantity_needed"],
        use_case=row["use_case"],
        product_mix=product_mix,
        budget_allocation=json.loads(row["budget_allocation"]),
        estimated_cost_breakdown=json.loads(row["cost_breakdown"]),
        impact_summary=row["impact_summary"],
        raw_ai_response=row["raw_ai_response"],
        created_at=row["created_at"],
    )
