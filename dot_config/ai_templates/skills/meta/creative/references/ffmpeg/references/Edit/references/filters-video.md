# Video Filters

Scale, crop, overlay, drawtext, and effect filters.

## Scale and Resize

### Specific dimensions

```bash
ffmpeg -i input.mp4 -vf "scale=1920:1080" output.mp4
```

### Preserve aspect ratio (fit within)

```bash
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease" output.mp4
```

### Scale with padding (letterbox / pillarbox)

```bash
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,\
pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" output.mp4
```

### Scale by width only (auto-height)

```bash
ffmpeg -i input.mp4 -vf "scale=1280:-2" output.mp4
```

`-2` instead of `-1` ensures the height is divisible by 2 (required by many codecs).

### Scale to 50%

```bash
ffmpeg -i input.mp4 -vf "scale=iw/2:ih/2" output.mp4
```

## Crop

### Specific dimensions and offset

```bash
ffmpeg -i input.mp4 -vf "crop=640:480:100:50" output.mp4
```

Format: `crop=width:height:x:y` where `(x,y)` is the top-left corner.

### Center crop to 16:9

```bash
ffmpeg -i input.mp4 -vf "crop=ih*16/9:ih" output.mp4
```

### Center crop to 1:1 square

```bash
ffmpeg -i input.mp4 -vf "crop=min(iw\,ih):min(iw\,ih)" output.mp4
```

## Overlay / Watermark

### Overlay image in top-right with margin

```bash
ffmpeg -i video.mp4 -i watermark.png \
  -filter_complex "[0:v][1:v] overlay=W-w-10:10" out.mp4
```

### Overlay image in bottom-right

```bash
ffmpeg -i video.mp4 -i watermark.png \
  -filter_complex "overlay=W-w-10:H-h-10" output.mp4
```

### Overlay with opacity (80%)

```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.8[logo];\
[0:v][logo]overlay=W-w-20:20" output.mp4
```

## Draw Text

### Basic title overlay

```bash
ffmpeg -i input.mp4 -vf \
  "drawtext=text='Hello World':fontsize=24:fontcolor=white:x=10:y=10" output.mp4
```

### Centered title with shadow

```bash
ffmpeg -i in.mp4 -vf \
  "drawtext=text='My Title':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf\
:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2\
:shadowx=2:shadowy=2" out.mp4
```

### Timecode overlay

```bash
ffmpeg -i in.mp4 -vf \
  "drawtext=text='%{pts\:hms}':fontsize=24:fontcolor=white:x=10:y=10:\
box=1:boxcolor=black@0.5" out.mp4
```

## Color and Effects

### Brightness / contrast / saturation

```bash
ffmpeg -i input.mp4 -vf "eq=brightness=0.1:contrast=1.2:saturation=1.3" output.mp4
```

### Convert to grayscale

```bash
ffmpeg -i input.mp4 -vf "colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3" output.mp4
```

Or simpler:

```bash
ffmpeg -i input.mp4 -vf "hue=s=0" output.mp4
```

### Fade in / out

```bash
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=2,fade=t=out:st=8:d=2" output.mp4
```

- `st=0:d=2` — fade in over 2s starting at 0
- `st=8:d=2` — fade out over 2s starting at second 8

### Box blur

```bash
ffmpeg -i input.mp4 -vf "boxblur=5:1" output.mp4
```

Format: `boxblur=luma_radius:luma_power:chroma_radius:chroma_power`.

### Gaussian blur (better quality)

```bash
ffmpeg -i input.mp4 -vf "gblur=sigma=5" output.mp4
```

## See Also

- **Color grading / LUTs** → `color-grading.md`
- **Chroma key / green screen** → `chroma-key.md`
- **Compositing and subtitles** → `compositing.md`
- **Transitions between clips** → `transitions.md`
