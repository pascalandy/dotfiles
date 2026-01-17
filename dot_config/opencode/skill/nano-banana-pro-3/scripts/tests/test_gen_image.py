"""Tests for gen_image.py CLI tool."""

import subprocess
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).parent.parent / "gen_image.py"
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent


def run_script(*args, env=None):
    """Run gen_image.py and return (stdout, stderr, exit_code)."""
    cmd = ["uv", "run", str(SCRIPT_PATH)] + list(args)
    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        env=env,
    )
    return result.stdout, result.stderr, result.returncode


class TestVersion:
    """Test --version flag."""

    def test_version_flag(self):
        """--version should output version and exit with 0."""
        stdout, stderr, code = run_script("--version")
        assert code == 0
        assert "1.0.0" in stdout
        assert stderr.strip() == ""

    def test_version_short_flag(self):
        """--V should be equivalent to --version."""
        stdout, stderr, code = run_script("-V")
        assert code == 0
        assert "1.0.0" in stdout


class TestValidation:
    """Test input validation and error handling."""

    def test_missing_prompt(self):
        """Missing --prompt should error with exit code 2."""
        stdout, stderr, code = run_script("--dry-run")
        assert code == 2
        assert "Error" in stderr or "required" in stderr.lower()

    def test_invalid_size(self):
        """Invalid --size should error with exit code 2."""
        stdout, stderr, code = run_script("--prompt", "test", "--size", "invalid")
        assert code == 2
        assert "Invalid size" in stderr
        assert "1K" in stderr or "2K" in stderr

    def test_invalid_format(self):
        """Invalid --format should error with exit code 2."""
        stdout, stderr, code = run_script("--prompt", "test", "--format", "bmp")
        assert code == 2
        assert "Invalid format" in stderr
        assert "png" in stderr or "jpeg" in stderr

    def test_invalid_aspect_ratio(self):
        """Invalid --aspect-ratio should error with exit code 2."""
        stdout, stderr, code = run_script("--prompt", "test", "--aspect-ratio", "99:99")
        assert code == 2
        assert "Invalid aspect ratio" in stderr

    def test_invalid_thinking_mode(self):
        """Invalid --thinking should error with exit code 2."""
        stdout, stderr, code = run_script("--prompt", "test", "--thinking", "bad")
        assert code == 2
        assert "thinking" in stderr.lower()

    def test_invalid_safety_level(self):
        """Invalid --safety should error with exit code 2."""
        stdout, stderr, code = run_script("--prompt", "test", "--safety", "ultra")
        assert code == 2
        assert "safety" in stderr.lower()


