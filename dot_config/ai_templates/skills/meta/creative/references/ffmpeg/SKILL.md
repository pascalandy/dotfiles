---
name: ffmpeg
description: Unified video and audio toolkit — create AI-generated videos from text briefs, run quick one-shot operations (cut, merge, thumbnail, gif), analyse existing video content with sub-agent vision, or edit with the full ffmpeg command cookbook (transcode, filters, LUTs, transitions, chroma key, hardware acceleration). USE WHEN the user mentions video, audio, ffmpeg, ffprobe, mp4, mov, mkv, webm, mp3, wav, cut, trim, merge, concat, thumbnail, gif, extract audio, watermark, speed change, transcode, H.264, H.265, VP9, AV1, HLS, DASH, LUT, color grade, chroma key, green screen, picture in picture, xfade, drawtext, subtitles, loudnorm, NVENC, VideoToolbox, analyse video, summarise recording, AI voiceover, talking head, Remotion, FLUX, SadTalker, LTX-2, Qwen3-TTS, explainer video.
---

# FFmpeg Meta-Skill

> One entry point for every video and audio task — AI video creation, quick operations, content analysis, and full editing.

## Problem

FFmpeg is the swiss-army knife of media processing, but its surface area is enormous. Users come to it with wildly different intents: one wants to cut 30 seconds out of a screen recording, another wants to understand what's in a 20-minute video, another wants to produce a polished explainer video from a text brief, and another wants to set up HLS streaming with multi-bitrate rendering. Loading every recipe into context for every request wastes tokens and buries the relevant command.

## Solution

A router-based meta-skill that inspects the request and loads exactly one specialist sub-skill. The user never picks a sub-skill — they describe what they need, and the right domain activates automatically.

## What's Included

| Sub-Skill | Domain | When to use |
|---|---|---|
| **Create** | AI-generated videos | Produce an explainer/demo/marketing video from a text brief using cloud GPU models for voiceover, images, music, talking heads, and LTX-2 video clips, composed with Remotion. |
| **Quick** | One-shot operations | Single-purpose tasks via wrapper scripts — cut, merge, extract audio, thumbnail, gif, convert format, change speed, add watermark. |
| **Analyse** | Content understanding | Extract frames from a video and delegate vision to sub-agents to produce a timestamped summary without blowing out the main context. |
| **Edit** | Full editing cookbook | Raw ffmpeg commands for transcoding (H.264/H.265/VP9/AV1), filters, transitions (xfade), color grading and LUTs, chroma key, picture-in-picture, subtitles, loudnorm, hardware encoding, HLS/DASH streaming, and preset profiles. |

## Invocation Scenarios

| Trigger phrase | What happens |
|---|---|
| "Create a 60-second explainer video about X" | Loads **Create** → runs the full toolkit pipeline (voiceover → images → music → Remotion render) |
| "Cut this video from 1:30 to 2:45" | Loads **Quick** → runs `scripts/cut.sh` |
| "What happens in this video? / Summarise this recording" | Loads **Analyse** → extracts frames, delegates to sub-agents, synthesises timeline |
| "Convert this .mov to H.264 web-safe MP4" | Loads **Edit** → constructs `ffmpeg -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p ...` |
| "Add a watermark to this clip" | Loads **Quick** → runs `scripts/watermark.sh` |
| "Generate a talking-head narrator with AI voiceover" | Loads **Create** → FLUX portrait → Qwen3-TTS → SadTalker per-scene |
| "Apply this .cube LUT to the footage" | Loads **Edit** → `lut3d=file=lut.cube` |
| "Set up HLS multi-bitrate streaming" | Loads **Edit** → `references/transcode.md` multi-bitrate pattern |
| "Burn these SRT subtitles into the video" | Loads **Edit** → `subtitles=subs.srt` |
| "Extract the audio as MP3" | Loads **Quick** → runs `scripts/extract-audio.sh` |

## Usage Examples

```
"Analyse /path/to/demo.mp4 and tell me what happens"
  → Analyse sub-skill: ffprobe → frame extraction → sub-agent batches → timeline

"Build me a product demo video for MyApp, 60s, 5 scenes"
  → Create sub-skill: templates/product-demo → voiceover → images → render

"Cut screencast.mov from 00:05:00 to 00:08:30, keep the audio"
  → Quick sub-skill: scripts/cut.sh

"Convert raw.mov to VP9 WebM with Opus audio for the web"
  → Edit sub-skill: references/transcode.md VP9 pattern

"Overlay logo.png top-right on all .mp4 files in this folder"
  → Edit sub-skill: references/compositing.md overlay + references/batch-processing.md
```

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

## Design Notes

- **Single entry point** — invoke by meta-skill name, never a sub-skill directly
- **Invisible delegation** — the router picks the specialist automatically from the request
- **No domain overlap** — Create produces new videos, Quick runs one-shot scripts, Analyse understands content, Edit manipulates raw ffmpeg commands
- **Progressive disclosure** — only the selected sub-skill's files load; its own workflows/references are read on demand
- **Harness agnostic** — every path is relative to the meta-skill root; no `~/.claude/`, no harness-specific tool assumptions
