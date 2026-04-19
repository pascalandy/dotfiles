---
name: slidev-code
description: Embed, animate, and edit code inside Slidev slides — line highlighting, click-phased highlights, line numbers, scrollable blocks, code tabs, magic-move transitions, Monaco editor (read/run/write files), TypeScript twoslash hovers, external snippet imports, and related editor tooling. USE WHEN code block, syntax highlighting, line highlight, line numbers, scrollable code, code max height, code tabs, code-group, magic move, monaco editor, monaco run, monaco write, runnable code, twoslash, typescript types, import snippet, external code file, side editor, vscode extension, prettier plugin slidev.
---

# Slidev Code

Everything about showing, animating, and interacting with code on a slide.

## Core Concept

A fenced code block in Slidev is a rich, configurable component. Three axes of control:

1. **Static highlighting** — which lines are emphasized (`{2,3}` or click-phased `{1|2-3|all}`).
2. **Interactivity** — Monaco editor modes (read-only, run, write-to-file), twoslash hovers.
3. **Animation** — magic-move between code snapshots, or pull code from an external file.

## Routing Inside This Sub-Skill

| Intent | Open |
|---|---|
| Highlight lines once, or advance highlight on click | [`references/code-line-highlighting.md`](references/code-line-highlighting.md) |
| Show line numbers on a single block or deck-wide | [`references/code-line-numbers.md`](references/code-line-numbers.md) |
| Constrain tall code blocks with scroll | [`references/code-max-height.md`](references/code-max-height.md) |
| Tabs across multiple code blocks | [`references/code-groups.md`](references/code-groups.md) |
| Animate transitions between code snapshots | [`references/code-magic-move.md`](references/code-magic-move.md) |
| Import code from an external file | [`references/code-import-snippet.md`](references/code-import-snippet.md) |
| TypeScript type hovers and errors | [`references/code-twoslash.md`](references/code-twoslash.md) |
| Turn a code block into a Monaco editor | [`references/editor-monaco.md`](references/editor-monaco.md) |
| Make Monaco run the code live | [`references/editor-monaco-run.md`](references/editor-monaco-run.md) |
| Let Monaco write changes back to a file | [`references/editor-monaco-write.md`](references/editor-monaco-write.md) |
| Enable the built-in side editor | [`references/editor-side.md`](references/editor-side.md) |
| VS Code extension for preview + intellisense | [`references/editor-vscode.md`](references/editor-vscode.md) |
| Format Slidev Markdown with Prettier | [`references/editor-prettier.md`](references/editor-prettier.md) |

## Canonical Patterns

**Click-phased line highlighting** (three clicks: just line 1, then 2-3, then all):

````md
```ts {1|2-3|all}
const user = getUser()
if (!user) return
render(user)
```
````

**Magic-move between snapshots** (outer fence uses four backticks so inner fences render):

`````md
````md magic-move
```js
let x = 1
```

```js
const x = 1
```
````
`````

**Runnable Monaco block:**

````md
```ts {monaco-run}
const greet = (name: string) => `hi ${name}`
greet('world')
```
````

**Import from a file** (with click-phased highlight):

```md
<<< @/snippets/example.ts {1-10|all}
```

## Output Contract

A good Code output delivers:

1. The exact fenced block string (including the language tag and the `{...}` meta) ready to paste.
2. No reliance on Monaco when the user only asked for static highlight.
3. When twoslash is used, explicit note that it needs `twoslash: true` in headmatter and a TypeScript language tag on the block.
4. When magic-move is used, note that the slide advances one *click* per snapshot transition (the slide itself does not change).

## Prerequisites Checklist

| Feature | Requirement |
|---|---|
| `{monaco}`, `{monaco-run}`, `{monaco-write}` | `monaco: true` in headmatter (or `'dev'` / `'build'` to scope) |
| `twoslash` | `twoslash: true` in headmatter, TypeScript language tag on the block |
| `::code-group` | `comark: true` in headmatter |
| `<<< @/path` | File lives under project root and is readable at build time |