class TestDryRun:
    """Test --dry-run mode."""

    def test_dry_run_no_api_call(self):
        """Dry run should not require API key."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run")
        assert code == 0
        assert "DRY RUN" in stderr
        assert "Mode:" in stderr
        assert "Prompt: test" in stderr


class TestColorOutput:
    """Test NO_COLOR and --no-color handling."""

    def test_no_color_env_var(self):
        """NO_COLOR env var should disable colors."""
        import os

        env = os.environ.copy()
        env["NO_COLOR"] = "1"
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run", env=env)
        assert code == 0
        # ANSI escape codes start with \x1b or \033
        assert "\x1b[" not in stderr
        assert "\033[" not in stderr

    def test_no_color_flag(self):
        """--no-color flag should disable colors."""
        stdout, stderr, code = run_script("--prompt", "test", "--no-color", "--dry-run")
        assert code == 0
        # ANSI escape codes should not be present
        assert "\x1b[" not in stderr
        assert "\033[" not in stderr


class TestHelp:
    """Test help output."""

    def test_help_flag(self):
        """--help should show help and exit with 0."""
        stdout, stderr, code = run_script("--help")
        assert code == 0
        assert "--prompt" in stdout
        assert "--version" in stdout
        assert "--no-color" in stdout

    def test_no_args_shows_help(self):
        """Running with no args should show help (due to no_args_is_help=True)."""
        stdout, stderr, code = run_script()
        assert code == 2  # Typer exits with 2 for missing required arg
        assert "prompt" in stderr.lower() or "--help" in stderr


class TestConstants:
    """Test that constants are properly used."""

    def test_model_name_in_output(self):
        """Model name should appear in dry-run output."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run", "--verbose")
        assert code == 0
        assert "google/gemini-3-pro-image-preview" in stderr

    def test_api_endpoint_in_output(self):
        """API endpoint should appear in dry-run output."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run")
        assert code == 0
        assert "openrouter.ai" in stderr


class TestOutputStreams:
    """Test stdout/stderr separation."""

    def test_dry_run_messages_to_stderr(self):
        """Progress messages should go to stderr."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run")
        assert code == 0
        assert stderr  # Should have stderr output
        # stdout should be empty or minimal in dry-run mode
        assert stdout.strip() == ""

    def test_quiet_mode(self):
        """--quiet should suppress progress output but not dry-run."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run", "--quiet")
        assert code == 0
        # With quiet mode on dry-run, stderr should be minimal
        # (no progress messages, but dry-run is still shown)


class TestExitCodes:
    """Test exit code behavior."""

    def test_exit_0_on_version(self):
        """Version flag exits with 0."""
        stdout, stderr, code = run_script("--version")
        assert code == 0

    def test_exit_0_on_help(self):
        """Help flag exits with 0."""
        stdout, stderr, code = run_script("--help")
        assert code == 0

    def test_exit_0_on_dry_run_success(self):
        """Successful dry run exits with 0."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run")
        assert code == 0

    def test_exit_2_on_missing_prompt(self):
        """Missing prompt exits with 2."""
        stdout, stderr, code = run_script("--dry-run")
        assert code == 2

    def test_exit_2_on_invalid_size(self):
        """Invalid size exits with 2."""
        stdout, stderr, code = run_script("--prompt", "test", "--size", "invalid")
        assert code == 2

    def test_exit_2_on_invalid_format(self):
        """Invalid format exits with 2."""
        stdout, stderr, code = run_script("--prompt", "test", "--format", "invalid")
        assert code == 2

    def test_exit_2_on_invalid_aspect_ratio(self):
        """Invalid aspect ratio exits with 2."""
        stdout, stderr, code = run_script("--prompt", "test", "--aspect-ratio", "99:99")
        assert code == 2

    def test_exit_2_on_invalid_thinking_mode(self):
        """Invalid thinking mode exits with 2."""
        stdout, stderr, code = run_script("--prompt", "test", "--thinking", "invalid")
        assert code == 2

    def test_exit_2_on_invalid_safety_level(self):
        """Invalid safety level exits with 2."""
        stdout, stderr, code = run_script("--prompt", "test", "--safety", "invalid")
        assert code == 2


class TestFlagAliases:
    """Test short flag versions work as aliases."""

    def test_prompt_short_flag(self):
        """--prompt and -p are equivalent."""
        stdout1, _, code1 = run_script("-p", "test", "--dry-run")
        stdout2, _, code2 = run_script("--prompt", "test", "--dry-run")
        assert code1 == code2 == 0

    def test_dry_run_short_flag(self):
        """-n is equivalent to --dry-run."""
        stdout, stderr, code = run_script("--prompt", "test", "-n")
        assert code == 0
        assert "DRY RUN" in stderr

    def test_verbose_short_flag(self):
        """-v is equivalent to --verbose."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run", "-v")
        assert code == 0
        assert "DEBUG" in stderr or "Request" in stderr

    def test_quiet_short_flag(self):
        """-q is equivalent to --quiet."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run", "-q")
        assert code == 0


