# Command Groups

## Context and Handles

```bash
cmux identify --json
cmux --json --id-format both identify
```

## Windows and Workspaces

```bash
cmux list-windows
cmux list-workspaces
cmux new-window
cmux new-workspace
cmux focus-window --window window:2
cmux select-workspace --workspace workspace:4
```

## Panes and Surfaces

```bash
cmux list-panes
cmux list-pane-surfaces --pane pane:1
cmux new-split right --panel pane:1
cmux new-surface --type terminal --pane pane:1
cmux move-surface --surface surface:7 --pane pane:2 --focus true
```

## Confirmation

```bash
cmux trigger-flash --surface surface:7
cmux surface-health
```
