# Preset Profiles

Named output profiles tuned for common delivery targets. Pick one by use case and copy the command.

## Profile Catalogue

| Profile | Codec | CRF | Resolution | Use Case |
|---|---|---|---|---|
| `web-optimized` | H.264 | 23 | Source | Browser streaming, CDN delivery |
| `high-quality` | H.264 | 18 | Source | Archive master, editing intermediate |
| `social-media-vertical` | H.264 | 23 | 1080×1920 (9:16) | TikTok, Instagram Reels, YouTube Shorts |
| `social-media-square` | H.264 | 23 | 1080×1080 (1:1) | Instagram feed, LinkedIn |
| `social-media-landscape` | H.264 | 23 | 1920×1080 (16:9) | YouTube, Twitter |
| `fast-preview` | H.264 | 28 | 960×540 | Proxy, review link, first-pass check |
| `lossless-intermediate` | FFV1 | — | Source | Post-production master, archival |
| `av1-small` | AV1 | 35 | Source | Smallest file, archive-ready |
| `mobile-friendly` | H.264 | 26 | 1280×720 max | Limited bandwidth, older devices |

## Commands

### `web-optimized`

```bash
ffmpeg -i INPUT \
  -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  OUTPUT.mp4
```

### `high-quality`

```bash
ffmpeg -i INPUT \
  -c:v libx264 -crf 18 -preset veryslow -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  OUTPUT.mp4
```

### `social-media-vertical` (9:16, TikTok / Reels)

```bash
ffmpeg -i INPUT \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,\
pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1" \
  -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 \
  -movflags +faststart \
  OUTPUT.mp4
```

### `social-media-square` (1:1, Instagram feed)

```bash
ffmpeg -i INPUT \
  -vf "scale=1080:1080:force_original_aspect_ratio=decrease,\
pad=1080:1080:(ow-iw)/2:(oh-ih)/2:black,setsar=1" \
  -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 \
  -movflags +faststart \
  OUTPUT.mp4
```

### `social-media-landscape` (16:9, YouTube / Twitter)

```bash
ffmpeg -i INPUT \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,\
pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,setsar=1" \
  -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 \
  -movflags +faststart \
  OUTPUT.mp4
```

### `fast-preview`

```bash
ffmpeg -i INPUT \
  -vf "scale=960:-2" \
  -c:v libx264 -crf 28 -preset ultrafast -pix_fmt yuv420p \
  -c:a aac -b:a 96k \
  -movflags +faststart \
  OUTPUT.mp4
```

### `lossless-intermediate` (FFV1 in Matroska)

```bash
ffmpeg -i INPUT \
  -c:v ffv1 -level 3 -g 1 -slicecrc 1 \
  -c:a flac \
  OUTPUT.mkv
```

### `av1-small` (best compression)

```bash
ffmpeg -i INPUT \
  -c:v libaom-av1 -crf 35 -cpu-used 4 -pix_fmt yuv420p \
  -c:a libopus -b:a 96k \
  OUTPUT.mkv
```

### `mobile-friendly`

```bash
ffmpeg -i INPUT \
  -vf "scale='min(1280,iw)':-2" \
  -c:v libx264 -crf 26 -preset slow -pix_fmt yuv420p \
  -profile:v main -level 4.0 \
  -c:a aac -b:a 96k -ar 44100 \
  -movflags +faststart \
  OUTPUT.mp4
```

The `-profile:v main -level 4.0` ensures playback on older iOS and Android devices.

## When to Deviate from a Preset

- **Source is vertical phone footage going to a 16:9 target** → add `transpose=1` or `transpose=2` before the scale
- **Source has terrible audio** → add `afftdn=nf=-25` to the audio filter chain
- **Source is log-gamma** → add `lut3d=file=<vendor>_to_rec709.cube` before scaling
- **Target is a platform with strict bitrate limits** → replace `-crf` with `-b:v` at the exact target rate
