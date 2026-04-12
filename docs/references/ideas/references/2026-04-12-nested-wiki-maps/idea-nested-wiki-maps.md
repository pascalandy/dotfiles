# Nested Wiki Maps

Some wikis contain subdirectories that are themselves full wiki maps, each with their own `INDEX.md`, `references/`, and `LOG.md`.

## Rules

- Treat a nested wiki map as a navigational boundary, not as a flat content folder.
- The parent `INDEX.md` should link to the child wiki's `INDEX.md`, not inline every page inside that child wiki.
- Parent indexes should describe the child wiki in one line: what it covers, why it exists, when to use it.
- Child wiki pages stay cataloged in the child wiki's own `INDEX.md`.
- Avoid duplicating the same leaf pages in both the parent and child indexes unless the user explicitly wants a cross-wiki global catalog.
- Root or parent indexes act as routers: route to the right child wiki first, then let that child wiki route to its own pages.
- When a directory mixes plain markdown files and nested wiki maps, list plain files directly and list each nested wiki map by its `INDEX.md`.
- Preserve local ownership: conventions that only matter inside the child wiki should stay documented there, not repeated at the parent level.

## Recommended Pattern

In parent `INDEX.md`:

```md
### kind/wiki

| File | Description |
|------|-------------|
| [`references/configs/INDEX.md`](references/configs/INDEX.md) | Child wiki map for configuration references and setup docs |
| [`references/workflows/INDEX.md`](references/workflows/INDEX.md) | Child wiki map for workflows, methods, and skill usage |
```

## Guidance

- Use this pattern when the subdirectory is large enough to need its own map, has its own `LOG.md`, or has a distinct scope.
- Prefer one-layer-at-a-time navigation: parent index → child index → leaf page.
- Keep the parent index intentionally lighter when nested wiki maps exist.

