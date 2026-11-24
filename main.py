import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from dotenv import load_dotenv

from ai_summary import (
    generate_ai_summary,
    generate_conversation_response,
    generate_local_summary,
)
from financial_system.expense_categorizer import categorize_expense
from financial_system.expense_manager import add_expense, expenses as recorded_expenses
from financial_system.financial_calculator import (
    answer_financial_question,
    calculate_financial_data,
)
from financial_system.mpesa_processor import process_mpesa_sms

load_dotenv()


SESSIONS_DIR = Path(__file__).resolve().parent / "sessions"
current_transactions = []


def record_expenses():
    """Collect expenses manually or from pasted M-Pesa confirmation messages."""
    recorded_expenses.clear()

    while True:
        print("\nHow would you like to record expenses?")
        print("1. Enter expenses manually")
        print("2. Paste M-Pesa SMS messages")
        choice = input("Choose option: ").strip()
        if choice in {"1", "2"}:
            break
        print("Invalid choice. Select 1 or 2.")

    if choice == "1":
        print("\nEnter each expense. Leave the description blank when finished.")
        while True:
            description = input("Description: ").strip()
            if not description:
                break

            while True:
                amount_text = input("Amount (KES): ").strip().replace(",", "")
                try:
                    amount = Decimal(amount_text)
                except InvalidOperation:
                    print("Enter a valid amount greater than zero.")
                    continue
                if not amount.is_finite() or amount <= 0:
                    print("Enter a valid amount greater than zero.")
                    continue
                break

            entry = add_expense(
                description,
                float(amount),
                categorize_expense(description),
            )
            entry.update({
                "description": description,
                "transaction_type": "Expense",
                "date": datetime.now().date().isoformat(),
            })
    else:
        print("\nPaste one M-Pesa SMS per line. Leave the line blank when finished.")
        while True:
            message = input("M-Pesa SMS: ").strip()
            if not message:
                break

            transaction = process_mpesa_sms(message)
            if transaction is None:
                print("Could not read that message. No expense was recorded.")
            else:
                category = (
                    "Income"
                    if transaction["transaction_type"] == "Income"
                    else transaction["category"]
                )
                entry = add_expense(
                    transaction["description"],
                    transaction["amount"],
                    category,
                )
                entry.update(transaction)
                entry["category"] = category

    return list(recorded_expenses)


def create_ai_summary(expense_data, conversation_history=None):
    """Return a validated summary based on the expenses and conversation."""
    financial_data = calculate_financial_data(expense_data)
    try:
        summary = generate_ai_summary(financial_data, conversation_history)
    except (RuntimeError, ValueError) as error:
        print(f"\nAI summary could not be generated: {error}")
        print("Using a local summary of the recorded transactions instead.")
        summary = generate_local_summary(financial_data)
    if not isinstance(summary, dict):
        raise ValueError("The AI summary did not return a usable result.")

    return summary


def format_ai_summary(summary):
    """Format a validated summary object for the terminal."""
    suggestions = "\n".join(
        f"- {suggestion}" for suggestion in summary["saving_suggestions"]
    )
    return (
        f"Spending analysis: {summary['spending_analysis']}\n"
        f"Largest category: {summary['largest_category']}\n"
        f"Saving suggestions:\n{suggestions}\n"
        f"Financial advice: {summary['financial_advice']}"
    )


def run_conversation(expense_data):
    """Collect conversational turns and keep only validated answers in history."""
    financial_data = calculate_financial_data(expense_data)
    messages = []
    print("\nAsk questions or follow up on earlier turns.")
    print("Type 'done' when you want the final summary.")

    while True:
        try:
            user_text = input("You: ").strip()
        except EOFError:
            print("\nEnding the conversation.")
            break

        if user_text.lower() in {"done", "exit", "back"}:
            break
        if not user_text:
            print("Please enter a message, or type 'done' to finish.")
            continue

        user_message = {"role": "user", "content": user_text}
        request_messages = messages + [user_message]
        try:
            answer = generate_conversation_response(
                request_messages,
                financial_data,
            )
        except (RuntimeError, ValueError) as error:
            print(f"Could not complete the AI turn: {error}")
            print("Ending the conversation and continuing to the summary.")
            return messages

        assistant_message = {
            "role": "assistant",
            "content": json.dumps(answer, ensure_ascii=False),
        }
        messages.extend([user_message, assistant_message])
        print(answer["message"])

    return messages


def save_session(session):
    """Save a completed session to the sessions folder."""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    filename = SESSIONS_DIR / f"session_{datetime.now():%Y%m%d_%H%M%S_%f}.json"

    with filename.open("w", encoding="utf-8") as file:
        json.dump(session, file, ensure_ascii=False, indent=2)

    return filename


