# Plan: Missing Files Reformatting Script

## Objective
Create a Python script to reformat Obsidian missing files list from verbose format to clean, simple format.

## Analysis of the Problem

### Input Format (BEFORE)
```md
- [[Blinkist - 12 Rules For Life]] in [[_cards/12 Rules for Life; An Antidote to Chaos]]
- [[Gemini 2.5 Pro]] in [[_cards/2025 AGA (Planification)]], [[_cards/Act as editor v11, outline list of topics fro this video]], [[_cards/Claude & Gemini in Concert]], [[_cards/LLM pricing]], [[_cards/Powerlevel10k]], [[_cards/Privatisation De la Vente d'électricité]], [[_cards/Resolving SSL Conflicts between Cloudflare & Traefik (by gemini)]], [[_cards/WNRS, create a new game]], [[_cards/_webclip/100x AI Coding for Real Work]], [[_local/_locally/3e mandat, Desjardins]]
- [[2025-12-16]] in [[_cards/2025 year calendar]], [[_cards/_journal/_daily/2025-12-15]], [[_cards/_journal/_daily/2025-12-17]]
```

### Desired Output Format (AFTER)
```md
- Blinkist - 12 Rules For Life
- Gemini 2.5 Pro
- 2025-12-16
```

## Technical Requirements

### Core Functionality
1. **Parse Input**: Read markdown file with missing files list
2. **Extract Filenames**: Extract the filename from `[[filename]]` pattern
3. **Remove Duplicates**: Each file should appear only once
4. **Clean Format**: Output as simple markdown list without `[[ ]]` or location references
5. **Sort Output**: Alphabetical sorting for easier reading

### Script Specifications
- **Language**: Python 3.12+
- **Runtime**: uv run (PEP 723 format)
- **Dependencies**: Minimal (avoid external dependencies unless necessary)
- **Input**: File path to markdown file containing missing files list
- **Output**: Cleaned list to stdout or new file

### Implementation Plan

#### 1. Script Structure
```python
#!/usr/bin/env uv run python3
# /// script
# dependencies = [
#     "typer",
#     "rich"
# ]
# ///
```

#### 2. Core Functions
- `parse_missing_file(content: str) -> List[str]`
- `extract_filename(line: str) -> Optional[str]`
- `clean_and_sort(filenames: List[str]) -> List[str]`
- `save_output(filenames: List[str], output_path: str) -> None`

#### 3. CLI Interface
- `--input`: Input file path (required)
- `--output`: Output file path (optional, defaults to stdout)
- `--sort`: Sort alphabetically (default: True)
- `--unique`: Remove duplicates (default: True)

#### 4. Error Handling
- File not found errors
- Invalid markdown format
- Empty input handling
- Permission errors for output

### Development Workflow
1. **Create stub functions** with type hints
2. **Write tests** for each function (pytest)
3. **Implement parsing logic** using regex
4. **Add CLI interface** with typer
5. **Add rich output** for better UX
6. **Test with example data**

### Testing Strategy
- Unit tests for parsing logic
- Integration tests with sample files
- CLI argument testing
- Edge case handling (empty files, malformed input)

### File Structure
```
EXPORT/obs_restore/
├── scripts/
│   ├── missing_files_formatter.py
│   └── test_missing_files_formatter.py
├── input/
│   └── missing_files_example.md
└── output/
    └── cleaned_missing_files.md
```

## Success Criteria
1. ✅ Parses the complex input format correctly
2. ✅ Extracts clean filenames without brackets
3. ✅ Removes duplicates and sorts output
4. ✅ Handles edge cases gracefully
5. ✅ Provides clear CLI interface
6. ✅ Follows uv/PEP 723 conventions
7. ✅ Includes comprehensive tests

## Next Steps
1. Create the script with basic structure
2. Implement core parsing logic
3. Add CLI interface with typer
4. Write comprehensive tests
5. Test with provided example
6. Export final script to EXPORT/obs_restore/