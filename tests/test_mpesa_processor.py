import unittest

from financial_system.mpesa_processor import process_mpesa_sms


class TestMpesaProcessor(unittest.TestCase):

    def test_expense_transaction(self):
        message = "QAB123XYZ0 Confirmed. Ksh500.00 paid to Naivas Supermarket."
        result = process_mpesa_sms(message)

        self.assertEqual(result["transaction_id"], "QAB123XYZ0")
        self.assertEqual(result["amount"], 500.0)
        self.assertEqual(result["transaction_type"], "Expense")
        self.assertEqual(result["description"], "Naivas Supermarket")

    def test_income_transaction(self):
        message = "QBC456XYZ1 Confirmed. Ksh2,500.00 received from John."
        result = process_mpesa_sms(message)

        self.assertEqual(result["amount"], 2500.0)
        self.assertEqual(result["transaction_type"], "Income")
        self.assertEqual(result["description"], "John")

    def test_unknown_transaction_type(self):
        message = "QCD789XYZ2 Confirmed. Ksh200.00 transaction completed."
        result = process_mpesa_sms(message)

        self.assertEqual(result["transaction_type"], "Unknown")

    def test_missing_amount(self):
        message = "QCD789XYZ2 Transaction completed."
        result = process_mpesa_sms(message)

        self.assertIsNone(result["amount"])


if __name__ == "__main__":
    unittest.main()