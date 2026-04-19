---
marp: true
theme: default
paginate: true
size: 16:9
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Fira+Code:wght@400;500;700&display=swap');

:root {
  --color-background: #0d1117;
  --color-foreground: #c9d1d9;
  --color-heading: #58a6ff;
  --color-accent: #7ee787;
  --color-code-bg: #161b22;
  --color-border: #30363d;
  --font-default: 'Noto Sans JP', 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif;
  --font-code: 'Fira Code', 'Consolas', 'Monaco', monospace;
}

section {
  background-color: var(--color-background);
  color: var(--color-foreground);
  font-family: var(--font-default);
  font-weight: 400;
  box-sizing: border-box;
  border-left: 4px solid var(--color-accent);
  position: relative;
  line-height: 1.55;
  font-size: 20px;
  padding: 56px;
}

h1, h2, h3, h4, h5, h6 {
  font-weight: 700;
  color: var(--color-heading);
  margin: 0;
  padding: 0;
  font-family: var(--font-code);
}

h1 {
  font-size: 50px;
  line-height: 1.3;
  text-align: left;
}

h1::before {
  content: '# ';
  color: var(--color-accent);
}

h2 {
  font-size: 36px;
  margin-bottom: 28px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--color-border);
}

h2::before {
  content: '## ';
  color: var(--color-accent);
}

h3 {
  color: var(--color-foreground);
  font-size: 24px;
  margin-top: 24px;
  margin-bottom: 10px;
}

h3::before {
  content: '### ';
  color: var(--color-accent);
}

ul, ol {
  padding-left: 30px;
}

li {
  margin-bottom: 8px;
}

li::marker {
  color: var(--color-accent);
}

blockquote {
  border-left: 3px solid var(--color-heading);
  padding: 8px 20px;
  color: #c9d1d9;
  font-style: italic;
  background-color: rgba(88, 166, 255, 0.06);
  margin: 16px 0;
}

pre {
  background-color: var(--color-code-bg);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 16px;
  overflow-x: auto;
  font-family: var(--font-code);
  font-size: 16px;
  line-height: 1.5;
}

code {
  background-color: var(--color-code-bg);
  color: var(--color-accent);
  padding: 2px 6px;
  border-radius: 3px;
  font-family: var(--font-code);
  font-size: 0.9em;
}

pre code {
  background-color: transparent;
  padding: 0;
  color: var(--color-foreground);
}

table {
  border-collapse: collapse;
  margin: 12px 0;
  width: 100%;
}

th, td {
  border: 1px solid var(--color-border);
  padding: 8px 12px;
  text-align: left;
}

th {
  background-color: var(--color-code-bg);
  color: var(--color-heading);
  font-family: var(--font-code);
}

footer {
  font-size: 14px;
  color: #8b949e;
  font-family: var(--font-code);
  position: absolute;
  left: 56px;
  right: 56px;
  bottom: 40px;
  text-align: right;
}

footer::before {
  content: '// ';
  color: var(--color-accent);
}

section::after {
  color: #8b949e;
  font-family: var(--font-code);
  font-size: 14px;
}

