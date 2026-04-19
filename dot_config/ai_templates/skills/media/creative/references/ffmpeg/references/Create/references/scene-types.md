# Scene Types Reference

The `product-demo` template supports these scene types. Each has its own content shape in `demo-config.ts`.

## Type: `title`

Opening card — brand introduction.

```typescript
{
  type: 'title',
  durationSeconds: 9,
  content: {
    headline: 'Build Videos with AI',
    subheadline: 'The complete creator toolkit',
  }
}
```

## Type: `problem`

Pain point the product solves. Use bullet list for punch.

```typescript
{
  type: 'problem',
  durationSeconds: 14,
  content: {
    headline: 'Manual video editing is slow',
    problems: [
      'Hours cutting footage',
      'Expensive voiceover talent',
      'Inconsistent branding',
    ],
  }
}
```

## Type: `solution`

Your product's approach — high-level benefits.

```typescript
{
  type: 'solution',
  durationSeconds: 13,
  content: {
    headline: 'Generate videos in minutes',
    highlights: [
      'AI voiceover in 9 voices',
      'Auto-generated scene images',
      'One-command render',
    ],
  }
}
```

## Type: `demo`

Screen recording or product walkthrough.

```typescript
{
  type: 'demo',
  durationSeconds: 20,
  content: {
    headline: 'See it in action',
    videoFile: 'videos/demo-clip.mp4',
  }
}
```

## Type: `feature`

Deep-dive on one specific capability.

```typescript
{
  type: 'feature',
  durationSeconds: 12,
  content: {
    headline: 'Voice cloning',
    description: 'Upload a 30-second sample and use your own voice.',
    imageFile: 'images/voice-clone.png',
  }
}
```

## Type: `stats`

Proof points, benchmarks, ROI numbers.

```typescript
{
  type: 'stats',
  durationSeconds: 12,
  content: {
    stats: [
      { value: '99%', label: 'Accuracy' },
      { value: '10x', label: 'Faster' },
      { value: '$1', label: 'Per video' },
    ],
  }
}
```

## Type: `cta`

Call to action — closing card with links.

```typescript
{
  type: 'cta',
  durationSeconds: 10,
  content: {
    headline: 'Get started free',
    links: ['example.com', 'twitter.com/example'],
  }
}
```

## Typical Scene Flow

A 60-second product video:

1. `title` (9s) — brand
2. `problem` (14s) — why this matters
3. `solution` (13s) — how you solve it
4. `stats` (12s) — proof
5. `cta` (10s) — next step

Total: 58s + padding = 60s.
