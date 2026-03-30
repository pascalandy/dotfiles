#!/usr/bin/env bash
set -euo pipefail

# sync-upstream.sh — Detect GStack changes since last sync using git diff
#
# Usage:
#   ./sync-upstream.sh              Show what changed since last sync
#   ./sync-upstream.sh --prompt     Generate an agent prompt to apply the updates
#   ./sync-upstream.sh --lock       Update UPSTREAM.lock to current HEAD (run after applying updates)
#   ./sync-upstream.sh --verbose    Show full diffs for changed skills
#
# Reads UPSTREAM.lock for the baseline commit, compares against current GStack HEAD.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
GSMETA_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
GSMETA_REFS="$GSMETA_DIR/references"
LOCK_FILE="$GSMETA_DIR/UPSTREAM.lock"

GSTACK_SOURCE="${GSTACK_SOURCE:-$HOME/Documents/github_local/SKILLS_MONO/vendors/garrytan-gstack}"

MODE="${1:-}"

# Git root and relative prefix (GStack may be a subdirectory of a larger repo)
GIT_ROOT="$(git -C "$GSTACK_SOURCE" rev-parse --show-toplevel)"
GIT_PREFIX="$(git -C "$GSTACK_SOURCE" rev-parse --show-prefix)"

# ── Skill map ──────────────────────────────────────────────
# Maps gsmeta reference name -> GStack skill directory
# "browse" is special: its SKILL.md is at the repo root
declare -A SKILL_MAP=(
	["office-hours"]="office-hours"
	["plan-ceo-review"]="plan-ceo-review"
	["plan-eng-review"]="plan-eng-review"
	["plan-design-review"]="plan-design-review"
	["design-consultation"]="design-consultation"
	["design-shotgun"]="design-shotgun"
	["autoplan"]="autoplan"
	["investigate"]="investigate"
	["review"]="review"
	["codex"]="codex"
	["cso"]="cso"
	["qa"]="qa"
	["qa-only"]="qa-only"
	["design-review"]="design-review"
	["benchmark"]="benchmark"
	["ship"]="ship"
	["land-and-deploy"]="land-and-deploy"
	["canary"]="canary"
	["document-release"]="document-release"
	["retro"]="retro"
	["browse"]="SKILL.md"
	["connect-chrome"]="connect-chrome"
	["setup-browser-cookies"]="setup-browser-cookies"
	["setup-deploy"]="setup-deploy"
	["learn"]="learn"
	["careful"]="careful"
	["freeze"]="freeze"
	["guard"]="guard"
	["unfreeze"]="unfreeze"
	["gstack-upgrade"]="gstack-upgrade"
)

# ── Helpers ────────────────────────────────────────────────

fct_read_lock() {
	if [[ ! -f "$LOCK_FILE" ]]; then
		echo ""
		return
	fi
	sed -n 's/^upstream_commit=//p' "$LOCK_FILE"
}

fct_get_skill_path() {
	local skill_dir="$1"
	if [[ "$skill_dir" == "SKILL.md" ]]; then
		echo "SKILL.md"
	else
		echo "$skill_dir/SKILL.md"
	fi
}

fct_check_prereqs() {
	if [[ ! -d "$GSTACK_SOURCE" ]]; then
		echo "ERROR: GStack source not found: $GSTACK_SOURCE"
		echo "Set GSTACK_SOURCE env var to the correct path."
		exit 1
	fi

	if ! git -C "$GSTACK_SOURCE" rev-parse --git-dir &>/dev/null; then
		echo "ERROR: $GSTACK_SOURCE is not inside a git repository."
		exit 1
	fi
}

# ── Lock command ───────────────────────────────────────────

fct_lock() {
	local current_head
	current_head="$(git -C "$GIT_ROOT" rev-parse HEAD)"
	local current_version="unknown"
	if [[ -f "$GSTACK_SOURCE/VERSION" ]]; then
		current_version="$(cat "$GSTACK_SOURCE/VERSION")"
	fi
	local now
	now="$(date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S%z')"

	cat >"$LOCK_FILE" <<EOF
## gsmeta upstream lock
## This file records which GStack commit was used to generate/update the references.
## Do not edit manually. Updated by scripts/sync-upstream.sh after a successful sync.

upstream_repo=$GSTACK_SOURCE
upstream_commit=$current_head
upstream_version=$current_version
synced_at=$now
EOF

	echo "UPSTREAM.lock updated."
	echo "  commit:  $current_head"
	echo "  version: $current_version"
	echo "  time:    $now"
}

# ── Diff command (default) ─────────────────────────────────

