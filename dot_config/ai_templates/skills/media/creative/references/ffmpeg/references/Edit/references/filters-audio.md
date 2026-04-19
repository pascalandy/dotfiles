# Audio Filters

Volume, normalization, denoising, filtering, and mixing.

## Volume

### Simple gain

```bash
ffmpeg -i input.mp4 -af "volume=1.5" output.mp4
```

- `1.0` = unchanged
- `1.5` = +50% louder (~+3.5 dB)
- `0.5` = -50% quieter (~-6 dB)
- `volume=-6dB` = explicit dB notation

### Fade in / out

```bash
ffmpeg -i in.mp4 -af "afade=t=in:d=2,afade=t=out:st=57:d=3" out.mp4
```

## Normalization

### EBU R128 loudness normalization (two-pass, highest quality)

Use the helper script:

```bash
scripts/normalize-audio.sh in.mp4 out.mp4
```

### EBU R128 one-pass

```bash
ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.mp4
```

- `I=-16` — integrated loudness target (LUFS). `-16` is standard for streaming; `-23` for broadcast.
- `TP=-1.5` — true peak maximum (dBTP). `-1.5` avoids inter-sample clipping on lossy codecs.
- `LRA=11` — loudness range (LU). `11` preserves dynamics; lower = more compressed.

### Peak normalization (simpler, less accurate)

```bash
ffmpeg -i input.mp4 -af "dynaudnorm" output.mp4
```

## Denoising

### Remove background hiss / hum

```bash
ffmpeg -i input.mp4 -af "afftdn=nf=-25" output.mp4
```

- `nf=-25` — noise floor in dB. More negative = more aggressive reduction. Start at `-20` and increase if needed.

### Aggressive noise reduction (RNNoise)

```bash
ffmpeg -i input.mp4 -af "arnndn=m=bd.rnnn" output.mp4
```

Requires a pre-trained model file (e.g. `bd.rnnn` from https://github.com/GregorR/rnnoise-models).

## Filters

### High-pass (remove low frequencies)

```bash
ffmpeg -i input.mp4 -af "highpass=f=200" output.mp4
```

Removes everything below 200 Hz. Useful for cleaning up voiceover (removes rumble, mic handling noise).

### Low-pass (remove high frequencies)

```bash
ffmpeg -i input.mp4 -af "lowpass=f=3000" output.mp4
```

Removes everything above 3000 Hz. Useful for telephony / lo-fi effects.

### Band-pass (voice range)

```bash
ffmpeg -i input.mp4 -af "highpass=f=200,lowpass=f=4000" output.mp4
```

## Effects

### Echo / reverb

```bash
ffmpeg -i input.mp4 -af "aecho=0.8:0.88:60:0.4" output.mp4
```

Format: `aecho=in_gain:out_gain:delays(ms):decays`.

### Compress dynamic range

```bash
ffmpeg -i input.mp4 -af "acompressor=threshold=-20dB:ratio=4:attack=5:release=50" output.mp4
```

## Silence Detection

Detect silent sections (doesn't modify audio, prints timestamps to stderr):

```bash
ffmpeg -i input.mp4 -af "silencedetect=noise=-30dB:d=0.5" -f null -
```

- `noise=-30dB` — anything quieter than -30 dB counts as silence
- `d=0.5` — must be silent for at least 0.5 seconds to register

Parse the `silence_start` / `silence_end` lines from stderr to find gaps.

## Mix Multiple Audio Tracks

### Mix two sources with custom weights

```bash
ffmpeg -i video.mp4 -i music.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first:weights=1 0.3[a]" \
  -map 0:v -map "[a]" -c:v copy out.mp4
```

- `weights=1 0.3` — main audio at 100%, music bed at 30%
- `duration=first` — output length matches the first input (avoids padding the video)

### Merge stereo from two mono tracks

```bash
ffmpeg -i left.wav -i right.wav \
  -filter_complex "[0:a][1:a]amerge=inputs=2[a]" \
  -map "[a]" -ac 2 output.wav
```
