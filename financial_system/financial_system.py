from mpesa_processor import process_mpesa_sms
from transaction_storage import save_transaction

# Sample M-Pesa messages
messages = [
    "QAB123XYZ0 Confirmed. Ksh500.00 paid to Naivas Supermarket.",
    "QBC456XYZ1 Confirmed. Ksh2,500.00 received from John.",
    "QCD789XYZ2 Confirmed. Ksh200.00 paid to Uber."
]

# Process and save each message
for message in messages:

    transaction = process_mpesa_sms(message)

    print("\nProcessing transaction...")

    if transaction["amount"] :
        if transaction["transaction_type"] != "Unknown":
            save_transaction(transaction)
        else:
            print("Unknown transaction type. Not saved.")
    else:
        print("Invalid amount. Not saved.")

print("\nAll messages processed!")