import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main
from financial_system.expense_manager import calculate_total, expenses
from financial_system.mpesa_processor import process_mpesa_sms


class MpesaProcessorTests(unittest.TestCase):
    def tearDown(self):
        expenses.clear()

    def test_income_sms_is_recorded_as_income(self):
        message = "QBC456XYZ1 Confirmed. Ksh5,000.00 received from Employer."
        transaction = process_mpesa_sms(message)
        self.assertEqual(transaction["transaction_type"], "Income")
        self.assertEqual(transaction["amount"], 5000.0)

        with patch("builtins.input", side_effect=["2", message, "", ""]):
            with redirect_stdout(io.StringIO()):
                records = main.record_expenses()

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["transaction_type"], "Income")
        self.assertEqual(records[0]["category"], "Income")

    def test_manual_income_uses_user_entered_amount(self):
        with patch(
            "builtins.input",
            side_effect=["1", "", "12,500.50", "Salary"],
        ):
            with redirect_stdout(io.StringIO()):
                records = main.record_expenses()

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["amount"], 12500.5)
        self.assertEqual(records[0]["description"], "Salary")
        self.assertEqual(records[0]["transaction_type"], "Income")
        self.assertEqual(records[0]["category"], "Income")

    def test_invalid_manual_income_is_rejected_before_valid_amount(self):
        with patch(
            "builtins.input",
            side_effect=["1", "", "not-an-amount", "0", "2500", ""],
        ):
            output = io.StringIO()
            with redirect_stdout(output):
                records = main.record_expenses()

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["amount"], 2500)
        self.assertEqual(output.getvalue().count(
            "Enter a valid income amount greater than zero."
        ), 2)

    def test_zero_amount_sms_is_rejected(self):
        message = "QAB123XYZ0 Confirmed. Ksh0.00 paid to Naivas Supermarket."
        self.assertIsNone(process_mpesa_sms(message))

    def test_expense_total_excludes_income(self):
        expenses.extend([
            {"amount": 5000.0, "transaction_type": "Income"},
            {"amount": 700.0, "transaction_type": "Expense"},
        ])
        output = io.StringIO()
        with redirect_stdout(output):
            calculate_total()
        self.assertIn("700.0", output.getvalue())


if __name__ == "__main__":
    unittest.main()