fct_diff() {
	local baseline_commit
	baseline_commit="$(fct_read_lock)"

	local current_head
	current_head="$(git -C "$GIT_ROOT" rev-parse HEAD)"

	local current_version="unknown"
	if [[ -f "$GSTACK_SOURCE/VERSION" ]]; then
		current_version="$(cat "$GSTACK_SOURCE/VERSION")"
	fi

	echo "=== gsmeta sync-upstream (git diff mode) ==="
	echo "GStack source:  $GSTACK_SOURCE"
	echo "GStack version: $current_version"
	echo "GStack HEAD:    ${current_head:0:12}"
	echo ""

	if [[ -z "$baseline_commit" ]]; then
		echo "WARNING: No UPSTREAM.lock found. Cannot diff."
		echo "Run: ./sync-upstream.sh --lock  (to set baseline)"
		exit 1
	fi

	local baseline_short="${baseline_commit:0:12}"
	local head_short="${current_head:0:12}"

	echo "Baseline:       $baseline_short"
	echo "Current:        $head_short"
	echo ""

	if [[ "$baseline_commit" == "$current_head" ]]; then
		echo "No changes. GStack HEAD matches baseline."
		fct_scan_new_skills
		exit 0
	fi

	# Count commits between baseline and HEAD
	local commit_count
	commit_count="$(git -C "$GIT_ROOT" rev-list --count "$baseline_commit..$current_head")"
	echo "Commits since baseline: $commit_count"
	echo ""

	# Find which SKILL.md files changed (scoped to GStack subdirectory)
	local changed_files
	changed_files="$(git -C "$GIT_ROOT" diff --name-only "$baseline_commit..$current_head" -- "${GIT_PREFIX}*/SKILL.md" "${GIT_PREFIX}SKILL.md" | sed "s|^${GIT_PREFIX}||")"

	if [[ -z "$changed_files" ]]; then
		echo "No SKILL.md files changed."
		fct_scan_new_skills
		echo ""
		echo "Run: ./sync-upstream.sh --lock  (to update baseline)"
		exit 0
	fi

	# Map changed files back to gsmeta references
	local count_changed=0
	local changed_skills=()

	printf "%-25s %-12s %s\n" "SKILL" "STATUS" "CHANGES"
	printf "%-25s %-12s %s\n" "-----" "------" "-------"

	for ref_name in $(printf '%s\n' "${!SKILL_MAP[@]}" | sort); do
		local skill_path
		skill_path="$(fct_get_skill_path "${SKILL_MAP[$ref_name]}")"

		if echo "$changed_files" | grep -q "^${skill_path}$"; then
			# Get a one-line summary of what changed
			local stat_line
			stat_line="$(git -C "$GIT_ROOT" diff --stat "$baseline_commit..$current_head" -- "${GIT_PREFIX}${skill_path}" | head -1)"
			local insertions deletions
			insertions="$(echo "$stat_line" | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo 0)"
			deletions="$(echo "$stat_line" | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo 0)"

			printf "%-25s %-12s +%s/-%s lines\n" "$ref_name" "CHANGED" "$insertions" "$deletions"
			changed_skills+=("$ref_name")
			count_changed=$((count_changed + 1))

			if [[ "$MODE" == "--verbose" ]]; then
				echo "  --- diff ---"
				git -C "$GIT_ROOT" diff "$baseline_commit..$current_head" -- "${GIT_PREFIX}${skill_path}" | head -40
				echo "  --- end ---"
				echo ""
			fi
		fi
	done

	echo ""
	echo "Changed: $count_changed / ${#SKILL_MAP[@]} skills"

	fct_scan_new_skills

	echo ""
	echo "Next steps:"
	echo "  1. ./sync-upstream.sh --prompt    Generate agent prompt to apply updates"
	echo "  2. (run the agent with the prompt)"
	echo "  3. ./sync-upstream.sh --lock      Update baseline after applying"
}

# ── Scan for new skills ────────────────────────────────────

