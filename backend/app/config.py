"""
Configuration module — loads environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DB_PATH: str = os.getenv("DB_PATH", "sustainable_commerce.db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Predefined product categories
    PRODUCT_CATEGORIES: list[str] = [
        "Food & Beverage",
        "Personal Care",
        "Home & Living",
        "Clothing & Apparel",
        "Electronics",
        "Stationery & Office",
        "Fitness & Wellness",
        "Pet Supplies",
        "Baby & Kids",
        "Outdoor & Garden",
    ]

    # Recognised sustainability filters
    SUSTAINABILITY_FILTERS: list[str] = [
        "plastic-free",
        "compostable",
        "vegan",
        "recycled",
        "organic",
        "zero-waste",
        "fair-trade",
        "biodegradable",
        "carbon-neutral",
        "locally-sourced",
    ]


settings = Settings()
