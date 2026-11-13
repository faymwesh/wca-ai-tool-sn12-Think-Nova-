
# summary.py
# Generates and saves final session summaries.

import json
from datetime import datetime
from pathlib import Path


def save_session(memory, summary):
    """Save conversation and summary to JSON."""

    Path("sessions").mkdir(exist_ok=True)

    filename = (
        "sessions/session_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".json"
    )

    session_data = {
        "date": datetime.now().isoformat(),
        "conversation": memory,
        "summary": summary
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            session_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    return filename
