"""
Router for Module 1: AI Auto-Category & Tag Generator
"""
from fastapi import APIRouter, HTTPException

from app.models.product import ProductCategoryOutput, ProductInput, ProductListResponse
from app.services.categorizer import (
    categorize_product,
    get_all_products,
    get_product_by_id,
)

router = APIRouter(prefix="/api/v1/catalog", tags=["Module 1 — Catalog"])


@router.post(
    "/categorize",
    response_model=ProductCategoryOutput,
    summary="Categorize a product using AI",
    description=(
        "Accepts a product name and description. "
        "Uses Gemini AI to assign a primary category, sub-category, "
        "5–10 SEO tags, and applicable sustainability filters. "
        "Result is stored in the database."
    ),
)
def categorize(payload: ProductInput) -> ProductCategoryOutput:
    try:
        return categorize_product(name=payload.name, description=payload.description)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI categorization failed: {exc}") from exc


@router.get(
    "/products",
    response_model=ProductListResponse,
    summary="List all categorized products",
)
def list_products() -> ProductListResponse:
    products = get_all_products()
    return ProductListResponse(total=len(products), products=products)


@router.get(
    "/products/{product_id}",
    response_model=ProductCategoryOutput,
    summary="Get a single categorized product",
)
def get_product(product_id: str) -> ProductCategoryOutput:
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
