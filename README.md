# wca-ai-tool-sn12-Think-Nova-
# M-Pesa Expense Coach
M-Pesa Expense Coach is a Python-based financial management assistant designed to help users track, analyze, and manage their M-Pesa expenses. By leveraging AI-powered insights, the system helps users understand their spending habits, categorize transactions, monitor expenses to make smarter financial decisions.


## Project Description
An AI-powered conversational expense tracking
assistant that helps users monitor spending
and identify ways to save money.

## Features
- Conversation memory
- Expense categorization
- JSON response validation
- Spending summaries
- Three saving suggestions
- Session saving
- Past session viewing

## Requirements
Python 3.10+
Hugging Face access token with Inference Providers enabled

## Installation
pip install -r requirements.txt

## Hugging Face Setup
Create a Hugging Face access token, then create a `.env` file in the project
folder containing:

HF_TOKEN=your_hugging_face_token

The app uses `Qwen/Qwen2.5-7B-Instruct-1M` by default, routed automatically to
an available Inference Provider. To use a different supported chat model, set:

HF_MODEL=provider/model-id

The model must be available through an Inference Provider for your account.

## Running the Project
python main.py

# M-Pesa Expense Coach – AI Integration & Repository Management
Submitted by: Quinter

# Overview
This repository contains my individual contribution to the M-Pesa Expense Coach project. My role focused on AI API integration, prompt design, JSON response validation, AI financial summaries, and GitHub repository management.

# Files Included
-ai_handler.py: Connects the Python application to the AI API securely using environment variables stored in .env.
-prompts.py: Contains the system instructions that guide the AI to analyze spending in KES and give practical financial advice.
-json_validator.py: Validates the AI's JSON response to ensure all required fields are present before displaying results.
-ai_summary.py: Formats the validated JSON data into a clear spending summary for the user.
-requirements.txt: Lists the required Python packages (openai,python-dotenv).
-Github Repository Management: Manage the group repository structure,
configure "gitignore" to block sensitive files like; env and coordinate branch merges across the team.

# Setup & Installation
1. Clone this repository from Github and copy its URL from Github
2. Install the required libraries:
    python-dotenv and openai
    bash
   pip install requirements.txt
3. Create a `.env` file in the project folder and add your API key:
   text
   OPENAI_API_KEY=your_api_key_here
