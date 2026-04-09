---
name: ffmpeg-create
description: Create professional explainer, demo, and marketing videos autonomously using the claude-code-video-toolkit — AI voiceover (Qwen3-TTS), image generation (FLUX.2), music (acemusic / ACE-Step), talking-head animation (SadTalker), AI video clips (LTX-2), composed and rendered with Remotion. USE WHEN the user wants to create a video from a text brief, build an explainer, produce a product demo, generate AI voiceover, add a talking-head narrator, make a marketing video, or orchestrate cloud GPU video production.
---

# Create — AI Video Production Pipeline

Create professional videos from a text brief. The toolkit uses open-source AI models on cloud GPUs (Modal or RunPod) for voiceover, image generation, music, and talking-head animation. Remotion (React) handles composition and rendering.

## Three Critical Rules

**These rules are load-bearing. Breaking any one of them will cause the pipeline to fail or stall.**

### 1. Toolkit Path — ALWAYS `cd` first

The toolkit lives at a fixed path. **ALWAYS `cd` here before running any tool command.**

```bash
TOOLKIT=~/.openclaw/workspace/claude-code-video-toolkit
cd $TOOLKIT
```

**NEVER run tool commands from inside a project directory.** Tools resolve paths relative to the toolkit root.

### 2. Progress Reporting — ALWAYS `--progress json`

**Add `--progress json` to every cloud GPU tool command.** This gives structured JSON Lines on stderr so you can monitor job status, detect stuck jobs, and report progress in real-time.

```bash
# CORRECT
python3 tools/music_gen.py --preset corporate-bg --duration 60 --output bg.mp3 --progress json

# WRONG — no visibility
python3 tools/music_gen.py --preset corporate-bg --duration 60 --output bg.mp3
```

Tools that support `--progress json`: `music_gen.py`, `qwen3_tts.py`, `flux2.py`, `upscale.py`, `sadtalker.py`, `image_edit.py`, `dewatermark.py`, `ltx2.py`, `chain_video.py`.

See `workflows/06-progress-polling.md` for the output format and stage definitions.

### 3. Long-Running Tasks — `yieldMs`, NEVER `background:true`

**Any command taking more than 30 seconds MUST use `exec` with `yieldMs` so you can report progress live.** This includes: batch FLUX generation, chain_video, SadTalker, music generation, and any multi-scene pipeline.

```
exec command:"cd ~/.openclaw/workspace/claude-code-video-toolkit && python3 tools/chain_video.py --output-dir /path/ --progress json ..." yieldMs:10000
```

**NEVER do this:**
- `bash background:true` then promise to "monitor" — your agent run ends, you lose control
- Break a batch into per-scene tool calls across separate messages — the run ends between calls, sequence stalls
- Promise to "continue autonomously" — you literally cannot without an external trigger

See `workflows/06-progress-polling.md` for the full polling loop pattern.

## Workflow Routing

Read workflow files in order for a full pipeline, or jump to a specific phase:

| Phase | File | What it does |
|---|---|---|
| 1 | `workflows/01-setup.md` | Verify toolkit, install deps, configure Modal endpoints in `.env` |
| 2 | `workflows/02-project-init.md` | Copy template, write `demo-config.ts`, write `VOICEOVER-SCRIPT.md` |
| 3 | `workflows/03-generate-assets.md` | Generate music, per-scene voiceover, images, video clips, narrator clips |
| 4 | `workflows/04-chain-video.md` | Chained video sequences (visual continuity across scenes) |
| 5 | `workflows/05-sync-and-render.md` | Sync scene durations to audio, review still frames, run `npm run render` |
| 6 | `workflows/06-progress-polling.md` | The `yieldMs` + `--progress json` + `process poll` loop |

## References

| File | Content |
|---|---|
| `references/scene-types.md` | Scene type catalogue (title, problem, solution, demo, feature, stats, cta) |
| `references/speakers-tones.md` | Qwen3-TTS speaker + tone matrix, voice cloning instructions |
| `references/ltx2-rules.md` | LTX-2 constraints, style drift prevention, chain prompts |
| `references/cost-estimates.md` | Per-tool cost estimates on Modal |

## Composition Patterns

### Per-Scene Audio (1s delay)

```tsx
<Sequence from={30}>
  <Audio src={staticFile('audio/scenes/01.mp3')} volume={1} />
</Sequence>
```

### Per-Scene Narrator PiP

```tsx
<Sequence from={30}>
  <OffthreadVideo
    src={staticFile('narrator-01.mp4')}
    style={{ width: 320, height: 180, objectFit: 'cover' }}
    muted
  />
</Sequence>
```

**ALWAYS use `<OffthreadVideo>`, NEVER `<video>`.** Remotion requires its own component for frame-accurate rendering.

### Transitions

```tsx
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { glitch } from '../../../lib/transitions/presentations/glitch';
import { lightLeak } from '../../../lib/transitions/presentations/light-leak';
```

**NEVER import from `lib/transitions` barrel** — import custom transitions from `lib/transitions/presentations/` directly.

## Error Recovery

| Problem | Solution |
|---|---|
| "No module named..." | Run `pip3 install --break-system-packages -r tools/requirements.txt` from toolkit root |
| "MODAL_*_ENDPOINT_URL not configured" | Check `.env`. Run `python3 tools/verify_setup.py` |
| SadTalker output is square/cropped | Missing `--preprocess full`. Re-run with that flag |
| Audio too short/long for scene | Re-run `workflows/05-sync-and-render.md` timing sync, update config |
| `npm run render` fails | Run from project dir, not toolkit root. `npm install` first |
| "Cannot find module" in Remotion | Check import paths. Custom components use `../../../lib/` |
| Cold start timeout on Modal | First call after idle takes 30-120s. Retry once — second is warm |
| SadTalker client timeout (long audio) | HTTP request times out before Modal finishes. Result is still uploaded to R2 `sadtalker/results/`. List via boto3 with R2 creds from `.env` |
