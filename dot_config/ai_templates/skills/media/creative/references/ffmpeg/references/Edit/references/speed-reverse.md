# Speed and Reverse

## Speed Change (within native range)

### 2× speed

```bash
ffmpeg -i in.mp4 -vf "setpts=0.5*PTS" -af "atempo=2.0" out.mp4
```

### 0.5× speed (half speed)

```bash
ffmpeg -i in.mp4 -vf "setpts=2.0*PTS" -af "atempo=0.5" out.mp4
```

## Extreme Speed Change (chain atempo)

The `atempo` filter is limited to `0.5` - `2.0` per instance. For ratios outside that range, chain multiple `atempo` filters.

### 4× speed

```bash
ffmpeg -i in.mp4 -vf "setpts=0.25*PTS" -af "atempo=2.0,atempo=2.0" out.mp4
```

### 8× speed

```bash
ffmpeg -i in.mp4 -vf "setpts=0.125*PTS" -af "atempo=2.0,atempo=2.0,atempo=2.0" out.mp4
```

### 0.25× speed (quarter speed)

```bash
ffmpeg -i in.mp4 -vf "setpts=4.0*PTS" -af "atempo=0.5,atempo=0.5" out.mp4
```

## The Math

| User wants | `setpts` multiplier | `atempo` chain |
|---|---|---|
| 0.25× (quarter speed) | `4.0*PTS` | `atempo=0.5,atempo=0.5` |
| 0.5× (half speed) | `2.0*PTS` | `atempo=0.5` |
| 0.75× | `1.333*PTS` | `atempo=0.75` |
| 1.0× (normal) | `1.0*PTS` | `atempo=1.0` (no-op) |
| 1.5× | `0.6667*PTS` | `atempo=1.5` |
| 2.0× | `0.5*PTS` | `atempo=2.0` |
| 4.0× | `0.25*PTS` | `atempo=2.0,atempo=2.0` |
| 8.0× | `0.125*PTS` | `atempo=2.0,atempo=2.0,atempo=2.0` |

**Rule:** `setpts` multiplier is the reciprocal of the speed ratio. Chain `atempo` filters (each in 0.5-2.0) until their product equals the speed ratio.

## Drop Audio (video-only speed change)

If you don't care about audio, this is simpler:

```bash
ffmpeg -i in.mp4 -vf "setpts=0.5*PTS" -an out.mp4
```

## Reverse

### Reverse video + audio

```bash
ffmpeg -i in.mp4 -vf "reverse" -af "areverse" out.mp4
```

Note: `reverse` loads the entire video into memory. For long videos, split into chunks first, reverse each, then concat in reverse order.

### Reverse video only

```bash
ffmpeg -i in.mp4 -vf "reverse" -an out.mp4
```

## Time Stretch without Pitch Change

`atempo` already handles this — it preserves pitch when changing speed. If you want the opposite (speed unchanged, pitch shifted), use:

```bash
ffmpeg -i in.mp4 -af "asetrate=44100*1.25,aresample=44100,atempo=0.8" out.mp4
```

This shifts pitch up a major third while keeping playback speed constant.
