expenses = []

def add_expense(name, amount, category):
    expense = {
        "name": name,
        "amount": float(amount),
        "category": category
    }

    expenses.append(expense)
    print("Expense recorded successfully!")


def show_expenses():
    print("\n--- EXPENSE RECORDS ---")

    for expense in expenses:
        print(
            expense["name"],
            expense["amount"],
            expense["category"]
        )


def calculate_total():
    total = 0

    for expense in expenses:
        total += expense["amount"]

    print("Total expenses: KSh", total)


# Test the system
add_expense("Shopping", 500, "Food")
add_expense("Fare", 200, "Transport")
add_expense("Airtime", 100, "Communication")

show_expenses()
calculate_total()
transaction = {
    "transaction_id": "QAB123XYZ",
    "amount": 500.00,
    "transaction_type": "expense",
    "description": "Naivas Supermarket",
    "category": "Shopping",
    "date": "2026-11-12"
}