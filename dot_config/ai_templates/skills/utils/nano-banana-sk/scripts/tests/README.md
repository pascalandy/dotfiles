# Test Suite for gen_image.py

## Overview

This test suite provides comprehensive coverage for the `gen_image.py` CLI tool. Tests are organized by functionality and use pytest for execution.

**Current: 65 tests across 18 test classes** (high + medium priority areas covered)

## Test File Structure

```
tests/
├── test_gen_image.py    # Main test file
├── TEST_PLAN.md         # Planned tests (current + future)
└── README.md            # This file
```

## Test Organization

### Test Classes (Current Implementation)

**Tier 1: Core Functionality (39 tests)**

#### 1. **TestVersion** (2 tests)

- `test_version_flag` - Verifies `--version` outputs version
- `test_version_short_flag` - Verifies `-V` alias works

#### 2. **TestValidation** (6 tests)

- `test_missing_prompt` - Prompt is required
- `test_invalid_size` - Size validation
- `test_invalid_format` - Format validation
- `test_invalid_aspect_ratio` - Aspect ratio validation
- `test_invalid_thinking_mode` - Thinking mode validation
- `test_invalid_safety_level` - Safety level validation

#### 3. **TestDryRun** (1 test)

- `test_dry_run_no_api_call` - Dry-run doesn't need API key

#### 4. **TestColorOutput** (2 tests)

- `test_no_color_env_var` - NO_COLOR environment variable support
- `test_no_color_flag` - --no-color flag support

#### 5. **TestHelp** (2 tests)

- `test_help_flag` - --help shows help
- `test_no_args_shows_help` - No args triggers help

#### 6. **TestConstants** (2 tests)

- `test_model_name_in_output` - MODEL_NAME constant used
- `test_api_endpoint_in_output` - API_BASE_URL constant used

#### 7. **TestOutputStreams** (2 tests)

- `test_dry_run_messages_to_stderr` - Messages go to stderr
- `test_quiet_mode` - Quiet mode suppresses output

#### 8. **TestExitCodes** (8 tests)

- Exit code 0 for: version, help, dry-run success
- Exit code 2 for: missing prompt, invalid size/format/aspect-ratio/thinking/safety

#### 9. **TestFlagAliases** (4 tests)

- Short flags: `-p`, `-n`, `-v`, `-q` work as aliases

#### 10. **TestModeDetection** (3 tests)

- "Generating" - no input images
- "Editing" - one input image
- "Composing/Blending" - multiple input images

#### 11. **TestOptionValues** (5 tests)

- All sizes (1K, 2K, 4K) accepted
- All formats (png, jpeg) accepted
- All aspect ratios accepted
- All thinking modes (low, medium, high) accepted
- All safety levels (off, low, medium, high) accepted

#### 12. **TestInputImageValidation** (2 tests)

- Nonexistent input image errors
- Max 14 images enforced

**Tier 2: High-Priority Edge Cases (16 tests)**

#### 13. **TestFileHandling** (5 tests)

- Output directory creation
- Default filename format (timestamp)
- Custom filename respected
- Filename extension matches format
- Multiple output filenames generated

#### 14. **TestStreamBehavior** (3 tests)

- Only paths on stdout in quiet mode
- Errors always to stderr
- Progress messages to stderr

#### 15. **TestBoundaryConditions** (5 tests)

- Empty prompt handling
- Very long prompt (5000+ chars)
- Special characters in filename
- Unicode in prompt (émojis)
- Max images boundary (4 limit)

**Tier 3: Medium-Priority Features (10 tests)**

#### 16. **TestVerboseOutput** (3 tests)

- Verbose shows DEBUG labels
- Verbose shows request body
- Verbose includes model name

#### 17. **TestErrorMessages** (4 tests)

- Invalid size suggests valid options
- Invalid aspect ratio suggests options
- API key error includes help URL
- Nonexistent file error is clear

#### 18. **TestFlagCombinations** (4 tests)

- Size + aspect ratio together
- Negative prompt + positive prompt
- Quiet + verbose compatibility
- --no-color with other flags

#### 19. **TestQuietMode** (2 tests)

