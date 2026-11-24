expenses = []

def add_expense(name, amount, category):
    expense = {
        "name": name,
        "amount": float(amount),
        "category": category
    }

    expenses.append(expense)
    print("Transaction recorded successfully!")
    return expense


def show_expenses():
    print("\n--- FINANCIAL RECORDS ---")

    for expense in expenses:
        print(
            expense["name"],
            expense["amount"],
            expense["category"]
        )


def calculate_total():
    total = 0

    for expense in expenses:
        if expense.get("transaction_type", "Expense") == "Expense":
            total += expense["amount"]

    print("Total expenses: KSh", total)