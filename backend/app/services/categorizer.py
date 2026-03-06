"""
Module 1: AI Auto-Category & Tag Generator

Business logic for categorising products using Gemini AI.
Separates AI prompting from data persistence and validation.
"""
import json
from typing import List

from app.config import settings
from app.database import get_connection, new_id, now_iso
from app.models.product import ProductCategoryOutput
from app.services.gemini import call_gemini, extract_json


# --------------------------------------------------------------------------- #
#  Prompt builder (pure function — no side effects)                            #
# --------------------------------------------------------------------------- #

def _build_prompt(name: str, description: str) -> str:
    categories = json.dumps(settings.PRODUCT_CATEGORIES)
    filters = json.dumps(settings.SUSTAINABILITY_FILTERS)

    return f"""You are an AI product cataloguing assistant for a sustainable e-commerce platform.

Given the product information below, return a valid JSON object with EXACTLY the following keys:
- "primary_category": one value chosen strictly from the allowed list
- "sub_category": a sensible sub-category string (not from a fixed list)
- "seo_tags": an array of 5 to 10 relevant SEO keywords/phrases
- "sustainability_filters": an array of applicable values chosen strictly from the allowed list (can be empty)

**Allowed primary categories (use exactly as written):**
{categories}

**Allowed sustainability filters (use exactly as written):**
{filters}

**Product:**
Name: {name}
Description: {description}

Respond with JSON only — no prose, no markdown fences, no extra text.
"""


# --------------------------------------------------------------------------- #
#  Core service function                                                        #
# --------------------------------------------------------------------------- #

def categorize_product(name: str, description: str) -> ProductCategoryOutput:
    """
    AI business logic:
      1. Build structured prompt
      2. Call Gemini (logged automatically)
      3. Parse + validate response
      4. Persist to DB
      5. Return typed output
    """
    prompt = _build_prompt(name, description)
    raw_response = call_gemini(module="module1_categorizer", prompt=prompt)

    # --- Parse AI response ---
    data = extract_json(raw_response)

    # --- Validate + sanitize against predefined lists ---
    primary_category = _validate_category(data.get("primary_category", ""))
    sustainability_filters = _validate_filters(data.get("sustainability_filters", []))
    seo_tags = _sanitize_tags(data.get("seo_tags", []))
    sub_category = str(data.get("sub_category", "General")).strip()

    # --- Persist to DB ---
    product_id = new_id()
    created_at = now_iso()

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO products
                (product_id, name, description, primary_category, sub_category,
                 seo_tags, sustainability_filters, raw_ai_response, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                product_id,
                name,
                description,
                primary_category,
                sub_category,
                json.dumps(seo_tags),
                json.dumps(sustainability_filters),
                raw_response,
                created_at,
            ),
        )
        conn.commit()
    finally:
        conn.close()

    return ProductCategoryOutput(
        product_id=product_id,
        name=name,
        description=description,
        primary_category=primary_category,
        sub_category=sub_category,
        seo_tags=seo_tags,
        sustainability_filters=sustainability_filters,
        raw_ai_response=raw_response,
        created_at=created_at,
    )


def get_all_products() -> List[ProductCategoryOutput]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM products ORDER BY created_at DESC"
        ).fetchall()
    finally:
        conn.close()

    return [_row_to_product(r) for r in rows]


def get_product_by_id(product_id: str) -> ProductCategoryOutput | None:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM products WHERE product_id = ?", (product_id,)
        ).fetchone()
    finally:
        conn.close()

    return _row_to_product(row) if row else None


# --------------------------------------------------------------------------- #
#  Helpers                                                                      #
# --------------------------------------------------------------------------- #

def _validate_category(value: str) -> str:
    for cat in settings.PRODUCT_CATEGORIES:
        if cat.lower() == value.lower():
            return cat
    # Fallback: pick closest match or first
    return settings.PRODUCT_CATEGORIES[0]


def _validate_filters(values: list) -> list:
    allowed = {f.lower(): f for f in settings.SUSTAINABILITY_FILTERS}
    return [allowed[v.lower()] for v in values if v.lower() in allowed]


def _sanitize_tags(tags: list) -> list:
    cleaned = [str(t).strip() for t in tags if str(t).strip()]
    return cleaned[:10] if len(cleaned) > 10 else (cleaned if len(cleaned) >= 5 else cleaned)


def _row_to_product(row: dict) -> ProductCategoryOutput:
    return ProductCategoryOutput(
        product_id=row["product_id"],
        name=row["name"],
        description=row["description"],
        primary_category=row["primary_category"],
        sub_category=row["sub_category"],
        seo_tags=json.loads(row["seo_tags"]),
        sustainability_filters=json.loads(row["sustainability_filters"]),
        raw_ai_response=row["raw_ai_response"],
        created_at=row["created_at"],
    )
