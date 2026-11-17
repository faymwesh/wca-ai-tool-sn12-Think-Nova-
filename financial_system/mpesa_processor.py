import re

def process_mpesa_sms(message):

    # Extract transaction code
    code = re.search(r'\b[A-Z0-9]{10}\b', message)

    # Extract amount
    amount = re.search(r'Ksh([\d,]+\.\d{2})', message, re.IGNORECASE)

    # Extract transaction type
    if "received" in message.lower():
        transaction_type = "Income"

    elif "paid" in message.lower() or "sent" in message.lower():
        transaction_type = "Expense"

    else:
        transaction_type = "Unknown"

    # Display extracted information
    print("Transaction Code:", code.group() if code else "Not found")

    print("Amount:", amount.group(1) if amount else "Not found")

    print("Transaction Type:", transaction_type)


# Sample M-Pesa SMS
sms = "QAB123XYZ0 Confirmed. Ksh500.00 paid to Naivas Supermarket."

process_mpesa_sms(sms)