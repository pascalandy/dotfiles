# gstack-upgrade

> Upgrade gstack to the latest version, detect the install type, handle consent/snooze logic, sync local vendored copies, and show a changelog summary.

## When to Use

- User says "upgrade gstack", "update gstack", or "get latest version"
- Any skill preamble detects `UPGRADE_AVAILABLE` and triggers inline upgrade flow
- Local vendored copy is out of sync with the global install

## Inputs

- Auto-upgrade preference (checked from config or env before prompting)
- The `UPGRADE_AVAILABLE <old> <new>` signal from `gstack-update-check` (when triggered from a preamble)
- User consent (unless auto-upgrade is enabled)

## Methodology

### Phase A: Consent

#### Check auto-upgrade preference

```bash
_AUTO=""
[ "${GSTACK_AUTO_UPGRADE:-}" = "1" ] && _AUTO="true"
[ -z "$_AUTO" ] && _AUTO=$(~/.claude/skills/gstack/bin/gstack-config get auto_upgrade 2>/dev/null || true)
echo "AUTO_UPGRADE=$_AUTO"
```

**If `AUTO_UPGRADE=true` or `AUTO_UPGRADE=1`:** Skip asking. Log "Auto-upgrading gstack v{old} → v{new}..." and proceed directly to Phase B.

**Otherwise, ask the user:**
- Question: "gstack v{new} is available (you're on v{old}). Upgrade now?"
- Options: Yes / Always keep me up to date / Not now / Never ask again

**"Yes":** Proceed to Phase B.

**"Always keep me up to date":**
```bash
~/.claude/skills/gstack/bin/gstack-config set auto_upgrade true
```
Tell user auto-upgrade is enabled, then proceed to Phase B.

**"Not now" — snooze with escalating backoff:**

Snooze levels: 1st snooze = 24h, 2nd = 48h, 3rd+ = 1 week.

```bash
_SNOOZE_FILE=~/.gstack/update-snoozed
_REMOTE_VER="{new}"
_CUR_LEVEL=0
if [ -f "$_SNOOZE_FILE" ]; then
  _SNOOZED_VER=$(awk '{print $1}' "$_SNOOZE_FILE")
  if [ "$_SNOOZED_VER" = "$_REMOTE_VER" ]; then
    _CUR_LEVEL=$(awk '{print $2}' "$_SNOOZE_FILE")
    case "$_CUR_LEVEL" in *[!0-9]*) _CUR_LEVEL=0 ;; esac
  fi
fi
_NEW_LEVEL=$((_CUR_LEVEL + 1))
[ "$_NEW_LEVEL" -gt 3 ] && _NEW_LEVEL=3
echo "$_REMOTE_VER $_NEW_LEVEL $(date +%s)" > "$_SNOOZE_FILE"
```

Tell user the snooze duration. Tip: set `auto_upgrade: true` in `~/.gstack/config.yaml` for silent upgrades. Continue with the original skill.

**"Never ask again":**
```bash
~/.claude/skills/gstack/bin/gstack-config set update_check false
```
Tell user update checks are disabled and how to re-enable. Continue with the original skill.

---

### Phase B: Detect Install Type

```bash
if [ -d "$HOME/.claude/skills/gstack/.git" ]; then
  INSTALL_TYPE="global-git"
  INSTALL_DIR="$HOME/.claude/skills/gstack"
elif [ -d "$HOME/.gstack/repos/gstack/.git" ]; then
  INSTALL_TYPE="global-git"
  INSTALL_DIR="$HOME/.gstack/repos/gstack"
elif [ -d ".claude/skills/gstack/.git" ]; then
  INSTALL_TYPE="local-git"
  INSTALL_DIR=".claude/skills/gstack"
elif [ -d ".agents/skills/gstack/.git" ]; then
  INSTALL_TYPE="local-git"
  INSTALL_DIR=".agents/skills/gstack"
elif [ -d ".claude/skills/gstack" ]; then
  INSTALL_TYPE="vendored"
  INSTALL_DIR=".claude/skills/gstack"
elif [ -d "$HOME/.claude/skills/gstack" ]; then
  INSTALL_TYPE="vendored-global"
  INSTALL_DIR="$HOME/.claude/skills/gstack"
else
  echo "ERROR: gstack not found"
  exit 1
fi
echo "Install type: $INSTALL_TYPE at $INSTALL_DIR"
```

---

### Phase C: Save Old Version

```bash
OLD_VERSION=$(cat "$INSTALL_DIR/VERSION" 2>/dev/null || echo "unknown")
```

---

### Phase D: Upgrade

**Git installs** (global-git, local-git):
```bash
cd "$INSTALL_DIR"
STASH_OUTPUT=$(git stash 2>&1)
git fetch origin
git reset --hard origin/main
./setup
```
If stash output contains "Saved working directory", warn: "Note: local changes were stashed. Run `git stash pop` in the skill directory to restore them."

