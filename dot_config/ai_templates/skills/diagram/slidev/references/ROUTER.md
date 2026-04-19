---
name: slidev-router
description: Route Slidev-related requests to the right specialist sub-skill. USE WHEN slidev, sli.dev, pnpm create slidev, slidev project, slidev cli, slidev headmatter, slidev markdown, slide separator, slide frontmatter, slidev layout, two-cols, cover slide, slidev component, slidev slot, draggable slide, canvas size, zoom slide, import slides, code block in slides, line highlighting, magic move, monaco editor, monaco run, monaco write, twoslash types, code tabs, import snippet, v-click, v-clicks, slide animation, slide transition, rough marker, drawing mode, style direction, slide hooks, onSlideEnter, onSlideLeave, mermaid diagram, plantuml diagram, latex math, equation in slides, presenter mode, record presentation, camera overlay, presentation timer, remote control slidev, speaker notes, ruby text notes, slidev theme, eject theme, scoped css, slidev icons, export slidev pdf, export slidev pptx, slidev png, slidev spa, slidev build, slidev deploy, slidev hosting, og image, seo meta, remote asset caching.
---

# Slidev Router

Map the request to exactly one sub-skill, then load that sub-skill's `MetaSkill.md`.

## Routing Table

| Request pattern | Route to |
|---|---|
| create project, scaffold, `pnpm create slidev`, new deck, project structure, CLI flags, `slidev dev/build/export/theme`, deck-wide headmatter, title, theme selection, default config | `Bootstrap/MetaSkill.md` |
| markdown syntax, slide separator, per-slide frontmatter, layouts (`cover`, `center`, `two-cols`, `image`, `iframe`, `quote`, `section`, `fact`, `statement`, `intro`, `end`), built-in Vue components, slots (`::right::`, `::default::`), draggable elements (`v-drag`), canvas size, zoom, transform, global layers, importing slides, comark/MDC syntax, block frontmatter, frontmatter merging | `Authoring/MetaSkill.md` |
| code blocks, line highlighting (`{2,3}`, `{1\|2-3\|all}`), line numbers, scrollable code (`maxHeight`), code tabs (`::code-group`), magic-move animations, Monaco editor, Monaco run, Monaco write (edit files live), twoslash (TS types), external snippet import (`<<<`), side editor, VS Code extension, Prettier plugin | `Code/MetaSkill.md` |
| `v-click`, `<v-clicks>`, click animations, click counter, slide transitions, page transitions, rough markers (`v-mark.underline`, `v-mark.circle`), drawing mode (`C` key, `drawings:` config), direction styles (`forward:delay-300`), click markers in notes, slide hooks (`onSlideEnter`, `onSlideLeave`) | `Motion/MetaSkill.md` |
| Mermaid diagrams, PlantUML diagrams, LaTeX inline and block math, equations | `Diagrams/MetaSkill.md` |
| presenter mode, camera overlay, recording the talk, timer (`duration`, `timer: countdown`), remote control (`slidev --remote`), speaker notes, ruby text notes (`notesAutoRuby`), `$nav`, `$slidev`, navigation API, global context | `Present/MetaSkill.md` |
| custom theme, eject theme (`slidev theme eject`), theme gallery, scoped CSS (`<style scoped>`), global styling, icons (`<mdi-icon />`) | `Theme/MetaSkill.md` |
| export to PDF, PPTX, PNG, requires `playwright-chromium`, build SPA, `slidev build`, hosting on GitHub Pages/Netlify/Vercel, bundled PDF (`download: true`), remote image caching, OG image (`seoMeta.ogImage`, `og-image.png`), SEO metadata (`seoMeta:`) | `Ship/MetaSkill.md` |

## Dispatch Rules

1. Match on the most specific keyword set available.
2. If a request spans two domains, route to the more specific one first, then cross-link only if needed (e.g. "embed Mermaid inside a two-cols layout" -> Diagrams handles the diagram; Authoring is consulted only for the surrounding layout).
3. After dispatching, read the sub-skill's `MetaSkill.md` in full and follow its internal routing into its `references/` directory.
4. Never invoke a sub-skill's `MetaSkill.md` as a standalone skill -- only through this router.
