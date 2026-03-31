---
name: CoreControl
description: Deterministic cmux topology and routing control for windows, workspaces, panes, and surfaces. USE WHEN the request is about inspect, identify, split, focus, move, reorder, or trigger-flash behavior outside browser-specific and markdown-specific tasks.
---

# CoreControl

## Core Concept

Treat cmux topology as explicit handles, not implicit UI state. Start by identifying the caller context, target concrete refs such as `workspace:2` or `surface:7`, then perform the smallest topology change that satisfies the request.

Use this specialist for:

- Listing or identifying the current cmux context
- Creating or rearranging windows, workspaces, panes, and surfaces
- Focusing the correct target after a move
- Triggering visual confirmation with `trigger-flash`
- Recovering when UI focus or surface health looks stale

## Workflow Routing

| Intent | Workflow |
|---|---|
| inspect current context, list handles, identify caller | `workflows/InspectAndTarget.md` |
| split, create, move, reorder, route topology | `workflows/ReshapeTopology.md` |
| focus, flash, health check, recover from stale UI state | `workflows/ConfirmAndRecover.md` |

## Output Format

Return results in this structure:

1. `Context`: current or target refs involved in the task.
2. `Workflow`: which workflow is being applied.
3. `Commands`: exact `cmux` commands in execution order.
4. `Verification`: how success was confirmed.
5. `Next state`: final focused or moved target.

## Examples

### Inspect and target

```text
Request: identify the current workspace and list panes

Workflow: InspectAndTarget
Commands:
- cmux identify --json
- cmux list-panes
Verification: current workspace and pane refs returned
```

### Move and focus

```text
Request: move surface:7 to pane:2 and focus it

Workflow: ReshapeTopology
Commands:
- cmux move-surface --surface surface:7 --pane pane:2 --focus true
- cmux trigger-flash --surface surface:7
Verification: moved surface is focused and flashed
```

## Reference

See `references/command-groups.md` for a compact command map.