- Quiet mode suppresses progress
- Quiet mode still shows dry-run

**Total: 65 tests** (across 19 test classes)

---

## Running Tests

### Run All Tests

```bash
uv run pytest .opencode/skill/nano-banana-pro-3/scripts/tests/ -v
```

### Run Specific Test Class

```bash
uv run pytest .opencode/skill/nano-banana-pro-3/scripts/tests/test_gen_image.py::TestValidation -v
```

### Run Specific Test

```bash
uv run pytest .opencode/skill/nano-banana-pro-3/scripts/tests/test_gen_image.py::TestValidation::test_invalid_size -v
```

### Run with Coverage

```bash
uv run pytest .opencode/skill/nano-banana-pro-3/scripts/tests/ --cov
```

### Run Tests Matching Pattern

```bash
uv run pytest .opencode/skill/nano-banana-pro-3/scripts/tests/ -k "exit_code" -v
```

---

## Test Coverage

| Category              | Tests  | Coverage                    |
| --------------------- | ------ | --------------------------- |
| Version & Help        | 4      | Version, help flags         |
| Validation            | 6      | Input validation errors     |
| Exit Codes            | 8      | All exit code scenarios     |
| Flag Aliases          | 4      | Short form flags            |
| Mode Detection        | 3      | Generate/Edit/Compose modes |
| Option Values         | 5      | Valid option combinations   |
| Input Images          | 2      | File validation, limits     |
| Color Output          | 2      | NO_COLOR, --no-color        |
| Dry Run               | 1      | Dry-run mode                |
| Help                  | 2      | Help output                 |
| Constants             | 2      | Centralized constants       |
| Streams               | 2      | stdout/stderr separation    |
| **File Handling**     | **5**  | **Paths, naming, formats**  |
| **Stream Behavior**   | **3**  | **stdout/stderr details**   |
| **Boundaries**        | **5**  | **Edge cases, limits**      |
| **Verbose Output**    | **3**  | **Debug info verification** |
| **Error Messages**    | **4**  | **Clarity, helpfulness**    |
| **Flag Combinations** | **4**  | **Multi-flag scenarios**    |
| **Quiet Mode**        | **2**  | **Output suppression**      |
| **TOTAL**             | **65** | **High + Medium priority**  |

---

## Remaining Planned Additions (See TEST_PLAN.md)

### Low Priority (15 tests) - Optional enhancements

- [ ] Seed reproducibility verification
- [ ] Complete help documentation tests
- [ ] Integration tests with mocked API
- [ ] More input image combinations (all 14 at once)
- [ ] File type validation (jpg, png, gif, etc.)
- [ ] Timeout parameter behavior
- [ ] Configuration from .env files
- [ ] API endpoint verification
- [ ] Response status code handling

---

## Test Patterns Used

### Basic Pattern

```python
def test_something(self):
    """Description of what is tested."""
    stdout, stderr, code = run_script("--flag", "value")
    assert code == expected_exit_code
    assert "expected text" in stderr or stdout
```

### With Temporary Files

```python
import tempfile
with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
    temp_path = f.name
try:
    stdout, stderr, code = run_script("--input-image", temp_path)
    assert code == 0
finally:
    Path(temp_path).unlink()
```

### Helper Function

```python
def run_script(*args, env=None):
    """Run gen_image.py and return (stdout, stderr, exit_code)."""
    cmd = ["uv", "run", str(SCRIPT_PATH)] + list(args)
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, env=env)
    return result.stdout, result.stderr, result.returncode
```

---

## Key Testing Principles

1. **No External Dependencies** - Tests use `--dry-run` to avoid API calls
2. **Temporary Files** - Input files created/destroyed per test
3. **Clear Assertions** - Each test verifies one specific behavior
4. **Exit Code Verification** - All user-facing scenarios checked
5. **Stream Separation** - stdout/stderr handled correctly
6. **Option Coverage** - All valid option values tested

---

## Notes

- Tests use `uv run` to execute the script (respects dependencies)
- All tests are non-destructive (no permanent state changes)
- Dry-run mode used to avoid API key requirements
- Temporary files cleaned up after each test
- Tests run quickly (all CLI, no network calls)
