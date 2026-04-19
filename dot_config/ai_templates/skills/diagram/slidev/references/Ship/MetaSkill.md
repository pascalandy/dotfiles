---
name: slidev-ship
description: Export a Slidev deck to PDF, PPTX, or PNG, build it as a static SPA, host it on common platforms, cache remote assets for offline viewing, attach an OG image and SEO metadata, and offer a download link from the live deck. USE WHEN export slidev, slidev pdf, slidev pptx, slidev png, slidev build, build spa, static site, deploy slidev, host slidev, github pages, netlify slidev, vercel slidev, download pdf from deck, og image, seoMeta, seo meta, remote asset cache, playwright chromium.
---

# Slidev Ship

Take the deck from the dev server to a shareable artefact — PDF, PPTX, SPA, or hosted URL — with the SEO and social-sharing metadata set.

## Core Concept

Shipping a deck is two independent axes:

- **Export** produces a file: PDF, PPTX, PNG, or Markdown. Runs in a headless browser (`playwright-chromium`).
- **Build** produces a static SPA under `dist/` suitable for any static host.

Both can be combined: `build` with `download: true` bundles an exported PDF inside the SPA and adds a download button.

## Routing Inside This Sub-Skill

| Intent | Open |
|---|---|
| CLI flags for `slidev export` (format, pages, ranges, clicks, timeout) | [`references/core-exporting.md`](references/core-exporting.md) |
| `slidev build` and deployment to GitHub Pages, Netlify, Vercel | [`references/core-hosting.md`](references/core-hosting.md) |
| Attach an exported PDF to the built SPA with a download button | [`references/build-pdf.md`](references/build-pdf.md) |
| Cache remote images at build time for offline use | [`references/build-remote-assets.md`](references/build-remote-assets.md) |
| Configure the Open Graph image | [`references/build-og-image.md`](references/build-og-image.md) |
| Configure `<meta>` SEO tags | [`references/build-seo-meta.md`](references/build-seo-meta.md) |

## Canonical Patterns

**One-time setup for any export:**

```bash
pnpm add -D playwright-chromium
```

**Export to PDF or other formats:**

```bash
pnpm exec slidev export                          # deck.pdf
pnpm exec slidev export --output my-talk.pdf
pnpm exec slidev export --with-clicks            # one page per click step
pnpm exec slidev export --range 1,4-7,10         # subset of slides
pnpm exec slidev export --format pptx            # PowerPoint
pnpm exec slidev export --format png --range 1-5 # PNG per slide
pnpm exec slidev export --format md              # Markdown
pnpm exec slidev export --with-toc               # PDF with clickable outline
pnpm exec slidev export --dark                   # force dark mode
```

Alternative: open `http://localhost:3030/export` in the dev server for a browser-driven export UI.

**Build SPA with embedded PDF download:**

```yaml
---
download: true
---
```

```bash
pnpm run build
# → dist/
```

**OG + SEO:**

```yaml
---
seoMeta:
  ogImage: https://example.com/og.png
  ogTitle: My Talk
  ogDescription: A deep dive
  twitterCard: summary_large_image
---
```

Alternatives for the OG image:

- Drop a file named `og-image.png` in the **project root** (not `public/`) — Slidev picks it up automatically.
- Auto-generate from the first slide: `seoMeta.ogImage: auto` (needs `playwright-chromium`; output is saved back to `./og-image.png`).

**Deploy to GitHub Pages (subpath):**

```bash
pnpm exec slidev build --base /talk/
# push dist/ to the gh-pages branch
```

## Output Contract

A good Ship output delivers:

1. The exact CLI invocation for the requested artefact — no hand-waving at "run `slidev export` somehow".
2. A reminder to install `playwright-chromium` *before* the first export attempt.
3. The `--base` flag whenever the deployment is under a subpath.
4. SEO / OG metadata in the right scope (headmatter only).
5. For `download: true`, the note that the build runs the export internally and therefore also needs `playwright-chromium`.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `browserType.launch: Executable doesn't exist` | Missing `playwright-chromium` dev dep |
| Broken asset paths on GitHub Pages | Missing `--base /subpath/` |
| Magic-move collapses in exported PDF | Missing `--with-clicks` |
| Remote images 404 after deploy | Disable `remoteAssets` caching or verify the upstream URL |
