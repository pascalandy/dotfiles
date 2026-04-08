# 01 — Probe Metadata

Gather the video's metadata and set up the scratch directory.

## Step 1: Set Up Temp Directory

```bash
# macOS/Linux
TMPDIR="/tmp/video-analysis-$(date +%s)"
mkdir -p "$TMPDIR"
```

Windows (PowerShell):

```powershell
$TMPDIR = "$env:TEMP\video-analysis-$(Get-Date -UFormat %s)"
New-Item -ItemType Directory -Path $TMPDIR
```

Keep the variable around — every subsequent workflow uses it.

## Step 2: Probe the Video

```bash
ffprobe -v quiet -print_format json -show_format -show_streams "VIDEO_PATH"
```

## Step 3: Extract and Report Metadata

From the JSON response, pull out and report to the user:

- **Duration** (format.duration)
- **Resolution** (streams[video].width × height)
- **Frame rate** (streams[video].r_frame_rate)
- **Codec** (streams[video].codec_name)
- **File size** (format.size in bytes)
- **Audio present?** (any stream with codec_type="audio")

Sample report format:

```
Video Metadata
──────────────
Duration:   4:32
Resolution: 1920×1080
FPS:        30
Codec:      h264
Size:       47 MB
Audio:      Yes (aac, stereo)
```

## Step 4: Pre-flight Checks

Run these checks before extracting frames:

### Check 1: Is there a video stream?

If no stream has `codec_type="video"`:

```
Report to user: "This file has no video stream — it appears to be audio-only."
STOP.
```

### Check 2: Is the file too large?

If file size > 2 GB:

```
Warn user: "This file is over 2 GB. Extracting frames across the full duration may be slow.
Consider analysing a specific time range with 'analyse 5:00 to 10:00 of video.mp4'."
Ask whether to continue or restrict to a range.
```

### Check 3: Select extraction strategy

Based on duration, pick the strategy for `workflows/02-extract-frames.md`:

| Duration | Strategy |
|---|---|
| 0-60 seconds | Interval: 1 frame every 2s |
| 1-10 minutes | Scene detection, threshold 0.3 |
| 10-30 minutes | Keyframe extraction |
| 30 minutes+ | Thumbnail filter |

Record the chosen strategy; it's an input to the next workflow.

## Next

Move to `workflows/02-extract-frames.md` with the strategy and `$TMPDIR` in hand.
