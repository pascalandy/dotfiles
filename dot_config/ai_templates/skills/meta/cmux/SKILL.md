---
name: cmux
description: Unified cmux control through one entry point for topology management, browser surfaces, markdown panels, and debug windows.
keywords: [cmux, topology, windows, workspaces, panes, surfaces, inspect, identify, split, create, focus, move, reorder, trigger-flash, health check, browser, webview, open site, click, fill, type, submit, snapshot, wait, login, authentication, auth state, session state, cookies, storage, extract data, markdown, preview, live reload, plan panel, docs panel, notes viewer, documentation, readme, debug windows, sidebar debug, background debug, menu bar extra debug, debug menu, copy config, debug snapshot]
---

# cmux

> One entry point for cmux work. Describe the outcome you need, and the router loads the specialist for topology control, browser automation, markdown viewing, or debug-window work.

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

## The Problem

cmux exposes several distinct domains behind one CLI surface:

- Topology control for windows, workspaces, panes, and surfaces
- Browser automation inside surface-backed webviews
- Markdown viewing with live reload
- Debug window and Debug menu maintenance

If all of that lives in one undifferentiated skill, the instructions get noisy, routing becomes implicit, and browser-specific guidance bleeds into non-browser tasks.

## The Solution

This meta-skill separates cmux work into four specialists:

1. `CoreControl` handles deterministic topology and routing.
2. `BrowserAutomation` handles webview navigation, interaction, waiting, and session state.
3. `MarkdownPanels` handles markdown viewer panels and live reload.
4. `DebugWindows` handles the existing debug windows, Debug menu wiring, and combined debug snapshots.

The collection stays user-facing. The router stays tiny. Each specialist owns a distinct domain and can also be loaded directly.

## What's Included

| Component | Path | Purpose | Workflows |
|---|---|---|---|
| Collection entry point | `SKILL.md` | User-facing overview and invocation guide | N/A |
| Router | `references/ROUTER.md` | Maps request patterns to specialists | N/A |
| Core topology specialist | `references/CoreControl/MetaSkill.md` | Windows, workspaces, panes, surfaces, focus, moves, reorder, flash | `InspectAndTarget`, `ReshapeTopology`, `ConfirmAndRecover` |
| Browser specialist | `references/BrowserAutomation/MetaSkill.md` | Open sites, snapshot refs, interact, wait, extract state | `OpenAndAnchor`, `InteractAndVerify`, `SessionAndAuth` |
| Markdown specialist | `references/MarkdownPanels/MetaSkill.md` | Open markdown viewers and rely on live updates | `OpenViewer`, `FollowLiveReload` |
| Debug specialist | `references/DebugWindows/MetaSkill.md` | Debug menu wiring, debug windows, config snapshots | `InspectDebugMenu`, `CaptureDebugSnapshot` |
| Debug snapshot script | `references/DebugWindows/scripts/debug_windows_snapshot.sh` | Print or copy combined debug defaults payload | N/A |

## Invocation Scenarios

| Trigger Phrase | What Happens |
|---|---|
| "move this terminal to another pane" | Routes to `CoreControl`, then runs `ReshapeTopology` |
| "identify the current cmux context" | Routes to `CoreControl`, then runs `InspectAndTarget` |
| "open this site in a cmux browser surface" | Routes to `BrowserAutomation`, then runs `OpenAndAnchor` |
| "click this button and wait for the dashboard" | Routes to `BrowserAutomation`, then runs `InteractAndVerify` |
| "show this plan in a markdown panel" | Routes to `MarkdownPanels`, then runs `OpenViewer` |
| "keep this markdown file visible while it updates" | Routes to `MarkdownPanels`, then runs `FollowLiveReload` |
| "open the sidebar debug window" | Routes to `DebugWindows`, then runs `InspectDebugMenu` |
| "copy the combined debug config" | Routes to `DebugWindows`, then runs `CaptureDebugSnapshot` |

## Example Usage

### Topology Control

```text
User: move surface:7 into pane:2 and focus it

AI routes to CoreControl and returns:
- Context: source surface `surface:7`, destination `pane:2`
- Workflow: `ReshapeTopology`
- Commands:
  - `cmux move-surface --surface surface:7 --pane pane:2 --focus true`
  - `cmux trigger-flash --surface surface:7`
- Result: surface moved and visually confirmed
```

### Browser Automation

```text
User: open https://example.com in cmux and fill the signup form

AI routes to BrowserAutomation and returns:
- Workflow: `OpenAndAnchor` then `InteractAndVerify`
- Commands:
  - `cmux --json browser open https://example.com/signup`
  - `cmux browser surface:7 wait --load-state complete --timeout-ms 15000`
  - `cmux browser surface:7 snapshot --interactive`
  - `cmux browser surface:7 fill e1 "Jane Doe"`
  - `cmux browser surface:7 fill e2 "jane@example.com"`
```

### Markdown Viewer

```text
User: show docs/plan.md beside my current terminal

AI routes to MarkdownPanels and returns:
- Workflow: `OpenViewer`
- Command: `cmux markdown open docs/plan.md`
- Result: a markdown panel opens in the caller's workspace and updates on file save
```

### Debug Windows

```text
User: copy the sidebar/background/menu bar extra debug settings

AI routes to DebugWindows and returns:
- Workflow: `CaptureDebugSnapshot`
- Command: `references/DebugWindows/scripts/debug_windows_snapshot.sh --copy`
- Result: combined payload printed and copied to the clipboard
```

## Customization

No installation or harness-specific configuration is required.

Optional customization points:

| Area | Location | Purpose |
|---|---|---|
| Routing keywords | `references/ROUTER.md` | Add a new request pattern or a new specialist |
| Topology workflows | `references/CoreControl/workflows/` | Extend routing and operator guidance |
| Browser workflows | `references/BrowserAutomation/workflows/` | Add patterns for richer webview tasks |
| Markdown workflows | `references/MarkdownPanels/workflows/` | Add panel-management conventions |
| Debug workflows | `references/DebugWindows/workflows/` | Expand debug maintenance procedures |
