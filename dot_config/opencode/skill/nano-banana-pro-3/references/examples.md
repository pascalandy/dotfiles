# Examples

**Note:** Examples use `gen_image.py` as shorthand. Full path:

```bash
uv run .opencode/skill/nano-banana-pro-3/scripts/gen_image.py
```

## Basic Generation

```bash
# Quick test with dry run (no API cost)
gen_image.py --dry-run --prompt "A serene Japanese garden with cherry blossoms"

# Dry run with verbose debug output
gen_image.py --dry-run --verbose --prompt "A sunset over mountains"

# Generate with custom filename
gen_image.py --prompt "A serene Japanese garden" \
  --filename "2025-12-23-14-23-05-japanese-garden.png"
```

## Size and Aspect Ratio

```bash
# 4K image with 16:9 aspect ratio
gen_image.py --prompt "A futuristic cityscape at night" \
  --size 4K --aspect-ratio 16:9

# Portrait image (9:16 for mobile)
gen_image.py --prompt "A tall waterfall in a forest" \
  --size 2K --aspect-ratio 9:16
```

## Image Editing

```bash
# Edit an existing image
gen_image.py --prompt "Make the sky more dramatic with storm clouds" \
  --input-image "original-photo.jpg" \
  --filename "edited-dramatic-sky.png"

# Compose/blend multiple images
gen_image.py --prompt "Blend these styles together" \
  --input-image "style1.png" \
  --input-image "style2.png" \
  --input-image "subject.png"
```

## Advanced Options

```bash
# Reproducible generation with seed
gen_image.py --prompt "A robot in a garden" --seed 12345 --size 2K

# Generate multiple images in one call
gen_image.py --prompt "A sunset over mountains" --nbr-img-output 3

# Generate as JPEG instead of PNG
gen_image.py --prompt "A sunset over mountains" --format jpeg

# Use thinking mode for complex prompts
gen_image.py --prompt "Complex infographic about climate change" --thinking high

# Use negative prompt to avoid unwanted elements
gen_image.py --prompt "A serene beach" --negative-prompt "people, crowds, text"

# Adjust safety filter level
gen_image.py --prompt "Action movie scene" --safety low
```

## Output Control

```bash
# Specify custom output directory
gen_image.py --prompt "A sunset over mountains" --output-dir ./my-images

# Open image automatically after generation
gen_image.py --prompt "A sunset over mountains" --open-after

# Quiet mode: only output file paths (for scripting)
gen_image.py --prompt "A sunset over mountains" --quiet

# Capture path for use in another command
path=$(gen_image.py --prompt "A sunset" --quiet)
echo "Saved to: $path"

# Custom timeout for slow networks
gen_image.py --prompt "Complex generation" --timeout 300
```

## Image Editing Tips

When editing with `--input-image`:

- Prompt should contain editing instructions ("make the sky dramatic", "add a rainbow")
- Common tasks: add/remove elements, change style, adjust colors, blur background
