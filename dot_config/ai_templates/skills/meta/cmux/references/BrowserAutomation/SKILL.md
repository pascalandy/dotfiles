---
name: BrowserAutomation
description: Browser automation on cmux webview surfaces using snapshot, ref, wait, and session-state loops. USE WHEN the request is about opening sites, interacting with page elements, waiting for page state changes, extracting data, or saving authenticated session state inside cmux.
---

# BrowserAutomation

## Core Concept

Run browser work as a stable loop:

1. Open or target one browser surface.
2. Verify navigation before waiting.
3. Snapshot to get fresh refs.
4. Act on those refs.
5. Wait for the resulting state change.
6. Re-snapshot after DOM or navigation changes.

Use one `surface:N` per task unless there is a clear reason to switch.

## Workflow Routing

| Intent | Workflow |
|---|---|
| open a site, choose the right browser surface, confirm navigation | `workflows/OpenAndAnchor.md` |
| click, fill, submit, wait, extract content, avoid stale refs | `workflows/InteractAndVerify.md` |
| log in, save state, reload state, work with cookies or storage | `workflows/SessionAndAuth.md` |

## Output Format

Return results in this structure:

1. `Surface`: active browser surface ref.
2. `Workflow`: which browser workflow is being applied.
3. `Commands`: exact `cmux browser` commands.
4. `Observed state`: URL, text, or wait condition that confirms progress.
5. `Next action`: what to do after the current state is stable.

## Examples

### Open and anchor

```text
Request: open https://example.com in cmux browser

Workflow: OpenAndAnchor
Commands:
- cmux --json browser open https://example.com
- cmux browser surface:7 get url
- cmux browser surface:7 wait --load-state complete --timeout-ms 15000
Verification: URL matches and load state is complete
```

### Interact and verify

```text
Request: click submit and wait for the dashboard

Workflow: InteractAndVerify
Commands:
- cmux browser surface:7 snapshot --interactive
- cmux --json browser surface:7 click e3 --snapshot-after
- cmux browser surface:7 wait --url-contains "/dashboard" --timeout-ms 15000
Verification: dashboard URL observed
```

## Reference

See `references/wkwebview-limits.md` for unsupported capabilities and safe fallbacks.
