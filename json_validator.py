import json


def validate_conversation_response(response):
  if not isinstance(response, str):
    return None

  try:
    data = json.loads(response)
  except json.JSONDecodeError:
    return None

  if not isinstance(data, dict):
    return None

  if data.get("type") != "answer":
    return None

  message = data.get("message")
  if not isinstance(message, str) or not message.strip():
    return None

  return {"type": "answer", "message": message.strip()}


def validate_ai_response(response):
  try:
    # Convert JSON text into a Python dictionary
    data = json.loads(response)

    # Make sure the converted data is a dictionary
    if not isinstance(data, dict):
      print("Validation error: Response is not a JSON object.")
      return None

    # Check that all required fields exist and are not empty
    for field in ("spending_analysis", "largest_category", "financial_advice"):
      if not isinstance(data.get(field), str) or not data[field].strip():
        return None

    suggestions = data.get("saving_suggestions")
    if (
        not isinstance(suggestions, list)
        or len(suggestions) != 3
        or any(not isinstance(item, str) or not item.strip() for item in suggestions)
    ):
      return None

    return data
  except (json.JSONDecodeError, TypeError):
    return None