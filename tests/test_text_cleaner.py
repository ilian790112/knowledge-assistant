import unittest

from app.utils.text_cleaner import clean_text


class TextCleanerTests(unittest.TestCase):
    def test_empty_text_stays_empty(self) -> None:
        self.assertEqual(clean_text(""), "")

    def test_collapses_newlines_and_whitespace(self) -> None:
        text = "First\n\nSecond\t\tThird"

        self.assertEqual(
            clean_text(text),
            "First Second Third",
        )

    def test_strips_leading_and_trailing_whitespace(self) -> None:
        self.assertEqual(
            clean_text("  hello world  "),
            "hello world",
        )

    def test_handles_mixed_whitespace(self) -> None:
        text = "\n\n  A\r\n\r\n B\t C  \n"

        self.assertEqual(
            clean_text(text),
            "A B C",
        )


if __name__ == "__main__":
    unittest.main()
