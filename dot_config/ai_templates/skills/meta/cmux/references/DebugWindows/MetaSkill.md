---
name: DebugWindows
description: Manage existing cmux debug windows, their Debug menu wiring, and combined debug snapshots. USE WHEN the request is about Sidebar Debug, Background Debug, Menu Bar Extra Debug, Debug menu entries, or copying current debug configuration.
---

# DebugWindows

## Core Concept

Keep this domain constrained to the existing debug windows and their menu hooks. Reuse the built-in controls and the snapshot script before inventing new debug UI.

Use this specialist for:

- Opening or checking Sidebar Debug, Background Debug, and Menu Bar Extra Debug
- Verifying `Debug` -> `Debug Windows` menu wiring in debug builds
- Capturing one combined payload of current debug defaults

## Workflow Routing

| Intent | Workflow |
|---|---|
| inspect or adjust existing Debug menu wiring and debug windows | `workflows/InspectDebugMenu.md` |
| print or copy a combined debug snapshot payload | `workflows/CaptureDebugSnapshot.md` |

## Output Format

Return results in this structure:

1. `Scope`: which debug window or menu path is involved.
2. `Workflow`: which debug workflow is being applied.
3. `Files or commands`: code locations or script invocations.
4. `Verification`: build, reload, or clipboard confirmation.

## Examples

### Inspect menu wiring

```text
Request: make sure Sidebar Debug is still wired under the Debug menu

Workflow: InspectDebugMenu
Files:
- Sources/cmuxApp.swift
- Sources/AppDelegate.swift
Verification: Debug build exposes Debug -> Debug Windows entries
```

### Capture current debug state

```text
Request: copy the combined debug settings snapshot

Workflow: CaptureDebugSnapshot
Command: scripts/debug_windows_snapshot.sh --copy
Verification: payload printed and copied to clipboard
```

## Reference

See `references/key-files.md` for the primary code locations.
