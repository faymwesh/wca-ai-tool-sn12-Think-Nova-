import json
import os


FILE_NAME = "transactions.json"


def save_transaction(transaction):

    transactions = []

    # Read existing transactions
    if os.path.exists(FILE_NAME):

        with open(FILE_NAME, "r") as file:
            try:
                transactions = json.load(file)
            except json.JSONDecodeError:
                transactions = []

    # Prevent duplicate transaction IDs
    transaction_id = transaction.get("transaction_id")

    if transaction_id and any(
        item.get("transaction_id") == transaction_id
        for item in transactions
    ):
        print("Transaction already exists!")
        return

    # Add new transaction
    transactions.append(transaction)

    # Save transactions
    with open(FILE_NAME, "w") as file:
        json.dump(transactions, file, indent=4)

    print("Transaction saved successfully!")


def view_transactions():

    if not os.path.exists(FILE_NAME):
        print("No transactions found.")
        return

    with open(FILE_NAME, "r") as file:
        transactions = json.load(file)

    print("\n--- SAVED TRANSACTIONS ---")

    for transaction in transactions:
        print(transaction)


# Test the storage system
sample_transaction = {
    "transaction_id": "QAB123XYZ0",
    "amount": 500.00,
    "transaction_type": "Expense",
    "description": "Naivas Supermarket",
    "category": "Shopping"
}

save_transaction(sample_transaction)

view_transactions()