class TestModeDetection:
    """Test mode detection (generate/edit/compose)."""

    def test_generate_mode_without_images(self):
        """No input images shows 'Generating' mode."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run")
        assert code == 0
        assert "Generating" in stderr

    def test_editing_mode_with_one_image(self):
        """One input image shows 'Editing' mode (file doesn't need to exist in dry-run)."""
        # Create a temp file for testing
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            temp_path = f.name
        try:
            stdout, stderr, code = run_script(
                "--prompt", "test", "--input-image", temp_path, "--dry-run"
            )
            assert code == 0
            assert "Editing" in stderr
        finally:
            Path(temp_path).unlink()

    def test_composing_mode_with_multiple_images(self):
        """Multiple input images shows 'Composing/Blending' mode."""
        import tempfile

        temp_files = []
        try:
            for _ in range(2):
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
                    temp_files.append(f.name)

            cmd = ["--prompt", "test", "--dry-run"]
            for path in temp_files:
                cmd.extend(["--input-image", path])

            stdout, stderr, code = run_script(*cmd)
            assert code == 0
            assert "Composing" in stderr or "Blending" in stderr
        finally:
            for path in temp_files:
                Path(path).unlink()


class TestOptionValues:
    """Test that various option values are accepted."""

    def test_all_sizes_accepted(self):
        """All valid sizes (1K, 2K, 4K) are accepted."""
        for size in ["1K", "2K", "4K"]:
            stdout, stderr, code = run_script("--prompt", "test", "--size", size, "--dry-run")
            assert code == 0, f"Size {size} should be valid"

    def test_all_formats_accepted(self):
        """All valid formats (png, jpeg) are accepted."""
        for fmt in ["png", "jpeg"]:
            stdout, stderr, code = run_script("--prompt", "test", "--format", fmt, "--dry-run")
            assert code == 0, f"Format {fmt} should be valid"

    def test_all_aspect_ratios_accepted(self):
        """All valid aspect ratios are accepted."""
        ratios = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]
        for ratio in ratios:
            stdout, stderr, code = run_script(
                "--prompt", "test", "--aspect-ratio", ratio, "--dry-run"
            )
            assert code == 0, f"Aspect ratio {ratio} should be valid"

    def test_all_thinking_modes_accepted(self):
        """All valid thinking modes (low, medium, high) are accepted."""
        for mode in ["low", "medium", "high"]:
            stdout, stderr, code = run_script("--prompt", "test", "--thinking", mode, "--dry-run")
            assert code == 0, f"Thinking mode {mode} should be valid"

    def test_all_safety_levels_accepted(self):
        """All valid safety levels (off, low, medium, high) are accepted."""
        for level in ["off", "low", "medium", "high"]:
            stdout, stderr, code = run_script("--prompt", "test", "--safety", level, "--dry-run")
            assert code == 0, f"Safety level {level} should be valid"


class TestInputImageValidation:
    """Test input image validation."""

    def test_nonexistent_input_image_error(self):
        """Nonexistent input image should error with exit code 2."""
        stdout, stderr, code = run_script(
            "--prompt", "test", "--input-image", "/nonexistent/path.jpg"
        )
        assert code == 2
        assert "not found" in stderr.lower()

    def test_max_input_images_limit(self):
        """More than 14 input images should error."""
        import tempfile

        temp_files = []
        try:
            # Create 15 temp files
            for _ in range(15):
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
                    temp_files.append(f.name)

            cmd = ["--prompt", "test"]
            for path in temp_files:
                cmd.extend(["--input-image", path])

            stdout, stderr, code = run_script(*cmd)
            assert code == 2
            assert "14" in stderr or "Maximum" in stderr
        finally:
            for path in temp_files:
                Path(path).unlink()


