---
name: creative
description: Creative content generation collection -- ASCII art and banners, ASCII video production, hand-drawn Excalidraw diagrams, Manim math/technical animations, p5.js generative and interactive art, popular website design systems (Stripe/Linear/Vercel/etc.), and songwriting with AI music (Suno) prompts. USE WHEN ASCII art, figlet, banners, cowsay, text art, ASCII video, terminal video, matrix effect, audio visualizer, excalidraw, hand-drawn diagram, flowchart, architecture diagram, sequence diagram, concept map, manim, math animation, 3blue1brown, algorithm visualization, equation animation, p5.js, creative coding, generative art, canvas sketch, shader, GLSL, interactive visualization, web design template, landing page CSS, Stripe style, Linear style, Vercel style, Notion style, design system, songwriting, lyrics, Suno prompt, AI music, parody song.
---

# Creative

> Unified entry point for seven creative production pipelines sourced from the Hermes agent skills.

## Problem

Creative requests span wildly different media: text art, animated video, vector diagrams, math explainers, browser sketches, branded web pages, and song lyrics. Each has its own toolchain, file format, and craft rules. Loading all of them at once bloats context. Picking the right one manually breaks flow.

## Solution

One meta-skill with seven specialist sub-skills. Describe what you want to make; the router picks the right specialist automatically.

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

## Invocation Scenarios

| User says | Routes to |
|---|---|
| "make a figlet banner that says HELLO" | `ascii-art` |
| "convert this mp4 into an ASCII video" | `ascii-video` |
| "draw an architecture diagram for my API" | `excalidraw` |
| "animate how quicksort works, 3b1b style" | `manim-video` |
| "generative flow field in p5.js" | `p5js` |
| "landing page in Stripe's visual style" | `popular-web-designs` |
| "write a parody song about Docker, Suno prompt" | `songwriting-and-ai-music` |

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

## Design Rules

- Single entry point -- invoke `creative`, never a sub-skill directly.
- No domain overlap -- each sub-skill owns distinct territory.
- Sub-skills are standalone and work independently if loaded directly.
- Adding a new medium means one new directory under `references/` plus one new row in `ROUTER.md`.
