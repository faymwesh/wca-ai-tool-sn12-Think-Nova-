from ai_handler import get_ai_response
from json_validator import (
    validate_ai_response,
    validate_conversation_response,
)
from prompts import (
    SUMMARY_SYSTEM_PROMPT,
    build_conversation_system_prompt,
    build_user_prompt,
)


def generate_local_summary(financial_data):
  """Build a factual summary from locally calculated totals without an API."""
  income = float(financial_data.get("total_income", 0))
  expenses = float(financial_data.get("total_expenses", 0))
  balance = float(financial_data.get("balance", income - expenses))
  categories = financial_data.get("categories", {})

  if categories:
    largest_category = max(categories, key=categories.get)
    largest_label = (
        f"{largest_category} (KES {categories[largest_category]:,.2f})"
    )
    category_breakdown = ", ".join(
        f"{category}: KES {amount:,.2f}"
        for category, amount in sorted(categories.items())
    )
    suggestions = [
        f"Set a weekly spending limit for {largest_category.lower()}.",
        "Plan purchases ahead to reduce unplanned expenses.",
        "Keep recording expenses and compare category totals over time.",
    ]
  else:
    largest_label = "No expenses recorded"
    category_breakdown = "No expense categories recorded"
    suggestions = [
        "Record expenses consistently to identify spending patterns.",
        "Set a budget after reviewing your regular income and expenses.",
        "Review your records regularly and adjust your budget as needed.",
    ]

  return {
      "spending_analysis": (
          f"You recorded KES {expenses:,.2f} in expenses and "
          f"KES {income:,.2f} in income. Category totals: {category_breakdown}."
      ),
      "largest_category": largest_label,
      "saving_suggestions": suggestions,
      "financial_advice": (
          f"Your recorded income minus expenses is KES {balance:,.2f}. "
          "Use this as a snapshot of the transactions you recorded."
      ),
  }


def _request_valid_response(
    system_prompt,
    messages,
    validator,
    financial_data=None,
    allow_offline_fallback=False,
):
  raw_response = get_ai_response(
      system_prompt,
      financial_data=financial_data,
      messages=messages,
      allow_offline_fallback=allow_offline_fallback,
  )
  validated = validator(raw_response)
  if validated is not None:
    return validated

  retry_messages = list(messages)
  retry_messages.extend([
      {
          "role": "assistant",
          "content": raw_response or "The previous response was empty.",
      },
      {
          "role": "user",
          "content": (
              "Your previous response did not pass JSON validation. "
              "Return a corrected response that follows the required JSON "
              "schema exactly, with no text outside the JSON object."
          ),
      },
  ])
  raw_response = get_ai_response(
      system_prompt,
      financial_data=financial_data,
      messages=retry_messages,
      allow_offline_fallback=allow_offline_fallback,
  )
  validated = validator(raw_response)
  if validated is None:
    raise ValueError("The AI returned invalid JSON after one retry.")
  return validated


def generate_conversation_response(messages, financial_data):
  """Send the complete turn history and validate the AI's JSON answer."""
  system_prompt = build_conversation_system_prompt(financial_data)
  return _request_valid_response(
      system_prompt,
      messages,
      validate_conversation_response,
      financial_data=financial_data,
  )


def generate_ai_summary(financial_data, conversation_history=None):
  """Make a final summary call using the full conversation and verified totals."""
  messages = list(conversation_history or [])
  messages.append({"role": "user", "content": build_user_prompt(financial_data)})
  return _request_valid_response(
      SUMMARY_SYSTEM_PROMPT,
      messages,
      validate_ai_response,
      financial_data=financial_data,
      allow_offline_fallback=True,
  )


# Test block to verify your code works on its own
if __name__ == "__main__":
  test_data = {
      "total_income": 5000.0,
      "total_expenses": 1000.0,
      "balance": 4000.0,
      "categories": {"Food": 700.0, "Transport": 300.0},
  }

  result = generate_ai_summary(test_data)
  print(result)
    