fct_scan_new_skills() {
	echo ""
	echo "--- Scanning for new upstream skills ---"
	local count_new=0

	for dir in "$GSTACK_SOURCE"/*/; do
		local dir_name
		dir_name="$(basename "$dir")"
		local skill_md="$dir/SKILL.md"

		[[ ! -f "$skill_md" ]] && continue

		case "$dir_name" in
		bin | browse | design | docs | extension | lib | scripts | supabase | test | agents | setup) continue ;;
		esac

		local found=false
		for mapped_dir in "${SKILL_MAP[@]}"; do
			if [[ "$mapped_dir" == "$dir_name" ]]; then
				found=true
				break
			fi
		done

		if [[ "$found" == "false" ]]; then
			printf "%-25s %-12s %s\n" "$dir_name" "NEW" "Not in gsmeta"
			count_new=$((count_new + 1))
		fi
	done

	if [[ "$count_new" -eq 0 ]]; then
		echo "(none)"
	fi
}

# ── Prompt command ─────────────────────────────────────────

fct_prompt() {
	local baseline_commit
	baseline_commit="$(fct_read_lock)"

	local current_head
	current_head="$(git -C "$GIT_ROOT" rev-parse HEAD)"

	if [[ -z "$baseline_commit" ]]; then
		echo "ERROR: No UPSTREAM.lock found. Run: ./sync-upstream.sh --lock"
		exit 1
	fi

	if [[ "$baseline_commit" == "$current_head" ]]; then
		echo "No changes. Nothing to update."
		exit 0
	fi

	# Find changed SKILL.md files
	local changed_files
	changed_files="$(git -C "$GSTACK_SOURCE" diff --name-only "$baseline_commit..$current_head" -- '*/SKILL.md' 'SKILL.md')"

	if [[ -z "$changed_files" ]]; then
		echo "No SKILL.md files changed. Nothing to update."
		exit 0
	fi

	# Build the list of changed skills
	local changed_skills=()
	for ref_name in $(printf '%s\n' "${!SKILL_MAP[@]}" | sort); do
		local skill_path
		skill_path="$(fct_get_skill_path "${SKILL_MAP[$ref_name]}")"
		if echo "$changed_files" | grep -q "^${skill_path}$"; then
			changed_skills+=("$ref_name")
		fi
	done

	# Scan for new skills
	local new_skills=()
	for dir in "$GSTACK_SOURCE"/*/; do
		local dir_name
		dir_name="$(basename "$dir")"
		[[ ! -f "$dir/SKILL.md" ]] && continue
		case "$dir_name" in
		bin | browse | design | docs | extension | lib | scripts | supabase | test | agents | setup) continue ;;
		esac
		local found=false
		for mapped_dir in "${SKILL_MAP[@]}"; do
			[[ "$mapped_dir" == "$dir_name" ]] && found=true && break
		done
		[[ "$found" == "false" ]] && new_skills+=("$dir_name")
	done

	# Generate the prompt
	cat <<PROMPT
You are updating the gsmeta meta-skill references to match upstream GStack changes.

## Context

GStack repo: $GSTACK_SOURCE
Baseline commit: $baseline_commit
Current HEAD:    $current_head

To see the full diff, run in terminal:
  git -C $GSTACK_SOURCE diff $baseline_commit..$current_head -- '*/SKILL.md' 'SKILL.md'

## Changed Skills (${#changed_skills[@]})

PROMPT

	for skill in "${changed_skills[@]}"; do
		local skill_path
		skill_path="$(fct_get_skill_path "${SKILL_MAP[$skill]}")"
		echo "### $skill"
		echo ""
		echo "Original: \`$GSTACK_SOURCE/$skill_path\`"
		echo "Distilled: \`$GSMETA_REFS/$skill.md\`"
		echo ""
		echo "Diff:"
		echo '```'
		git -C "$GSTACK_SOURCE" diff --stat "$baseline_commit..$current_head" -- "$skill_path"
		echo '```'
		echo ""
	done

	if [[ ${#new_skills[@]} -gt 0 ]]; then
		cat <<PROMPT

## New Skills (${#new_skills[@]})

These are new upstream skills that need distilled references created:

PROMPT
		for skill in "${new_skills[@]}"; do
			echo "- \`$skill\` -> create \`$GSMETA_REFS/$skill.md\`"
		done
		echo ""
	fi

	cat <<'PROMPT'

## Instructions

For each CHANGED skill above:

1. Run the git diff command to see exactly what changed in the original SKILL.md
2. Read the current distilled reference file
3. Apply ONLY the changes from the diff to the distilled reference
4. Keep the same distilled format (harness-agnostic language, same section structure)

Rules:
- Do NOT re-distill from scratch. Apply the delta only.
- "read the file" not "use Read tool", "run in terminal" not "use Bash tool"
- Do NOT restore preamble, telemetry, YAML frontmatter, Voice, Contributor Mode
- DO restore: methodology changes, new rules, updated checklists, new modes, changed quality gates

For each NEW skill:
1. Read the original SKILL.md
2. Create a new distilled reference following the standard template (see any existing reference for format)

After all updates are applied, run:
  bash <GSMETA_DIR>/scripts/sync-upstream.sh --lock

to update the baseline.
PROMPT

	# Replace <GSMETA_DIR> placeholder
	echo ""
	echo "Lock command: \`bash $GSMETA_DIR/scripts/sync-upstream.sh --lock\`"
}

# ── Main ───────────────────────────────────────────────────

fct_check_prereqs

case "$MODE" in
--lock)
	fct_lock
	;;
--prompt)
	fct_prompt
	;;
--verbose)
	fct_diff
	;;
*)
	fct_diff
	;;
esac