**Vendored installs** (vendored, vendored-global):
```bash
PARENT=$(dirname "$INSTALL_DIR")
TMP_DIR=$(mktemp -d)
git clone --depth 1 https://github.com/garrytan/gstack.git "$TMP_DIR/gstack"
mv "$INSTALL_DIR" "$INSTALL_DIR.bak"
mv "$TMP_DIR/gstack" "$INSTALL_DIR"
cd "$INSTALL_DIR" && ./setup
rm -rf "$INSTALL_DIR.bak" "$TMP_DIR"
```

On failure: restore from `.bak`, warn the user, stop.

---

### Phase E: Sync Local Vendored Copy

Check whether there's a local vendored copy that also needs updating:

```bash
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
LOCAL_GSTACK=""
if [ -n "$_ROOT" ] && [ -d "$_ROOT/.claude/skills/gstack" ]; then
  _RESOLVED_LOCAL=$(cd "$_ROOT/.claude/skills/gstack" && pwd -P)
  _RESOLVED_PRIMARY=$(cd "$INSTALL_DIR" && pwd -P)
  if [ "$_RESOLVED_LOCAL" != "$_RESOLVED_PRIMARY" ]; then
    LOCAL_GSTACK="$_ROOT/.claude/skills/gstack"
  fi
fi
echo "LOCAL_GSTACK=$LOCAL_GSTACK"
```

If `LOCAL_GSTACK` is non-empty, sync it from the freshly-upgraded primary:
```bash
mv "$LOCAL_GSTACK" "$LOCAL_GSTACK.bak"
cp -Rf "$INSTALL_DIR" "$LOCAL_GSTACK"
rm -rf "$LOCAL_GSTACK/.git"
cd "$LOCAL_GSTACK" && ./setup
rm -rf "$LOCAL_GSTACK.bak"
```

Tell user: "Also updated vendored copy at `$LOCAL_GSTACK` — commit `.claude/skills/gstack/` when you're ready."

On failure: restore from `.bak` and warn.

---

### Phase F: Write Upgrade Marker + Clear Cache

```bash
mkdir -p ~/.gstack
echo "$OLD_VERSION" > ~/.gstack/just-upgraded-from
rm -f ~/.gstack/last-update-check
rm -f ~/.gstack/update-snoozed
```

---

### Phase G: Show What's New

Read `$INSTALL_DIR/CHANGELOG.md`. Find all version entries between `$OLD_VERSION` and the new version. Summarize as 5-7 bullets, grouped by theme. Focus on user-facing changes. Skip internal refactors unless significant.

Format:
```
gstack v{new} — upgraded from v{old}!

What's new:
- [bullet 1]
- ...

Happy shipping!
```

---

### Standalone Invocation (no preamble trigger)

When called directly (not from a preamble `UPGRADE_AVAILABLE` signal):

1. Force a fresh update check:
```bash
~/.claude/skills/gstack/bin/gstack-update-check --force 2>/dev/null || \
.claude/skills/gstack/bin/gstack-update-check --force 2>/dev/null || true
```

2. If `UPGRADE_AVAILABLE <old> <new>` in output: run Phases B–G above.

3. If no upgrade signal: check for a stale local vendored copy.
   - Run Phase B to detect primary install type and directory.
   - Run the LOCAL_GSTACK detection from Phase E.
   - If `LOCAL_GSTACK` empty: "You're already on the latest version (v{version})."
   - If `LOCAL_GSTACK` non-empty: compare versions:
     ```bash
     PRIMARY_VER=$(cat "$INSTALL_DIR/VERSION" 2>/dev/null || echo "unknown")
     LOCAL_VER=$(cat "$LOCAL_GSTACK/VERSION" 2>/dev/null || echo "unknown")
     ```
     - If versions differ: run Phase E sync, tell user.
     - If versions match: "You're on the latest version (v{PRIMARY_VER}). Global and local vendored copy are both up to date."

## Quality Gates

- [ ] Auto-upgrade config is checked before prompting the user
- [ ] Snooze writes escalating backoff level (24h → 48h → 1 week), capped at 3
- [ ] Install type is detected before attempting upgrade (no hardcoded paths)
- [ ] Old version is saved before the upgrade begins
- [ ] Local stash is flagged when git stash saves changes
- [ ] Local vendored copy is synced if it differs from the primary (by resolved path, not just path string)
- [ ] Upgrade marker and cache files are written after success
- [ ] Changelog summary covers only the delta between old and new versions
- [ ] On any failure: backup is restored and user is warned

## Outputs

- Updated gstack skill files at the detected install directory
- Synced local vendored copy (if applicable)
- `~/.gstack/just-upgraded-from` marker file
- Changelog summary displayed to user
- (Optional) `auto_upgrade: true` written to gstack config if user selected "always"

## Feeds Into

- Any skill that was originally invoked (upgrade is transparent — the original skill continues after)
- >ship (after upgrading, resume whatever workflow triggered the upgrade)

## Harness Notes

The upgrade runs entirely via terminal commands — no file-edit tools required except for vendored installs where `cp`/`mv` moves directories. The `AskUserQuestion` interaction (consent step) maps to any harness-native prompt mechanism; in harnesses without structured prompts, present the four options as a numbered list and ask for input. The `gstack-config` binary and `gstack-update-check` binary are bundled with the gstack install — they will be present after any successful install.