section.lead {
  border-left: 4px solid var(--color-accent);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

section.lead h1 {
  margin-bottom: 24px;
}

section.lead p {
  font-size: 22px;
  color: var(--color-foreground);
  font-family: var(--font-code);
}

section.section-divider {
  justify-content: center;
}

section.section-divider h1 {
  font-size: 64px;
  border: none;
}

strong {
  color: var(--color-accent);
  font-weight: 700;
}

em {
  color: #f0883e;
  font-style: normal;
}
</style>

<!-- _class: lead -->
<!-- _paginate: false -->

# How China Caught Up in the AI Race

The full stack — hardware, model, data.
From AlphaGo (2016) to DeepSeek & ByteDance (2026).

*Based on Steven Park / Asian Boss*

---

## Agenda

- **Layer 0** — why Seoul 2016 mattered
- **Layer 1** — hardware & the TSMC chokepoint
- **Layer 2** — models: transformer → DeepSeek
- **Layer 3** — applications & the data wall
- Where the race goes next

---

<!-- _class: section-divider -->

# Layer 0
## The Wake-Up Call

---

## Seoul, March 2016

- **AlphaGo** (DeepMind) vs **Lee Sedol**, 18-time world champion
- Go: ~2,500 years old, more board states than atoms in the observable universe
- Consensus before the match: machines can't win yet
- Final result: **4 – 1** to AlphaGo
- Demis Hassabis and Sergey Brin flew in personally

---

## Move 37

- Game 2, midway through — AlphaGo plays a stone *no top human would play*
- Commentators confused; Lee Sedol leaves the room ~15 min
- Not an error — a strategy **no human had considered in 2,000+ years**
- Lee's "divine move" in Game 4 was his only counter

> "A machine had revealed an entirely new strategy that no human had even considered in more than 2,000 years."

---

## China's Response

- What the West saw as a cool algorithm milestone
- What **Beijing** saw: a geopolitical alarm bell
- **2017** — *Next Generation AI Development Plan*
- Explicit national goal: **world leader in AI by 2030**

The race officially starts here.

---

## The Stack Model

AI is not a single technology — it is a **stack**:

| Layer | What it is | What matters |
|---|---|---|
| **3 — Application** | Consumer apps & data | Who owns training data |
| **2 — Model** | Foundation models (the "brain") | Architecture & efficiency |
| **1 — Hardware** | Chips, GPUs, data centers | Who can manufacture |

The US-China rivalry is playing out on **all three** simultaneously.

---

<!-- _class: section-divider -->

# Layer 1
## Hardware

---

## GPUs — The AI Engine

- Silicon chip, thousands of parallel cores etched in
- Originally: video game graphics — shadows, reflections, 3D
- Same parallel math = ideal for AI training/inference
- A top-tier GPU runs **10¹¹–10¹²** operations *per fraction of a second*

```
Blackwell B200     →  208B transistors, two dies stitched together
Rubin (Jan 2026)   →  next-gen NVIDIA architecture
Price              →  $30,000 – $40,000 / GPU
Training GPT-class →  tens of thousands of GPUs, multi-$B data centers
```

---

## The Chokepoint

- **NVIDIA** (~$4.5T, Mar 2026) *designs* the chips
- **TSMC** (Taiwan) *manufactures* them
- TSMC controls **~70%** of global chip fab
- TSMC controls **>90%** of advanced AI chip fab
- TSMC's tools rely on US software, patents, machinery
- Under US law: no advanced AI chips to China — period

Break the rule → US cuts off TSMC's tooling → TSMC dies.

---

## Why China Can't Replicate TSMC

- Arguably **the most complex physical process in human history**
- Decades of accumulated engineering know-how
- **$200M** EUV laser machines — from the Netherlands (ASML)
- Ultra-pure chemicals — from Japan
- Even **Samsung**, with billions in, can't match TSMC's yields
- Elon Musk announced **Project TerraFab** — Tesla's own fab — because third-party supply cannot meet demand

Western consensus in 2023: *China's AI is dead in the water.*
They were wrong about one thing: **software**.

---

<!-- _class: section-divider -->

# Layer 2
## Models

---

## The Transformer (2017)

American researchers invent a new architecture.

**Before:** process text word-by-word, left-to-right. Long sentences → model forgets earlier context.

**After:** look at the entire block *at once*. Draw invisible mathematical connections between every concept. **Never lose context.**

Apply it to massive human-text corpora → **Large Language Model (LLM)**.

---

## LLM = Ultimate Autocomplete

> "At its core, the structure of an LLM is basically playing the ultimate game of guess the next word."

- Smartphone autocomplete: predicts one word
- LLM: predicts with *full* context, trained on grammar, logic, physics, math, the whole internet
- Prediction starts to resemble **reasoning**
- **App vs model**: *ChatGPT* is the app — *GPT 5.4* is the brain

---

## DeepSeek — The Constraint

- **Banned** from buying top-tier NVIDIA chips
- Forced to work with *older, stockpiled* GPUs
- Became **obsessed with efficiency**

Two fundamental breakthroughs follow.

---

## Breakthrough 1a — Extreme MoE

**Mixture of Experts**: cluster of neurons specializing in specific patterns.

- **Dense models** — entire brain lights up for every query → enormous GPU cost
- **OpenAI-era MoE** — a few large expert clusters
- **DeepSeek** — took it to the extreme:

```
256 hyper-specialized experts
  ↓
Router activates only 8 per query
  ↓
The other 248 stay asleep
```

---

## Breakthrough 1b — MLA

**Multi-Head Latent Attention** — DeepSeek's invention.

- The key-value cache = AI's short-term memory
- Normally consumes massive GPU power
- MLA is **extreme memory compression**:

```
Memory footprint   →  reduced by >90%
Context tracking   →  preserved
Net effect         →  the same reasoning on a fraction of the RAM
```

---

## Breakthrough 2 — PTX under CUDA

Most AI companies write against **CUDA** — NVIDIA's standard runtime.

> "CUDA is the automatic transmission of AI development."

DeepSeek went one layer deeper: **PTX (Parallel Thread Execution)** — the assembly layer inside CUDA.

- Hand-tuned low-level code
- Forced *older* chips to talk and compute far more efficiently than NVIDIA's default
- Equivalent to **switching from automatic to manual transmission**

---

## Could American Labs Do This?

**Yes.** OpenAI, Anthropic, NVIDIA all optimize at low levels.

The difference is **necessity**:

- Unlimited budget + unlimited chips → *buy more hardware* is faster
- Capped chips + capped budget → *optimize the silicon you have*

DeepSeek had no choice.

---

## The Result

| Metric | OpenAI (GPT-class) | DeepSeek |
|---|---|---|
| Training cost | **Hundreds of $M** | **< $6M** reported |
| Hardware tier | Latest NVIDIA | Older NVIDIA stock |
| Release model | Closed | **Open source** |

A world-class model for ~**1–2%** of the budget.

---

## Open Source as Distribution

- Weights + architecture published
- Anyone can run, fine-tune, extend
- The world **learned** the 256-expert + MLA design from the release itself
- Direct opposite of OpenAI's closed approach

> "DeepSeek turned its model into a platform and started handing out the secret recipe."

Progress no longer depends on one company.

---

## Training Philosophy

**Western approach** — hybrid, expensive:
- Armies of annotators, researchers, domain specialists
- Premium hand-crafted step-by-step data
- Reinforcement learning layered on top

**DeepSeek** — RL-first, out of necessity:
- Generate many answers, score them, reward correct/clear/useful
- Penalize wrong/sloppy/inconsistent
- Model learns like a person solving problems repeatedly

---

## The Language-Mixing Problem

Pure RL worked *too* literally.

- Brilliant at logic, math, coding
- **Terrible** at talking to humans
- It stopped caring how it sounded

> "It basically turned into a genius mathematician who mumbles to himself."

**Fix:** small dose of expensive human-labeled data to teach formatting.
Reasoning core built for a fraction of the cost.

---

<!-- _class: section-divider -->

# Layer 3
## Applications & Data

---

## The Sputnik Moment

DeepSeek's open-source release ≈ **Sputnik 1957**.

- 1957 — USSR launches the first satellite; US stunned
- 2025 — DeepSeek ships a competitive model at ~1% cost, open weights
- Same shockwave pattern: *"a rival is catching up via a completely different path"*

The US AI industry realizes the real fight is somewhere else.

---

## The Multimodal Data Wall

LLMs are hitting a ceiling — **language alone isn't enough**.

> "A language model is a brain trapped in a dark room that only knows how to read. A multimodal model has been given eyes and ears."

US position in 2026:
- Early models trained by **scraping the open internet** (often illegally)
- **Essentially out** of high-quality multimodal data
- Copyright lawsuits, privacy walls, compressed/fragmented feeds
- Elon Musk: fallback will be **synthetic data** (AI training AI)

---

## China's Structural Advantage

**ByteDance** — parent of Douyin (CN TikTok) + TikTok.

- Hundreds of millions of daily ultra-HD uploads
- Owns the **native uncompressed** video on its servers
- Perfectly paired with user engagement metrics:
  - camera angle, lighting, exact millisecond of swipe

> "A perfectly labeled, infinitely growing database that exists entirely behind the Chinese internet wall."

---

## Cdance 2.0 vs Sora

- **Cdance 2.0** (ByteDance) outperforms **OpenAI's Sora**
- Sora: physical inconsistency, bad audio sync, visual hallucinations
- OpenAI hit the legal-multimodal ceiling; ByteDance didn't

**Natural motion synthesis** — when Cdance renders a person walking through a puddle: the water splashes right, reflections match, audio syncs to the frame.

**DuoBao** (ByteDance's chatbot) is now #1 in China — surpassed DeepSeek by plugging into that data engine.

---

## China's Counter-Wall

The flip side nobody mentions:

- Chinese AI has no clean access to Western multimodal data
- Douyin alone can't teach a model **Western culture, cityscapes, physics**
- Same wall — just from the opposite direction

> "The AI race is far from over. It's just shifting to a new battlefield."

---

## Beyond the Internet

The speaker's bet: the most valuable **future** data is not on the internet.

Next frontiers:
- **AI agents** acting in real systems
- **Physical robots** operating in real environments
- **Real human context** — conversations, intent, ambiguity

> "If the future of AI requires understanding real human beings, the most valuable data won't come from scraping websites. It'll come from actually talking to people."

---

## Takeaways

1. AI is a **3-layer stack** — hardware, model, data
2. US owns the **hardware chokepoint** via NVIDIA + TSMC + export bans
3. China compensated with **software** — MoE, MLA, PTX optimization
4. DeepSeek: world-class model at **< $6M**, fully **open source**
5. China's structural edge is **multimodal data** (Douyin, ByteDance)
6. **Both sides** face data walls — just from opposite ends
7. The next battlefield is **real-world data** that doesn't exist online yet

---

## Key Terms (1/2)

- **Transformer** — attention across the whole block; 2017 breakthrough
- **LLM** — transformer trained on massive text; predicts next token
- **GPU** — thousands of parallel cores; AI's workhorse
- **Semiconductor** — silicon switching on/off → binary
- **MoE** — divide model into expert clusters; activate only relevant ones
- **MLA** — DeepSeek's >90% memory compression for KV cache
- **CUDA** — NVIDIA's runtime; standard AI software interface
- **PTX** — assembly layer inside CUDA; low-level optimization path

---

## Key Terms (2/2)

- **Key-Value Cache** — AI's short-term memory during a conversation
- **Multimodal Data** — text + image + audio + video combined
- **Synthetic Data** — AI-generated training data
- **Reinforcement Learning** — reward correct outputs, penalize bad ones
- **Natural Motion Synthesis** — physically consistent video generation
- **Sputnik Moment** — rival advances unexpectedly via a different path
- **Foundation Model** — the brain (e.g. GPT 5.4) behind an app (ChatGPT)
- **Open Source** — weights + architecture publicly available

---

<!-- _class: lead -->
<!-- _paginate: false -->

# End.

The stack is the game. Each layer has its own battle.

*Source: Asian Boss / Steven Park — MIudp4xv7Io*
