
# main.py
# Main menu and conversation loop.
import requests
import json
from pathlib import Path

from rtcco import SYSTEM_PROMPT, SUMMARY_PROMPT
from history import create_memory, add_message
from assistant import ask_ai
from validator import validate_response
from summary import save_session


def get_valid_ai_response(memory):
    """Ask AI and retry once if JSON validation fails."""

    for attempt in range(2):
        try:
            response = ask_ai(memory)
            data = validate_response(response)

            if data is not None:
                return data

        except Exception as error:
            print("AI error:", error)

    return None


def start_session():
    """Start a new expense tracking conversation."""

    memory = create_memory(SYSTEM_PROMPT)

    print("\nM-Pesa Expense Coach started!")
    print("Enter 'done' to finish your session.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            print("Please enter an expense or question.")
            continue

        if user_input.lower() == "done":
            break

        add_message(memory, "user", user_input)

        data = get_valid_ai_response(memory)

        if data is None:
            print("Sorry, I could not process that response.")
            continue

        ai_response = json.dumps(data)

        add_message(memory, "assistant", ai_response)

        print("\nCoach:", data["message"])
        print("Total spent:", data["total_spent"])
        print("Category totals:", data["category_totals"])
        print()

    # Generate final summary.
    add_message(memory, "user", SUMMARY_PROMPT)

    summary_data = get_valid_ai_response(memory)

    if summary_data is None:
        print("Could not generate the final summary.")
        return

    summary = summary_data["message"]

    print("\nFINAL SPENDING SUMMARY")
    print(summary)

    filename = save_session(memory, summary)
    print("\nSession saved:", filename)


def view_session():
    """Display an existing session file."""

    files = list(Path("sessions").glob("*.json"))

    if not files:
        print("No saved sessions found.")
        return

    for index, file in enumerate(files, start=1):
        print(index, file.name)

    try:
        choice = int(input("Select session number: "))

        if choice < 1 or choice > len(files):
            print("Invalid selection.")
            return

        with open(files[choice - 1], encoding="utf-8") as file:
            data = json.load(file)

        print("\nSaved Summary:")
        print(data["summary"])

    except (ValueError, FileNotFoundError, json.JSONDecodeError):
        print("Could not open session file.")


def main():
    """Display the application menu."""

    while True:
        print("\n=== M-PESA EXPENSE COACH ===")
        print("1. Start new session")
        print("2. View past session")
        print("3. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            start_session()

        elif choice == "2":
            view_session()

        elif choice == "3":
            print("Thank you for using Expense Coach!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
