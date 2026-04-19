# 03 — Generate Assets

Produce background music, per-scene voiceover, scene images, and optional b-roll / narrator clips.

**CRITICAL: All commands below MUST be run from the toolkit root, not the project directory.**

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
```

**CRITICAL: Every command includes `--progress json`.** See `06-progress-polling.md` for the reporting format.

## 3a. Background Music

Default provider is **acemusic** (cloud API, free key, best quality). Falls back to Modal/RunPod for self-hosted.

```bash
# Using acemusic (default — XL Turbo 4B model)
python3 tools/music_gen.py \
  --preset corporate-bg \
  --duration 90 \
  --output projects/PROJECT_NAME/public/audio/bg-music.mp3 \
  --progress json

# Custom prompt
python3 tools/music_gen.py \
  --prompt "Subtle ambient tech, soft synth pads" \
  --duration 90 \
  --output projects/PROJECT_NAME/public/audio/bg-music.mp3 \
  --progress json

# Fall back to Modal if no acemusic key
python3 tools/music_gen.py \
  --preset corporate-bg \
  --duration 90 \
  --output projects/PROJECT_NAME/public/audio/bg-music.mp3 \
  --cloud modal --progress json
```

**Presets:** `corporate-bg`, `upbeat-tech`, `ambient`, `dramatic`, `tension`, `hopeful`, `cta`, `lofi`

**Setup:** `echo "ACEMUSIC_API_KEY=your_key" >> .env` (free key at acemusic.ai/api-key).

## 3b. Voiceover (per-scene)

Generate ONE .mp3 file PER SCENE. **Do NOT generate a single voiceover file.**

```bash
# Scene 01
python3 tools/qwen3_tts.py \
  --text "The voiceover text for scene one." \
  --speaker Ryan --tone warm \
  --output projects/PROJECT_NAME/public/audio/scenes/01.mp3 \
  --cloud modal --progress json

# Scene 02
python3 tools/qwen3_tts.py \
  --text "The voiceover text for scene two." \
  --speaker Ryan --tone warm \
  --output projects/PROJECT_NAME/public/audio/scenes/02.mp3 \
  --cloud modal --progress json

# ... repeat for each scene
```

See `../references/speakers-tones.md` for the full speaker + tone matrix and voice cloning.

## 3c. Scene Images

### Text prompt

```bash
python3 tools/flux2.py \
  --prompt "Dark tech background with blue geometric grid, cinematic lighting" \
  --width 1920 --height 1080 \
  --output projects/PROJECT_NAME/public/images/title-bg.png \
  --cloud modal --progress json
```

### Preset

```bash
python3 tools/flux2.py \
  --preset title-bg \
  --output projects/PROJECT_NAME/public/images/title-bg.png \
  --cloud modal --progress json
```

**Image presets:** `title-bg`, `problem`, `solution`, `demo-bg`, `stats-bg`, `cta`, `thumbnail`, `portrait-bg`

## 3d. Video Clips — B-Roll & Animated Backgrounds (optional)

```bash
# B-roll from text
python3 tools/ltx2.py \
  --prompt "Aerial drone shot over a European city at golden hour" \
  --output projects/PROJECT_NAME/public/videos/broll-europe.mp4 \
  --cloud modal --progress json

# Animate a slide/screenshot (image-to-video)
python3 tools/ltx2.py \
  --prompt "Gentle particle effects, soft ambient light shifts, slight camera drift" \
  --input projects/PROJECT_NAME/public/images/title-bg.png \
  --output projects/PROJECT_NAME/public/videos/animated-title.mp4 \
  --cloud modal --progress json
```

Use in Remotion with `<OffthreadVideo>`:

```tsx
<OffthreadVideo src={staticFile('videos/broll-europe.mp4')} />
```

See `../references/ltx2-rules.md` for LTX-2 constraints, seeds, and style-drift prevention.

## 3e. Talking-Head Narrator (optional)

Generate a presenter portrait, then animate per-scene clips:

```bash
# 1. Generate portrait
python3 tools/flux2.py \
  --prompt "Professional presenter portrait, clean style, dark background, facing camera, upper body" \
  --width 1024 --height 576 \
  --output projects/PROJECT_NAME/public/images/presenter.png \
  --cloud modal --progress json

# 2. Per-scene narrator clips (one per scene)
python3 tools/sadtalker.py \
  --image projects/PROJECT_NAME/public/images/presenter.png \
  --audio projects/PROJECT_NAME/public/audio/scenes/01.mp3 \
  --preprocess full --still --expression-scale 0.8 \
  --output projects/PROJECT_NAME/public/narrator-01.mp4 \
  --cloud modal --progress json

# Repeat for each scene that needs a narrator
```

**SadTalker rules — follow exactly:**

- **ALWAYS** use `--preprocess full` (default `crop` outputs a square, wrong aspect ratio)
- **ALWAYS** use `--still` (reduces head movement, looks professional)
- **ALWAYS** generate per-scene clips (6-15s each), NEVER one long video
- Processing: ~3-4 min per 10s of audio on Modal A10G
- `--expression-scale 0.8` keeps expressions subtle (range 0.0-1.5)

## 3f. Image Editing (optional)

Create scene variants from existing images:

```bash
python3 tools/image_edit.py \
  --input projects/PROJECT_NAME/public/images/title-bg.png \
  --prompt "Make it darker with red tones, more ominous" \
  --output projects/PROJECT_NAME/public/images/problem-bg.png \
  --cloud modal --progress json
```

## 3g. Upscaling (optional)

```bash
python3 tools/upscale.py \
  --input projects/PROJECT_NAME/public/images/some-image.png \
  --output projects/PROJECT_NAME/public/images/some-image-4x.png \
  --scale 4 --cloud modal --progress json
```

## Next

For visually continuous video sequences across multiple scenes, move to `04-chain-video.md`. Otherwise go to `05-sync-and-render.md`.
