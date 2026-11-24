# M-Pesa Expense Coach

**Group:** THINK NOVA  
**Repository:** https://github.com/faymwesh/wca-ai-tool-sn12-Think-Nova-  
**Group members:** Add each member's full name and GitHub username before submission.

## What it does

M-Pesa Expense Coach is a command-line tool for recording and reviewing income
and expenses. Transactions can be entered manually or parsed from pasted
M-Pesa SMS messages. The app categorizes expenses, calculates totals and
balances, saves sessions as JSON, and can summarize a saved session.

## Requirements

- Python 3
- Packages listed in `requirements.txt`
- An Anthropic API key for live AI conversation and AI-generated summaries

## Setup on Windows

From the repository folder:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the repository root and add your own Anthropic API key:

```text
ANTHROPIC_API_KEY=your_anthropic_api_key
```

Do not commit `.env` or share the key. If the API key is rejected or the API is
unavailable, the app reports the error and can generate a local summary from
the recorded totals.

## Run

```powershell
python main.py
```

The menu provides:

1. Start a session and record expenses manually or from M-Pesa SMS.
2. Open a saved session.
3. Ask a calculation question about the loaded session.
4. Exit.
5. Regenerate and save a summary for a selected session.

Saved sessions are written to the project's `sessions/` folder. Session files
may contain personal financial data and are excluded from Git. The
`samples/demo_session.json` file contains fictional example data.

## Tests

Run the local tests with:

```powershell
python -m unittest -v
```

The draft written report is `THINK_NOVA_Project_Report_DRAFT.docx`. It includes
the required sections and source appendix, but member names and individual.

## Submission details to complete

- Add all group members' names and GitHub usernames above.
- Rehearse the live demo and ensure every member participates.
- Each member must make at least three meaningful commits to the shared
  repository.
- Complete the written report and each student's individual reflection.
