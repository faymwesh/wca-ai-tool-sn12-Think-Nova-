import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import main
from ai_handler import get_ai_response
from ai_summary import generate_ai_summary, generate_conversation_response


class AIConversationTests(unittest.TestCase):
    def setUp(self):
        self.financial_data = {
            "total_income": 5000.0,
            "total_expenses": 450.0,
            "balance": 4550.0,
            "categories": {"Transport": 450.0},
        }

    @patch("ai_handler.anthropic.Anthropic")
    def test_api_handler_sends_the_supplied_history(self, anthropic_client):
        history = [
            {"role": "user", "content": "I paid KES 450 for a matatu."},

            {
                "role": "assistant",
                "content": '{"type":"answer","message":"Recorded."}',
            },
            {"role": "user", "content": "How much was transport?"},
        ]
        anthropic_client.return_value.messages.create.return_value.content = [
            SimpleNamespace(
                type="text",
                text='{"type":"answer","message":"KES 450."}',
            )
        ]

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            response = get_ai_response(
                "system instructions",
                financial_data=self.financial_data,
                messages=history,
                allow_offline_fallback=False,
            )

        self.assertEqual(response, '{"type":"answer","message":"KES 450."}')
        anthropic_client.return_value.messages.create.assert_called_once_with(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            system="system instructions",
            messages=history,
        )

    @patch("ai_summary.get_ai_response")
    def test_sends_full_history_on_each_turn(self, get_ai_response):
        get_ai_response.side_effect = [
            json.dumps({"type": "answer", "message": f"Answer {turn}"})
            for turn in range(1, 5)
        ]
        history = []

        for turn in range(1, 5):
            user_message = {
                "role": "user",
                "content": f"Question {turn}",
            }
            request_messages = history + [user_message]
            answer = generate_conversation_response(
                request_messages,
                self.financial_data,
            )
            history.extend([
                user_message,
                {
                    "role": "assistant",
                    "content": json.dumps(answer),
                },
            ])

        sent_histories = [
            call.kwargs["messages"]
            for call in get_ai_response.call_args_list
        ]
        self.assertEqual([len(messages) for messages in sent_histories], [1, 3, 5, 7])
        self.assertEqual(sent_histories[-1], history[:-1])

    @patch("ai_summary.get_ai_response")
    def test_retries_invalid_json_once_with_prior_history(self, get_ai_response):
        history = [
            {"role": "user", "content": "I spent KES 450 on transport."},
            {
                "role": "assistant",
                "content": '{"type":"answer","message":"Recorded."}',
            },
        ]
        get_ai_response.side_effect = [
            '{"type":"answer","message":""}',
            (
                '{"type":"answer",'
                '"message":"Your recorded transport spend is KES 450."}'
            ),
        ]

        answer = generate_conversation_response(
            history + [{"role": "user", "content": "How much was transport?"}],
            self.financial_data,
        )

        self.assertEqual(
            answer["message"],
            "Your recorded transport spend is KES 450.",
        )
        first_messages = get_ai_response.call_args_list[0].kwargs["messages"]
        retry_messages = get_ai_response.call_args_list[1].kwargs["messages"]
        self.assertEqual(first_messages[:2], history)
        self.assertEqual(retry_messages[:3], first_messages)
        self.assertEqual(
            retry_messages[3]["content"],
            '{"type":"answer","message":""}',
        )
        self.assertIn("did not pass JSON validation", retry_messages[4]["content"])
        self.assertEqual(get_ai_response.call_count, 2)

    @patch("ai_summary.get_ai_response", return_value="not json")
    def test_fails_after_one_invalid_response_retry(self, get_ai_response):
        with self.assertRaisesRegex(ValueError, "after one retry"):
            generate_conversation_response(
                [{"role": "user", "content": "Help me budget."}],
                self.financial_data,
            )
        self.assertEqual(get_ai_response.call_count, 2)

    @patch(
        "ai_summary.get_ai_response",
        return_value=json.dumps({
            "spending_analysis": "Transport is your recorded expense.",
            "largest_category": "Transport",
            "saving_suggestions": ["One", "Two", "Three"],
            "financial_advice": "Continue tracking expenses.",
        }),
    )
    def test_final_summary_receives_full_conversation(self, get_ai_response):
        history = [
            {"role": "user", "content": "I paid KES 450 for a matatu."},
            {
                "role": "assistant",
                "content": '{"type":"answer","message":"Recorded."}',
            },
        ]

        summary = generate_ai_summary(self.financial_data, history)

        sent_messages = get_ai_response.call_args.kwargs["messages"]
        self.assertEqual(sent_messages[:2], history)
        self.assertIn("verified financial information", sent_messages[-1]["content"])
        self.assertEqual(len(summary["saving_suggestions"]), 3)

    @patch("ai_summary.get_ai_response")
    def test_final_summary_retries_invalid_json_once(self, get_ai_response):
        valid_summary = {
            "spending_analysis": "You recorded KES 450 in transport expenses.",
            "largest_category": "Transport",
            "saving_suggestions": ["One", "Two", "Three"],
            "financial_advice": "Keep tracking your spending.",
        }
        get_ai_response.side_effect = [
            '{"spending_analysis":""}',
            json.dumps(valid_summary),
        ]

        result = generate_ai_summary(self.financial_data, [])

        self.assertEqual(result, valid_summary)
        self.assertEqual(get_ai_response.call_count, 2)

    @patch("main.generate_ai_summary")
    @patch("main.generate_conversation_response")
    @patch("main.record_expenses")
    def test_start_session_saves_four_turn_transcript_and_summary(
        self,
        record_expenses,
        generate_conversation_response_mock,
        generate_ai_summary_mock,
    ):
        expenses = [{
            "description": "Matatu",
            "amount": 450.0,
            "category": "Transport",
            "transaction_type": "Expense",
            "date": "2026-11-24",
        }]
        record_expenses.return_value = expenses
        generate_conversation_response_mock.side_effect = (
            lambda messages, _: {
                "type": "answer",
                "message": f"Answer {len(messages) // 2 + 1}",
            }
        )
        summary = {
            "spending_analysis": "You recorded KES 450 in transport expenses.",
            "largest_category": "Transport",
            "saving_suggestions": ["One", "Two", "Three"],
            "financial_advice": "Keep tracking your spending.",
        }
        generate_ai_summary_mock.return_value = summary

        with tempfile.TemporaryDirectory() as temporary_directory:
            with patch.object(main, "SESSIONS_DIR", Path(temporary_directory)):
                with patch(
                    "builtins.input",
                    side_effect=[
                        "How much did I spend?",
                        "What was that transport expense?",
                        "How can I save?",
                        "Can you recap?",
                        "done",
                    ],
                ):
                    with redirect_stdout(io.StringIO()):
                        main.start_session()

            saved_files = list(Path(temporary_directory).glob("*.json"))
            self.assertEqual(len(saved_files), 1)
            session = json.loads(saved_files[0].read_text(encoding="utf-8"))

        self.assertEqual(len(session["conversation"]), 8)
        self.assertEqual(session["conversation"][0]["content"], "How much did I spend?")
        self.assertEqual(session["conversation"][-2]["content"], "Can you recap?")
        self.assertEqual(session["expense_data"], expenses)
        self.assertEqual(session["summary"], summary)
        generate_ai_summary_mock.assert_called_once()
        self.assertEqual(
            generate_ai_summary_mock.call_args.args[1],
            session["conversation"],
        )

    @patch(
        "main.generate_ai_summary",
        side_effect=RuntimeError("Anthropic API request failed: 401"),
    )
    def test_regenerates_saved_summary_locally_after_api_401(
        self,
        generate_ai_summary_mock,
    ):
        expenses = [
            {
                "description": "Naivas Supermarket",
                "amount": 700.0,
                "category": "Shopping",
                "transaction_type": "Expense",
            },
            {
                "description": "Uber",
                "amount": 300.0,
                "category": "Transport",
                "transaction_type": "Expense",
            },
        ]
        original_session = {
            "started_at": "2026-11-22T14:55:06",
            "expense_data": expenses,
            "conversation": [],
            "summary": "Old summary",
        }

        with tempfile.TemporaryDirectory() as temporary_directory:
            session_path = Path(temporary_directory) / "saved_session.json"
            session_path.write_text(
                json.dumps(original_session),
                encoding="utf-8",
            )
            with patch.object(main, "SESSIONS_DIR", Path(temporary_directory)):
                with patch("builtins.input", return_value="1"):
                    output = io.StringIO()
                    with redirect_stdout(output):
                        main.regenerate_saved_summary()
            updated_session = json.loads(
                session_path.read_text(encoding="utf-8")
            )

        self.assertEqual(updated_session["expense_data"], expenses)
        self.assertEqual(
            updated_session["summary"]["largest_category"],
            "Shopping (KES 700.00)",
        )
        self.assertEqual(
            len(updated_session["summary"]["saving_suggestions"]),
            3,
        )
        self.assertIn("401", output.getvalue())
        self.assertIn("local summary", output.getvalue())
        generate_ai_summary_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
