"""
Tests for Module 2: AI B2B Proposal Generator
Uses mocked Gemini responses to avoid real API calls.
"""
import json
import unittest
from unittest.mock import MagicMock, patch


class TestProposalGen(unittest.TestCase):

    MOCK_AI_RESPONSE = json.dumps({
        "product_mix": [
            {
                "product_name": "Recycled Notebook",
                "category": "Stationery & Office",
                "sustainability_attributes": ["recycled", "plastic-free"],
                "quantity": 50,
                "unit_price": 150.0,
                "total_price": 7500.0,
                "reason": "Perfect for corporate gifting, made from 100% recycled paper.",
            },
            {
                "product_name": "Bamboo Pen Set",
                "category": "Stationery & Office",
                "sustainability_attributes": ["biodegradable", "plastic-free"],
                "quantity": 50,
                "unit_price": 80.0,
                "total_price": 4000.0,
                "reason": "Eco-friendly alternative to plastic pens.",
            },
        ],
        "budget_allocation": {
            "Recycled Notebook": 7500.0,
            "Bamboo Pen Set": 4000.0,
        },
        "estimated_cost_breakdown": {
            "subtotal": 11500.0,
            "packaging": 500.0,
            "logistics": 800.0,
            "platform_fee": 200.0,
            "total": 13000.0,
        },
        "impact_summary": (
            "This procurement avoids ~2.5 kg of plastic waste. "
            "Both products are sourced from certified sustainable suppliers, "
            "contributing to a 30% reduction in carbon footprint versus conventional alternatives."
        ),
    })

    @patch("app.services.proposal_gen.call_gemini")
    @patch("app.services.proposal_gen.get_connection")
    def test_generate_proposal_returns_output(self, mock_conn_factory, mock_gemini):
        """Module 2 should parse AI response and return a B2BProposalOutput."""
        mock_gemini.return_value = self.MOCK_AI_RESPONSE

        mock_conn = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn_factory.return_value = mock_conn

        from app.services.proposal_gen import generate_proposal

        result = generate_proposal(
            company_name="GreenCorp Solutions",
            industry="Corporate Gifting",
            budget=50000,
            preferences=["plastic-free", "recycled"],
            quantity_needed=100,
            use_case="Employee gifting for Earth Day 2025",
        )

        self.assertEqual(result.company_name, "GreenCorp Solutions")
        self.assertEqual(len(result.product_mix), 2)
        self.assertIn("plastic-free", result.product_mix[0].sustainability_attributes)
        self.assertGreater(len(result.impact_summary), 10)
        self.assertIn("subtotal", result.estimated_cost_breakdown)

    @patch("app.services.proposal_gen.call_gemini")
    @patch("app.services.proposal_gen.get_connection")
    def test_proposal_within_budget(self, mock_conn_factory, mock_gemini):
        """Total cost in the proposal should not exceed the provided budget."""
        mock_gemini.return_value = self.MOCK_AI_RESPONSE

        mock_conn = MagicMock()
        mock_conn_factory.return_value = mock_conn

        from app.services.proposal_gen import generate_proposal

        budget = 50000.0
        result = generate_proposal(
            company_name="Test Corp",
            industry="Retail",
            budget=budget,
            preferences=[],
            quantity_needed=100,
            use_case="Product launch",
        )

        total = result.estimated_cost_breakdown.get("total", 0)
        self.assertLessEqual(total, budget)


if __name__ == "__main__":
    unittest.main()
