import math
import re
from datetime import date
from decimal import Decimal, InvalidOperation

from financial_system.expense_categorizer import categorize_expense


def process_mpesa_sms(message):
    """Parse an M-Pesa SMS into a transaction, or return None if unrecognized."""
    if not isinstance(message, str):
        return None

    code = re.search(r"\b[A-Z0-9]{10}\b", message, re.IGNORECASE)
    amount_match = re.search(
        r"\b(?:Ksh|KES)\s*([\d,]+(?:\.\d{1,2})?)",
        message,
        re.IGNORECASE,
    )

    if re.search(r"\breceived\b", message, re.IGNORECASE):
        transaction_type = "Income"
    elif re.search(r"\b(?:paid|sent)\b", message, re.IGNORECASE):
        transaction_type = "Expense"
    else:
        return None

    counterparty = re.search(
        r"\b(?:paid to|sent to|received from)\s+(.+?)(?:[.;]|$)",
        message,
        re.IGNORECASE,
    )
    if amount_match is None or counterparty is None:
        return None

    description = counterparty.group(1).strip()
    if not description:
        return None

    try:
        amount_value = float(
            Decimal(amount_match.group(1).replace(",", ""))
        )
    except (InvalidOperation, OverflowError):
        return None
    if not math.isfinite(amount_value) or amount_value <= 0:
        return None

    return {
        "transaction_id": code.group() if code else None,
        "amount": amount_value,
        "transaction_type": transaction_type,
        "description": description,
        "category": categorize_expense(description),
        "date": date.today().isoformat(),
    }