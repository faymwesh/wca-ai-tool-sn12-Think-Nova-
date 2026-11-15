from ai_handler import get_ai_response
from json_validator import validate_ai_response
from prompts import SYSTEM_PROMPT, build_user_prompt


def generate_ai_summary(financial_data):
  # Step 1: Create the prompt using the financial totals
  user_prompt = build_user_prompt(financial_data)

  # Step 2: Send the prompt to the AI handler
  raw_response = get_ai_response(SYSTEM_PROMPT, user_prompt)

  # Step 3: Validate the JSON returned by the AI
  summary = validate_ai_response(raw_response)

  if summary is None:
    return "Could not generate a valid financial summary."

  return summary


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
    
