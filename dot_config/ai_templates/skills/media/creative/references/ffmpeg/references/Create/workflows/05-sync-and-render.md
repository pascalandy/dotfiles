# 05 — Sync Timing and Render

Refine scene durations to match the actual audio, spot-check still frames, then render the video.

## Step 1: Sync Timing

**ALWAYS do this after generating voiceover.** Audio duration differs from initial word-count estimates.

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit

for f in projects/PROJECT_NAME/public/audio/scenes/*.mp3; do
  echo "$(basename $f): $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")s"
done
```

Update each scene's `durationSeconds` in `demo-config.ts` to:

```
durationSeconds = ceil(actual_audio_duration + 2)
```

**Example:** if `01.mp3` is 6.8s, set scene 1 `durationSeconds` to `9` (ceil(6.8 + 2) = 9).

The `+ 2` budget:
- 1s delay before audio starts (`<Sequence from={30}>` at 30fps)
- 1s trailing padding so the next scene doesn't clip the last word

## Step 2: Review Still Frames

Generate still images at specific frames and inspect them before rendering the full video:

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit/projects/PROJECT_NAME

npx remotion still src/index.ts ProductDemo --frame=100 --output=/tmp/review-scene1.png
npx remotion still src/index.ts ProductDemo --frame=400 --output=/tmp/review-scene2.png
```

**Check for:**

- Text truncation (headlines, bullet lists)
- Animation timing (entrance / exit frames)
- Narrator PiP positioning and size
- Background contrast vs foreground text
- Logo / watermark placement

Pick frames strategically: one near the start of each scene where the layout is fully visible.

## Step 3: Render

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit/projects/PROJECT_NAME
npm run render
```

**Output:** `out/ProductDemo.mp4`

## If Render Fails

| Problem | Solution |
|---|---|
| "Cannot find module" | Check import paths use `../../../lib/` relative paths for custom transitions |
| Transition imports fail | Import from `lib/transitions/presentations/` directly, **NEVER from the `lib/transitions` barrel** |
| Video component not rendering | Must use `<OffthreadVideo>`, not `<video>`. Remotion needs frame-accurate playback |
| Audio missing from one scene | Check `from={30}` Sequence wrapper is present and audio file path is correct |
| Background music too loud | Reduce `backgroundMusicVolume` in `demo-config.ts` (typical: 0.08-0.15) |

## Quality Checklist Before Shipping

- [ ] All scenes have full audio playback (no clipping at end)
- [ ] Title card is readable at thumbnail size
- [ ] No text overflow on any scene
- [ ] Narrator face is centered and non-distracting
- [ ] Background music sits under voiceover (not competing)
- [ ] CTA scene has clear next-action for the viewer
- [ ] Transitions are smooth (no jarring cuts)
