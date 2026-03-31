# CaptureDebugSnapshot

Use this workflow when the user wants one combined snapshot of current debug-related defaults.

## Steps

1. Run the snapshot script.
2. Add `--copy` when the user wants clipboard output.
3. Pass `--domain <bundle-id>` if auto-detection is insufficient.

## Commands

```bash
scripts/debug_windows_snapshot.sh
scripts/debug_windows_snapshot.sh --copy
scripts/debug_windows_snapshot.sh --domain <bundle-id> --copy
```

## Success Criteria

- The combined payload includes sidebar, background, menu bar extra, and browser devtools settings.
- Clipboard copy succeeds when requested.
