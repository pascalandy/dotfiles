# unfreeze

> Clear the directory edit boundary set by freeze, allowing edits everywhere again without ending the session.

## When to Use

- You've finished scoping work to one directory and want to widen edit access
- User says "unfreeze", "unlock edits", "remove freeze", or "allow all edits"
- Mid-session after freeze or guard, when the restriction is no longer needed

## Inputs

Nothing required. Reads the current freeze state file and clears it.

## Methodology

### Step 1: Check for existing boundary

Read the state file:

```bash
STATE_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.gstack}"
if [ -f "$STATE_DIR/freeze-dir.txt" ]; then
  PREV=$(cat "$STATE_DIR/freeze-dir.txt")
  rm -f "$STATE_DIR/freeze-dir.txt"
  echo "Freeze boundary cleared (was: $PREV). Edits are now allowed everywhere."
else
  echo "No freeze boundary was set."
fi
```

### Step 2: Report to user

Tell the user the result:

- If a boundary existed: "Freeze boundary cleared (was `<path>`). Edits are now allowed everywhere."
- If no boundary was set: "No freeze boundary was active."

### Step 3: Session note

If the session was started with freeze or guard, the gate check logic is still registered. It will allow all edits because the state file no longer exists. No further action is needed. To re-freeze to a different directory, run freeze again.

## Quality Gates

- The state file is deleted, not just emptied
- User is told what the previous boundary was (confirms the right boundary was cleared)
- If no boundary existed, user is told clearly rather than silently succeeding

## Outputs

No artifacts. The freeze state file is removed. Edit access is restored everywhere for the remainder of the session.

## Feeds Into

- >freeze (re-freeze to a new directory if needed)
- >guard (re-activate full safety mode)

## Harness Notes

In hook-capable harnesses (Claude Code), the freeze hooks remain registered after unfreeze — they just find no state file and allow all edits. This is by design; hooks are session-scoped and cannot be unregistered mid-session. In harnesses without hooks, unfreeze simply means the agent stops performing the path check before writes.
