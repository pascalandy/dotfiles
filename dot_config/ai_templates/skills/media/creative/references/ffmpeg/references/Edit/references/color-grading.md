# Color Grading

Adjust brightness, contrast, saturation, hue, and apply LUTs.

## Basic Adjustments (`eq` filter)

```bash
ffmpeg -i in.mp4 -vf "eq=brightness=0.05:contrast=1.2:saturation=1.3" out.mp4
```

| Parameter | Range | Default | Notes |
|---|---|---|---|
| `brightness` | -1.0 to 1.0 | 0.0 | Additive offset |
| `contrast` | -1000 to 1000 | 1.0 | Multiplicative around midpoint |
| `saturation` | 0 to 3.0 | 1.0 | 0 = grayscale, >1 = more vivid |
| `gamma` | 0.1 to 10.0 | 1.0 | Midtone lift |
| `gamma_r` / `gamma_g` / `gamma_b` | 0.1 to 10.0 | 1.0 | Per-channel gamma |

## Hue Shift

```bash
ffmpeg -i in.mp4 -vf "hue=h=30:s=1.1" out.mp4
```

- `h=30` — rotate hue by 30 degrees
- `s=1.1` — multiply saturation by 1.1
- `b=0` — brightness adjustment (additive)

## White Balance / Color Balance

```bash
ffmpeg -i in.mp4 -vf "colorbalance=rs=0.1:gs=-0.05:bs=-0.1:rm=0.05:gm=0:bm=-0.05" out.mp4
```

Each channel has three sliders:

- `rs` / `gs` / `bs` — shadows (red, green, blue)
- `rm` / `gm` / `bm` — midtones
- `rh` / `gh` / `bh` — highlights

Range `-1.0` to `1.0`.

## Curves

```bash
ffmpeg -i in.mp4 -vf "curves=preset=increase_contrast" out.mp4
```

Presets:

- `color_negative` — film negative
- `cross_process` — cross-processing look
- `darker` / `lighter`
- `increase_contrast` / `decrease_contrast`
- `linear_contrast`
- `medium_contrast` / `strong_contrast`
- `negative` — invert all colors
- `vintage`

Custom curve (per-channel Bezier):

```bash
ffmpeg -i in.mp4 -vf "curves=r='0/0 0.5/0.58 1/1':g='0/0 0.5/0.5 1/1':b='0/0 0.5/0.45 1/1'" out.mp4
```

Each channel is a list of `input/output` anchor points.

## Apply 3D LUT (.cube files)

```bash
ffmpeg -i in.mp4 -vf "lut3d=file=lut.cube" out.mp4
```

### Interpolation modes

```bash
ffmpeg -i in.mp4 -vf "lut3d=file=lut.cube:interp=tetrahedral" out.mp4
```

- `nearest` — fastest, lowest quality
- `trilinear` — default, balanced
- `tetrahedral` — slowest, highest quality (recommended for final renders)

## Apply Hald CLUT (PNG lookup images)

Hald CLUTs are PNG images that encode a color transformation. Free ones are widely available (e.g. from Photoshop LUT bundles).

```bash
ffmpeg -i in.mp4 -i lut.png \
  -filter_complex "[0:v][1:v]haldclut" out.mp4
```

## Log → Rec.709 Conversion

If your footage is in a log color space (S-Log, C-Log, V-Log), you need to convert to Rec.709 before displaying. Use a vendor-provided 3D LUT:

```bash
ffmpeg -i slog.mp4 -vf "lut3d=file=slog3_to_rec709.cube:interp=tetrahedral" rec709.mp4
```

## Film Emulation Stack

A typical film look recipe:

```bash
ffmpeg -i in.mp4 -vf "\
curves=preset=vintage,\
eq=saturation=0.9:contrast=1.1,\
vignette=angle=PI/5" out.mp4
```

Each filter is applied in order — curves first, then EQ, then vignette.

## Vignette

```bash
ffmpeg -i in.mp4 -vf "vignette=angle=PI/4" out.mp4
```

- `angle=PI/4` — darker at corners
- `angle=0` — no vignette
- `x0=` / `y0=` — offset the vignette center

## Color Histogram (for analysis)

```bash
ffmpeg -i in.mp4 -vf "histogram" -frames:v 1 histogram.png
```

Produces a static histogram image showing luma/chroma distribution.
