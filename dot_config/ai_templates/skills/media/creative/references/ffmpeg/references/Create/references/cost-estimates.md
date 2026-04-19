# Cost Estimates (Modal)

Per-tool cost estimates on Modal's A10G/A100 GPUs. Modal's Starter plan includes $30/month free compute and apps scale to zero when idle.

## Per-Tool Breakdown

| Tool | Typical Cost | Notes |
|---|---|---|
| **Qwen3-TTS** | ~$0.01 per scene | ~20s per scene on warm GPU |
| **FLUX.2** | ~$0.01 per image | ~3s warm, ~30s cold |
| **ACE-Step** (music) | ~$0.02-0.05 | Depends on duration |
| **SadTalker** | ~$0.05-0.20 per scene | ~3-4 min per 10s of audio |
| **Qwen-Edit** (image-edit) | ~$0.03-0.15 | ~8 min cold start (25GB model) |
| **RealESRGAN** (upscale) | ~$0.005 per image | Very fast |
| **LTX-2.3** | ~$0.20-0.25 per clip | ~2.5 min per 5s clip, A100-80GB |

## Per-Project Totals

| Project shape | Total |
|---|---|
| 60s video, 5 scenes, no narrator, no AI video clips | ~$0.10-0.30 |
| 60s video, 5 scenes, narrator in every scene | ~$0.50-1.50 |
| 60s video, 5 scenes, narrator + 2 LTX-2 b-roll clips | ~$1.00-2.50 |
| 60s video, 5 scenes, narrator + 5 chained LTX-2 clips | ~$2.00-3.50 |

## Cost-Saving Tips

- **Reuse generated assets** — music and scene images can be shared across variants
- **Use acemusic instead of self-hosted ACE-Step** for music — it's free with the API key
- **Batch voiceover generation** — cold-start cost is amortized across all scenes in one session
- **Use warm GPUs** — run all FLUX calls in one batch rather than spaced out; second+ calls use a warm container
- **Skip LTX-2 for static scenes** — a still FLUX image with Remotion motion (pan/zoom) is $0.01 vs $0.20 for an animated clip
- **Image-to-video instead of text-to-video** for LTX-2 — more reliable, fewer re-rolls needed

## Watching Costs

Modal has a usage dashboard. Check it mid-pipeline if you're running many tools:

```bash
# Open dashboard
open https://modal.com/apps
```

## Free Tier Math

$30/month free compute gets you approximately:

- **3,000** FLUX images, **or**
- **1,500** TTS scenes (warm), **or**
- **300** SadTalker narrator clips (10s each), **or**
- **120-150** LTX-2 video clips (5s each), **or**
- **~25** complete 60s narrator videos with b-roll

Mix and match based on the project.
