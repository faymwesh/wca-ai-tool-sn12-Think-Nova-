import re

def process_mpesa_sms(message):
    # Extract transaction code
    code = re.search(r'\b[A-Z0-9]{10}\b', message)

    # Extract amount
    amount = re.search(
        r'Ksh\s*([\d,]+\.\d{2})',
        message,
        re.IGNORECASE
    )

    # Identify transaction type
    message_lower = message.lower()

    if "received" in message_lower:
        transaction_type = "Income"
    elif "paid" in message_lower or "sent" in message_lower:
        transaction_type = "Expense"
    else:
        transaction_type = "Unknown"

    # Extract description
    description = "Unknown"
    if "paid to" in message_lower:
        description = message.split("paid to", 1)[1].strip().rstrip(".")
    elif "received from" in message_lower:
        description = message.split("received from", 1)[1].strip().rstrip(".")

    # Return structured transaction data
    return {
        "transaction_id": code.group() if code else None,
        "amount": float(amount.group(1).replace(",", "")) if amount else None,
        "transaction_type": transaction_type,
        "description": description,
        "category": "Uncategorised"
    }