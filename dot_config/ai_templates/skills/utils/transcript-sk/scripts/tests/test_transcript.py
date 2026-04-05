"""Tests for transcript.py -- YouTube transcript generator.

Uses subprocess to test the CLI interface (public API) and direct
imports to test pure functions. No network calls.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.parent / "transcript.py"
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def run_script(*args: str) -> tuple[str, str, int]:
    """Execute transcript.py via uv and return (stdout, stderr, returncode)."""
    cmd = ["uv", "run", str(SCRIPT_PATH), *args]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return result.stdout, result.stderr, result.returncode


# ---------------------------------------------------------------------------
# Slice 1: CLI basics (tracer bullet)
# ---------------------------------------------------------------------------


class TestHelp:
    """--help should print usage and exit 0."""

    def test_help_flag(self) -> None:
        stdout, _stderr, code = run_script("--help")
        assert code == 0
        assert "YouTube" in stdout or "youtube" in stdout.lower()

    def test_no_args_exits_zero(self) -> None:
        """No arguments should show help and exit 0."""
        stdout, _stderr, code = run_script()
        assert code == 0
        assert "YouTube" in stdout or "youtube" in stdout.lower()


class TestListPrompts:
    """--list-prompts should print prompt names from scripts/prompts/."""

    def test_lists_bundled_prompts(self) -> None:
        stdout, _stderr, code = run_script("--list-prompts")
        assert code == 0
        prompt_names = stdout.strip().splitlines()
        assert len(prompt_names) >= 1
        # follow_along_note is the default, must exist
        assert "follow_along_note" in prompt_names

    def test_lists_all_prompts(self) -> None:
        """Every .md file in prompts/ should appear."""
        stdout, _stderr, code = run_script("--list-prompts")
        assert code == 0
        expected = sorted(p.stem for p in PROMPTS_DIR.glob("*.md"))
        actual = sorted(stdout.strip().splitlines())
        assert actual == expected


class TestListModels:
    """--list-models should print model names."""

    def test_default_provider_models(self) -> None:
        stdout, _stderr, code = run_script("--list-models")
        assert code == 0
        assert len(stdout.strip().splitlines()) >= 1

    def test_claude_models(self) -> None:
        stdout, _stderr, code = run_script("--list-models", "--provider", "claude")
        assert code == 0
        models = stdout.strip().splitlines()
        assert any("claude" in m for m in models)

    def test_codex_models(self) -> None:
        stdout, _stderr, code = run_script("--list-models", "--provider", "codex")
        assert code == 0
        assert len(stdout.strip().splitlines()) >= 1


# ---------------------------------------------------------------------------
# Slice 2: --version flag (NEW behavior)
# ---------------------------------------------------------------------------


class TestVersion:
    """--version should print version and exit 0."""

    def test_version_flag(self) -> None:
        stdout, _stderr, code = run_script("--version")
        assert code == 0
        assert "transcript" in stdout.lower()


# ---------------------------------------------------------------------------
# Slice 3: Pure function tests (direct imports)
# ---------------------------------------------------------------------------


class TestCleanTitle:
    def test_removes_special_characters(self) -> None:
        from transcript import clean_title

        assert clean_title("Hello, World!") == "Hello_World"

    def test_truncates_to_50_chars(self) -> None:
        from transcript import clean_title

        result = clean_title("A" * 100)
        assert len(result) == 50

    def test_replaces_spaces_with_underscores(self) -> None:
        from transcript import clean_title

        assert clean_title("foo bar baz") == "foo_bar_baz"

    def test_empty_string(self) -> None:
        from transcript import clean_title

        assert clean_title("") == ""


class TestValidateYoutubeUrl:
    def test_standard_url(self) -> None:
        from transcript import validate_youtube_url

        assert validate_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    def test_short_url(self) -> None:
        from transcript import validate_youtube_url

        assert validate_youtube_url("https://youtu.be/dQw4w9WgXcQ")

    def test_shorts_url(self) -> None:
        from transcript import validate_youtube_url

        assert validate_youtube_url("https://www.youtube.com/shorts/dQw4w9WgXcQ")

    def test_invalid_url(self) -> None:
        from transcript import validate_youtube_url

        assert not validate_youtube_url("https://example.com/video")

    def test_empty_string(self) -> None:
        from transcript import validate_youtube_url

        assert not validate_youtube_url("")


class TestNormalizePromptName:
    def test_strips_md_extension(self) -> None:
        from transcript import normalize_prompt_name

        assert normalize_prompt_name("follow_along_note.md") == "follow_along_note"

    def test_lowercase(self) -> None:
        from transcript import normalize_prompt_name

        assert normalize_prompt_name("Follow_Along_Note") == "follow_along_note"

    def test_strips_whitespace(self) -> None:
        from transcript import normalize_prompt_name

        assert normalize_prompt_name("  short_summary  ") == "short_summary"


class TestResolveModel:
    def test_claude_default(self) -> None:
        from transcript import DEFAULT_CLAUDE_MODEL, PROVIDER_CLAUDE, resolve_model

        assert resolve_model(PROVIDER_CLAUDE, None) == DEFAULT_CLAUDE_MODEL

    def test_codex_default(self) -> None:
        from transcript import DEFAULT_CODEX_MODEL, PROVIDER_CODEX, resolve_model

        assert resolve_model(PROVIDER_CODEX, None) == DEFAULT_CODEX_MODEL

    def test_explicit_model(self) -> None:
        from transcript import PROVIDER_CLAUDE, resolve_model

        assert resolve_model(PROVIDER_CLAUDE, "claude-haiku-4-5") == "claude-haiku-4-5"


class TestIsValidModel:
    def test_valid_claude_model(self) -> None:
        from transcript import PROVIDER_CLAUDE, is_valid_model

        assert is_valid_model(PROVIDER_CLAUDE, "claude-sonnet-4-5")

    def test_invalid_claude_model(self) -> None:
        from transcript import PROVIDER_CLAUDE, is_valid_model

        assert not is_valid_model(PROVIDER_CLAUDE, "gpt-4")

    def test_codex_accepts_anything(self) -> None:
        from transcript import PROVIDER_CODEX, is_valid_model

        assert is_valid_model(PROVIDER_CODEX, "anything-goes")


class TestFormatSummaryMeta:
    def test_claude_stats(self) -> None:
        from transcript import PROVIDER_CLAUDE, format_summary_meta

        stats = {
            "provider": PROVIDER_CLAUDE,
            "model": "claude-sonnet-4-5",
            "effort": "medium",
            "total_tokens": 5000,
            "input_tokens": 4000,
            "output_tokens": 1000,
        }
        result = format_summary_meta(stats)
        assert "Claude" in result
        assert "5,000" in result

    def test_codex_stats(self) -> None:
        from transcript import PROVIDER_CODEX, format_summary_meta

        stats = {
            "provider": PROVIDER_CODEX,
            "model": "gpt-5.4",
            "reasoning_effort": "high",
        }
        result = format_summary_meta(stats)
        assert "Codex" in result

    def test_none_stats(self) -> None:
        from transcript import format_summary_meta

        assert format_summary_meta(None) == "No AI summary"


# ---------------------------------------------------------------------------
# Slice 4: Exit codes -- validation errors should exit 2
# ---------------------------------------------------------------------------


class TestExitCodes:
    """Validation errors should exit 2, not 1."""

    def test_invalid_url_exits_2(self) -> None:
        _stdout, _stderr, code = run_script("https://example.com/not-a-video")
        assert code == 2, f"Expected exit 2 for invalid URL, got {code}"

    def test_invalid_provider_exits_2(self) -> None:
        _stdout, stderr, code = run_script(
            "--provider", "nonexistent", "https://youtu.be/abc"
        )
        assert code == 2, f"Expected exit 2 for invalid provider, got {code}"

    def test_invalid_prompt_exits_2(self) -> None:
        """Unknown prompt name should exit 2."""
        _stdout, _stderr, code = run_script(
            "--prompt", "nonexistent_prompt", "https://youtu.be/dQw4w9WgXcQ"
        )
        assert code == 2, f"Expected exit 2 for invalid prompt, got {code}"
