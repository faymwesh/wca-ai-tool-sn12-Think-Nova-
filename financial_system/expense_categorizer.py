def categorize_expense(description):

    description = description.lower()

    if any(
        word in description
        for word in ("naivas", "supermarket", "shopping", "shop", "clothes")
    ):
        return "Shopping"

    elif any(
        word in description
        for word in ("uber", "matatu", "transport", "bus", "taxi", "fuel")
    ):
        return "Transport"

    elif any(
        word in description
        for word in ("airtime", "safaricom", "communication", "internet", "data")
    ):
        return "Communication"

    elif "kplc" in description or "electricity" in description:
        return "Electricity"

    elif "restaurant" in description or "food" in description:
        return "Food"

    else:
        return "Other"