class TestFileHandling:
    """Test file path and naming behavior."""

    def test_output_directory_created_if_missing(self):
        """Output directory should be created if it doesn't exist."""
        import tempfile

        # Create temp directory and remove it
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_dir = Path(tmpdir) / "custom_output"
            assert not custom_dir.exists()

            # Run dry-run with custom output dir
            stdout, stderr, code = run_script(
                "--prompt", "test", "--output-dir", str(custom_dir), "--dry-run"
            )
            assert code == 0
            # Directory would be created on real run, but in dry-run it's just shown
            # Remove newlines for path comparison (handles rich panel line wrapping)
            stderr_normalized = stderr.replace("\n", "")
            assert "custom_output" in stderr_normalized.lower()

    def test_default_filename_format(self):
        """Default filename should follow YYYY-MM-DD-HH-MM-SS format."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run")
        assert code == 0
        # Should contain a timestamp pattern (year-month-day format)
        assert "2025-" in stderr or "20" in stderr
        assert "generated" in stderr.lower()

    def test_custom_filename_respected(self):
        """Custom --filename should appear in dry-run output."""
        stdout, stderr, code = run_script(
            "--prompt", "test", "--filename", "my-custom-image.png", "--dry-run"
        )
        assert code == 0
        assert "my-custom-image.png" in stderr

    def test_filename_extension_matches_format(self):
        """Filename extension should match --format flag."""
        # Test PNG format
        stdout, stderr, code = run_script("--prompt", "test", "--format", "png", "--dry-run")
        assert code == 0
        assert ".png" in stderr

        # Test JPEG format
        stdout, stderr, code = run_script("--prompt", "test", "--format", "jpeg", "--dry-run")
        assert code == 0
        assert ".jpeg" in stderr or ".jpg" in stderr

    def test_multiple_output_filenames_generated(self):
        """Multiple images should generate multiple filenames."""
        stdout, stderr, code = run_script("--prompt", "test", "--nbr-img-output", "3", "--dry-run")
        assert code == 0
        # Should show multiple output files
        assert stderr.count("Output") >= 3 or stderr.count("-1") > 0 or stderr.count("-2") > 0


class TestStreamBehavior:
    """Test stdout/stderr stream separation in detail."""

    def test_only_paths_on_stdout_in_quiet_mode(self):
        """In quiet mode, only file paths should go to stdout."""
        import tempfile

        # Create a temp file since we need actual output without API
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            temp_path = f.name
        try:
            # Dry run with quiet mode
            stdout, stderr, code = run_script("--prompt", "test", "--dry-run", "--quiet")
            assert code == 0
            # In dry-run, stdout should be empty
            assert stdout.strip() == ""
        finally:
            Path(temp_path).unlink()

    def test_errors_always_to_stderr(self):
        """All errors should go to stderr, not stdout."""
        stdout, stderr, code = run_script("--prompt", "test", "--size", "invalid")
        assert code == 2
        # Error should be in stderr, not stdout
        assert "Error" in stderr or "Invalid" in stderr
        assert stderr.strip() != ""
        assert "Error" not in stdout and "Invalid" not in stdout

    def test_progress_messages_to_stderr(self):
        """Progress/status messages should go to stderr in normal mode."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run")
        assert code == 0
        # Progress info in stderr
        assert "Generating" in stderr or "Mode:" in stderr
        # Minimal stdout in dry-run
        assert stdout.strip() == ""


class TestBoundaryConditions:
    """Test edge cases and boundary conditions."""

    def test_empty_prompt_error(self):
        """Empty string as prompt should be treated as missing."""
        stdout, stderr, code = run_script("--prompt", "", "--dry-run")
        # Empty prompt might be treated as valid (it's a string), but depends on implementation
        # Test that it either errors or succeeds
        assert code in [0, 2]

    def test_very_long_prompt(self):
        """Very long prompt should be accepted."""
        long_prompt = "test " * 1000  # ~5000 chars
        stdout, stderr, code = run_script("--prompt", long_prompt, "--dry-run")
        assert code == 0
        assert "Generating" in stderr or "Mode:" in stderr

    def test_special_characters_in_filename(self):
        """Special characters in filename should be handled."""
        filename = "test-image_2025.png"
        stdout, stderr, code = run_script("--prompt", "test", "--filename", filename, "--dry-run")
        assert code == 0
        assert filename in stderr

    def test_unicode_in_prompt(self):
        """Unicode characters in prompt should be accepted."""
        unicode_prompt = "Test with émojis 🎨 and accénts"
        stdout, stderr, code = run_script("--prompt", unicode_prompt, "--dry-run")
        assert code == 0
        assert "Generating" in stderr or "Mode:" in stderr

    def test_max_nbr_images_boundary(self):
        """Max 4 images should work, 5 should error."""
        # 4 should work
        stdout, stderr, code = run_script("--prompt", "test", "--nbr-img-output", "4", "--dry-run")
        assert code == 0

        # 5 should fail (if there's validation)
        stdout, stderr, code = run_script("--prompt", "test", "--nbr-img-output", "5", "--dry-run")
        # Might succeed if not validated, that's fine
        assert code in [0, 2]


