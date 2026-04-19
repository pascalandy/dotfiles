# Transitions (xfade)

Smooth transitions between two clips using the `xfade` video filter and `acrossfade` audio filter.

## Dissolve (the classic)

1-second overlap at t=5:

```bash
ffmpeg -i a.mp4 -i b.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=dissolve:duration=1:offset=5[v];\
[0:a][1:a]acrossfade=d=1[a]" \
  -map "[v]" -map "[a]" out.mp4
```

- `transition=dissolve` — the type of transition
- `duration=1` — 1 second overlap
- `offset=5` — transition starts at second 5 of clip A
- `acrossfade=d=1` — matching 1-second audio crossfade

## xfade Transition Catalogue

### Fades and dissolves

- `fade` — simple opacity fade to black then from black
- `fadeblack` — fade to black between clips
- `fadewhite` — fade to white between clips
- `fadegrays` — fade through grayscale
- `dissolve` — random pixel dissolve

### Wipes

- `wipeleft` / `wiperight` — horizontal wipe
- `wipeup` / `wipedown` — vertical wipe
- `wipetl` / `wipetr` / `wipebl` / `wipebr` — diagonal wipe (top-left, top-right, etc.)

### Slides

- `slideleft` / `slideright` / `slideup` / `slidedown`

### Smooth directional

- `smoothleft` / `smoothright` / `smoothup` / `smoothdown`

### Geometric

- `circlecrop` / `rectcrop` — shape-based reveals
- `circleclose` / `circleopen` — circular reveals
- `horzclose` / `horzopen` — horizontal bar reveals
- `vertclose` / `vertopen` — vertical bar reveals
- `diagbl` / `diagbr` / `diagtl` / `diagtr` — diagonal reveals

### Creative

- `radial` — radial sweep
- `pixelize` — pixelated transition
- `hlslice` / `hrslice` — horizontal slices
- `vuslice` / `vdslice` — vertical slices
- `hblur` — blur transition
- `squeezev` / `squeezeh` — squeeze transition
- `distance` — depth-based transition

All 40+ xfade transitions are documented in the official FFmpeg filter docs.

## Calculating Offset for Multi-Clip Sequences

When joining clip A (10s) + clip B (8s) + clip C (7s) with 1s overlaps:

- Transition 1 offset = `A.duration - overlap` = `10 - 1 = 9`
- After first transition, total length = `A + B - overlap` = `10 + 8 - 1 = 17`
- Transition 2 offset = `17 - overlap` = `16`

Example three-clip dissolve:

```bash
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 \
  -filter_complex "\
    [0:v][1:v]xfade=transition=dissolve:duration=1:offset=9[ab];\
    [ab][2:v]xfade=transition=dissolve:duration=1:offset=16[v];\
    [0:a][1:a]acrossfade=d=1[ab_a];\
    [ab_a][2:a]acrossfade=d=1[a]" \
  -map "[v]" -map "[a]" out.mp4
```

## Offset Is the Single Biggest Pitfall

- `offset` is measured **from the start of clip A** (the first input)
- If clip A is 10s and you want a 1s transition at the very end, `offset = 9` (not 10)
- An offset that's too late = black frames before the transition; too early = clip B appears before A finishes

## Audio Sync

Use `acrossfade=d=N` where N matches the video transition `duration`. Otherwise audio and video desynchronize across the cut.

## Custom Matte Transitions

For truly custom transitions (company logo wipes, branded shapes), generate a matte video and use `alphamerge`:

```bash
ffmpeg -i a.mp4 -i b.mp4 -i matte.mp4 \
  -filter_complex "[2:v]format=gray,fps=30[m];\
[1:v][m]alphamerge[b_alpha];\
[0:v][b_alpha]overlay=shortest=1[v]" \
  -map "[v]" -map 0:a out.mp4
```
