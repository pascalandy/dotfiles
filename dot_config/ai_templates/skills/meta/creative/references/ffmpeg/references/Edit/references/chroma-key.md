# Chroma Key / Green Screen

Remove a solid color from a video and composite over a background.

## `chromakey` — YUV-space keying (recommended)

Works in YUV color space; more robust against JPEG / H.264 compression artifacts than RGB keying.

```bash
ffmpeg -i foreground.mp4 -i background.mp4 \
  -filter_complex "[0:v]chromakey=0x00FF00:0.3:0.2[fg];\
[1:v][fg]overlay" out.mp4
```

Parameters: `chromakey=color:similarity:blend`

- `color` — target color in hex (`0x00FF00` = pure green, `0x0000FF` = pure blue)
- `similarity` — how close a pixel must be to the target color (0.01 to 1.0). Higher = more pixels removed. Start at 0.1 and raise as needed.
- `blend` — edge softness (0.0 to 1.0). Higher = smoother edges but bleeds background color. Start at 0.1.

## `colorkey` — RGB-space keying (simpler)

```bash
ffmpeg -i in.mp4 -vf "colorkey=green:0.3:0.2" out.mp4
```

Same parameter shape as `chromakey` but operates in RGB. More likely to leave green halos on compressed sources — prefer `chromakey` unless the source is uncompressed.

## Named Colors

Both filters accept named colors:

- `green` / `lime`
- `blue`
- `red`
- Any named color from [FFmpeg's color list](https://ffmpeg.org/ffmpeg-utils.html#Color)

Or hex: `0xRRGGBB`.

## With Spill Suppression

Green screen footage often has green light spill on the subject. The `despill` filter removes it:

```bash
ffmpeg -i foreground.mp4 -i background.mp4 \
  -filter_complex "\
    [0:v]despill=type=green:mix=0.5:expand=0.1,\
         chromakey=0x00FF00:0.15:0.1[fg];\
    [1:v][fg]overlay" out.mp4
```

`despill` parameters:

- `type` — `green` or `blue`
- `mix` — amount of spill reduction (0.0 to 1.0)
- `expand` — expand the spill area (0.0 to 1.0)

## Animated / Moving Background

The overlay filter handles video backgrounds automatically — just use a video for input 2:

```bash
ffmpeg -i foreground.mp4 -i bg_loop.mp4 \
  -filter_complex "[0:v]chromakey=0x00FF00:0.3:0.2[fg];\
[1:v][fg]overlay=shortest=1" out.mp4
```

`shortest=1` ensures the output stops when either input ends (prevents the overlay from outlasting the foreground).

## With Scaling (common case)

If the foreground is a different resolution from the background, scale first:

```bash
ffmpeg -i foreground.mp4 -i background.mp4 \
  -filter_complex "\
    [0:v]scale=1920:1080,chromakey=0x00FF00:0.3:0.2[fg];\
    [1:v]scale=1920:1080[bg];\
    [bg][fg]overlay=0:0" out.mp4
```

## Tips

- **Lower similarity is better** — start at 0.1 and only raise if there are still green pixels visible
- **Higher blend is NOT better** — too much blend makes the edges look washed out
- **Pre-process if needed** — if the source is JPEG-compressed, consider denoising first: `chromakey` after a light `hqdn3d` filter tends to clean up DCT blocks
- **Consistent lighting matters more than any filter tweak** — if the green screen has shadows, uneven lighting, or wrinkles, no amount of chromakey tuning will fully clean it up

## Debugging Key Quality

Use the `chromakey_studio` combination of chromakey + a magenta background to inspect edges:

```bash
ffmpeg -i in.mp4 -f lavfi -i "color=c=magenta:s=1920x1080" \
  -filter_complex "[0:v]chromakey=0x00FF00:0.3:0.2[fg];\
[1:v][fg]overlay" debug.mp4
```

Bright magenta makes stray green pixels and jagged edges easy to spot.
