"""
Router for Module 2: AI B2B Proposal Generator
"""
from fastapi import APIRouter, HTTPException

from app.models.proposal import B2BProposalInput, B2BProposalOutput, ProposalListResponse
from app.services.proposal_gen import (
    generate_proposal,
    get_all_proposals,
    get_proposal_by_id,
)

router = APIRouter(prefix="/api/v1/proposals", tags=["Module 2 — B2B Proposals"])


@router.post(
    "/generate",
    response_model=B2BProposalOutput,
    summary="Generate a B2B sustainable procurement proposal",
    description=(
        "Accepts company details, budget, and sustainability preferences. "
        "Uses Gemini AI to generate a full proposal with product mix, "
        "budget allocation, cost breakdown, and impact summary. "
        "Result is stored in the database."
    ),
)
def generate(payload: B2BProposalInput) -> B2BProposalOutput:
    try:
        return generate_proposal(
            company_name=payload.company_name,
            industry=payload.industry,
            budget=payload.budget,
            preferences=payload.preferences,
            quantity_needed=payload.quantity_needed,
            use_case=payload.use_case,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Proposal generation failed: {exc}") from exc


@router.get(
    "/",
    response_model=ProposalListResponse,
    summary="List all B2B proposals",
)
def list_proposals() -> ProposalListResponse:
    proposals = get_all_proposals()
    return ProposalListResponse(total=len(proposals), proposals=proposals)


@router.get(
    "/{proposal_id}",
    response_model=B2BProposalOutput,
    summary="Get a single B2B proposal",
)
def get_proposal(proposal_id: str) -> B2BProposalOutput:
    proposal = get_proposal_by_id(proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal
