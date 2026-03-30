# freeze

> Restrict file edits to a single directory for the session, blocking any write outside that boundary.

## When to Use

- Debugging a specific module and you want to prevent accidentally touching unrelated code
- Scoping a feature to one package or service
- User says "freeze", "restrict edits", "only edit this folder", or "lock down edits"

## Inputs

- A directory path from the user (prompted at setup). Can be relative or absolute.

## Methodology

### Step 1: Ask for the boundary

Ask the user: "Which directory should I restrict edits to? Files outside this path will be blocked from editing."

Accept a free-text path (not a multiple-choice list).

### Step 2: Resolve to absolute path

Run in terminal:
```bash
FREEZE_DIR=$(cd "<user-provided-path>" 2>/dev/null && pwd)
echo "$FREEZE_DIR"
```

If the path doesn't resolve (directory doesn't exist), tell the user and ask again.

### Step 3: Persist the boundary

```bash
FREEZE_DIR="${FREEZE_DIR%/}/"
STATE_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.gstack}"
mkdir -p "$STATE_DIR"
echo "$FREEZE_DIR" > "$STATE_DIR/freeze-dir.txt"
echo "Freeze boundary set: $FREEZE_DIR"
```

The trailing `/` is required — it prevents `/src` from matching `/src-old`.

### Step 4: Confirm to user

Tell the user: "Edits are now restricted to `<path>/`. Any Edit or Write outside this directory will be blocked. To change the boundary, run freeze again. To remove it, run unfreeze or end the session."

### Pre-edit gate (ongoing, every file write)

Before every file edit or write operation, check whether the target file path starts with the freeze directory:

```
if target_path does NOT start with freeze_dir:
    DENY the operation — tell the user the file is outside the freeze boundary
else:
    allow
```

Read the boundary from `$STATE_DIR/freeze-dir.txt` on each check (state file may change mid-session via unfreeze/re-freeze).

### Scope

- Applies to Edit and Write operations only
- Read, search, glob, and terminal commands are unaffected
- This is an accidental-edit guard, not a security boundary — terminal commands (e.g., `sed -i`) can still write outside the boundary
- If no state file exists, allow all edits (i.e., unfreeze implicitly clears by removing the file)

## Quality Gates

- Any file path outside the frozen directory is **denied**, not just warned
- The trailing-slash normalization must be applied — `/src` must not match `/src-old`
- The boundary persists across the session via the state file

## Outputs

No artifacts. Behavioral change for the session: all file edits are pre-screened against the boundary.

## Feeds Into

- >unfreeze (clears the boundary without ending the session)
- >guard (activates freeze + careful together)

## Harness Notes

In hook-capable harnesses (Claude Code), this is a `PreToolUse` hook on Edit and Write tools returning `permissionDecision: "deny"`. In harnesses without hooks, the agent must check the target path against the state file inline before every file write — refuse and explain if the path falls outside the boundary. The state file lives at `~/.gstack/freeze-dir.txt` (or `$CLAUDE_PLUGIN_DATA/freeze-dir.txt`).
