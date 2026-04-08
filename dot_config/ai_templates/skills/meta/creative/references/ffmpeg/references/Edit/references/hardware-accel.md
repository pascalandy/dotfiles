# Hardware-Accelerated Encoding

Use the GPU to accelerate encoding. Dramatically faster than software, with a small quality penalty at matching bitrates.

## NVIDIA NVENC

### H.264

```bash
ffmpeg -hwaccel cuda -i in.mp4 -c:v h264_nvenc -preset p4 -cq 23 out.mp4
```

### H.265 / HEVC

```bash
ffmpeg -hwaccel cuda -i in.mp4 -c:v hevc_nvenc -preset p4 -cq 26 out.mp4
```

### NVENC presets

- `p1` — fastest, lowest quality
- `p4` — balanced (like software `medium`)
- `p7` — slowest, highest quality

### NVENC rate control

- `-cq` — constant quality (like CRF)
- `-b:v` — constant bitrate
- `-rc vbr_hq` — variable bitrate high quality

### Full NVDEC + NVENC pipeline (GPU decode + GPU encode)

```bash
ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
  -i input.mp4 \
  -c:v h264_nvenc -preset p4 -cq 23 \
  output.mp4
```

`-hwaccel_output_format cuda` keeps decoded frames on the GPU — no round-trip to CPU memory.

## Intel QuickSync (QSV)

### H.264

```bash
ffmpeg -hwaccel qsv -i in.mp4 -c:v h264_qsv -global_quality 23 out.mp4
```

### H.265

```bash
ffmpeg -hwaccel qsv -i in.mp4 -c:v hevc_qsv -global_quality 26 out.mp4
```

### QSV with scaling on GPU

```bash
ffmpeg -hwaccel qsv -c:v h264_qsv -i in.mp4 \
  -vf "scale_qsv=w=1920:h=1080" \
  -c:v h264_qsv -global_quality 23 out.mp4
```

## Apple VideoToolbox (macOS)

### H.264

```bash
ffmpeg -i in.mp4 -c:v h264_videotoolbox -b:v 5M out.mp4
```

### H.265

```bash
ffmpeg -i in.mp4 -c:v hevc_videotoolbox -q:v 60 out.mp4
```

### VideoToolbox quality mode

```bash
ffmpeg -i in.mp4 -c:v hevc_videotoolbox -q:v 60 -tag:v hvc1 out.mp4
```

`-tag:v hvc1` fixes HEVC playback on Apple devices (QuickTime won't play `hev1` tags).

Note: VideoToolbox quality range is 0-100 (higher = better), **opposite of CRF**.

## VAAPI (Linux — Intel, AMD)

### H.264

```bash
ffmpeg -vaapi_device /dev/dri/renderD128 \
  -i in.mp4 \
  -vf 'format=nv12,hwupload' \
  -c:v h264_vaapi -qp 23 \
  out.mp4
```

### H.265

```bash
ffmpeg -vaapi_device /dev/dri/renderD128 \
  -i in.mp4 \
  -vf 'format=nv12,hwupload' \
  -c:v hevc_vaapi -qp 25 \
  out.mp4
```

## AMD AMF (Windows)

### H.264

```bash
ffmpeg -i in.mp4 -c:v h264_amf -quality quality -b:v 5M out.mp4
```

### H.265

```bash
ffmpeg -i in.mp4 -c:v hevc_amf -quality quality -b:v 5M out.mp4
```

## Which Should I Use?

| Platform | Recommendation |
|---|---|
| Linux / NVIDIA GPU | NVENC (`h264_nvenc` / `hevc_nvenc`) |
| Linux / Intel or AMD | VAAPI |
| macOS (any chip) | VideoToolbox (`hevc_videotoolbox` for efficiency) |
| Windows / NVIDIA | NVENC |
| Windows / Intel | QSV |
| Windows / AMD | AMF |

## Quality Considerations

Hardware encoders produce 5-15% larger files than software encoders at matching quality. This is the tradeoff for 5-20× speed gains.

**When hardware encoding is a good fit:**
- Real-time streaming (OBS, Zoom, Teams)
- Quick previews during editing
- Batch transcoding where the time savings exceed the storage cost
- Any workload where encoding time is the bottleneck

**When software encoding is a better fit:**
- Final deliverables for archive or broadcast
- Small output files where every byte counts
- Content with difficult motion (sports, game capture) where software handles motion estimation better

## Checking Hardware Support

```bash
# List all encoders
ffmpeg -encoders | grep -E "^.V"

# Check if NVENC is available
ffmpeg -hide_banner -encoders 2>&1 | grep -i nvenc

# Check CUDA devices
ffmpeg -init_hw_device list
```
