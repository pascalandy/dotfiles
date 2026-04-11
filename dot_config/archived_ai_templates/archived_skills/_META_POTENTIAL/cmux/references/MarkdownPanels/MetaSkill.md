---
name: MarkdownPanels
description: Render markdown files in a dedicated cmux panel with live reload. USE WHEN the request is about opening plans, notes, documentation, or README-style content in a formatted viewer beside the terminal.
---

# MarkdownPanels

## Core Concept

Use the markdown viewer when the user needs a readable file beside active terminal work. The panel is for display, not editing. The file stays on disk, and the panel updates when that file changes.

## Workflow Routing

| Intent | Workflow |
|---|---|
| open a markdown file beside the current task | `workflows/OpenViewer.md` |
| keep a markdown panel useful while the file keeps changing | `workflows/FollowLiveReload.md` |

## Output Format

Return results in this structure:

1. `Path`: resolved markdown file path.
2. `Workflow`: which viewer workflow is being applied.
3. `Command`: the `cmux markdown` invocation.
4. `Placement`: where the panel opens.
5. `Live state`: whether subsequent file saves should refresh automatically.

## Examples

### Open a plan

```text
Request: show docs/plan.md next to my terminal

Workflow: OpenViewer
Command: cmux markdown open docs/plan.md
Result: a right-side markdown panel opens in the caller's workspace
```

### Follow live updates

```text
Request: keep plan.md visible while another process updates it

Workflow: FollowLiveReload
Command: cmux markdown open plan.md
Verification: the panel re-renders on file save or atomic replace
```

## Reference

See `references/live-reload.md` for refresh behavior and edge cases.
