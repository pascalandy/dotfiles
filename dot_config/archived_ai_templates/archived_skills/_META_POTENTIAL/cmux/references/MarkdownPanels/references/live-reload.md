# Live Reload

The markdown panel watches the file on disk and re-renders when it changes.

## Works Well With

- Editor saves
- Direct appends or overwrites
- Atomic replace patterns

## Edge Cases

- If the file is removed, the panel shows a file-unavailable state.
- If the file returns quickly after an atomic replace, the panel usually reconnects.
- If the file stays missing, close and reopen the panel after the file exists again.
