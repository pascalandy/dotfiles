# Best Practices

Use this file for general OpenCode operating guidance.

## Trigger discipline

- Do not load an OpenCode management skill for ordinary coding work.
- Make descriptions specific enough to trigger only on real matches.
- Merge or narrow overlapping skills instead of stacking vague ones.

## Permission discipline

- Start from standard access.
- Add explicit permission blocks only when needed.
- Whitelist skills intentionally when an agent should load only a small set.

## Workflow discipline

- Prefer planning before editing when the change is broad or unclear.
- Preserve one source of truth for config.
- If OpenCode dotfiles are managed by chezmoi, the source of truth is the chezmoi source, not the copy in `$HOME`.
- Keep `SKILL.md` short and push detail to `references/`.
- Use audits for targeted fixes, not blanket rewrites.
- Apply chezmoi-managed config changes with `just cma`.

## Validation

- Re-read metadata after editing descriptions or frontmatter.
- Run the smallest useful validation command.
- State clearly when validation could not be run.
