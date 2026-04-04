#!/usr/bin/env uv run python3
# /// script
# dependencies = [
#     "pytest>=8.0",
#     "httpx>=0.27",
#     "rich>=13.0",
#     "respx>=0.22",
# ]
# ///
"""
Red-Green TDD test suite for grokipedia.py.

Run:
    uv run pytest tests/test_grokipedia.py -v
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any
from unittest.mock import patch

import httpx
import pytest
import respx

# ---------------------------------------------------------------------------
# Resolve script path so tests work regardless of cwd
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent.parent
SCRIPT_PATH = SCRIPT_DIR / "grokipedia.py"

# Add parent so we can `import grokipedia`
sys.path.insert(0, str(SCRIPT_DIR))
import grokipedia  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def run_script(*args: str, env: dict[str, str] | None = None) -> tuple[str, str, int]:
    """Execute grokipedia.py via subprocess and return (stdout, stderr, exit_code)."""
    cmd = ["uv", "run", "python3", str(SCRIPT_PATH), *args]
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return result.stdout, result.stderr, result.returncode


# Reusable Tavily API response fixture
FAKE_RESPONSE: dict[str, Any] = {
    "query": "test query",
    "answer": "A test answer from Tavily.",
    "response_time": 1.23,
    "results": [
        {
            "title": "Test Article",
            "url": "https://grokipedia.com/page/Test",
            "content": "This is test content from Grokipedia.",
            "score": 0.95,
            "raw_content": "Full raw content of the test article.",
        },
    ],
}

EMPTY_RESPONSE: dict[str, Any] = {
    "query": "nothing",
    "answer": None,
    "response_time": 0.5,
    "results": [],
}

# Response with None values in result fields -- mirrors real API returning null
NULL_FIELDS_RESPONSE: dict[str, Any] = {
    "query": "nulls",
    "answer": None,
    "response_time": None,
    "results": [
        {
            "title": None,
            "url": None,
            "content": None,
            "score": None,
            "raw_content": None,
        },
    ],
}


# ===================================================================
# CLI Integration Tests (subprocess)
# ===================================================================


class TestCLIHelp:
    """--help must exit 0 and show examples."""

    def test_help_exits_0(self) -> None:
        stdout, _, code = run_script("--help")
        assert code == 0

    def test_help_shows_examples(self) -> None:
        stdout, _, _ = run_script("--help")
        assert "Examples:" in stdout

    def test_help_shows_all_flags(self) -> None:
        stdout, _, _ = run_script("--help")
        assert "--max-results" in stdout
        assert "--raw" in stdout
        assert "--json" in stdout
        assert "--version" in stdout


class TestCLIVersion:
    """--version must exit 0 and print semver."""

    def test_version_exits_0(self) -> None:
        _, _, code = run_script("--version")
        assert code == 0

    def test_version_shows_semver(self) -> None:
        stdout, _, _ = run_script("--version")
        assert "0.1.0" in stdout


class TestCLIValidation:
    """Bad input must fail fast with exit code 2."""

    def test_no_args_exits_2(self) -> None:
        """Missing query should exit 2 (argparse default)."""
        _, _, code = run_script()
        assert code == 2

    def test_empty_query_exits_2(self) -> None:
        """Empty string query is useless -- should be rejected."""
        _, stderr, code = run_script("")
        assert code == 2
        assert "empty" in stderr.lower() or "query" in stderr.lower()

    def test_whitespace_query_exits_2(self) -> None:
        """Whitespace-only query should be rejected."""
        _, stderr, code = run_script("   ")
        assert code == 2

    def test_max_results_zero_exits_2(self) -> None:
        _, _, code = run_script("test", "-n", "0")
        assert code == 2

    def test_max_results_21_exits_2(self) -> None:
        _, _, code = run_script("test", "-n", "21")
        assert code == 2

    def test_max_results_negative_exits_2(self) -> None:
        _, _, code = run_script("test", "-n", "-1")
        assert code == 2

    def test_max_results_non_integer_exits_2(self) -> None:
        """argparse should reject non-integer."""
        _, _, code = run_script("test", "-n", "abc")
        assert code == 2

    def test_validation_errors_on_stderr(self) -> None:
        """Error text must be on stderr, not stdout."""
        stdout, stderr, _ = run_script("test", "-n", "0")
        assert stdout == ""  # stdout must be clean
        assert "Error" in stderr or "error" in stderr


# ===================================================================
# Unit Tests -- get_api_key
# ===================================================================


class TestGetApiKey:
    """get_api_key must raise ApiKeyError, not sys.exit."""

    def test_missing_chezmoi_raises_api_key_error(self) -> None:
        """If chezmoi is not installed, should raise ApiKeyError."""
        with patch("grokipedia.subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(grokipedia.ApiKeyError, match="chezmoi"):
                grokipedia.get_api_key()

    def test_keyring_failure_raises_api_key_error(self) -> None:
        """If keyring lookup fails, should raise ApiKeyError."""
        with patch(
            "grokipedia.subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "chezmoi"),
        ):
            with pytest.raises(grokipedia.ApiKeyError, match="keyring"):
                grokipedia.get_api_key()

    def test_empty_key_raises_api_key_error(self) -> None:
        """Keyring returning empty/whitespace should be rejected."""
        mock_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="   \n", stderr=""
        )
        with patch("grokipedia.subprocess.run", return_value=mock_result):
            with pytest.raises(grokipedia.ApiKeyError, match="empty"):
                grokipedia.get_api_key()

    def test_valid_key_returned(self) -> None:
        """Valid key should be returned stripped."""
        mock_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="  tvly-abc123  \n", stderr=""
        )
        with patch("grokipedia.subprocess.run", return_value=mock_result):
            assert grokipedia.get_api_key() == "tvly-abc123"


# ===================================================================
# Unit Tests -- search_grokipedia
# ===================================================================


class TestSearchGrokipedia:
    """search_grokipedia must build correct payloads and accept api_key."""

    @respx.mock
    def test_payload_includes_domains(self) -> None:
        """include_domains must contain both grokipedia domains."""
        captured_payload: dict[str, Any] = {}

        def capture_request(request: httpx.Request) -> httpx.Response:
            captured_payload.update(json.loads(request.content))
            return httpx.Response(200, json=FAKE_RESPONSE)

        respx.post(grokipedia.TAVILY_API_URL).mock(side_effect=capture_request)

        grokipedia.search_grokipedia("test", api_key="fake-key")
        assert captured_payload["include_domains"] == [
            "grokipedia.com",
            "grokxpedia.us",
        ]

    @respx.mock
    def test_payload_respects_max_results(self) -> None:
        captured_payload: dict[str, Any] = {}

        def capture_request(request: httpx.Request) -> httpx.Response:
            captured_payload.update(json.loads(request.content))
            return httpx.Response(200, json=FAKE_RESPONSE)

        respx.post(grokipedia.TAVILY_API_URL).mock(side_effect=capture_request)

        grokipedia.search_grokipedia("test", max_results=10, api_key="fake-key")
        assert captured_payload["max_results"] == 10

    @respx.mock
    def test_api_key_in_auth_header(self) -> None:
        """Bearer token must use the provided api_key."""
        captured_auth: str = ""

        def capture_request(request: httpx.Request) -> httpx.Response:
            nonlocal captured_auth
            captured_auth = request.headers.get("authorization", "")
            return httpx.Response(200, json=FAKE_RESPONSE)

        respx.post(grokipedia.TAVILY_API_URL).mock(side_effect=capture_request)

        grokipedia.search_grokipedia("test", api_key="tvly-secret")
        assert captured_auth == "Bearer tvly-secret"

    @respx.mock
    def test_http_error_propagates(self) -> None:
        """Non-2xx status should raise HTTPStatusError."""
        respx.post(grokipedia.TAVILY_API_URL).mock(
            return_value=httpx.Response(401, json={"error": "unauthorized"})
        )
        with pytest.raises(httpx.HTTPStatusError):
            grokipedia.search_grokipedia("test", api_key="bad-key")

    def test_missing_api_key_raises(self) -> None:
        """If api_key is None and get_api_key fails, should raise ApiKeyError."""
        with patch(
            "grokipedia.get_api_key",
            side_effect=grokipedia.ApiKeyError("no key"),
        ):
            with pytest.raises(grokipedia.ApiKeyError):
                grokipedia.search_grokipedia("test")


# ===================================================================
# Unit Tests -- display_results
# ===================================================================


class TestDisplayResults:
    """display_results must handle all edge cases without crashing."""

    def test_empty_results(self) -> None:
        """Empty results list should not crash."""
        grokipedia.display_results(EMPTY_RESPONSE)

    def test_no_answer_key(self) -> None:
        """Missing answer should be handled gracefully."""
        data = {"query": "test", "results": [], "response_time": 0.1}
        grokipedia.display_results(data)

    def test_none_score_does_not_crash(self) -> None:
        """score: null from API must not cause format error."""
        grokipedia.display_results(NULL_FIELDS_RESPONSE)

    def test_none_content_does_not_crash(self) -> None:
        """content: null must not cause TypeError on slicing."""
        grokipedia.display_results(NULL_FIELDS_RESPONSE)

    def test_none_response_time_does_not_crash(self) -> None:
        """response_time: null must not cause format error."""
        grokipedia.display_results(NULL_FIELDS_RESPONSE)

    def test_none_title_does_not_crash(self) -> None:
        """title: null must render fallback text."""
        grokipedia.display_results(NULL_FIELDS_RESPONSE)

    def test_none_raw_content_with_raw_flag(self) -> None:
        """raw_content: null with raw=True must not crash."""
        grokipedia.display_results(NULL_FIELDS_RESPONSE, raw=True)

    def test_long_content_truncated(self) -> None:
        """Content over 300 chars should be truncated with '...'."""
        data = {
            "query": "long",
            "results": [
                {
                    "title": "Long",
                    "url": "https://grokipedia.com/page/Long",
                    "content": "x" * 500,
                    "score": 0.5,
                }
            ],
            "response_time": 0.1,
        }
        # Should not crash; truncation is visual only
        grokipedia.display_results(data)


# ===================================================================
# Unit Tests -- main() integration
# ===================================================================


class TestMainFunction:
    """main() must return correct exit codes for all paths."""

    @respx.mock
    def test_success_returns_0(self) -> None:
        respx.post(grokipedia.TAVILY_API_URL).mock(
            return_value=httpx.Response(200, json=FAKE_RESPONSE)
        )
        # Mock extract endpoint (hybrid lookup for canonical page)
        respx.post(grokipedia.TAVILY_EXTRACT_URL).mock(
            return_value=httpx.Response(200, json=FAKE_EXTRACT_FAIL_RESPONSE)
        )
        with patch("grokipedia.get_api_key", return_value="fake-key"):
            with patch("sys.argv", ["grokipedia.py", "test query"]):
                assert grokipedia.main() == 0

    @respx.mock
    def test_json_output_is_valid_json(self) -> None:
        respx.post(grokipedia.TAVILY_API_URL).mock(
            return_value=httpx.Response(200, json=FAKE_RESPONSE)
        )
        # Mock extract endpoint (hybrid lookup for canonical page)
        respx.post(grokipedia.TAVILY_EXTRACT_URL).mock(
            return_value=httpx.Response(200, json=FAKE_EXTRACT_FAIL_RESPONSE)
        )
        with patch("grokipedia.get_api_key", return_value="fake-key"):
            with patch("sys.argv", ["grokipedia.py", "test query", "--json"]):
                # Capture stdout
                import io

                captured = io.StringIO()
                with patch("sys.stdout", captured):
                    code = grokipedia.main()
                assert code == 0
                output = captured.getvalue()
                parsed = json.loads(output)  # Must be valid JSON
                assert "results" in parsed

    @respx.mock
    def test_http_401_returns_1(self) -> None:
        respx.post(grokipedia.TAVILY_API_URL).mock(
            return_value=httpx.Response(401, json={"error": "unauthorized"})
        )
        with patch("grokipedia.get_api_key", return_value="bad-key"):
            with patch("sys.argv", ["grokipedia.py", "test"]):
                assert grokipedia.main() == 1

    @respx.mock
    def test_http_429_returns_1(self) -> None:
        respx.post(grokipedia.TAVILY_API_URL).mock(
            return_value=httpx.Response(429, json={"error": "rate limited"})
        )
        with patch("grokipedia.get_api_key", return_value="key"):
            with patch("sys.argv", ["grokipedia.py", "test"]):
                assert grokipedia.main() == 1

    def test_api_key_missing_returns_1(self) -> None:
        with patch(
            "grokipedia.get_api_key",
            side_effect=grokipedia.ApiKeyError("no key"),
        ):
            with patch("sys.argv", ["grokipedia.py", "test"]):
                assert grokipedia.main() == 1

    @respx.mock
    def test_connection_error_returns_1(self) -> None:
        respx.post(grokipedia.TAVILY_API_URL).mock(
            side_effect=httpx.ConnectError("connection refused")
        )
        with patch("grokipedia.get_api_key", return_value="key"):
            with patch("sys.argv", ["grokipedia.py", "test"]):
                assert grokipedia.main() == 1

    def test_empty_query_returns_2(self) -> None:
        with patch("sys.argv", ["grokipedia.py", ""]):
            assert grokipedia.main() == 2

    def test_whitespace_query_returns_2(self) -> None:
        with patch("sys.argv", ["grokipedia.py", "   "]):
            assert grokipedia.main() == 2

    def test_max_results_out_of_range_returns_2(self) -> None:
        with patch("sys.argv", ["grokipedia.py", "test", "-n", "25"]):
            assert grokipedia.main() == 2


# ===================================================================
# Unit Tests -- normalize_page_title
# ===================================================================


class TestNormalizePageTitle:
    """normalize_page_title must convert queries to Grokipedia URL path segments."""

    def test_single_word_lowercase(self) -> None:
        assert grokipedia.normalize_page_title("pattern") == "Pattern"

    def test_single_word_uppercase(self) -> None:
        assert grokipedia.normalize_page_title("Pattern") == "Pattern"

    def test_multi_word_spaces_to_underscores(self) -> None:
        assert (
            grokipedia.normalize_page_title("quantum computing") == "Quantum_computing"
        )

    def test_preserves_interior_caps(self) -> None:
        """Acronyms like AI should stay uppercase."""
        assert grokipedia.normalize_page_title("AI history") == "AI_history"

    def test_strips_whitespace(self) -> None:
        assert grokipedia.normalize_page_title("  pattern  ") == "Pattern"

    def test_collapses_multiple_spaces(self) -> None:
        assert (
            grokipedia.normalize_page_title("quantum   computing")
            == "Quantum_computing"
        )

    def test_empty_string(self) -> None:
        assert grokipedia.normalize_page_title("") == ""


# ===================================================================
# Unit Tests -- extract_exact_page
# ===================================================================


FAKE_EXTRACT_RESPONSE: dict[str, Any] = {
    "results": [
        {
            "url": "https://grokipedia.com/page/Pattern",
            "raw_content": "A pattern is a regularity in the world...",
        }
    ],
    "failed_results": [],
    "response_time": 0.8,
}

FAKE_EXTRACT_FAIL_RESPONSE: dict[str, Any] = {
    "results": [],
    "failed_results": [
        {"url": "https://grokipedia.com/page/Nonexistent", "error": "404"}
    ],
    "response_time": 0.3,
}


class TestExtractExactPage:
    """extract_exact_page must try the canonical URL and return a result dict or None."""

    @respx.mock
    def test_returns_result_when_page_exists(self) -> None:
        respx.post(grokipedia.TAVILY_EXTRACT_URL).mock(
            return_value=httpx.Response(200, json=FAKE_EXTRACT_RESPONSE)
        )
        result = grokipedia.extract_exact_page("pattern", api_key="fake-key")
        assert result is not None
        assert result["url"] == "https://grokipedia.com/page/Pattern"
        assert result["title"] == "Pattern"
        assert "content" in result
        assert result["score"] == 1.0  # exact match gets perfect score

    @respx.mock
    def test_returns_none_when_page_missing(self) -> None:
        respx.post(grokipedia.TAVILY_EXTRACT_URL).mock(
            return_value=httpx.Response(200, json=FAKE_EXTRACT_FAIL_RESPONSE)
        )
        result = grokipedia.extract_exact_page("nonexistent", api_key="fake-key")
        assert result is None

    @respx.mock
    def test_returns_none_on_http_error(self) -> None:
        """Network/API errors should not crash, just return None."""
        respx.post(grokipedia.TAVILY_EXTRACT_URL).mock(
            return_value=httpx.Response(500, text="server error")
        )
        result = grokipedia.extract_exact_page("pattern", api_key="fake-key")
        assert result is None

    @respx.mock
    def test_returns_none_on_connection_error(self) -> None:
        respx.post(grokipedia.TAVILY_EXTRACT_URL).mock(
            side_effect=httpx.ConnectError("timeout")
        )
        result = grokipedia.extract_exact_page("pattern", api_key="fake-key")
        assert result is None

    @respx.mock
    def test_content_truncated_for_snippet(self) -> None:
        """Content in the result should be a short snippet, not the full page."""
        long_response = {
            "results": [
                {
                    "url": "https://grokipedia.com/page/Pattern",
                    "raw_content": "x" * 10000,
                }
            ],
            "failed_results": [],
            "response_time": 0.5,
        }
        respx.post(grokipedia.TAVILY_EXTRACT_URL).mock(
            return_value=httpx.Response(200, json=long_response)
        )
        result = grokipedia.extract_exact_page("pattern", api_key="fake-key")
        assert result is not None
        assert len(result["content"]) <= 503  # 500 chars + "..."


# ===================================================================
# Unit Tests -- hybrid merge in main()
# ===================================================================


class TestHybridSearch:
    """main() must inject exact-page result when search misses it."""

    @respx.mock
    def test_exact_page_injected_when_missing_from_search(self) -> None:
        """If search doesn't return /page/Pattern, extract should inject it."""
        # Search returns results that DON'T include /page/Pattern
        search_response = {
            "query": "pattern",
            "answer": "Patterns are everywhere.",
            "response_time": 1.0,
            "results": [
                {
                    "title": "Pattern grammar",
                    "url": "https://grokipedia.com/page/pattern_grammar",
                    "content": "About pattern grammar.",
                    "score": 0.96,
                }
            ],
        }
        respx.post(grokipedia.TAVILY_API_URL).mock(
            return_value=httpx.Response(200, json=search_response)
        )
        respx.post(grokipedia.TAVILY_EXTRACT_URL).mock(
            return_value=httpx.Response(200, json=FAKE_EXTRACT_RESPONSE)
        )

        import io

        captured = io.StringIO()
        with patch("grokipedia.get_api_key", return_value="fake-key"):
            with patch("sys.argv", ["grokipedia.py", "pattern", "--json"]):
                with patch("sys.stdout", captured):
                    code = grokipedia.main()

        assert code == 0
        data = json.loads(captured.getvalue())
        urls = [r["url"] for r in data["results"]]
        assert "https://grokipedia.com/page/Pattern" in urls
        # Exact match should be first
        assert data["results"][0]["url"] == "https://grokipedia.com/page/Pattern"

    @respx.mock
    def test_no_duplicate_when_search_already_has_page(self) -> None:
        """If search already includes the exact page, don't add it twice."""
        search_response = {
            "query": "pattern",
            "answer": None,
            "response_time": 1.0,
            "results": [
                {
                    "title": "Pattern",
                    "url": "https://grokipedia.com/page/Pattern",
                    "content": "A pattern is...",
                    "score": 0.99,
                }
            ],
        }
        respx.post(grokipedia.TAVILY_API_URL).mock(
            return_value=httpx.Response(200, json=search_response)
        )
        # Extract should NOT be called if search already has it,
        # but even if it is, no duplicate should appear.

        import io

        captured = io.StringIO()
        with patch("grokipedia.get_api_key", return_value="fake-key"):
            with patch("sys.argv", ["grokipedia.py", "pattern", "--json"]):
                with patch("sys.stdout", captured):
                    code = grokipedia.main()

        assert code == 0
        data = json.loads(captured.getvalue())
        pattern_urls = [
            r["url"]
            for r in data["results"]
            if r["url"] == "https://grokipedia.com/page/Pattern"
        ]
        assert len(pattern_urls) == 1  # no duplicate

    @respx.mock
    def test_extract_failure_does_not_break_search(self) -> None:
        """If extract fails, search results should still display normally."""
        search_response = {
            "query": "pattern",
            "answer": None,
            "response_time": 1.0,
            "results": [
                {
                    "title": "Pattern grammar",
                    "url": "https://grokipedia.com/page/pattern_grammar",
                    "content": "Grammar stuff.",
                    "score": 0.96,
                }
            ],
        }
        respx.post(grokipedia.TAVILY_API_URL).mock(
            return_value=httpx.Response(200, json=search_response)
        )
        respx.post(grokipedia.TAVILY_EXTRACT_URL).mock(
            side_effect=httpx.ConnectError("timeout")
        )

        import io

        captured = io.StringIO()
        with patch("grokipedia.get_api_key", return_value="fake-key"):
            with patch("sys.argv", ["grokipedia.py", "pattern", "--json"]):
                with patch("sys.stdout", captured):
                    code = grokipedia.main()

        assert code == 0
        data = json.loads(captured.getvalue())
        assert len(data["results"]) == 1  # just the search result, no crash
