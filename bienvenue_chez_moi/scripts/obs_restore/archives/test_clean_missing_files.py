#!/usr/bin/env uv run python3
# /// script
# dependencies = [
#     "rich",
# ]
# ///

"""
Test suite for clean_missing_files.py
"""

import unittest
from pathlib import Path
from unittest.mock import patch, mock_open
import sys
import os

# Add the script directory to the path to import the module
script_dir = Path(__file__).parent.resolve()
sys.path.insert(0, str(script_dir))

from clean_missing_files import extract_filename, process_file


class TestExtractFilename(unittest.TestCase):
    """Test the extract_filename function."""

    def test_extract_filename_standard_line(self):
        """Test extracting filename from standard line with 'in'."""
        line = "- [[Blinkist - 12 Rules For Life]] in [[_cards/12 Rules for Life; An Antidote to Chaos]]"
        result = extract_filename(line)
        assert result == "Blinkist - 12 Rules For Life"

    def test_extract_filename_multiple_locations(self):
        """Test extracting filename from line with multiple 'in' locations."""
        line = "- [[Gemini 2.5 Pro]] in [[_cards/2025 AGA (Planification)]], [[_cards/Act as editor v11, outline list of topics fro this video]], [[_cards/Claude & Gemini in Concert]]"
        result = extract_filename(line)
        assert result == "Gemini 2.5 Pro"

    def test_extract_filename_no_in_clause(self):
        """Test extracting filename from line without 'in' clause."""
        line = "- [[Simple File]]"
        result = extract_filename(line)
        assert result == "Simple File"

    def test_extract_filename_special_characters(self):
        """Test extracting filename with special characters."""
        line = "- [[File with (parentheses) & symbols]] in [[_cards/Some Location]]"
        result = extract_filename(line)
        assert result == "File with (parentheses) & symbols"

    def test_extract_filename_date_format(self):
        """Test extracting filename that is a date."""
        line = "- [[2025-12-16]] in [[_cards/2025 year calendar]], [[_cards/_journal/_daily/2025-12-15]]"
        result = extract_filename(line)
        assert result == "2025-12-16"

    def test_extract_filename_empty_line(self):
        """Test extracting filename from empty line."""
        result = extract_filename("")
        assert result is None

    def test_extract_filename_non_list_line(self):
        """Test extracting filename from non-list line."""
        result = extract_filename("This is not a list line")
        assert result is None

    def test_extract_filename_no_brackets(self):
        """Test extracting filename from line without brackets."""
        result = extract_filename("- No brackets here")
        assert result is None

    def test_extract_filename_malformed_brackets(self):
        """Test extracting filename from line with malformed brackets."""
        result = extract_filename("- [[Only opening bracket")
        assert result is None


class TestProcessFile(unittest.TestCase):
    """Test the process_file function."""

    def test_process_file_standard_input(self):
        """Test processing a standard input file."""
        input_content = """- [[Blinkist - 12 Rules For Life]] in [[_cards/12 Rules for Life; An Antidote to Chaos]]
- [[Gemini 2.5 Pro]] in [[_cards/2025 AGA (Planification)]], [[_cards/Act as editor v11, outline list of topics fro this video]], [[_cards/Claude & Gemini in Concert]], [[_cards/LLM pricing]], [[_cards/Powerlevel10k]], [[_cards/Privatisation De la Vente d'électricité]], [[_cards/Resolving SSL Conflicts between Cloudflare & Traefik (by gemini)]], [[_cards/WNRS, create a new game]], [[_cards/_webclip/100x AI Coding for Real Work]], [[_local/_locally/3e mandat, Desjardins]]
- [[2025-12-16]] in [[_cards/2025 year calendar]], [[_cards/_journal/_daily/2025-12-15]], [[_cards/_journal/_daily/2025-12-17]]

Some random text here
- [[Simple File]]
"""
        expected_output = """- Blinkist - 12 Rules For Life
- Gemini 2.5 Pro
- 2025-12-16
- Simple File"""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.read_text", return_value=input_content):
                result = process_file(Path("dummy_input.md"))
                self.assertEqual(result, expected_output)

    def test_process_file_empty_file(self):
        """Test processing an empty file."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.read_text", return_value=""):
                result = process_file(Path("empty.md"))
                self.assertEqual(result, "")

    def test_process_file_not_found(self):
        """Test processing a file that doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            with self.assertRaises(FileNotFoundError) as cm:
                process_file(Path("nonexistent.md"))
            self.assertIn("File not found", str(cm.exception))

    def test_process_file_only_invalid_lines(self):
        """Test processing a file with only invalid lines."""
        input_content = """This is not a list line
- No brackets here
[[Only opening bracket

Another random line
"""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.read_text", return_value=input_content):
                result = process_file(Path("invalid.md"))
                self.assertEqual(result, "")


class TestDryRun(unittest.TestCase):
    """Test dry-run functionality through integration testing."""

    @patch("sys.argv", ["clean_missing_files.py", "test.md", "--dry-run"])
    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.read_text", return_value="- [[Test File]] in [[location]]")
    @patch("rich.console.Console.print")
    def test_dry_run_output(self, mock_console_print, mock_read, mock_exists):
        """Test that dry-run shows output without writing file."""
        # Import after patching to avoid import issues
        from clean_missing_files import main

        # Capture what would be printed
        main()

        # Check that the result was printed (not written to file)
        print_calls = [str(call) for call in mock_console_print.call_args_list]
        output_text = " ".join(print_calls)
        self.assertIn("Dry run", output_text)
        self.assertIn("Test File", output_text)


if __name__ == "__main__":
    unittest.main()
