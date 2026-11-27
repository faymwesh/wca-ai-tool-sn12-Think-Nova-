import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main


class MainMenuTests(unittest.TestCase):
    @patch("main.regenerate_saved_summary")
    def test_option_five_starts_summary_regeneration(self, regenerate_summary):
        with patch("builtins.input", side_effect=["5", "4"]):
            with redirect_stdout(io.StringIO()):
                main.main()

        regenerate_summary.assert_called_once_with()

    def test_view_session_replaces_legacy_summary_error(self):
        session = {
            "expense_data": [
                {
                    "description": "Groceries",
                    "amount": 12.5,
                    "category": "Food",
                    "transaction_type": "Expense",
                }
            ],
            "summary": "Could not generate a valid financial summary.",
        }

        with tempfile.TemporaryDirectory() as temporary_directory:
            session_path = Path(temporary_directory) / "session.json"
            session_path.write_text(json.dumps(session), encoding="utf-8")
            output = io.StringIO()
            with patch.object(main, "SESSIONS_DIR", Path(temporary_directory)):
                with patch("builtins.input", return_value="1"):
                    with redirect_stdout(output):
                        main.view_session()

            repaired_session = json.loads(
                session_path.read_text(encoding="utf-8")
            )

        self.assertNotIn(session["summary"], output.getvalue())
        self.assertIn("Spending analysis:", output.getvalue())
        self.assertEqual(
            repaired_session["summary"]["largest_category"],
            "Food (KES 12.50)",
        )


if __name__ == "__main__":
    unittest.main()
