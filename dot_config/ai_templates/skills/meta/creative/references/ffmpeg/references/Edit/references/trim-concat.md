# Trim and Concat

## Trim / Cut

### Fast stream-copy trim (no re-encode)

```bash
ffmpeg -ss 00:01:00 -to 00:02:30 -i input.mp4 -c copy out.mp4
```

- `-ss` **before** `-i` enables fast seeking (jumps to the nearest keyframe). Output start will snap to a keyframe, which may be slightly before the requested time.
- Use this when precision is not required and speed matters.

### Precise trim (re-encodes around keyframes)

```bash
ffmpeg -ss 00:01:00 -i input.mp4 -t 90 -c:v libx264 -crf 18 -c:a aac out.mp4
```

- `-ss` **after** `-i` is frame-accurate but decodes from the start of the file to the seek point.
- Use this when you need exact start/end times.

### Cut from start timestamp to duration

```bash
ffmpeg -i input.mp4 -ss 00:01:30 -t 00:02:00 -c copy out.mp4
```

### Cut from start to end timestamp

```bash
ffmpeg -i input.mp4 -ss 00:01:30 -to 00:03:30 -c copy out.mp4
```

### Seek hybrid (fast + accurate)

```bash
# Seek roughly with -ss before -i, then fine-tune with -ss after -i
ffmpeg -ss 00:00:55 -i input.mp4 -ss 5 -t 90 -c:v libx264 -crf 18 out.mp4
```

## Concatenate Files

### Concat demuxer (same codec, no re-encode)

Create the list file:

```bash
cat > files.txt << EOF
file 'video1.mp4'
file 'video2.mp4'
file 'video3.mp4'
EOF
```

Then concat:

```bash
ffmpeg -f concat -safe 0 -i files.txt -c copy output.mp4
```

**All files must share the same codec, resolution, frame rate, and pixel format** for this to work.

### Concat with helper script

```bash
scripts/concat.sh out.mp4 clip1.mp4 clip2.mp4 clip3.mp4
```

The helper script handles absolute paths automatically.

### Concat different codecs (re-encode)

```bash
ffmpeg -f concat -safe 0 -i files.txt -c:v libx264 -c:a aac output.mp4
```

### Concat filter (true frame-accurate join)

When the concat demuxer can't handle it (different resolutions or codecs):

```bash
ffmpeg -i video1.mp4 -i video2.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" output.mp4
```

This re-encodes but guarantees frame-accurate joins regardless of input differences.

## Fast Seek for Large Files

When the input file is very large (multi-GB), put `-ss` before `-i` even for re-encoding workflows:

```bash
ffmpeg -ss 00:10:00 -i large_video.mp4 -t 00:05:00 -c copy clip.mp4
```

This avoids decoding from the start of the file and is dramatically faster.
