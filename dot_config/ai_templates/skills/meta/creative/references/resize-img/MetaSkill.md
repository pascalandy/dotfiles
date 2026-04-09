---
name: resize-img
description: Resize and compress images with ImageMagick for token-efficient use in AI workflows. Use when preparing screenshots, photos, or reference images for LLM upload, especially when the user wants smaller files by default.
compatibility: Requires ImageMagick installed and available as `magick` on PATH.
---

# Resize Images

Default to the user's preference: make images token efficient.

## Default Behavior

1. Convert the input image to `.jpg` unless the user explicitly asks to keep the original format.
2. Resize the resulting `.jpg` so neither dimension exceeds `1920`.
3. Compress with JPEG quality `70`.

Default command for the final compression step:

```bash
magick mogrify -resize '1920x1920>' -quality 70 {filename}
```

## Procedure

For a non-JPEG input, create a JPEG first, then run the default `mogrify` step on that JPEG.

Example:

```bash
magick "input.png" "input.jpg"
magick mogrify -resize '1920x1920>' -quality 70 "input.jpg"
```

For an existing JPEG:

```bash
magick mogrify -resize '1920x1920>' -quality 70 "input.jpg"
```

## Batch Pattern

When processing multiple files, convert each one to a `.jpg`, then apply the same resize/compress step.

```bash
for img in path/to/images/*; do
    base="${img%.*}"
    jpg="${base}.jpg"
    magick "$img" "$jpg"
    magick mogrify -resize '1920x1920>' -quality 70 "$jpg"
done
```

## Gotchas

- `mogrify` edits files in place. If preserving the original matters, create the `.jpg` copy first and only modify that copy.
- Always quote paths.
- Do not preserve PNG or WebP by default when the goal is token efficiency. Convert to `.jpg` first unless the user says otherwise.
- If the user asks for exact dimensions, transparency, or lossless output, follow that request instead of the default.
