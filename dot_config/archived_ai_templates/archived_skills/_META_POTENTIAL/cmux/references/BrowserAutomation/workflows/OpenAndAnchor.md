# OpenAndAnchor

Use this workflow at the start of a browser task.

## Steps

1. Open a URL or target an existing browser surface.
2. Read the current URL before waiting.
3. Wait for a concrete load condition.

## Commands

```bash
cmux --json browser open https://example.com
cmux browser surface:7 get url
cmux browser surface:7 wait --load-state complete --timeout-ms 15000
cmux browser surface:7 snapshot --interactive
```

## Success Criteria

- A concrete `surface:N` ref is active.
- The page has navigated away from `about:blank`.
- Fresh refs are available for interaction.
