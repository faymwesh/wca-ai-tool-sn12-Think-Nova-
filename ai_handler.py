import json
import os
import anthropic
from dotenv import load_dotenv


load_dotenv()


def get_ai_response(
    system_prompt,
    user_prompt=None,
    financial_data=None,
    messages=None,
    allow_offline_fallback=True,
):
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key == "your_api_key_here":
        if allow_offline_fallback and financial_data is not None:
            total_income = float(financial_data.get("total_income", 0))
            total_expenses = float(financial_data.get("total_expenses", 0))
            balance = float(
                financial_data.get("balance", total_income - total_expenses)
            )
            categories = financial_data.get("categories", {})
            largest_category = (
                max(categories, key=categories.get)
                if categories
                else "No expenses recorded"
            )
            fallback = {
                "spending_analysis": (
                    f"You recorded KES {total_expenses:,.2f} in expenses and "
                    f"KES {total_income:,.2f} in income."
                ),
                "largest_category": (
                    f"{largest_category} "
                    f"(KES {categories[largest_category]:,.2f})"
                    if categories
                    else largest_category
                ),
                "saving_suggestions": [
                    "Review your largest spending category for expenses you can reduce.",
                    "Keep recording transactions to identify spending patterns over time.",
                    "Set a weekly spending limit for non-essential purchases.",
                ],
                "financial_advice": (
                    f"Your recorded income minus expenses is KES {balance:,.2f}. "
                    "Keep tracking expenses to support your budgeting decisions."
                ),
            }
            return json.dumps(fallback)

        raise RuntimeError(
            "ANTHROPIC_API_KEY is not configured; the AI conversation "
            "cannot continue."
        )

    if messages is None:
        if user_prompt is None:
            raise ValueError("A user prompt or conversation history is required.")
        request_messages = [{"role": "user", "content": user_prompt}]
    else:
        request_messages = messages

    client = anthropic.Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=request_messages,
        )
    except anthropic.APIError as error:
        raise RuntimeError(f"Anthropic API request failed: {error}") from error

    return "\n".join(
        block.text for block in response.content
        if getattr(block, "type", None) == "text"
    )