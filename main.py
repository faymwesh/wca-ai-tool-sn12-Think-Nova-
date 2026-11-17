import json
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()


SESSIONS_DIR = Path("sessions")


def record_expenses():
    """Integration point for Derick's expense-recordinng component.

    Replace this placeholder with the expense component. It should return
    session expense data as a JSON-serializable Python object.
    """
    raise NotImplementedError("Expense recording has not been integrated yet.")


def create_ai_summary(expense_data):
    """Integration point forQuinter's AI component.

    Replace this placeholder with the AI component. It should accept the
    expense data and return a summary string.
    """
    raise NotImplementedError("AI summaries have not been integrated yet.")


def save_session(session):
    """Save a completed session to the sessions folder."""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    filename = SESSIONS_DIR / f"session_{datetime.now():%Y%m%d_%H%M%S_%f}.json"

    with filename.open("w", encoding="utf-8") as file:
        json.dump(session, file, ensure_ascii=False, indent=2)

    return filename


def start_session():
    """Coordinate a session and save its results."""
    print("\nStarting a new M-Pesa Expense Coach session.")

    try:
        expense_data = record_expenses()
        summary = create_ai_summary(expense_data)
    except NotImplementedError as error:
        print(f"\nSession is not ready: {error}")
        return

    if not isinstance(summary, str):
        print("\nSession could not be saved: the summary must be text.")
        return

    session = {
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "expense_data": expense_data,
        "summary": summary,
    }

    try:
        filename = save_session(session)
    except (OSError, TypeError, ValueError) as error:
        print(f"\nCould not save the session: {error}")
        return

    print("\nSession summary:")
    print(summary)
    print("\nSession saved:", filename)


def view_session():
    """List saved sessions and display the selected session summary."""
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
        if not isinstance(summary, str):
            raise ValueError("The saved summary is not text.")

        print("\nSaved Summary:")
        print(summary)
    except (ValueError, KeyError, OSError, json.JSONDecodeError):
        print("Could not open session file.")


def main():
    """Display the application menu and route user choices."""
    while True:
        print("\n=== M-PESA EXPENSE COACH ===")
        print("1. Start new session")
        print("2. View past session")
        print("3. Exit")

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
            print("Thank you for using Expense Coach!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()