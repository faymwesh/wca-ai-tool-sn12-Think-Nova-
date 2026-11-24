import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main


class MainMenuTests(unittest.TestCase):
    @patch("main.regenerate_saved_summary")
    def test_option_five_generates_a_saved_summary(self, regenerate_summary):
        with patch("builtins.input", side_effect=["5", "4"]):
            with redirect_stdout(io.StringIO()):
                main.main()

        regenerate_summary.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
