# InteractAndVerify

Use this workflow for clicks, fills, submissions, and extraction.

## Steps

1. Take an interactive snapshot.
2. Use returned refs for actions.
3. Wait for URL, selector, text, or load-state confirmation.
4. Re-snapshot after major DOM changes.

## Commands

```bash
cmux browser surface:7 snapshot --interactive
cmux browser surface:7 fill e1 "Jane Doe"
cmux browser surface:7 fill e2 "jane@example.com"
cmux --json browser surface:7 click e3 --snapshot-after
cmux browser surface:7 wait --url-contains "/welcome" --timeout-ms 15000
cmux browser surface:7 get text body
```

## Success Criteria

- Every action uses a current selector or snapshot ref.
- A post-action wait proves the UI state changed.
- Follow-up extraction reads the expected page state.
