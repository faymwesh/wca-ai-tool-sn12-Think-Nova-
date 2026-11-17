
# validator.py
# Validates the AI's JSON responses.
import requests
import json


def validate_response(response):
    """Check JSON format and required fields."""

    try:
        data = json.loads(response)

        required_fields = [
            "type",
            "message",
            "expenses",
            "total_spent",
            "category_totals"
        ]

        for field in required_fields:
            if field not in data:
                return None

        if not isinstance(data["message"], str):
            return None

        if not data["message"].strip():
            return None

        if not isinstance(data["expenses"], list):
            return None

        if not isinstance(data["total_spent"], (int, float)):
            return None

        if not isinstance(data["category_totals"], dict):
            return None

        return data

    except json.JSONDecodeError:
        return None
