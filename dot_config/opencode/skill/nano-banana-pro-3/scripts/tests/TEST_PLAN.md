# Test Plan for gen_image.py

## Current Test Coverage

### ✅ Already Implemented (test_gen_image.py)

- **Version**: --version and -V flags
- **Validation**: Missing prompt, invalid size/format/aspect-ratio/thinking/safety
- **Dry Run**: Runs without API key
- **Color Output**: NO_COLOR env var, --no-color flag
- **Help**: --help flag, no-args behavior
- **Constants**: MODEL_NAME and API_BASE_URL used correctly
- **Output Streams**: stderr for progress, stdout separation
- **Quiet Mode**: Progress suppression

---

## Additional Tests to Implement

### 1. File & Path Handling

- [ ] **test_valid_output_directory_creation** - Directory created if doesn't exist
- [ ] **test_custom_filename** - --filename flag works
- [ ] **test_default_timestamped_filename** - Auto-generates YYYY-MM-DD-HH-MM-SS format
- [ ] **test_output_filename_includes_extension** - .png or .jpeg based on --format
- [ ] **test_output_directory_structure** - Respects --output-dir flag
- [ ] **test_absolute_path_filename** - Absolute paths work correctly

### 2. Input Image Handling

- [ ] **test_nonexistent_input_image** - Error when --input-image file not found
- [ ] **test_multiple_input_images** - Multiple --input-image flags accepted
- [ ] **test_max_input_images** - Max 14 images (should error with 15+)
- [ ] **test_input_image_extensions** - Accepts .jpg, .jpeg, .png, etc.

### 3. Flag Combinations & Options

- [ ] **test_size_aspect_ratio_combination** - Both flags work together
- [ ] **test_nbr_img_output_default** - Default is 1 image
- [ ] **test_nbr_img_output_multiple** - 2-4 images generate with -c flag
- [ ] **test_nbr_img_output_max** - Max 4 images (should error with 5+)
- [ ] **test_seed_reproducibility** - Same seed works (documented behavior)
- [ ] **test_negative_prompt_with_prompt** - Both work together
- [ ] **test_all_thinking_modes** - low, medium, high accepted
- [ ] **test_all_safety_levels** - off, low, medium, high accepted
- [ ] **test_all_sizes** - 1K, 2K, 4K accepted
- [ ] **test_all_aspect_ratios** - All 10 ratios accepted

### 4. Configuration & Environment

- [ ] **test_api_key_from_env_var** - OPENROUTER_API_KEY env var read
- [ ] **test_api_key_missing_error** - Helpful error message with URL
- [ ] **test_timeout_option** - --timeout changes timeout value
- [ ] **test_timeout_default** - Default is 120 seconds

### 5. Output & Stream Behavior

- [ ] **test_quiet_mode_only_paths** - Quiet mode outputs only file paths to stdout
- [ ] **test_quiet_mode_suppresses_stderr** - Progress messages suppressed
- [ ] **test_verbose_includes_debug_info** - --verbose shows API request/response
- [ ] **test_verbose_shows_traceback** - --verbose shows full error traceback
- [ ] **test_error_messages_to_stderr** - All errors go to stderr
- [ ] **test_file_paths_to_stdout** - Only output paths on stdout (for piping)

### 6. Exit Codes

- [ ] **test_exit_0_on_success** - Success returns 0
- [ ] **test_exit_2_on_validation_error** - Validation errors return 2
- [ ] **test_exit_1_on_runtime_error** - API/runtime errors return 1
- [ ] **test_exit_130_on_interrupt** - Ctrl-C returns 130

### 7. Error Messages

- [ ] **test_api_key_error_includes_url** - "https://openrouter.ai/keys" in error
- [ ] **test_validation_error_suggests_options** - Error shows valid choices
- [ ] **test_file_not_found_error_message** - Clear message for missing files
- [ ] **test_error_messages_are_colored** - Errors use red formatting (unless --no-color)

### 8. Flag Aliases (Short vs Long)

- [ ] **test_prompt_short_flag** - -p works as well as --prompt
- [ ] **test_filename_short_flag** - -f works
- [ ] **test_input_image_short_flag** - -i works
- [ ] **test_size_short_flag** - -s works
- [ ] **test_aspect_ratio_short_flag** - -a works
- [ ] **test_dry_run_short_flag** - -n works
- [ ] **test_verbose_short_flag** - -v works
- [ ] **test_nbr_img_output_short_flag** - -c works
- [ ] **test_format_short_flag** - -F works
- [ ] **test_thinking_short_flag** - -t works
- [ ] **test_negative_prompt_short_flag** - -N works
- [ ] **test_output_dir_short_flag** - -o works
- [ ] **test_quiet_short_flag** - -q works

### 9. Help Documentation

- [ ] **test_help_includes_all_flags** - All options documented
- [ ] **test_help_includes_examples** - Usage examples present
- [ ] **test_help_includes_docs_url** - GitHub URL present
- [ ] **test_each_flag_has_description** - All flags documented

### 10. Mode Detection

- [ ] **test_generate_mode** - No input images → "Generating"
- [ ] **test_editing_mode** - One input image → "Editing"
- [ ] **test_composing_mode** - Multiple input images → "Composing/Blending"

### 11. Integration Tests (Mocked API)

- [ ] **test_successful_api_call_outputs_path** - File path printed to stdout
- [ ] **test_api_error_handling** - 403, timeout, quota errors handled
- [ ] **test_api_call_includes_prompt** - Prompt sent to API
- [ ] **test_api_call_includes_model** - MODEL_NAME sent to API
- [ ] **test_api_call_includes_size** - Image size in config
- [ ] **test_api_call_includes_aspect_ratio** - Aspect ratio in config when set

---

## Priority Grouping

### High Priority (MVP Testing)

- Exit codes (0, 2, 1, 130)
- Flag aliases (short forms)
- Input validation (all invalid inputs return 2)
- File path handling (creation, naming)
- Mode detection (generate/edit/compose)
- Stream separation (stdout/stderr)

### Medium Priority (Robustness)

- All flag combinations
- All size/format/ratio/thinking/safety options
- Error messages quality
- Configuration handling
- Quiet/verbose modes
- Color handling

### Low Priority (Nice-to-Have)

- Help documentation completeness
- Integration with mocked API
- Timeout behavior
- Seed reproducibility verification

---

## Test Execution

Run all tests:

```bash
uv run pytest .opencode/skill/nano-banana-pro-3/scripts/tests/ -v
```

Run specific test class:

```bash
uv run pytest .opencode/skill/nano-banana-pro-3/scripts/tests/test_gen_image.py::TestValidation -v
```

Run specific test:

```bash
uv run pytest .opencode/skill/nano-banana-pro-3/scripts/tests/test_gen_image.py::TestValidation::test_invalid_size -v
```
