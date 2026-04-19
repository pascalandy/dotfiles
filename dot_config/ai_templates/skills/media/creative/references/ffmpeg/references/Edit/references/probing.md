# Probing with ffprobe

Query metadata about media files without modifying them.

## Full JSON Dump

```bash
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4
```

This is the canonical call — clean JSON with format (container) and all streams. Parse with `jq`:

```bash
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4 | \
  jq '.streams[] | select(.codec_type=="video") | {codec_name, width, height}'
```

## Single-Value Queries

### Duration (in seconds)

```bash
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 video.mp4
```

### Resolution

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height \
  -of csv=p=0 video.mp4
```

Output: `1920,1080`

### Video codec

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name \
  -of default=noprint_wrappers=1:nokey=1 video.mp4
```

### Frame rate

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate \
  -of default=noprint_wrappers=1:nokey=1 video.mp4
```

Output: `30000/1001` (29.97 fps) or `30/1` (30 fps) — a rational number.

### Bitrate

```bash
ffprobe -v error -show_entries format=bit_rate \
  -of default=noprint_wrappers=1:nokey=1 video.mp4
```

### Audio sample rate

```bash
ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate \
  -of default=noprint_wrappers=1:nokey=1 video.mp4
```

### Audio channel count

```bash
ffprobe -v error -select_streams a:0 -show_entries stream=channels \
  -of default=noprint_wrappers=1:nokey=1 video.mp4
```

### Pixel format

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt \
  -of default=noprint_wrappers=1:nokey=1 video.mp4
```

## Frame-Level Probing

### Exact frame count

```bash
ffprobe -v error -select_streams v:0 -count_frames \
  -show_entries stream=nb_read_frames \
  -of default=noprint_wrappers=1:nokey=1 video.mp4
```

Warning: this decodes the entire video. For approximate count from metadata:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames \
  -of default=noprint_wrappers=1:nokey=1 video.mp4
```

### I-frame positions (keyframes)

```bash
ffprobe -v error -select_streams v:0 -show_frames \
  -show_entries frame=pkt_pts_time,pict_type \
  -of csv=print_section=0 video.mp4 | grep ',I$'
```

Useful for finding safe cut points when using stream copy.

### GOP size

Look at keyframe positions to determine average GOP length:

```bash
ffprobe -v error -select_streams v:0 -show_frames \
  -show_entries frame=pict_type \
  -of csv=print_section=0 video.mp4 | head -200 | grep -c "^I"
```

## Stream Information

### Number of streams

```bash
ffprobe -v error -show_entries format=nb_streams \
  -of default=noprint_wrappers=1:nokey=1 video.mp4
```

### List all stream codecs

```bash
ffprobe -v error -show_entries stream=index,codec_type,codec_name \
  -of csv=p=0 video.mp4
```

### Language tags (for multi-language audio)

```bash
ffprobe -v error -show_entries stream=index,codec_type:stream_tags=language \
  -of csv=p=0 video.mp4
```

## Common Scripted Uses

### Get duration for a for-loop

```bash
for f in *.mp4; do
    dur=$(ffprobe -v error -show_entries format=duration \
            -of default=noprint_wrappers=1:nokey=1 "$f")
    echo "$f: ${dur}s"
done
```

### Check if audio track exists

```bash
has_audio=$(ffprobe -v error -select_streams a:0 \
              -show_entries stream=codec_type \
              -of default=noprint_wrappers=1:nokey=1 video.mp4)
if [[ "$has_audio" == "audio" ]]; then
    echo "has audio"
fi
```

### Validate file is a playable video

```bash
if ffprobe -v error video.mp4 >/dev/null 2>&1; then
    echo "valid"
else
    echo "corrupted"
fi
```

## Output Format Options

`-of` / `-print_format` controls the shape of ffprobe output:

- `default` — human-readable `key=value` pairs
- `json` — nested JSON
- `xml` — XML tree
- `csv` — comma-separated
- `flat` — dot-notation flat keys
- `ini` — INI file sections

Modifiers on `default`:

- `noprint_wrappers=1` — skip section headers
- `nokey=1` — print only values (not `key=value`)

These compose: `default=noprint_wrappers=1:nokey=1` prints raw values only.
