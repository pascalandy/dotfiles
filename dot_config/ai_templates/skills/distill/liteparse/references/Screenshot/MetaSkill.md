---
name: liteparse-screenshot
description: Render document pages as image files using `lit screenshot`. USE WHEN screenshot pages, render pages, page images, page thumbnails, visual layout for LLM.
---

# LiteParse — Screenshot

Generate per-page images, useful for vision-capable LLMs.

```bash
# All pages
lit screenshot document.pdf -o ./screenshots

# Specific pages
lit screenshot document.pdf --pages "1,3,5" -o ./screenshots

# Page range
lit screenshot document.pdf --pages "1-10" -o ./screenshots

# High-DPI PNG
lit screenshot document.pdf --dpi 300 --format png -o ./screenshots
```
