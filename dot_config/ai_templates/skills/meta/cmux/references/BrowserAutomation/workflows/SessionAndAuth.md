# SessionAndAuth

Use this workflow when a task includes login state or persistent sessions.

## Steps

1. Complete login on one surface.
2. Save state immediately after successful authentication.
3. Reload that state in future runs instead of logging in again.

## Commands

```bash
cmux browser surface:7 state save auth-state.json
cmux browser surface:7 cookies get --json
cmux browser surface:7 storage local get --json
cmux browser surface:7 state load auth-state.json
```

## Success Criteria

- Authenticated state is captured after login success.
- Future sessions can restore state without repeating the flow.
