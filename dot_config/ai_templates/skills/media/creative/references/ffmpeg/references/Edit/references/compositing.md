# Compositing

Picture-in-picture, stacking layouts, and subtitle burning.

## Picture-in-Picture (PiP)

### Small video over main video

```bash
ffmpeg -i main.mp4 -i overlay.mp4 \
  -filter_complex "[1:v]scale=320:-1[pip];\
[0:v][pip]overlay=W-w-10:H-h-10" \
  output.mp4
```

- `scale=320:-1` — shrinks the overlay to 320px wide, auto height
- `overlay=W-w-10:H-h-10` — position in bottom-right corner with 10px margin

### PiP with border / background

```bash
ffmpeg -i main.mp4 -i overlay.mp4 \
  -filter_complex "\
    [1:v]scale=320:-1,pad=iw+6:ih+6:3:3:color=white[pip];\
    [0:v][pip]overlay=W-w-10:H-h-10" \
  output.mp4
```

The `pad` filter adds a white border around the PiP before overlaying.

### PiP with custom position

```bash
# Top-left
overlay=10:10

# Top-right
overlay=W-w-10:10

# Bottom-left
overlay=10:H-h-10

# Bottom-right
overlay=W-w-10:H-h-10

# Center
overlay=(W-w)/2:(H-h)/2
```

Variables: `W`/`H` = main video dimensions, `w`/`h` = overlay dimensions.

## Stacking Layouts

### Side by side (hstack)

```bash
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0:v][1:v]hstack=inputs=2" out.mp4
```

Both videos must have the same height. If not, scale one first:

```bash
ffmpeg -i a.mp4 -i b.mp4 \
  -filter_complex "[0:v]scale=-1:720[a];[1:v]scale=-1:720[b];[a][b]hstack" \
  out.mp4
```

### Top / bottom (vstack)

```bash
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0:v][1:v]vstack=inputs=2" out.mp4
```

Both videos must have the same width.

### 2×2 grid (xstack)

```bash
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 -i d.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0" \
  out.mp4
```

Layout grammar:

- `0_0` = top-left (origin)
- `w0_0` = right of input 0, at the top
- `0_h0` = left, below input 0
- `w0_h0` = right of 0, below 0

Each entry is `Xoffset_Yoffset` where offsets can reference earlier inputs' widths (`w0`, `w1`) and heights (`h0`, `h1`).

### 1×3 row

```bash
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 \
  -filter_complex "[0:v][1:v][2:v]xstack=inputs=3:layout=0_0|w0_0|w0+w1_0" \
  out.mp4
```

### 3×1 column

```bash
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 \
  -filter_complex "[0:v][1:v][2:v]xstack=inputs=3:layout=0_0|0_h0|0_h0+h1" \
  out.mp4
```

## Burn Subtitles

### SRT subtitles (re-encode required)

```bash
ffmpeg -i video.mp4 -vf "subtitles=subs.srt" out.mp4
```

### ASS / SSA subtitles (preserves styling)

```bash
ffmpeg -i video.mp4 -vf "ass=subs.ass" out.mp4
```

Advanced SubStation Alpha supports fonts, colors, positioning, and animations.

### SRT with custom styling

```bash
ffmpeg -i video.mp4 -vf "subtitles=subs.srt:force_style='FontName=Arial,FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=3'" out.mp4
```

Colors use `&HBBGGRR` format (not RGB).

## Soft Subtitle Track (no burn)

Add subtitles as a selectable track without burning them into the video:

```bash
ffmpeg -i video.mp4 -i subs.srt -c:v copy -c:a copy -c:s mov_text out.mp4
```

MP4 requires `mov_text`. MKV accepts SRT directly with `-c:s copy`.

## Multi-Layer Composition Example

Main video + logo + PiP webcam + lower-third title:

```bash
ffmpeg -i main.mp4 -i logo.png -i webcam.mp4 \
  -filter_complex "\
    [0:v]setsar=1[base];\
    [1:v]scale=150:-1[logo];\
    [2:v]scale=320:-1[cam];\
    [base][logo]overlay=W-w-20:20[bg1];\
    [bg1][cam]overlay=20:H-h-20[bg2];\
    [bg2]drawtext=text='Live':fontsize=36:fontcolor=white:x=20:y=20:\
box=1:boxcolor=red@0.8:boxborderw=10[final]" \
  -map "[final]" -map 0:a -c:a copy out.mp4
```

Reads as: scale logo → scale webcam → overlay logo top-right → overlay webcam bottom-left → draw "Live" badge top-left.
