---
name: creative
description: Creative toolkit for videos, diagrams, generative art, web design, songwriting, and ffmpeg media work. Use for Manim videos, ASCII art or video, Excalidraw diagrams, p5.js sketches, design-system-inspired pages, Suno prompts, and common video or audio editing tasks.
---

# Creative

> Unified entry point for eight creative production pipelines sourced from the Hermes agent skills.

## Problem

Creative requests span wildly different media: text art, animated video, vector diagrams, math explainers, browser sketches, branded web pages, and song lyrics. Each has its own toolchain, file format, and craft rules. Loading all of them at once bloats context. Picking the right one manually breaks flow.

## Solution

One meta-skill with eight specialist sub-skills. Describe what you want to make; the router picks the right specialist automatically.

## What's Included

| Sub-skill | Purpose |
|---|---|
| `ascii-art` | Static ASCII art, figlet banners, cowsay, boxes, image-to-ASCII |
| `ascii-video` | ASCII video pipeline -- MP4/GIF, audio-reactive visualizers, matrix effects |
| `excalidraw` | Hand-drawn style `.excalidraw` diagrams (architecture, flowcharts, sequence, concept maps) |
| `manim-video` | 3Blue1Brown-style math and algorithm animations via Manim CE |
| `p5js` | Generative/interactive browser art, shaders, WebGL, audio-reactive sketches |
| `popular-web-designs` | 54 production design systems extracted from real sites (Stripe, Linear, Vercel, Notion, Airbnb, ...) |
| `songwriting-and-ai-music` | Songwriting craft, Suno prompts, parody techniques, phonetic tricks |
| `ffmpeg` | Nested meta-skill for video and audio — AI video creation, quick one-shot ops, content analysis, and the full ffmpeg editing cookbook |

## Invocation Scenarios

| User says | Routes to |
|---|---|
| "make a figlet banner that says HELLO" | `ascii-art` |
| "please create a video" | `manim-video` (default for general video) |
| "convert this mp4 into an ASCII video" | `ascii-video` (terminal-style only) |
| "draw an architecture diagram for my API" | `excalidraw` |
| "animate how quicksort works, 3b1b style" | `manim-video` |
| "generative flow field in p5.js" | `p5js` |
| "landing page in Stripe's visual style" | `popular-web-designs` |
| "write a parody song about Docker, Suno prompt" | `songwriting-and-ai-music` |
| "cut this video from 1:30 to 2:45" | `ffmpeg` (→ Quick) |
| "what happens in this recording?" | `ffmpeg` (→ Analyse) |
| "build a 60s explainer video from this brief" | `ffmpeg` (→ Create) |
| "transcode this mov to H.264 web-safe mp4" | `ffmpeg` (→ Edit) |

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

## Design Rules

- Single entry point -- invoke `creative`, never a sub-skill directly.
- No domain overlap -- each sub-skill owns distinct territory.
- Sub-skills are standalone and work independently if loaded directly.
- Adding a new medium means one new directory under `references/` plus one new row in `ROUTER.md`.
