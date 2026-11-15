import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_ai_response(system_prompt, user_prompt):
  api_key = os.getenv("OPENAI_API_KEY")

  # Use a sample response while testing without a paid API key
  if not api_key or api_key == "your_api_key_here":
    sample_data = {
        "spending_analysis": (
            "You spent KES 1,000 out of your KES 5,000 income."
        ),
        "largest_category": "Food (KES 700)",
        "saving_suggestions": [
            "Cook more meals at home to reduce food costs.",
            "Plan daily transport trips ahead to save money.",
        ],
        "financial_advice": (
            "You saved KES 4,000 this period, which is a good habit. Keep"
            " tracking your daily expenses."
        ),
    }
    return json.dumps(sample_data)

  # Connect to OpenAI once a real API key is added to .env
  try:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content

  except Exception as error:
    print("Error getting AI response:", error)
    return ""