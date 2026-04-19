# Qwen3-TTS Speakers and Tones

The Qwen3-TTS model supports nine preset speakers and eight tonal modes, plus voice cloning from a reference recording.

## Speakers

| Speaker | Gender | Character |
|---|---|---|
| `Ryan` | Male | Warm, corporate — default for product demos |
| `Aiden` | Male | Younger, energetic |
| `Vivian` | Female | Professional, clear enunciation |
| `Serena` | Female | Calm, storyteller |
| `Uncle_Fu` | Male | Older, authoritative |
| `Dylan` | Male | Casual, conversational |
| `Eric` | Male | News-anchor style |
| `Ono_Anna` | Female | Japanese accent (English speech) |
| `Sohee` | Female | Korean accent (English speech) |

## Tones

| Tone | Use case |
|---|---|
| `neutral` | Default, no particular emotional shading |
| `warm` | Friendly product intros, welcome messages |
| `professional` | B2B, enterprise-facing content |
| `excited` | Feature launches, announcements |
| `calm` | Meditation, educational, long-form |
| `serious` | Security, compliance, trust content |
| `storyteller` | Narrative-driven pieces |
| `tutorial` | Step-by-step instruction |

## Usage

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit

python3 tools/qwen3_tts.py \
  --text "Welcome to the product tour." \
  --speaker Ryan --tone warm \
  --output projects/PROJECT_NAME/public/audio/scenes/01.mp3 \
  --cloud modal --progress json
```

## Voice Cloning

Needs a reference recording (ideally 10-30 seconds of clean speech) and an exact transcript.

```bash
python3 tools/qwen3_tts.py \
  --text "Text to speak with the cloned voice." \
  --ref-audio assets/voices/reference.m4a \
  --ref-text "Exact transcript of the reference audio" \
  --output projects/PROJECT_NAME/public/audio/scenes/01.mp3 \
  --cloud modal --progress json
```

### Reference recording tips

- Mono or stereo, any common format (.mp3, .m4a, .wav)
- Clean environment — no background music, no room echo
- 10-30 seconds is the sweet spot (longer doesn't help much)
- `--ref-text` MUST exactly match what's said — typos hurt quality
- Consistent emotional tone with your target output works best
