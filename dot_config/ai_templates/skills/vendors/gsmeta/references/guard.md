# guard

> Full safety mode: destructive command warnings plus directory-scoped edit restrictions, activated together in one command.

## When to Use

- Touching production or a live system and you want maximum protection
- User says "guard mode", "full safety", "lock it down", or "maximum safety"
- Any situation where you want both careful and freeze active without invoking them separately

## Inputs

- A directory path from the user (prompted at setup, same as freeze)

## Methodology

Guard is the composition of `careful` + `freeze`. Run both setups in sequence.

### Step 1: Ask for the edit boundary

Ask the user: "Guard mode: which directory should edits be restricted to? Destructive command warnings are always on. Files outside the chosen path will be blocked from editing."

Accept free-text path input.

### Step 2: Resolve and persist the freeze boundary

Same as freeze setup — resolve the path to absolute, append trailing `/`, write to `$STATE_DIR/freeze-dir.txt`.

```bash
FREEZE_DIR=$(cd "<user-provided-path>" 2>/dev/null && pwd)
FREEZE_DIR="${FREEZE_DIR%/}/"
STATE_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.gstack}"
mkdir -p "$STATE_DIR"
echo "$FREEZE_DIR" > "$STATE_DIR/freeze-dir.txt"
echo "Freeze boundary set: $FREEZE_DIR"
```

### Step 3: Confirm both protections to user

Tell the user:

> Guard mode active. Two protections are now running:
> 1. **Destructive command warnings** — rm -rf, DROP TABLE, force-push, etc. will warn before executing (you can override)
> 2. **Edit boundary** — file edits restricted to `<path>/`. Edits outside this directory are blocked.
>
> To remove the edit boundary, run unfreeze. To deactivate everything, end the session.

### Ongoing pre-command gate (careful layer)

Before every terminal command, check against the destructive pattern list from `careful`. Warn + require confirmation on match. Allow safe exceptions (build artifact dirs) without warning.

Full pattern list: see careful.md.

### Ongoing pre-edit gate (freeze layer)

Before every file edit or write, check whether the target path starts with the freeze directory. Deny if outside. Allow if inside.

Full logic: see freeze.md.

## Quality Gates

Both protections must be active simultaneously:
- [ ] Terminal commands are screened for destructive patterns (warn + override)
- [ ] File edits outside the boundary are blocked (deny, no override)
- [ ] Safe rm exceptions pass without warning
- [ ] The freeze boundary uses trailing-slash normalization

## Outputs

No artifacts. Two concurrent behavioral changes for the session.

## Feeds Into

- >unfreeze (removes the edit boundary while keeping the session alive; careful warnings remain)
- >careful (use alone if only command warnings are needed, without edit scoping)
- >freeze (use alone if only edit scoping is needed, without command warnings)

## Harness Notes

In hook-capable harnesses (Claude Code), guard registers three `PreToolUse` hooks: one on Bash (careful check script) and two on Edit/Write (freeze check script). The hook scripts are shared with the sibling careful and freeze skill directories — both must be installed. In harnesses without hooks, the agent enforces both checks inline before every relevant operation.
