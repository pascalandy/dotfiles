# Plan: Clean Missing Files Script

## Objective
Create a Python script using `uv` to reformat a list of missing files from an Obsidian vault export.

**Input Format:**
```markdown
- [[Blinkist - 12 Rules For Life]] in [[_cards/12 Rules for Life; An Antidote to Chaos]]
```

**Output Format:**
```markdown
- Blinkist - 12 Rules For Life
```

## Constraints & Standards
- **Tool**: `uv` (PEP 723 inline dependencies).
- **Style**: Mimic `yt_transcriber.py` (shebang, type hinting, `rich` for output, `argparse`).
- **Methodology**: TDD (Test-Driven Development).
- **Location**: `EXPORT/obs_restore/`.

## Steps

### 1. TDD - Create Test Suite
Create `EXPORT/obs_restore/test_clean_missing_files.py` first.
- **Test Cases**:
    - Extract filename from standard line with "in".
    - Handle lines with no "in" clause.
    - Handle special characters in filenames.
    - Ignore non-list lines or empty lines.

### 2. Implementation - Create Script
Create `EXPORT/obs_restore/clean_missing_files.py`.
- **Header**: PEP 723 metadata.
- **Dependencies**: `rich`.
- **Logic**:
    - Use `argparse` for CLI arguments (`input_file`, optional `--output`).
    - Use `re` for robust regex matching: `^-\s*\[\[(.*?)\]\]`
    - Read file, process lines, output result.
- **Features**:
    - Progress display with `rich`.
    - Error handling for file not found.

### 3. Verification
- Run tests: `uv run pytest EXPORT/obs_restore/test_clean_missing_files.py`
- Run script against example: `uv run EXPORT/obs_restore/clean_missing_files.py EXPORT/obs_restore/MISSING_FILES/missing_file_example.md`

## Script Structure (Draft)

```python
#!/usr/bin/env uv run python3
# /// script
# dependencies = [
#     "rich",
# ]
# ///

import argparse
import re
from pathlib import Path
from rich.console import Console

# ... functions ...

if __name__ == "__main__":
    main()
```
