"""
Pydantic models for Module 2: AI B2B Proposal Generator.
"""
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class ProductRecommendation(BaseModel):
    product_name: str
    category: str
    sustainability_attributes: List[str]
    quantity: int
    unit_price: float
    total_price: float
    reason: str


class B2BProposalInput(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=200)
    industry: str = Field(..., min_length=2, max_length=100)
    budget: float = Field(..., gt=0, description="Total budget in INR")
    preferences: List[str] = Field(default=[], description="Sustainability preferences")
    quantity_needed: int = Field(..., gt=0, description="Total units needed")
    use_case: str = Field(..., min_length=5, max_length=500, description="Purpose of procurement")

    model_config = {
        "json_schema_extra": {
            "example": {
                "company_name": "GreenCorp Solutions",
                "industry": "Corporate Gifting",
                "budget": 50000,
                "preferences": ["plastic-free", "vegan", "recycled"],
                "quantity_needed": 100,
                "use_case": "Employee gifting for Earth Day 2025",
            }
        }
    }


class B2BProposalOutput(BaseModel):
    proposal_id: str
    company_name: str
    industry: str
    total_budget: float
    preferences: List[str]
    quantity_needed: int
    use_case: str
    product_mix: List[ProductRecommendation]
    budget_allocation: Dict[str, float]
    estimated_cost_breakdown: Dict[str, Any]
    impact_summary: str
    raw_ai_response: str
    created_at: str


class ProposalListResponse(BaseModel):
    total: int
    proposals: List[B2BProposalOutput]