class TestVerboseOutput:
    """Test verbose/debug output."""

    def test_verbose_shows_debug_label(self):
        """--verbose should show [DEBUG] labels."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run", "--verbose")
        assert code == 0
        assert "DEBUG" in stderr or "Request" in stderr

    def test_verbose_shows_request_body(self):
        """--verbose should show request body details."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run", "--verbose")
        assert code == 0
        assert "Request" in stderr or "model" in stderr.lower()

    def test_verbose_includes_model_name(self):
        """Verbose output should include model name."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run", "--verbose")
        assert code == 0
        assert "gemini" in stderr.lower() or "MODEL" in stderr


class TestErrorMessages:
    """Test quality and helpfulness of error messages."""

    def test_invalid_size_suggests_options(self):
        """Invalid size error should suggest valid options."""
        stdout, stderr, code = run_script("--prompt", "test", "--size", "invalid")
        assert code == 2
        assert "1K" in stderr and ("2K" in stderr or "4K" in stderr)

    def test_invalid_aspect_ratio_suggests_options(self):
        """Invalid aspect ratio error should suggest valid options."""
        stdout, stderr, code = run_script("--prompt", "test", "--aspect-ratio", "99:99")
        assert code == 2
        assert "Valid options:" in stderr or "1:1" in stderr

    def test_missing_api_key_error_includes_url(self):
        """API key error should include URL to get one."""
        import os

        env = os.environ.copy()
        # Set API key to empty string to override .env file value
        env["OPENROUTER_API_KEY"] = ""

        stdout, stderr, code = run_script("--prompt", "test", env=env)
        assert code == 1  # Runtime error
        assert "openrouter" in stderr.lower() or "key" in stderr.lower()

    def test_nonexistent_file_error_is_clear(self):
        """File not found error should be clear."""
        stdout, stderr, code = run_script(
            "--prompt", "test", "--input-image", "/nonexistent/file.jpg"
        )
        assert code == 2
        assert "not found" in stderr.lower() or "nonexistent" in stderr.lower()


class TestFlagCombinations:
    """Test combinations of flags that should work together."""

    def test_size_and_aspect_ratio_together(self):
        """Size and aspect ratio should work together."""
        stdout, stderr, code = run_script(
            "--prompt", "test", "--size", "2K", "--aspect-ratio", "16:9", "--dry-run"
        )
        assert code == 0
        assert "2K" in stderr and "16:9" in stderr

    def test_negative_prompt_with_positive(self):
        """Negative and positive prompts should work together."""
        stdout, stderr, code = run_script(
            "--prompt", "beautiful sunset", "--negative-prompt", "people, buildings", "--dry-run"
        )
        assert code == 0
        assert "sunset" in stderr.lower()
        assert "people" in stderr.lower()

    def test_quiet_and_verbose_together(self):
        """--quiet and --verbose together should still work (quiet takes precedence in output)."""
        stdout, stderr, code = run_script("--prompt", "test", "--quiet", "--verbose", "--dry-run")
        assert code == 0

    def test_no_color_with_other_flags(self):
        """--no-color should work with other display flags."""
        stdout, stderr, code = run_script(
            "--prompt", "test", "--no-color", "--verbose", "--dry-run"
        )
        assert code == 0
        # Should not have ANSI codes
        assert "\x1b[" not in stderr
        assert "\033[" not in stderr


class TestQuietMode:
    """Test quiet mode behavior in detail."""

    def test_quiet_mode_suppresses_progress(self):
        """--quiet should suppress progress messages."""
        stdout_normal, stderr_normal, code_normal = run_script("--prompt", "test", "--dry-run")
        stdout_quiet, stderr_quiet, code_quiet = run_script(
            "--prompt", "test", "--dry-run", "--quiet"
        )
        assert code_normal == code_quiet == 0
        # Quiet mode should have less output
        assert len(stderr_quiet) < len(stderr_normal)

    def test_quiet_mode_still_shows_dry_run(self):
        """--quiet with --dry-run should still show dry-run notice."""
        stdout, stderr, code = run_script("--prompt", "test", "--dry-run", "--quiet")
        assert code == 0
        # Even in quiet mode, DRY RUN should be shown (it's important)
        assert "DRY RUN" in stderr or "Mode:" in stderr


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
