# 02 — Extract Frames

Run the ffmpeg extraction command that matches the chosen strategy from the previous workflow. Expect 20-80 frames total; if the count is outside that range, apply the fallbacks below.

## Strategy Commands

### 0-60s videos — interval extraction (1 frame every 2s)

```bash
ffmpeg -hide_banner -y -i INPUT \
  -vf "fps=1/2,scale='min(1280,iw)':-2" \
  -q:v 5 "$TMPDIR/frame_%04d.jpg"
```

### 1-10min videos — scene detection (threshold 0.3)

```bash
ffmpeg -hide_banner -y -i INPUT \
  -vf "select='gt(scene,0.3)',scale='min(1280,iw)':-2" \
  -vsync vfr -q:v 5 "$TMPDIR/scene_%04d.jpg"
```

### 10-30min videos — keyframe extraction

```bash
ffmpeg -hide_banner -y -skip_frame nokey -i INPUT \
  -vf "scale='min(1280,iw)':-2" \
  -vsync vfr -q:v 5 "$TMPDIR/key_%04d.jpg"
```

### 30min+ videos — thumbnail filter

Calculate segment size so the output caps at ~60 frames:

```
SEGMENT_FRAMES = total_frames / 60
```

Then:

```bash
ffmpeg -hide_banner -y -i INPUT \
  -vf "thumbnail=SEGMENT_FRAMES,scale='min(1280,iw)':-2" \
  -vsync vfr -q:v 5 "$TMPDIR/thumb_%04d.jpg"
```

## Time Range Modifier

When the user specified a range (e.g. "analyse 2:00 to 5:00"), prepend `-ss START -to END` **before** `-i`:

```bash
ffmpeg -hide_banner -y \
  -ss 120 -to 300 \
  -i INPUT \
  -vf "fps=1/2,scale='min(1280,iw)':-2" \
  -q:v 5 "$TMPDIR/frame_%04d.jpg"
```

## High-Detail Modifier

When the user asks for "high detail" or "maximum detail":

- Double the fps rate (`fps=1/1` instead of `fps=1/2`)
- Lower the scene threshold to `0.2` instead of `0.3`

## Fallbacks

| Problem | Fallback |
|---|---|
| Scene detection yields 0 frames | Retry with interval extraction at 1 frame/5s |
| More than 100 frames extracted | Subsample evenly to 80 (keep every Nth frame) |
| Scene strategy fails entirely | Step down to interval |
| Keyframe strategy fails entirely | Step down to interval |

## Post-Extraction

After extraction:

1. List all frame files in `$TMPDIR`
2. Calculate each frame's timestamp from its sequence number + extraction rate
3. Check the total count — if it's not in the 20-80 range, apply fallbacks
4. Pass the frame list + timestamps to `workflows/03-delegate-batches.md`

### Calculating timestamps

**Interval extraction at 1 frame every 2s:** frame N timestamp = `(N-1) * 2` seconds

**Scene detection:** timestamps are non-uniform. If exact timestamps matter, rerun the extraction with `showinfo` enabled and capture `pts_time` from stderr; otherwise estimate as `(N / total_frames) * duration`

**Keyframe:** same as scene detection — non-uniform, so either capture `pts_time` during extraction or use an estimate

**Thumbnail filter:** uniform spacing — timestamp = `(N-1) * (duration / frame_count)` seconds

## Next

Move to `workflows/03-delegate-batches.md` with the frame list, timestamps, and `$TMPDIR`.
