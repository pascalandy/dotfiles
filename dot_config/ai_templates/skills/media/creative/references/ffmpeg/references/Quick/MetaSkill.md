---
name: ffmpeg-quick
description: One-shot video and audio operations via thin shell-script wrappers — cut, merge, extract audio, generate thumbnail, create GIF, convert format, change speed, add watermark. USE WHEN the user wants a single fast operation with positional flags rather than a multi-step editing pipeline, or says "just cut this", "quick merge", "grab a thumbnail", "make a gif", "extract the audio", "speed this up", "add my logo".
metadata:
  requires:
    bins: ["ffmpeg", "ffprobe"]
---

# Quick — One-Shot FFmpeg Operations

Thin shell-script wrappers for the most common single-purpose ffmpeg tasks. Each script lives in `scripts/` and takes positional flags. Output quality is tuned for a balance between file size and clarity.

## Quick Reference

| Task | Command |
|---|---|
| Cut video | `scripts/cut.sh -i <input> -s <start> -e <end> -o <output>` |
| Merge clips | `scripts/merge.sh -o <output> <file1> <file2> ...` |
| Extract audio | `scripts/extract-audio.sh -i <video> -o <output.mp3>` |
| Generate thumbnail | `scripts/thumb.sh -i <video> -t <timestamp> -o <out.jpg>` |
| Create GIF | `scripts/gif.sh -i <video> -s <start> -e <end> -o <out.gif>` |
| Convert format | `scripts/convert.sh -i <input> -o <output.mp4>` |
| Change speed | `scripts/speed.sh -i <input> -r <0.5-2.0> -o <output>` |
| Add watermark | `scripts/watermark.sh -i <video> -w <image> -o <output>` |

## Scripts

### `scripts/cut.sh` — Cut a video segment

```bash
scripts/cut.sh -i video.mp4 -s 00:01:30 -e 00:02:45 -o clip.mp4
```

Uses stream copy (no re-encode) — fast and lossless. Cut points snap to the nearest keyframe.

### `scripts/merge.sh` — Concatenate videos

```bash
scripts/merge.sh -o merged.mp4 part1.mp4 part2.mp4 part3.mp4
```

Uses the concat demuxer with stream copy. **All inputs must share the same codec, resolution, and frame rate.** For mixed-codec merges, route to **Edit** (`references/trim-concat.md`).

### `scripts/extract-audio.sh` — Pull audio track

```bash
scripts/extract-audio.sh -i video.mp4 -o audio.mp3
```

Encodes to MP3 at 192 kbps. For lossless WAV or time-range extraction, route to **Edit**.

### `scripts/thumb.sh` — Extract a single frame as image

```bash
scripts/thumb.sh -i video.mp4 -t 00:00:15 -o frame.jpg
```

Grabs ONE frame at the specified timestamp at best quality (`-q:v 2`).

### `scripts/gif.sh` — Convert a clip to GIF

```bash
scripts/gif.sh -i video.mp4 -s 00:00:10 -e 00:00:15 -o clip.gif
```

Uses the two-pass palette method for high-quality color. Scales to 480px wide by default to keep file sizes reasonable.

### `scripts/convert.sh` — Transcode to MP4

```bash
scripts/convert.sh -i input.avi -o output.mp4
```

Transcodes to H.264 + AAC with web-safe settings (`yuv420p`, `+faststart`). For other codecs (VP9, AV1, HEVC), route to **Edit**.

### `scripts/speed.sh` — Adjust playback speed

```bash
scripts/speed.sh -i video.mp4 -r 2.0 -o fast.mp4   # 2x speed
scripts/speed.sh -i video.mp4 -r 0.5 -o slow.mp4   # 0.5x speed
```

Accepts any ratio from 0.5 to 2.0. For extreme slow motion or fast-forward (outside that range), route to **Edit** (which chains `atempo` filters).

If the input has no audio stream, the script still works and keeps the output silent.

### `scripts/watermark.sh` — Overlay an image watermark

```bash
scripts/watermark.sh -i video.mp4 -w logo.png -o output.mp4
```

Places the watermark in the bottom-right corner with a 10px margin. For other positions, custom opacity, or animated watermarks, route to **Edit** (`references/compositing.md`).

## Notes

- All scripts support common video formats (mp4, avi, mov, mkv, webm, etc.)
- Every script prints usage info when called with `-h` or no arguments
- Scripts fail fast (`set -euo pipefail`) and report the exact ffmpeg error if anything goes wrong
- For anything beyond these single-purpose operations, route to the **Edit** sub-skill

## When NOT to Use Quick

Route to **Edit** instead if the user wants:

- Specific codec (VP9, AV1, HEVC)
- Multi-filter chains (scale + crop + overlay + drawtext)
- Color grading or LUT application
- Subtitle burning
- Chroma key / green screen
- Transitions (xfade) between clips
- HLS or DASH streaming output
- Hardware-accelerated encoding
- Batch processing a folder of files
