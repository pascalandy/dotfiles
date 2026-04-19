---
name: ffmpeg-analyse
description: Analyse video content by extracting frames with ffmpeg and using AI vision to generate timestamped step-by-step summaries. USE WHEN the user provides a video file and wants to understand its visual content — screen recordings, tutorials, presentations, footage, or animations. Triggers on "analyse this video", "what happens in this video", "summarise this recording", "describe what's shown", or any request involving understanding video file contents.
metadata:
  requires:
    bins: ["ffmpeg", "ffprobe"]
---

# Analyse — Video Content Understanding

Extract frames from a video file with ffmpeg, delegate frame reading to sub-agents to preserve the main context window, and synthesize a structured timestamped summary from text-only sub-agent reports.

## Architecture: Context-Efficient Sub-Agent Pipeline

**The Problem:** Reading dozens of images into the main conversation context consumes most of the context window, leaving little room for synthesis and follow-up.

**The Solution:** A 3-phase pipeline where images only ever exist inside sub-agent contexts:

```
Main Agent                          Sub-Agents (disposable context)
──────────                          ──────────────────────────────
1. ffprobe metadata        ───►
2. ffmpeg frame extraction ───►
3. Split frames into batches ──►   4. Read images (vision)
                                      Write text descriptions
                                      to batch_N_analysis.md
5. Read text files only    ◄───    (context discarded)
6. Synthesise final output
```

The main agent only ever reads lightweight text files. This cuts context usage by ~90%.

## Workflow Routing

| Phase | File | What it does |
|---|---|---|
| 1 | `workflows/01-probe-metadata.md` | ffprobe metadata + duration-based strategy selection |
| 2 | `workflows/02-extract-frames.md` | Run the right ffmpeg extraction strategy |
| 3 | `workflows/03-delegate-batches.md` | Split frames, spawn sub-agents, collect text files |
| 4 | `workflows/04-synthesise.md` | Merge batches into final timestamped output |

## References

| File | Content |
|---|---|
| `references/subagent-prompt-template.md` | Verbatim prompt template for the frame-reading sub-agents |

## Prerequisites

```bash
which ffmpeg && which ffprobe
```

If either is missing:

| Platform | Install |
|---|---|
| macOS | `brew install ffmpeg` |
| Ubuntu/Debian | `sudo apt install ffmpeg` |
| Windows | `choco install ffmpeg` or `winget install ffmpeg` |

## Advanced Options

These modify the extraction and analysis behaviour. Apply them by editing the relevant workflow step.

| User request | Modification |
|---|---|
| "Analyse 2:00 to 5:00 of video.mp4" | Prepend `-ss 120 -to 300` before `-i` in extraction command |
| "Analyse in high detail" | Double the fps rate; lower scene threshold to 0.2 |
| "Focus on the code shown" | Prioritise text / code extraction in sub-agent prompts |
| "Show me a visual overview" | Generate sprite sheet: `ffmpeg -hide_banner -y -i INPUT -vf "select='not(mod(n,EVERY_N))',scale='min(320,iw)':-2,tile=5xROWS" -frames:v 1 DIR/sprite.jpg` |

## Error Handling Matrix

| Error | Solution |
|---|---|
| ffmpeg not found | Install per-platform instructions, STOP |
| No video stream | Report "audio-only file", STOP |
| Scene detection yields 0 frames | Fall back to interval at 1 frame/5s |
| More than 100 frames extracted | Subsample evenly to 80 |
| File size > 2GB | Warn, suggest time range with `-ss START -to END` |
| Sub-agent fails or times out | Fall back to reading that batch's frames directly, warn about context usage |
| Frame read failure in sub-agent | Skip frame, note gap in batch analysis file |

## Cleanup

After output is complete:

```bash
# macOS/Linux
rm -rf "$TMPDIR"

# Windows (PowerShell)
# Remove-Item -Recurse -Force $TMPDIR
```

Skip cleanup if the user asks to keep frames.
