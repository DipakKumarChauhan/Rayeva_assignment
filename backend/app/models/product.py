"""
Pydantic models for Module 1: AI Auto-Category & Tag Generator.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class ProductInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=200, description="Product name")
    description: str = Field(..., min_length=10, max_length=2000, description="Product description")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Bamboo Toothbrush",
                "description": "Eco-friendly bamboo toothbrush with BPA-free soft bristles. Fully biodegradable handle made from sustainably harvested bamboo.",
            }
        }
    }


class ProductCategoryOutput(BaseModel):
    product_id: str
    name: str
    description: str
    primary_category: str
    sub_category: str
    seo_tags: List[str] = Field(..., min_length=5, max_length=10)
    sustainability_filters: List[str]
    raw_ai_response: str
    created_at: str


class ProductListResponse(BaseModel):
    total: int
    products: List[ProductCategoryOutput]
