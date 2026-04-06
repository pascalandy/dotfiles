---
name: liteparse-preferences
description: User's default LiteParse settings stored in per-language config files. USE WHEN my preferences, my defaults, parse with my settings, LYKRA, config.json, english parse, french parse.
---

# LiteParse — Preferences

Two configs deployed by chezmoi to `~/.config/liteparse/` (filenames use ISO 639-1; values inside use Tesseract 3-letter codes):

- `~/.config/liteparse/config.en.json` → `ocrLanguage: "eng"`
- `~/.config/liteparse/config.fr.json` → `ocrLanguage: "fra"`

Source of truth: `dot_config/liteparse/` in chezmoi. Edit there, then `chezmoi apply`.

Both share: `dpi: 300`, `outputFormat: text`, `outputSuffix: _LYKRA.md`, `preciseBoundingBox: true`.

Output is plain text (`.txt`). The `outputSuffix` field in the configs is a local naming convention applied by post-processing — `lit` itself ignores it.

## Auto-detect rules (do not ask, just run)

**Path type:**
- **File** → `lit parse <file> --config <cfg> -o <basename>_LYKRA.txt`
- **Directory** → `lit batch-parse <input-dir> <input-dir>_LYKRA --config <cfg> --recursive` THEN rename outputs to add `_LYKRA.txt` suffix.

**Language:** default to `config.en.json`. Switch to `config.fr.json` only if the user explicitly says French / français / fr / fra, or if filenames/content clearly indicate French.

**Output location convention:**
- File → output sibling file: `<dir>/<basename>_LYKRA.md`
- Directory → output sibling directory: `<parent>/<dirname>_LYKRA/`

`lit batch-parse` REQUIRES both `<input-dir>` and `<output-dir>` positional arguments. Never call it with only one path.

Do not prompt for format, DPI, or confirmation when a path is given. Execute immediately.

## Canonical commands

Configs are auto-installed by chezmoi at `~/.config/liteparse/`. No manual copy step.

Single file (English default) — example with `~/Downloads/doc.pdf`:

```bash
lit parse ~/Downloads/doc.pdf \
  --config ~/.config/liteparse/config.en.json \
  -o ~/Downloads/doc_LYKRA.txt
```

Batch a directory (English) — example with `~/Downloads/screenshot_test/`:

```bash
# 1. Parse
lit batch-parse \
  ~/Downloads/screenshot_test \
  ~/Downloads/screenshot_test_LYKRA \
  --config ~/.config/liteparse/config.en.json \
  --recursive

# 2. Rename outputs to add _LYKRA.txt suffix
find ~/Downloads/screenshot_test_LYKRA -type f -name '*.txt' ! -name '*_LYKRA.txt' \
  -exec sh -c 'mv "$1" "${1%.txt}_LYKRA.txt"' _ {} \;
```

For French, swap the config flag to `~/.config/liteparse/config.fr.json`.

For full option reference, see `../Parse/SKILL.md`.
