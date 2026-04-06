---
name: liteparse-preferences
description: User's default LiteParse settings stored in per-language config files. USE WHEN my preferences, my defaults, parse with my settings, LYKRA, config.json, english parse, french parse.
---

# LiteParse — Preferences

Two configs (filenames use ISO 639-1; values inside use Tesseract 3-letter codes):

- [`config.en.json`](./config.en.json) → `ocrLanguage: "eng"`
- [`config.fr.json`](./config.fr.json) → `ocrLanguage: "fra"`

Both share: `dpi: 300`, `outputFormat: text`, `outputSuffix: _LYKRA.md`, `preciseBoundingBox: true`.

Output is plain text saved with a `.md` extension so it renders in markdown viewers (LiteParse has no native markdown format).

## Auto-detect rules (do not ask, just run)

**Path type:**
- **File** → `lit parse <file> --config <cfg> -o <file_basename>_LYKRA.md`
- **Directory** → `lit batch-parse <input-dir> <input-dir>_LYKRA --config <cfg> --recursive`

**Language:** default to `config.en.json`. Switch to `config.fr.json` only if the user explicitly says French / français / fr / fra, or if filenames/content clearly indicate French.

**Output location convention:**
- File → output sibling file: `<dir>/<basename>_LYKRA.md`
- Directory → output sibling directory: `<parent>/<dirname>_LYKRA/`

`lit batch-parse` REQUIRES both `<input-dir>` and `<output-dir>` positional arguments. Never call it with only one path.

Do not prompt for format, DPI, or confirmation when a path is given. Execute immediately.

## Canonical commands

Install configs once:

```bash
mkdir -p ~/.config/liteparse
cp ./config.en.json ./config.fr.json ~/.config/liteparse/
```

Single file (English default) — example with `~/Downloads/doc.pdf`:

```bash
lit parse ~/Downloads/doc.pdf \
  --config ~/.config/liteparse/config.en.json \
  -o ~/Downloads/doc_LYKRA.md
```

Batch a directory (English) — example with `~/Downloads/screenshot_test/`:

```bash
lit batch-parse \
  ~/Downloads/screenshot_test \
  ~/Downloads/screenshot_test_LYKRA \
  --config ~/.config/liteparse/config.en.json \
  --recursive
```

For French, swap the config flag to `~/.config/liteparse/config.fr.json`.

For full option reference, see `../Parse/SKILL.md`.
