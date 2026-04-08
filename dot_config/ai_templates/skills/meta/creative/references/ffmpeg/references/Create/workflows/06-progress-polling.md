# 06 — Progress Polling Pattern

The canonical pattern for running long cloud GPU tasks while reporting live progress to the user.

## The Problem

Your agent run **ends when you finish responding**. If you start a long-running command with `bash background:true` and promise to "monitor", you lose control the moment your turn ends. The user sees silence until they nudge you. Breaking a batch into per-scene tool calls across separate messages has the same problem — the run ends between calls, the sequence stalls.

## The Solution

Use `exec` with `yieldMs` + `--progress json` output + `process action:poll`. This keeps you in the loop so you can relay structured progress every 10 seconds.

## The Loop

```
1. exec command:"cd TOOLKIT && python3 tools/X.py ... --progress json" yieldMs:10000
2. yieldMs:10000 returns control to you every 10 seconds
3. Read the stderr JSON Lines — look for "stage":"item" (scene complete) or "stage":"complete" (all done)
4. Report progress to the user ("Scene 05/30 complete, 17%")
5. process action:poll sessionId:<id>
6. Repeat step 3-5 until "stage":"complete"
```

## Tools That Support `--progress json`

`music_gen.py`, `qwen3_tts.py`, `flux2.py`, `upscale.py`, `sadtalker.py`, `image_edit.py`, `dewatermark.py`, `ltx2.py`, `chain_video.py`

## Output Format

Each line on stderr is a JSON object:

```json
{"ts":"14:23:15","stage":"submit","msg":"Sending to acemusic.ai (XL Turbo 4B, thinking: on)...","pct":null,"elapsed":0.0}
{"ts":"14:23:30","stage":"waiting","msg":"Waiting for acemusic.ai response... (15s)","pct":null,"elapsed":15.0}
{"ts":"14:23:45","stage":"waiting","msg":"Waiting for acemusic.ai response... (30s)","pct":null,"elapsed":30.0}
{"ts":"14:24:02","stage":"complete","msg":"Saved: bg-music.mp3 (245 KB, 60.1s)","pct":100,"elapsed":47.3}
```

## Stage Catalogue

| Stage | Meaning |
|---|---|
| `submit` | Job sent to provider |
| `queue` | RunPod: waiting for GPU |
| `processing` | RunPod: GPU processing |
| `waiting` | Heartbeat during synchronous calls (acemusic, Modal) |
| `complete` | Job finished successfully |
| `error` | Something failed — check `msg` for details |
| `item` | Multi-item progress (e.g., scene 3/7) — `pct` is populated |
| `cost` | Estimated cost for the operation |

## Behaviour by Provider

- **acemusic**: `submit` → periodic `waiting` heartbeats every 15s → `complete`
- **RunPod**: `submit` → `queue` → `processing` → `complete` (on each poll)
- **Modal**: `submit` → periodic `waiting` heartbeats → `complete`

Default mode (`--progress human`) shows the same events as colored terminal output.

## Full Example: Chain Video with Live Progress

```
exec command:"cd ~/.openclaw/workspace/claude-code-video-toolkit && python3 tools/chain_video.py --scenes-dir projects/myproject/public/images/scenes/ --output-dir projects/myproject/public/videos/chain/ --prompts-file projects/myproject/scenes.json --negative-prompt 'anime, manga, asian, cartoon' --progress json" yieldMs:10000
```

Then on each yield, parse the newest JSON Lines emitted, pick out `stage` + `msg` + `pct`, and report something like:

> Scene 07/30 complete (23%), currently processing scene 08...

Then `process action:poll sessionId:<id>` and repeat until `"stage":"complete"`.

## Anti-Patterns — NEVER Do These

- ❌ `bash background:true` followed by a promise to "check back" — you can't, your run ends
- ❌ Breaking a batch into individual tool calls across messages — the run ends between them
- ❌ Saying "I'll continue autonomously" — literally impossible without an external trigger
- ❌ Polling without `--progress json` — you have no visibility into what's actually happening