def start_session():
    """Coordinate a session and save its results."""
    global current_transactions
    print("\nStarting a new M-Pesa Expense Coach session.")

    try:
        expense_data = record_expenses()
        if not expense_data:
            print("\nNo expenses recorded; session was not saved.")
            return
        current_transactions = list(expense_data)
        conversation = run_conversation(expense_data)
        summary = create_ai_summary(expense_data, conversation)
    except (EOFError, OSError, RuntimeError, ValueError) as error:
        print(f"\nSession could not be completed: {error}")
        return

    session = {
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "expense_data": expense_data,
        "conversation": conversation,
        "summary": summary,
    }

    try:
        filename = save_session(session)
    except (OSError, TypeError, ValueError) as error:
        print(f"\nCould not save the session: {error}")
        return

    print("\nSession summary:")
    print(format_ai_summary(summary))
    print("\nSession saved:", filename)


def view_session():
    """List saved sessions and display the selected session summary."""
    global current_transactions
    files = sorted(SESSIONS_DIR.glob("*.json"))

    if not files:
        print("No saved sessions found.")
        return

    for index, file_path in enumerate(files, start=1):
        print(index, file_path.name)

    try:
        choice = int(input("Select session number: ").strip())
        if choice < 1 or choice > len(files):
            print("Invalid selection.")
            return

        with files[choice - 1].open(encoding="utf-8") as file:
            session = json.load(file)

        summary = session["summary"]
        if isinstance(summary, dict):
            summary_text = format_ai_summary(summary)
        elif isinstance(summary, str):
            summary_text = summary
        else:
            raise ValueError("The saved summary has an invalid format.")

        expenses = session.get("expense_data", [])
        if isinstance(expenses, list):
            current_transactions = expenses
            print("\nRecorded expenses:")
            for expense in expenses:
                print(
                    f"- {expense.get('description', expense.get('name', 'Expense'))}: "
                    f"KES {expense.get('amount', 0)} "
                    f"({expense.get('category', 'Other')})"
                )

        conversation = session.get("conversation", [])
        if isinstance(conversation, list) and conversation:
            print("\nSaved conversation:")
            for message in conversation:
                if not isinstance(message, dict):
                    continue
                role = message.get("role")
                content = message.get("content", "")
                if role == "assistant":
                    try:
                        content = json.loads(content).get("message", content)
                    except (json.JSONDecodeError, AttributeError, TypeError):
                        pass
                if role in {"user", "assistant"}:
                    print(f"{role.title()}: {content}")

        print("\nSaved Summary:")
        print(summary_text)
    except (ValueError, KeyError, OSError, json.JSONDecodeError):
        print("Could not open session file.")


def regenerate_saved_summary():
    """Create and persist a fresh summary for an existing session."""
    global current_transactions
    files = sorted(SESSIONS_DIR.glob("*.json"))

    if not files:
        print("No saved sessions found.")
        return

    for index, file_path in enumerate(files, start=1):
        print(index, file_path.name)

    try:
        choice = int(input("Select session number: ").strip())
        if choice < 1 or choice > len(files):
            print("Invalid selection.")
            return

        file_path = files[choice - 1]
        with file_path.open(encoding="utf-8") as file:
            session = json.load(file)
        if not isinstance(session, dict):
            raise ValueError("The saved session has an invalid format.")

        expense_data = session.get("expense_data")
        if not isinstance(expense_data, list) or any(
            not isinstance(expense, dict) for expense in expense_data
        ):
            raise ValueError("The saved session has invalid expense data.")

        conversation = session.get("conversation", [])
        if not isinstance(conversation, list):
            raise ValueError("The saved conversation has an invalid format.")

        summary = create_ai_summary(expense_data, conversation)
        session["summary"] = summary
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(session, file, ensure_ascii=False, indent=2)

        current_transactions = list(expense_data)
        print("\nUpdated financial summary:")
        print(format_ai_summary(summary))
        print("\nSummary saved to:", file_path)
    except (ValueError, KeyError, OSError, json.JSONDecodeError, TypeError) as error:
        print(f"Could not update the saved summary: {error}")


def ask_financial_question():
    """Answer calculation questions from the currently selected transactions."""
    if not current_transactions:
        print("\nNo transactions are loaded. Start or open a session first.")
        return

    print("\nAsk a calculation question (or type 'back').")
    print("Examples: What is my balance? How much did I spend? "
          "What is my largest category?")

    while True:
        try:
            question = input("Question: ").strip()
        except EOFError:
            print("Returning to the main menu.")
            return

        if question.lower() in {"back", "exit", ""}:
            return

        answer = answer_financial_question(question, current_transactions)
        if answer:
            print(answer)
        else:
            print("I could calculate income, expenses, balance, category totals, "
                  "or the largest expense category.")


def main():
    """Display the application menu and route user choices."""
    while True:
        print("\n=== M-PESA EXPENSE COACH ===")
        print("1. Start new session")
        print("2. View past session")
        print("3. Ask a financial question")
        print("4. Exit")
        print("5. Generate summary for a saved session")

        try:
            choice = input("Choose option: ").strip()
        except EOFError:
            print("\nThank you for using Expense Coach!")
            break

        if choice == "1":
            start_session()
        elif choice == "2":
            view_session()
        elif choice == "3":
            ask_financial_question()
        elif choice == "4":
            print("Thank you for using Expense Coach!")
            break
        elif choice == "5":
            regenerate_saved_summary()
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()