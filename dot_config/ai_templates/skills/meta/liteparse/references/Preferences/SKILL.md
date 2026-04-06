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
- **File** → `lit parse`
- **Directory** → `lit batch-parse`

**Language:** default to `config.en.json`. Switch to `config.fr.json` only if the user explicitly says French / français / fr / fra, or if filenames/content clearly indicate French.

Do not prompt for format, DPI, or confirmation when a path is given. Execute immediately.

## Canonical commands

Install configs once:

```bash
mkdir -p ~/.config/liteparse
cp ./config.en.json ./config.fr.json ~/.config/liteparse/
```

Single file (English default):

```bash
lit parse <file> \
  --config ~/.config/liteparse/config.en.json \
  -o "$(basename <file> .pdf)_LYKRA.md"
```

Single file (French):

```bash
lit parse <file> \
  --config ~/.config/liteparse/config.fr.json \
  -o "$(basename <file> .pdf)_LYKRA.md"
```

Batch a directory (English):

```bash
lit batch-parse <input-dir> <output-dir> \
  --config ~/.config/liteparse/config.en.json \
  --recursive
```

Batch a directory (French):

```bash
lit batch-parse <input-dir> <output-dir> \
  --config ~/.config/liteparse/config.fr.json \
  --recursive
```

For full option reference, see `../Parse/SKILL.md`.
