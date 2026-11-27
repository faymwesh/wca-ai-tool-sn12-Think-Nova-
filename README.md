# M-Pesa Expense Coach

A command-line expense tracker that records M-Pesa transactions, calculates
income and expenses, answers basic financial questions, and creates financial
summaries.

# Features

- Record expenses manually or paste M-Pesa confirmation messages.
- Enter additional income manually, or record income from M-Pesa messages.
- Calculate income, expenses, balance, and expense totals by category.
- Ask follow-up questions about the current session's transactions.
- Generate a financial summary with Anthropic, or use a local summary if AI
  summary generation is unavailable.
- Save sessions as JSON files in `sessions/` and view or regenerate summaries
  later.

# Requirements

- Python
- Packages listed in `requirements.txt`
- An Anthropic API key for AI-powered conversation and summaries. Without a
  configured key, summaries use a local fallback; AI conversation requires a
  key.

# Setup

From the project directory, create and activate a virtual environment in
PowerShell, then install the dependencies:

 powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create or edit a `.env` file in the project root and add your API key:

`text
ANTHROPIC_API_KEY=your_anthropic_api_key


Keep `.env private; it is excluded from Git.

# Run

```powershell
python main.py
``

The main menu lets you start a session, view a saved session, ask a financial
question about the loaded session, exit, or regenerate a saved summary.

During a new session, choose manual expense entry or M-Pesa SMS input. After
that, enter any additional income not already recorded, or press Enter to skip.
When finished asking follow-up questions, type `done` to generate the final
summary.

## Tests

Run the test suite with:

```powershell
python -m unittest discover -v
```

# Project layout

- main.py — command-line menu and session workflow
- `ai_handler.py`, `ai_summary.py`, `prompts.py` — AI requests, prompts, and
  summary handling
- `financial_system/` — M-Pesa parsing, expense categorization, calculations,
  and transaction storage
- `test_.py` — automated tests
