# OpenViewer

Use this workflow when the user wants a markdown file rendered in cmux.

## Steps

1. Resolve the file path.
2. Open the file in the caller's workspace or an explicit target.
3. Report where the panel was created.

## Commands

```bash
cmux markdown open plan.md
cmux markdown open /absolute/path/to/PLAN.md
cmux markdown open design.md --workspace workspace:2
```

## Success Criteria

- The file path resolves correctly.
- A markdown panel opens in the intended workspace or split.
