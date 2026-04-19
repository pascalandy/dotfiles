---
name: slidev-bootstrap
description: Scaffold a new Slidev project, drive the CLI, and configure deck-wide headmatter. USE WHEN create slidev, pnpm create slidev, new slidev project, slidev init, slidev cli, slidev dev, slidev build, slidev export command, slidev theme command, slidev format, slidev doctor, project structure, slides.md, deck-wide config, title, theme selection, headmatter options.
---

# Slidev Bootstrap

Turn an empty folder into a working Slidev deck and understand the CLI that drives it.

## Core Concept

A Slidev project is a single Markdown file (`slides.md`) plus a small `package.json` that depends on `@slidev/cli` and a theme. Everything else — layouts, components, styles — lives in optional sibling directories. The CLI offers five commands (`dev`, `build`, `export`, `format`, `theme`) that all operate on `slides.md`.

## Workflow

### 1. Create the project

```bash
pnpm create slidev
# prompts for project name, then scaffolds a minimal project:
#   slides.md       -- the deck
#   package.json    -- depends on @slidev/cli + the selected theme
# Additional directories (components/, public/, pages/, styles/, etc.)
# are created on demand as the deck grows.
```

### 2. Run the dev server

```bash
pnpm run dev                        # -> http://localhost:3030
pnpm exec slidev --open             # start and open the browser
pnpm exec slidev --port 4000        # custom port
```

When using the npm/pnpm script alias with extra flags, forward them explicitly:

```bash
pnpm run dev -- --port 4000 --open
```

**Verify**: open http://localhost:3030 and confirm the title slide renders.

### 3. Configure the deck (headmatter)

The first YAML block in `slides.md` is *headmatter* — deck-wide config:

```yaml
---
theme: default
title: My Talk
info: |
  Slides for the 2026 conference
drawings:
  persist: false
transition: slide-left
comark: true
seoMeta:
  ogImage: https://example.com/og.png
---
```

See [`references/core-headmatter.md`](references/core-headmatter.md) for every option, grouped into: theme & appearance, fonts, code & highlighting, features (drawings, record, selectable, contextMenu, wakeLock), export & build, info & SEO, addons, theme config, defaults, HTML attrs, presenter, router mode, and remote assets.

### 4. Drive the CLI

See [`references/core-cli.md`](references/core-cli.md) for the complete reference. High-frequency flags:

```bash
slidev                     # dev server
slidev build               # static SPA into dist/
slidev build --base /talk/ # for subpath hosting
slidev export              # deck.pdf (needs playwright-chromium)
slidev export --format pptx
slidev export --with-clicks
slidev format              # rewrite slides.md in a canonical format
slidev theme eject         # copy the active theme into ./theme/
```

## Output Contract

When Bootstrap finishes, the user should have:

- A runnable `pnpm run dev` that serves at http://localhost:3030.
- A `slides.md` with valid headmatter.
- A clear understanding of which CLI command to use next (write → `dev`, ship static → `build`, share artefact → `export`).

## Examples

**"Start a new deck."**

```bash
pnpm create slidev my-talk
cd my-talk
pnpm run dev
```

**"Change the theme to seriph."**

```yaml
---
theme: seriph
---
```

Re-run `pnpm run dev` -- the theme package is auto-installed on first use.

**"Export the deck to PDF with click animations preserved."**

```bash
pnpm add -D playwright-chromium
pnpm exec slidev export --with-clicks
```

## References

- [core-cli.md](references/core-cli.md) — every CLI command, flag, and exit condition
- [core-headmatter.md](references/core-headmatter.md) — every deck-wide config key
