# 02 — Project Initialization

Copy a template, write the config, and write the voiceover script.

## Step 1: Create Project

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
cp -r templates/product-demo projects/PROJECT_NAME
cd projects/PROJECT_NAME
npm install
```

Available templates:

- `product-demo` — marketing / explainer
- `sprint-review` — engineering sprint review
- `sprint-review-v2` — composable scenes

## Step 2: Write `demo-config.ts`

Edit `projects/PROJECT_NAME/src/config/demo-config.ts`:

```typescript
export const demoConfig: ProductDemoConfig = {
  product: {
    name: 'My Product',
    tagline: 'What it does in one line',
    website: 'example.com',
  },
  scenes: [
    { type: 'title',    durationSeconds: 9,  content: { headline: '...', subheadline: '...' } },
    { type: 'problem',  durationSeconds: 14, content: { headline: '...', problems: ['...', '...'] } },
    { type: 'solution', durationSeconds: 13, content: { headline: '...', highlights: ['...', '...'] } },
    { type: 'stats',    durationSeconds: 12, content: { stats: [{value: '99%', label: '...'}] } },
    { type: 'cta',      durationSeconds: 10, content: { headline: '...', links: ['...'] } },
  ],
  audio: {
    backgroundMusicFile: 'audio/bg-music.mp3',
    backgroundMusicVolume: 0.12,
  },
};
```

See `../references/scene-types.md` for the full scene type catalogue and content shapes.

### Duration Rule (initial estimate)

```
durationSeconds = ceil(word_count / 2.5) + 2
```

You will refine this in `05-sync-and-render.md` after actual audio is generated.

## Step 3: Write Voiceover Script

Create `projects/PROJECT_NAME/VOICEOVER-SCRIPT.md`:

```markdown
## Scene 1: Title (9s, ~17 words)
Build videos with AI. The product name toolkit makes it easy.

## Scene 2: Problem (14s, ~30 words)
The problem statement goes here. Keep it punchy and relatable.

## Scene 3: Solution (13s, ~27 words)
How your product solves the problem, in plain language.
```

### Word Budget per Scene

```
words = (durationSeconds - 2) * 2.5
```

The `-2` accounts for a 1-second audio delay at the start of each scene + 1 second of trailing padding.

## Next

Move to `03-generate-assets.md` to produce music, voiceover, images, and optional narrator clips.
