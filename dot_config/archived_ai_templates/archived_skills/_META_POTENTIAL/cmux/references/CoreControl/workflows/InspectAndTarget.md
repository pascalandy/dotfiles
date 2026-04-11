# InspectAndTarget

Use this workflow before any topology change or when the user asks where something is.

## Steps

1. Resolve the current caller anchor.
2. List only the topology level needed for the request.
3. Prefer short refs in follow-up actions.

## Commands

```bash
cmux identify --json
cmux list-windows
cmux list-workspaces
cmux list-panes
cmux list-pane-surfaces --pane pane:1
```

## Success Criteria

- The relevant `window:N`, `workspace:N`, `pane:N`, or `surface:N` ref is known.
- The next command can target an explicit handle.
