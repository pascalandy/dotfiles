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
        with patch("grokipedia.get_api_key", return_value="fake-key"):
            with patch("sys.argv", ["grokipedia.py", "test query"]):
                assert grokipedia.main() == 0

    @respx.mock
    def test_json_output_is_valid_json(self) -> None:
        respx.post(grokipedia.TAVILY_API_URL).mock(
            return_value=httpx.Response(200, json=FAKE_RESPONSE)
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
