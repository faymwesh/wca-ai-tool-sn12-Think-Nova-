import unittest

from financial_system.financial_calculator import (
    answer_financial_question,
    calculate_financial_data,
)
from financial_system.expense_categorizer import categorize_expense


class FinancialCalculatorTests(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            {
                "transaction_type": "Income",
                "amount": 5000,
                "category": "Income",
            },
            {
                "transaction_type": "Expense",
                "amount": 700,
                "category": "Food",
            },
            {
                "transaction_type": "Expense",
                "amount": 300,
                "category": "Transport",
            },
        ]

    def test_calculate_financial_data(self):
        data = calculate_financial_data(self.transactions)
        self.assertEqual(data["total_income"], 5000)
        self.assertEqual(data["total_expenses"], 1000)
        self.assertEqual(data["balance"], 4000)
        self.assertEqual(data["categories"], {"Food": 700, "Transport": 300})

    def test_answer_common_questions(self):
        self.assertEqual(
            answer_financial_question("How much did I earn?", self.transactions),
            "Total income: KES 5,000.00",
        )
        self.assertEqual(
            answer_financial_question("How much did I spend?", self.transactions),
            "Total expenses: KES 1,000.00",
        )
        self.assertEqual(
            answer_financial_question("What is my balance?", self.transactions),
            "Remaining balance: KES 4,000.00",
        )
        self.assertEqual(
            answer_financial_question(
                "How much did I spend on food?", self.transactions
            ),
            "Food expenses: KES 700.00",
        )
        self.assertEqual(
            answer_financial_question(
                "What is my largest category?", self.transactions
            ),
            "Largest expense category: Food (KES 700.00)",
        )

    def test_manual_expense_categories(self):
        self.assertEqual(categorize_expense("shopping"), "Shopping")
        self.assertEqual(categorize_expense("transport"), "Transport")
        self.assertEqual(categorize_expense("communication"), "Communication")
        self.assertEqual(categorize_expense("mobile data bundle"), "Communication")


if __name__ == "__main__":
    unittest.main()
