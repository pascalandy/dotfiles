---
name: nano-banana-pro-3
description: >
  Generate or edit images using Gemini 3 Pro Image via OpenRouter API.
  Use when the user wants to: (1) Generate images from text prompts,
  (2) Edit/modify existing images, (3) Compose/blend multiple images.
  Triggers: "generate image", "create picture", "edit photo", "make an image".
---

# Nano Banana Pro 3

Generate or edit images using Gemini 3 Pro Image model via OpenRouter.

## Quick Start

**Full path:** `uv run .opencode/skill/nano-banana-pro-3/scripts/gen_image.py`

```bash
# Show help
gen_image.py --help

# Dry run (no API cost)
gen_image.py --dry-run --prompt "A sunset over mountains"

# Generate image
gen_image.py --prompt "A sunset over mountains"

# Edit existing image
gen_image.py --prompt "Make the sky dramatic" --input-image photo.jpg
```

**Important:** Run from user's working directory so images save there.

## Workflow

1. Determine operation type:
   - **Generate new** → `--prompt` only
   - **Edit single image** → `--prompt` + `--input-image`
   - **Compose multiple** → `--prompt` + multiple `--input-image`

2. Use `--dry-run` first to verify parameters (no API cost)
3. Run the generation
4. Report output path to user (**do NOT read the image back**)

## API Key

Set `OPENROUTER_API_KEY` in `.env` or environment variable.

```bash
echo "OPENROUTER_API_KEY=your-key-here" > .env
```

Get key at: https://openrouter.ai/keys

## Common Failures

| Error                   | Solution                                  |
| ----------------------- | ----------------------------------------- |
| `No API key provided`   | Set OPENROUTER_API_KEY in .env            |
| `No image generated`    | Model returned text; try different prompt |
| API errors (403, quota) | Check credits at openrouter.ai            |

## Output

- Default directory: `./EXPORT/`
- Default filename: `yyyy-mm-dd-hh-mm-ss-generated.png`

## References

- **All flags & options**: See `references/options.md`
- **More examples**: See `references/examples.md`
