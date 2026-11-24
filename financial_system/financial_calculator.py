from decimal import Decimal, InvalidOperation

from financial_system.expense_categorizer import categorize_expense


def _amount(item):
    try:
        amount = Decimal(str(item.get("amount", "0")))
    except (InvalidOperation, AttributeError):
        return Decimal("0")
    return amount if amount.is_finite() else Decimal("0")


def calculate_financial_data(transactions):
    """Calculate verified totals and category totals from transactions."""
    total_income = Decimal("0")
    total_expenses = Decimal("0")
    category_totals = {}

    for item in transactions:
        if not isinstance(item, dict):
            continue

        amount = _amount(item)
        transaction_type = item.get("transaction_type", "")
        if transaction_type == "Income":
            total_income += amount
        elif transaction_type == "Expense":
            total_expenses += amount
            category = item.get("category", "Other") or "Other"
            if category == "Other":
                category = categorize_expense(
                    item.get("description") or item.get("name") or ""
                )
            category_totals[category] = (
                category_totals.get(category, Decimal("0")) + amount
            )

    return {
        "total_income": float(total_income),
        "total_expenses": float(total_expenses),
        "balance": float(total_income - total_expenses),
        "categories": {
            category: float(amount)
            for category, amount in category_totals.items()
        },
    }


def answer_financial_question(question, transactions):
    """Answer a basic financial question using deterministic calculations."""
    if not isinstance(question, str):
        return None

    text = question.lower().strip()
    if not text:
        return None

    data = calculate_financial_data(transactions)
    income = data["total_income"]
    expenses = data["total_expenses"]
    balance = data["balance"]
    categories = data["categories"]

    if "largest" in text or ("most" in text and "spend" in text):
        if not categories:
            return "You have no recorded expenses."
        category = max(categories, key=categories.get)
        return f"Largest expense category: {category} (KES {categories[category]:,.2f})"

    category_match = next(
        (
            category
            for category in categories
            if category.lower() in text
        ),
        None,
    )
    if category_match:
        return f"{category_match} expenses: KES {categories[category_match]:,.2f}"

    if any(word in text for word in ("balance", "left", "remaining", "remain")):
        return f"Remaining balance: KES {balance:,.2f}"

    if any(word in text for word in ("expense", "spent", "spend", "spending", "cost")):
        return f"Total expenses: KES {expenses:,.2f}"

    if any(word in text for word in ("income", "earned", "earn", "received", "salary")):
        return f"Total income: KES {income:,.2f}"

    return None