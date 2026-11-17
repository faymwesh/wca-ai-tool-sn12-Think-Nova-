# M-Pesa Expense Coach

A lightweight Python application for creating an expense-coaching session, saving session data, and reviewing past summaries.

## Overview

This project is a starter scaffold for an M-Pesa expense assistant. It provides the shell of a CLI workflow where:

- expense data can be captured through an integration point
- an AI summary can be generated from that expense data
- the completed session is saved to the `sessions/` directory
- prior sessions can be viewed from the terminal

## Current Status

The application is intentionally scaffolded with placeholder integration points:

- `record_expenses()`
- `create_ai_summary(expense_data)`

These functions currently raise `NotImplementedError` to make it clear where the real expense capture and AI summary logic should be added.

## Project Structure

```text
mpesa-coach-expense/
├── main.py
├── requirements.txt
├── README.md
└── sessions/
    └── (generated session files)
```

## Features

- Start a new expense coaching session from the CLI
- Save session payloads as JSON files
- Retrieve and display saved summaries from past sessions
- Easy extension points for real integrations

## Requirements

- Python 3.9+
- `requests`
- `python-dotenv`

## Installation

1. Open a terminal in the project folder.
2. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
```

3. Activate it:

- Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

- macOS/Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

```bash
python main.py
```

When the app starts, it shows a menu with three options:

1. Start new session
2. View past session
3. Exit

## Session Storage

Completed sessions are saved in the `sessions/` directory as JSON files with timestamps in the filename.

Each saved session includes:

- the timestamp when the session started
- expense data
- the final summary text

## Notes for Future Development

To turn this scaffold into a fully working product, implement:

- a real expense ingestion module for M-Pesa transactions or user-entered expense data
- AI or rule-based summary generation based on the captured expense data
- output formatting and validation
- optional API integration, database storage, or reporting features


