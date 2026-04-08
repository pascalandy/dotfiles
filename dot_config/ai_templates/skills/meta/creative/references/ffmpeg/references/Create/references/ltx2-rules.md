# LTX-2 Rules and Constraints

LTX-2 is the toolkit's AI video generation model (A100-80GB on Modal). It produces short clips from text prompts or image+text (image-to-video).

## Hard Constraints

| Constraint | Value |
|---|---|
| Max clip length | ~8 seconds (193 frames at 24fps) |
| Default clip length | ~5 seconds (121 frames) |
| Width / height divisibility | Must be divisible by 64 |
| Default resolution | 768 × 512 |
| Cold start | 60-90 seconds |
| Warm GPU generation | ~2.5 minutes per 5s clip |
| Cost | ~$0.20-0.25 per clip |
| Generated audio | Ambient only — use voiceover/music tools for speech and music |

## Training Data Contamination (the big one)

**~30% of generations may have training data artifacts.** Common issues:
- Anime / manga style drift
- Asian urban aesthetics leaking into unrelated scenes
- Watermarks or logos appearing in corners
- Small text artifacts

## Prevention Strategy

### 1. Always use negative prompts

```bash
python3 tools/ltx2.py \
  --prompt "Aerial drone shot over Irish coastline, cinematic wide angle" \
  --negative-prompt "anime, manga, asian, cartoon, illustration, watermark, text, logo" \
  --output output.mp4 \
  --cloud modal --progress json
```

### 2. Include strong style anchors in prompts

**Weak:** `"beautiful landscape, cinematic"`
**Strong:** `"Irish landscape, Celtic knotwork borders, oil painting style, golden hour lighting"`

The more specific the visual language, the less the model drifts.

### 3. Re-roll with `--seed`

If a clip has artifacts, re-run with a different seed:

```bash
python3 tools/ltx2.py \
  --prompt "..." \
  --seed 42 \
  --output output.mp4 \
  --cloud modal --progress json
```

## Chained Sequences

See `../workflows/04-chain-video.md` for the full chained-video workflow. Key rules:

1. **ALWAYS use `--prompts-file`** with per-scene prompts. A single generic prompt will drift toward anime within 5-10 scenes.
2. **ALWAYS add `--negative-prompt`** — same list as above.
3. Each per-scene prompt should include the overall style anchor so continuity isn't lost between scenes.

## Image-to-Video Mode

Animate an existing image (slide, screenshot, FLUX-generated background):

```bash
python3 tools/ltx2.py \
  --prompt "Gentle particle effects, soft light shifts, subtle camera drift" \
  --input projects/PROJECT_NAME/public/images/title-bg.png \
  --output projects/PROJECT_NAME/public/videos/animated-title.mp4 \
  --cloud modal --progress json
```

This is typically **more reliable** than pure text-to-video because the input image locks in the style.

## Remotion Integration

Use `<OffthreadVideo>` in the composition, **never `<video>`**:

```tsx
<OffthreadVideo
  src={staticFile('videos/broll-europe.mp4')}
  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
/>
```
