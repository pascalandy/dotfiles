---
name: liteparse-preferences
description: User's default LiteParse settings stored in per-language config files. USE WHEN my preferences, my defaults, parse with my settings, LYKRA, config.json, english parse, french parse.
---

# LiteParse — Preferences

Two configs deployed by chezmoi to `~/.config/liteparse/` (filenames use ISO 639-1; values inside use Tesseract 3-letter codes):

- `~/.config/liteparse/config.en.json` → `ocrLanguage: "eng"`
- `~/.config/liteparse/config.fr.json` → `ocrLanguage: "fra"`

Source of truth: `dot_config/liteparse/` in chezmoi. Edit there, then `chezmoi apply`.

Both share: `dpi: 300`, `outputFormat: text`, `outputSuffix: _lykra.md`, `preciseBoundingBox: true`.

Output is plain text (`.txt`). The `outputSuffix` field in the configs is a local naming convention applied by post-processing — `lit` itself ignores it.

## Canonical command: `lykra-parse`

Use the wrapper. It handles file/dir detection, config selection, and the `_lykra.txt` rename atomically.

```bash
lykra-parse ~/Downloads/doc.pdf              # → ~/Downloads/doc_lykra.txt
lykra-parse ~/Downloads/screenshot_test/     # → ~/Downloads/screenshot_test_lykra/*.txt
lykra-parse ~/Downloads/doc.pdf --fr         # French OCR
```

**Language default:** English. Switch to `--fr` only if the user explicitly says French / français / fr / fra, or if filenames/content clearly indicate French.

Configs at `~/.config/liteparse/config.{en,fr}.json` are auto-installed by chezmoi.

For non-default options (json output, page range, custom DPI, screenshots) bypass the wrapper and use `Parse` or `Screenshot` directly.

For full option reference, see `../Parse/SKILL.md`.
