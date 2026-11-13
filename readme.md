# M-Pesa Expense Coach

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