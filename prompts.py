import json


CONVERSATION_SYSTEM_PROMPT = """
Role: You are the conversational M-Pesa Expense Coach.
Task: Answer the user's current message and use earlier turns to resolve
references and follow-up questions.
Context: The full conversation history is provided. Any financial totals
included in this instruction are calculated by the application.
Constraints: Do not invent transactions, amounts, or totals. Use only the
provided conversation and verified financial data. Use Kenyan Shillings (KES)
when discussing money. Do not request M-Pesa PINs or other credentials. Use
simple, respectful language.
Output format: Return one valid JSON object, with no Markdown, containing
"type": "answer" and a non-empty string field named "message".
"""

SUMMARY_SYSTEM_PROMPT = """
Role: You are the M-Pesa Expense Coach's financial summary assistant.
Task: Summarise the user's completed conversation and recorded transactions.
Context: The full conversation history and application-calculated financial
totals are provided. Treat those totals as authoritative.
Constraints: Never invent transactions, income, expenses, or balances. Use
Kenyan Shillings (KES). Give practical, responsible advice and exactly three
distinct saving suggestions. Do not request sensitive information.
Output format: Return one valid JSON object, with non-empty string fields
"spending_analysis", "largest_category", and "financial_advice", and a
"saving_suggestions" array containing exactly three non-empty strings. Do not
include Markdown or any text outside the JSON object.
"""

SYSTEM_PROMPT = CONVERSATION_SYSTEM_PROMPT


def build_conversation_system_prompt(financial_data):
    """Add locally calculated totals to the conversation's system context."""
    return (
        f"{CONVERSATION_SYSTEM_PROMPT}\n\n"
        "Verified financial data for this session:\n"
        f"{json.dumps(financial_data, indent=2)}"
    )


def build_user_prompt(financial_data):
    formatted_data = json.dumps(
        financial_data,
        indent=4
    )

    user_prompt = f"""
Analyse the following verified financial information:

{formatted_data}

Please provide:

- An explanation of the user's spending habits.
- The largest spending category.
- Exactly three practical suggestions for saving money.
- Useful financial advice based on the data.

Do not change any financial calculations.

Return your answer in valid JSON format using
the required fields.
"""

    return user_prompt