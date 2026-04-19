# 04 — Chained Video Sequences

Generate a sequence of video clips where each scene flows from the last frame of the previous one. **Runs as a single command — no manual nudging between scenes.**

## Basic Usage

### Chain scenes 1-30 from a directory of FLUX images

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit

python3 tools/chain_video.py \
  --scenes-dir projects/PROJECT_NAME/public/images/scenes/ \
  --output-dir projects/PROJECT_NAME/public/videos/chain/ \
  --prompt "Cinematic continuation, flowing transition" \
  --start 1 --end 30 \
  --progress json
```

### Resume from a specific scene (skips existing files)

```bash
python3 tools/chain_video.py \
  --scenes-dir projects/PROJECT_NAME/public/images/scenes/ \
  --output-dir projects/PROJECT_NAME/public/videos/chain/ \
  --start 10 --end 30 \
  --progress json
```

### Per-scene prompts from a JSON file

```bash
python3 tools/chain_video.py \
  --scenes-dir projects/PROJECT_NAME/public/images/scenes/ \
  --output-dir projects/PROJECT_NAME/public/videos/chain/ \
  --prompts-file projects/PROJECT_NAME/scenes.json \
  --progress json
```

### Chain from an existing clip (no scene images needed)

```bash
python3 tools/chain_video.py \
  --first-clip output/chain-04.mp4 \
  --output-dir output/ \
  --start 5 --end 30 \
  --prompt "Celtic mythology, flowing transition" \
  --progress json
```

## Prompts File Format

`scenes.json`:

```json
{
  "1": "Ancient stone circle at dawn",
  "2": "Celtic spirals emerge from stone",
  "3": "Portal opens with golden light"
}
```

## Chain Rules

- Extracts last frame from scene N, feeds as `--input` to scene N+1 via LTX-2
- Skips scenes already on disk (safe to resume)
- Falls back to scene images from `--scenes-dir` if chaining fails
- Use `--prefix` to set output filename prefix (default: `chain`)
- ~2.5 min per scene, ~$0.20-0.25 per clip
- Extra args (e.g. `--negative-prompt`, `--seed`) pass through to `ltx2.py`

## CRITICAL: Style Drift Prevention

**LTX-2 has ~30% training data contamination (anime / Asian aesthetic).** Generic prompts like "cinematic transition" will drift toward anime within 5-10 chained scenes. To prevent this:

1. **ALWAYS use `--prompts-file`** with specific per-scene prompts — never a single generic prompt for the whole chain
2. **ALWAYS add `--negative-prompt`** to exclude unwanted styles:

   ```
   --negative-prompt "anime, manga, asian, cartoon, illustration, watermark, text, logo"
   ```

3. Each per-scene prompt should include **strong style anchors** (e.g. "Irish landscape, Celtic knotwork, oil painting style") not just subject descriptions

## CRITICAL: Run with `yieldMs` for Live Progress

**Don't break it into per-scene tool calls.** Your agent run ends between calls and the sequence stalls. Instead, use `exec` with `yieldMs` so you stay in the loop and can relay progress:

```
exec command:"cd ~/.openclaw/workspace/claude-code-video-toolkit && python3 tools/chain_video.py --scenes-dir /path/to/images/ --output-dir /path/to/output/ --prompts-file scenes.json --progress json" yieldMs:10000
```

### How the loop works

1. `yieldMs:10000` returns control every 10 seconds
2. Read `--progress json` output (JSON Lines on stderr with stage/pct/msg)
3. Report progress to the user ("Scene 05/30 complete, 17%")
4. Poll again: `process action:poll sessionId:<id>`
5. Repeat until `"stage":"complete"` appears

**This is the correct pattern for ALL long-running tool commands** (chain_video, batch flux, batch sadtalker, etc.). Full details in `06-progress-polling.md`.
