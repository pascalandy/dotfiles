---
name: gstack-upgrade
version: 2.0.0
description: |
  Refresh a local gstack install from its upstream source or another checked-out
  copy. Use when the skill bundle itself needs to be updated or re-synced across
  assistant-specific skill directories.
---

# gstack-upgrade

Refresh the installed gstack skill bundle in a way that works across assistants.

## Assistant Compatibility

- Treat references to `.opencode/...` and `.claude/...` as common install locations. Use whichever exists in the current environment.
- If a step says `AskUserQuestion`, ask the user directly using the current assistant's native interaction flow.
- Prefer non-destructive syncs. Do not silently discard local changes in a vendored skill directory.

## Step 1: Detect the active install

Run:

```bash
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || true)
INSTALL_DIR=""
for _candidate in \
  "${GSTACK_ROOT:-}" \
  "$_ROOT/.opencode/skill/gstack" \
  "$_ROOT/.opencode/skills/gstack" \
  "$_ROOT/.claude/skills/gstack" \
  "$HOME/.config/opencode/skill/gstack" \
  "$HOME/.config/opencode/skills/gstack" \
  "$HOME/.opencode/skill/gstack" \
  "$HOME/.opencode/skills/gstack" \
  "$HOME/.claude/skills/gstack"
do
  [ -n "$_candidate" ] && [ -d "$_candidate" ] && INSTALL_DIR="$_candidate" && break
done

if [ -z "$INSTALL_DIR" ]; then
  echo "ERROR: gstack install not found"
  exit 1
fi

echo "INSTALL_DIR=$INSTALL_DIR"
```

If no install is found, stop and tell the user which paths were checked.

## Step 2: Classify the install

Run:

```bash
if [ -d "$INSTALL_DIR/.git" ]; then
  echo "INSTALL_TYPE=git"
else
  echo "INSTALL_TYPE=vendored"
fi
```

## Step 3: Refresh safely

### Git checkout

If `INSTALL_TYPE=git`, refresh in place:

```bash
cd "$INSTALL_DIR"
git status --short
git pull --ff-only
[ -x ./setup ] && ./setup
```

If the working tree is dirty, ask the user whether to stop or continue after they handle their local changes. Do not reset hard.

### Vendored copy

If `INSTALL_TYPE=vendored`, ask the user which source to trust:

1. A fresh clone of `https://github.com/garrytan/gstack`
2. Another local gstack checkout
3. Stop and leave the vendored copy as-is

If they choose a fresh clone and network access is available, use:

```bash
TMP_DIR=$(mktemp -d)
git clone --depth 1 https://github.com/garrytan/gstack.git "$TMP_DIR/gstack"
```

If they choose another local checkout, ask for the source path and verify it exists.

After the source directory is known, replace the vendored copy without deleting the backup first:

```bash
mv "$INSTALL_DIR" "$INSTALL_DIR.bak"
cp -Rf "$SOURCE_DIR" "$INSTALL_DIR"
rm -rf "$INSTALL_DIR/.git"
[ -x "$INSTALL_DIR/setup" ] && (cd "$INSTALL_DIR" && ./setup)
```

Only remove `"$INSTALL_DIR.bak"` after the user confirms the refreshed copy works.

## Step 4: Sync adjacent installs

If the user keeps both a global install and a project-vendored copy, ask whether the second location should be refreshed from the same source. Reuse the same safe copy flow. Never overwrite a second install silently.

## Step 5: Summarize

Report:

- The install path that was refreshed
- Whether it was a git or vendored install
- Whether `./setup` was run
- Any backup directory still left in place
- Any follow-up action the user still needs to take
