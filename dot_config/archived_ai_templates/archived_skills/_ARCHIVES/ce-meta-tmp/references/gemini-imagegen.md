# Gemini Image Generation

> Generate and edit images using Google's Gemini API with text-to-image, image editing, multi-turn refinement, and multi-reference composition.

## When to Use

- Creating images from text prompts
- Editing existing images
- Applying style transfers
- Generating logos with text
- Creating stickers or product mockups
- Any image generation or manipulation task
- Multi-turn iterative image refinement

## Inputs

- `GEMINI_API_KEY` environment variable must be set
- A text prompt describing the desired image
- Optionally: one or more existing images to edit or use as references (up to 14)

## Methodology

### Default Model

| Model | Resolution | Best For |
|-------|------------|----------|
| `gemini-3-pro-image-preview` | 1K–4K | All image generation (default) |

**Always use this Pro model. Only use a different model if explicitly requested.**

---

### Default Settings

- **Model:** `gemini-3-pro-image-preview`
- **Resolution:** 1K (default; options: 1K, 2K, 4K)
- **Aspect Ratio:** 1:1 (default)

### Available Aspect Ratios

`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

### Available Resolutions

| Resolution | Notes |
|---|---|
| `1K` | Default — fast, good for previews |
| `2K` | Balanced quality/speed |
| `4K` | Maximum quality, slower |

---

### Core API Pattern

```python
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Basic generation (1K, 1:1 - defaults)
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["Your prompt here"],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
    ),
)

for part in response.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        image = part.as_image()
        image.save("output.jpg")
```

---

### Custom Resolution & Aspect Ratio

```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",  # Wide format
            image_size="2K"       # Higher resolution
        ),
    )
)
```

**Aspect ratio examples:**

```python
# Square (default)
image_config=types.ImageConfig(aspect_ratio="1:1")

# Landscape wide
image_config=types.ImageConfig(aspect_ratio="16:9")

# Ultra-wide panoramic
image_config=types.ImageConfig(aspect_ratio="21:9")

# Portrait
image_config=types.ImageConfig(aspect_ratio="9:16")

# Photo standard
image_config=types.ImageConfig(aspect_ratio="4:3")
```

---

### Editing Existing Images

Pass existing images with text prompts:

```python
from PIL import Image

img = Image.open("input.png")
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["Add a sunset to this scene", img],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
    ),
)
```

Describe changes conversationally — the model understands semantic masking.

---

### Multi-Turn Refinement

Use chat for iterative editing:

```python
from google.genai import types

chat = client.chats.create(
    model="gemini-3-pro-image-preview",
    config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
)

response = chat.send_message("Create a logo for 'Acme Corp'")
# Save first image...

response = chat.send_message("Make the text bolder and add a blue gradient")
# Save refined image...
```

---

### Multiple Reference Images (Up to 14)

Combine elements from multiple source images:

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Create a group photo of these people in an office",
        Image.open("person1.png"),
        Image.open("person2.png"),
        Image.open("person3.png"),
    ],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
    ),
)
```

---

### Google Search Grounding

Generate images based on real-time data:

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["Visualize today's weather in Tokyo as an infographic"],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        tools=[{"google_search": {}}]
    )
)
```

**Note:** Image-only mode (`responseModalities: ["IMAGE"]`) does not work with Google Search grounding.

---

### Prompting Best Practices

**Photorealistic scenes** — include camera details: lens type, lighting, angle, mood.
> "A photorealistic close-up portrait, 85mm lens, soft golden hour light, shallow depth of field"

**Stylized art** — specify style explicitly.
> "A kawaii-style sticker of a happy red panda, bold outlines, cel-shading, white background"

**Text in images** — be explicit about font style and placement.
> "Create a logo with text 'Daily Grind' in clean sans-serif, black and white, coffee bean motif"

**Product mockups** — describe lighting setup and surface.
> "Studio-lit product photo on polished concrete, three-point softbox setup, 45-degree angle"

---

### CRITICAL: File Format & Media Type

**The Gemini API returns images in JPEG format by default.** Always use `.jpg` extension to avoid media type mismatches.

```python
# CORRECT - Use .jpg extension (Gemini returns JPEG)
image.save("output.jpg")

# WRONG - Will cause "Image does not match media type" errors
image.save("output.png")  # Creates JPEG with PNG extension!
```

**Converting to PNG if needed:**

```python
from PIL import Image

for part in response.parts:
    if part.inline_data:
        img = part.as_image()
        # Convert to PNG by saving with explicit format
        img.save("output.png", format="PNG")
```

**Verifying image format** — check actual format vs extension in terminal:

```bash
file image.png
# If output shows "JPEG image data" - rename to .jpg!
```

## Quality Gates

- `GEMINI_API_KEY` confirmed set before running
- Correct model (`gemini-3-pro-image-preview`) used unless otherwise requested
- Output saved with `.jpg` extension (or explicitly converted with `format="PNG"` if PNG is required)
- Prompt includes sufficient detail for the desired output style

## Outputs

- Generated image file(s) saved to disk
- Any text commentary returned alongside the image

## Feeds Into

- `frontend-design` — use generated images as visual content in UI builds
- Any workflow requiring custom imagery or product mockups

## Harness Notes

- All API calls are Python-based using the `google-genai` library. Run them in the terminal or as a script.
- All generated images include SynthID watermarks.
- Default to 1K resolution for speed; use 2K/4K when quality is critical.
