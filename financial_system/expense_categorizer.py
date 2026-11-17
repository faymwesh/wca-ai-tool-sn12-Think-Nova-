def categorize_expense(description):

    description = description.lower()

    if "naivas" in description or "supermarket" in description:
        return "Shopping"

    elif "uber" in description or "matatu" in description:
        return "Transport"

    elif "airtime" in description or "safaricom" in description:
        return "Communication"

    elif "kplc" in description or "electricity" in description:
        return "Electricity"

    elif "restaurant" in description or "food" in description:
        return "Food"

    else:
        return "Other"


# Test the categorisation system

transactions = [
    "Naivas Supermarket",
    "Uber Trip",
    "Safaricom Airtime",
    "KPLC Electricity",
    "Restaurant Food",
    "Unknown Payment"
]

for transaction in transactions:
    category = categorize_expense(transaction)

    print(transaction, "=", category)