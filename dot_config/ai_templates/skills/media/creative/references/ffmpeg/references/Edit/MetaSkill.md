---
name: ffmpeg-edit
description: Full FFmpeg editing cookbook — transcoding (H.264/H.265/VP9/AV1/ProRes/FFV1), trim and concat, scale/crop/overlay, drawtext/titles, subtitle burning (SRT/ASS), speed/reverse, xfade transitions, audio normalization (loudnorm EBU R128), fade in/out, mixing, color grading and LUT application (.cube, haldclut), chroma key / green screen, frame rate conversion, slideshow creation, stacking (hstack/vstack/xstack), hardware-accelerated encoding (NVENC, QSV, VideoToolbox, VAAPI), HLS/DASH streaming, batch processing, and preset profiles. USE WHEN the user wants to construct raw ffmpeg commands, apply multi-filter chains, transcode between codecs, grade color, burn subtitles, build streaming manifests, or run hardware encoding.
metadata:
  requires:
    bins: ["ffmpeg", "ffprobe"]
---

# Edit — Full FFmpeg Editing Cookbook

You are an expert FFmpeg operator. This sub-skill covers the full editing surface area — from single-filter trims to multi-stream filter graphs. Always probe input files first, then load the reference file that matches the operation category.

## Probe First, Then Operate

Every editing task starts with probing the input:

```bash
scripts/probe.sh input.mp4
```

Or manually:

```bash
ffprobe -v error -show_streams -show_format -of json input.mp4
```

See `references/probing.md` for more ffprobe patterns (duration, codec, resolution, etc.).

## Category Router

| What the user wants | Load this |
|---|---|
| Convert format, change codec, output for web / streaming | `references/transcode.md` |
| Cut, trim, join clips together | `references/trim-concat.md` |
| Scale, crop, resize, overlay, watermark, drawtext, blur, fade | `references/filters-video.md` |
| Volume, normalize, denoise, echo, high/low pass, silence detect | `references/filters-audio.md` |
| Speed up, slow down, reverse | `references/speed-reverse.md` |
| xfade transition between clips, acrossfade audio | `references/transitions.md` |
| Brightness / contrast / saturation, hue, 3D LUT, haldclut | `references/color-grading.md` |
| Green screen, chromakey, colorkey | `references/chroma-key.md` |
| Picture-in-picture, side-by-side, 2×2 grid, burn subtitles | `references/compositing.md` |
| NVIDIA NVENC, Intel QSV, Apple VideoToolbox, VAAPI | `references/hardware-accel.md` |
| Loop over a folder of files | `references/batch-processing.md` |
| ffprobe queries (duration, codec, resolution) | `references/probing.md` |
| Named profile like web-optimized, social-vertical, archive | `references/preset-profiles.md` |

## Scripts

Three helper scripts live in `scripts/`:

| Script | Purpose |
|---|---|
| `scripts/probe.sh` | Thin ffprobe wrapper — prints streams + format as JSON |
| `scripts/concat.sh` | Concat demuxer wrapper with absolute-path handling |
| `scripts/normalize-audio.sh` | EBU R128 two-pass loudnorm |

## Common Options Reference

| Flag | Meaning |
|---|---|
| `-ss` | Seek / start time (before `-i` = fast seek, after `-i` = frame-accurate) |
| `-to` | End time (absolute) |
| `-t` | Duration |
| `-c copy` | Stream copy (no re-encode) |
| `-crf` | Constant Rate Factor (lower = higher quality) |
| `-preset` | Encoder speed/quality tradeoff |
| `-movflags +faststart` | Move moov atom to front (web streaming) |
| `-vf` | Video filter chain |
| `-af` | Audio filter chain |
| `-filter_complex` | Multi-input / multi-output filter graph |
| `-map` | Select output streams explicitly |
| `-an` | Drop audio |
| `-vn` | Drop video |
| `-y` | Overwrite output without prompt |
| `-hide_banner` | Suppress build/version banner |
| `-pix_fmt yuv420p` | Broad-compatibility pixel format |

## Multi-Stream Filter Graph Pattern

The canonical shape for non-trivial pipelines:

```bash
ffmpeg \
  -i input_video.mp4 \
  -i overlay.png \
  -i audio_bed.mp3 \
  -filter_complex "
    [0:v]scale=1920:1080,setsar=1[base];
    [1:v]scale=200:-2,format=rgba,colorchannelmixer=aa=0.8[logo];
    [base][logo]overlay=W-w-20:20[composited];
    [0:a][2:a]amix=inputs=2:weights=1 0.2[audio_mix]
  " \
  -map "[composited]" -map "[audio_mix]" \
  -c:v libx264 -crf 18 -preset slow \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  output.mp4
```

## Debugging

```bash
# Dry-run: print filter graph without encoding
ffmpeg -i in.mp4 -vf "scale=1280:-2" -f null -

# Benchmark encode speed
ffmpeg -benchmark -i in.mp4 -c:v libx264 -f null -

# Show available encoders
ffmpeg -encoders | grep -E "^.V|^.A"

# Show filter options
ffmpeg -help filter=loudnorm
```

## When NOT to Use Edit

- Single one-shot tasks with positional flags → use **Quick**
- Generating a video from a text brief using AI models → use **Create**
- Understanding what's in an existing video → use **Analyse**
