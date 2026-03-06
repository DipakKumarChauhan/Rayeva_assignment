"""
Tests for Module 1: AI Auto-Category & Tag Generator
Uses mocked Gemini responses to avoid real API calls.
"""
import json
import unittest
from unittest.mock import MagicMock, patch

from app.config import settings


class TestCategorizer(unittest.TestCase):

    MOCK_AI_RESPONSE = json.dumps({
        "primary_category": "Personal Care",
        "sub_category": "Oral Hygiene",
        "seo_tags": [
            "bamboo toothbrush",
            "eco-friendly toothbrush",
            "sustainable oral care",
            "biodegradable toothbrush",
            "BPA-free toothbrush",
            "zero-waste dental",
        ],
        "sustainability_filters": ["plastic-free", "biodegradable", "vegan"],
    })

    @patch("app.services.categorizer.call_gemini")
    @patch("app.services.categorizer.get_connection")
    def test_categorize_product_returns_output(self, mock_conn_factory, mock_gemini):
        """Module 1 should parse AI response and return a ProductCategoryOutput."""
        mock_gemini.return_value = self.MOCK_AI_RESPONSE

        mock_conn = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn_factory.return_value = mock_conn

        from app.services.categorizer import categorize_product

        result = categorize_product(
            name="Bamboo Toothbrush",
            description="Eco-friendly bamboo toothbrush with BPA-free soft bristles. Fully biodegradable.",
        )

        self.assertEqual(result.primary_category, "Personal Care")
        self.assertEqual(result.sub_category, "Oral Hygiene")
        self.assertIn("bamboo toothbrush", result.seo_tags)
        self.assertIn("plastic-free", result.sustainability_filters)
        self.assertGreaterEqual(len(result.seo_tags), 5)

    def test_validate_category_falls_back(self):
        """Unknown AI category should fall back to the first item in the predefined list."""
        from app.services.categorizer import _validate_category

        result = _validate_category("Completely Unknown Category XYZ")
        self.assertEqual(result, settings.PRODUCT_CATEGORIES[0])

    def test_validate_filters_ignores_unknown(self):
        """Filters not in the predefined list should be silently dropped."""
        from app.services.categorizer import _validate_filters

        result = _validate_filters(["plastic-free", "not-a-real-filter", "vegan"])
        self.assertIn("plastic-free", result)
        self.assertIn("vegan", result)
        self.assertNotIn("not-a-real-filter", result)

    def test_sanitize_tags_caps_at_10(self):
        """SEO tag list must be capped at 10 items."""
        from app.services.categorizer import _sanitize_tags

        tags = [f"tag-{i}" for i in range(15)]
        result = _sanitize_tags(tags)
        self.assertLessEqual(len(result), 10)


if __name__ == "__main__":
    unittest.main()
