import json

def validate_ai_response(response):
  required_fields = [
      "spending_analysis",
      "largest_category",
      "saving_suggestions",
      "financial_advice",
  ]

  try:
    # Convert JSON text into a Python dictionary
    data = json.loads(response)

    # Make sure the converted data is a dictionary
    if not isinstance(data, dict):
      print("Validation error: Response is not a JSON object.")
      return None

    # Check that all required fields exist and are not empty
    for field in required_fields:
      if field not in data or not data[field]:
        print(f"Validation error: Missing or empty field '{field}'.")
        return None

    # Make sure saving_suggestions is a list of strings
    if not isinstance(data["saving_suggestions"], list):
      print("Validation error: 'saving_suggestions' must be a list.")
      return None

    return data

  except json.JSONDecodeError as error:
    print("Invalid JSON format:", error)
    return None