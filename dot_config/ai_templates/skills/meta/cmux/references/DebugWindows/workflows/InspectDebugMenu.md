# InspectDebugMenu

Use this workflow when the task touches existing debug window wiring.

## Steps

1. Verify `Sources/cmuxApp.swift` still exposes `Debug` -> `Debug Windows` in debug builds.
2. Keep the existing entries available: `Sidebar Debug...`, `Background Debug...`, `Menu Bar Extra Debug...`, and `Open All Debug Windows`.
3. Check `Sources/AppDelegate.swift` when the task affects menu bar extra debug payload or defaults.
4. After edits, rebuild and reload a debug build.

## Verification

```bash
xcodebuild -project GhosttyTabs.xcodeproj -scheme cmux -configuration Debug -destination 'platform=macOS' build
./scripts/reload.sh --tag <tag>
```

## Success Criteria

- Debug windows remain reachable from the Debug menu in debug builds.
- Existing per-window copy controls still work.
