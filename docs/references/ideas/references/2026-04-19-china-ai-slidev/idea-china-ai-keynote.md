# Idea — China AI Keynote (Slidev)

Turn the Asian Boss / Steven Park transcript on China's AI rise into a
Slidev keynote. Use the three-layer stack (hardware → model → data) as
the spine, with DeepSeek's efficiency story as the pivot between layers
2 and 3.

## Source

- Transcript: `~/Documents/_my_docs/61_transcription_exports_yt/2026_04_19_11h30_Why_Chinese_AI_Is_Suddenly_So_Good_ft_DeepSeek_See_MIudp4xv7Io/follow_along_note.md`
- Related idea: [[2026-04-19-china-ai-stack]]

## Keynote

- Project: `~/Documents/_my_docs/61_transcription_exports_yt/2026_04_19_11h30_Why_Chinese_AI_Is_Suddenly_So_Good_ft_DeepSeek_See_MIudp4xv7Io/slidev/`
- Theme: `seriph`
- Entry file: `slides.md`
- Ran `pnpm install` + `pnpm exec slidev build` → builds clean.

## Spine

1. AlphaGo wake-up call (2016 Seoul, Move 37, 4–1 result)
2. The three-layer stack (mermaid diagram)
3. Hardware — silicon, GPUs, NVIDIA/TSMC chokepoint, export bans
4. Model — transformer, LLM, DeepSeek's MoE + MLA + PTX, open source
5. Training — Western hybrid vs DeepSeek's RL-first + language mixing
6. Data — Sputnik moment, US data wall, ByteDance / Douyin engine, Cdance vs Sora
7. Next frontier — agents + robots, off-internet human data
8. Takeaways + glossary (split across two slides)

## Run

```bash
cd ~/Documents/_my_docs/61_transcription_exports_yt/2026_04_19_11h30_Why_Chinese_AI_Is_Suddenly_So_Good_ft_DeepSeek_See_MIudp4xv7Io/slidev
pnpm run dev       # http://localhost:3030
pnpm run build     # static SPA in dist/
pnpm run export    # deck.pdf (playwright-chromium already installed)
```
