# ConfirmAndRecover

Use this workflow after a move or when the interface may be stale.

## Steps

1. Confirm the final target ref.
2. Flash the target when visual confirmation matters.
3. Check surface health before sending more input.

## Commands

```bash
cmux focus-pane --pane pane:2
cmux focus-panel --panel surface:7
cmux trigger-flash --surface surface:7
cmux surface-health
cmux surface-health --workspace workspace:2
```

## Success Criteria

- The target is focused or confirmed.
- No hidden or detached surface blocks the next action.
