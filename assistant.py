
# assistant.py
# Handles communication with Hugging Face Inference Providers.

import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv(Path(__file__).resolve().parent / ".env")

hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise ValueError("HF_TOKEN is missing. Add your Hugging Face token to the project .env file.")

DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct-1M"
MODEL = os.getenv("HF_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL

client = InferenceClient(  provider="featherless-ai", api_key=hf_token)



def ask_ai(messages):
    """Send conversation history to Hugging Face and return its text response."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        response_format={"type": "json_object"},
    )

    if not response.choices:
        raise RuntimeError("Hugging Face returned no response choices.")

    content = response.choices[0].message.content
    if not isinstance(content, str) or not content:
        raise RuntimeError("Hugging Face returned an empty response.")

    return content
