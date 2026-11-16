from decimal import Decimal

# Sample financial transactions
income = [
    Decimal("5000"),
    Decimal("2000")
]

expenses = [
    Decimal("500"),
    Decimal("300"),
    Decimal("200")
]


def calculate_income():
    return sum(income, Decimal("0"))


def calculate_expenses():
    return sum(expenses, Decimal("0"))


def calculate_balance():
    return calculate_income() - calculate_expenses()


# Display financial report
print("===== M-PESA FINANCIAL REPORT =====")

print("Total Income: KSh", calculate_income())

print("Total Expenses: KSh", calculate_expenses())

print("Remaining Balance: KSh", calculate_balance())