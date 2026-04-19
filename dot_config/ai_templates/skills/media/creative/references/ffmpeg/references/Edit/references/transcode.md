# Transcode

Convert between codecs. Choose the codec based on the target platform and quality/compression tradeoff.

## H.264 — Web-Safe MP4 (the default)

Broad compatibility, good quality/size ratio. This is what every browser and player understands.

```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset slow \
  -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart out.mp4
```

- `-crf 23` is visually transparent for most content. Lower for higher quality (18 is archive-grade).
- `-preset slow` gives 10-20% better compression than `medium`. Use `veryslow` for maximum efficiency at 5-10x the encoding time.
- `-pix_fmt yuv420p` ensures compatibility with hardware decoders.
- `-movflags +faststart` moves the moov atom to the front so the video starts playing before fully downloaded (web streaming).

## H.265 / HEVC — Smaller Files

About 50% smaller than H.264 at the same quality. Safari / iOS native; browser support varies.

```bash
ffmpeg -i input.mp4 -c:v libx265 -crf 28 -preset slow \
  -pix_fmt yuv420p -c:a aac -b:a 128k out.mp4
```

Note: H.265 `-crf 28` is roughly equivalent to H.264 `-crf 23`.

## VP9 — Web Native (no H.265 issues)

Good for YouTube-style delivery. Open codec, no licensing.

```bash
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 33 -b:v 0 \
  -c:a libopus -b:a 128k out.webm
```

- `-b:v 0` enables true constant-quality mode (needed for `-crf` to work correctly in VP9)

## AV1 — Best Compression

~30% smaller than VP9, ~50% smaller than H.264. Slow to encode; fast to decode (on modern hardware).

```bash
ffmpeg -i input.mp4 -c:v libaom-av1 -crf 35 -cpu-used 4 \
  -c:a libopus -b:a 128k out.mkv
```

- `-cpu-used 4` balances speed vs compression; range 0 (slowest, best) to 8 (fastest, worst)

## ProRes 422 — Editing Intermediate

Apple's lossy-but-edit-friendly codec. Huge files, very fast decode, perfect for NLE timelines.

```bash
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 3 -c:a pcm_s16le out.mov
```

Profiles: `0`=Proxy, `1`=LT, `2`=Standard, `3`=HQ, `4`=4444.

## FFV1 — Lossless Intermediate

Lossless archival codec. Use when you need a master copy.

```bash
ffmpeg -i input.mp4 -c:v ffv1 -level 3 -g 1 -slicecrc 1 -c:a copy out.mkv
```

## HLS — HTTP Live Streaming

Segments the video into chunks for adaptive streaming.

### Single-bitrate HLS

```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac \
  -hls_time 10 -hls_playlist_type vod \
  -hls_segment_filename "segment_%03d.ts" \
  playlist.m3u8
```

### Multi-bitrate HLS (adaptive)

```bash
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split=3[v1][v2][v3]; \
    [v1]scale=1920:1080[v1out]; \
    [v2]scale=1280:720[v2out]; \
    [v3]scale=854:480[v3out]" \
  -map "[v1out]" -map 0:a -c:v libx264 -b:v 5M -c:a aac -b:a 192k \
    -hls_time 10 -hls_playlist_type vod 1080p.m3u8 \
  -map "[v2out]" -map 0:a -c:v libx264 -b:v 2M -c:a aac -b:a 128k \
    -hls_time 10 -hls_playlist_type vod 720p.m3u8 \
  -map "[v3out]" -map 0:a -c:v libx264 -b:v 1M -c:a aac -b:a 96k \
    -hls_time 10 -hls_playlist_type vod 480p.m3u8
```

You'll want a master `.m3u8` manifest referencing the three rungs; either write it by hand or use a packager like Shaka.

## DASH — Dynamic Adaptive Streaming

MPEG-standard alternative to HLS.

```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac \
  -f dash -seg_duration 10 \
  -use_template 1 -use_timeline 1 \
  manifest.mpd
```

## Stream Copy (no re-encode)

Just changing the container:

```bash
ffmpeg -i input.mkv -c copy output.mp4
```

Works only if the source codecs are compatible with the destination container (e.g. H.264+AAC→MP4 works, VP9→MP4 doesn't).

## CRF Reference Table

| Codec | Visually Lossless | High Quality | Balanced | Low Quality |
|---|---|---|---|---|
| H.264 (libx264) | 18 | 20 | 23 | 28 |
| H.265 (libx265) | 22 | 24 | 28 | 32 |
| VP9 (libvpx-vp9) | 28 | 30 | 33 | 37 |
| AV1 (libaom-av1) | 25 | 30 | 35 | 40 |
