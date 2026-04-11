# ReshapeTopology

Use this workflow when the request changes layout or routing.

## Steps

1. Identify the source and destination refs.
2. Make one topology change at a time.
3. Focus the resulting target if the user needs immediate interaction.

## Commands

```bash
cmux new-window
cmux new-workspace
cmux new-split right --panel pane:1
cmux move-surface --surface surface:7 --pane pane:2 --focus true
cmux reorder-surface --surface surface:7 --before surface:3
cmux reorder-workspace --workspace workspace:4 --before workspace:2
```

## Success Criteria

- The requested object exists in the requested location.
- Focus and ordering match the user's intent.
