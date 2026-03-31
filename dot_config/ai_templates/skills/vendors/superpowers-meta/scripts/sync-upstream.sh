#!/usr/bin/env bash
set -euo pipefail

# sync-upstream.sh -- Detect source project changes since last sync using git diff
#
# Usage:
#   ./sync-upstream.sh              Show what changed since last sync
#   ./sync-upstream.sh --prompt     Generate an agent prompt to apply delta updates
#   ./sync-upstream.sh --lock       Update UPSTREAM.lock to current HEAD
#   ./sync-upstream.sh --verbose    Show full diffs for changed skills

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOCK_FILE="$PACKAGE_DIR/UPSTREAM.lock"
REFERENCES_DIR="$PACKAGE_DIR/references"

# Source project path
SOURCE_PATH="/Users/andy16/Documents/github_local/SKILLS_MONO/vendors/obra-superpowers"

# Skill map: reference_name -> source_directory_name
declare -A SKILL_MAP=(
	[brainstorming]="brainstorming"
	[dispatching - parallel - agents]="dispatching-parallel-agents"
	[executing - plans]="executing-plans"
	[finishing - a - development - branch]="finishing-a-development-branch"
	[receiving - code - review]="receiving-code-review"
	[requesting - code - review]="requesting-code-review"
	[subagent - driven - development]="subagent-driven-development"
	[systematic - debugging]="systematic-debugging"
	[test - driven - development]="test-driven-development"
	[using - git - worktrees]="using-git-worktrees"
	[using - superpowers]="using-superpowers"
	[verification - before - completion]="verification-before-completion"
	[writing - plans]="writing-plans"
	[writing - skills]="writing-skills"
)

# Resolve git root and prefix for the source (may be a subdirectory of a repo)
if ! GIT_ROOT="$(git -C "$SOURCE_PATH" rev-parse --show-toplevel 2>/dev/null)"; then
	echo "ERROR: $SOURCE_PATH is not inside a git repository" >&2
	exit 1
fi

GIT_PREFIX="$(git -C "$SOURCE_PATH" rev-parse --show-prefix 2>/dev/null)"

# Read baseline commit from lock file
fct_read_baseline() {
	if [[ ! -f "$LOCK_FILE" ]]; then
		echo ""
		return
	fi
	local commit
	commit="$(sed -n 's/^upstream_commit=//p' "$LOCK_FILE")"
	echo "$commit"
}

# Get current HEAD of source repo
fct_current_head() {
	git -C "$GIT_ROOT" rev-parse HEAD
}

# Get short hash
fct_short_hash() {
	local hash="$1"
	echo "${hash:0:10}"
}

# Detect changed skills between baseline and HEAD
fct_detect_changes() {
	local baseline="$1"
	local head="$2"
	local changed_files

	if [[ -z "$baseline" ]]; then
		echo "WARNING: No baseline commit in UPSTREAM.lock. Comparing against initial commit." >&2
		changed_files="$(git -C "$GIT_ROOT" diff --name-only "$(git -C "$GIT_ROOT" rev-list --max-parents=0 HEAD)".."$head" -- "${GIT_PREFIX}skills/")"
	else
		changed_files="$(git -C "$GIT_ROOT" diff --name-only "$baseline".."$head" -- "${GIT_PREFIX}skills/")"
	fi

	echo "$changed_files"
}

# Extract skill name from a changed file path
fct_skill_from_path() {
	local path="$1"
	# Remove prefix up to skills/
	local rel="${path#*skills/}"
	# Get first directory component
	echo "${rel%%/*}"
}

# Get insertion/deletion stats for a skill
fct_diff_stats() {
	local baseline="$1"
	local head="$2"
	local skill_dir="$3"

	if [[ -z "$baseline" ]]; then
		git -C "$GIT_ROOT" diff --stat "$(git -C "$GIT_ROOT" rev-list --max-parents=0 HEAD)".."$head" -- "${GIT_PREFIX}skills/$skill_dir/" 2>/dev/null | tail -1
	else
		git -C "$GIT_ROOT" diff --stat "$baseline".."$head" -- "${GIT_PREFIX}skills/$skill_dir/" 2>/dev/null | tail -1
	fi
}

# Detect new skills not in SKILL_MAP
fct_detect_new_skills() {
	local new_skills=()
	for dir in "$SOURCE_PATH/skills"/*/; do
		[[ -d "$dir" ]] || continue
		local name
		name="$(basename "$dir")"
		[[ "$name" == ".DS_Store" ]] && continue
		local found=false
		for ref_name in "${!SKILL_MAP[@]}"; do
			if [[ "${SKILL_MAP[$ref_name]}" == "$name" ]]; then
				found=true
				break
			fi
		done
		if [[ "$found" == "false" ]]; then
			new_skills+=("$name")
		fi
	done
	echo "${new_skills[*]:-}"
}

# --- MODE: default (show changes) ---
fct_mode_default() {
	local baseline head changed_files
	baseline="$(fct_read_baseline)"
	head="$(fct_current_head)"

	if [[ -z "$baseline" ]]; then
		echo "No baseline commit found. Run with --lock to set initial baseline."
		echo ""
	fi

	echo "Source:   $SOURCE_PATH"
	echo "Baseline: $(fct_short_hash "${baseline:-none}")"
	echo "Current:  $(fct_short_hash "$head")"
	echo ""

	changed_files="$(fct_detect_changes "$baseline" "$head")"

	if [[ -z "$changed_files" ]]; then
		echo "No changes detected since last sync."
		return
	fi

	# Collect unique skill names that changed
	declare -A changed_skills
	while IFS= read -r file; do
		[[ -z "$file" ]] && continue
		local skill_name
		skill_name="$(fct_skill_from_path "$file")"
		changed_skills["$skill_name"]=1
	done <<<"$changed_files"

	local count=0
	echo "Changed skills:"
	echo "| Skill | Status | Stats |"
	echo "|-------|--------|-------|"
	for skill_name in $(echo "${!changed_skills[@]}" | tr ' ' '\n' | sort); do
		local status="modified"
		local has_ref=false
		for ref_name in "${!SKILL_MAP[@]}"; do
			if [[ "${SKILL_MAP[$ref_name]}" == "$skill_name" ]]; then
				has_ref=true
				break
			fi
		done
		if [[ "$has_ref" == "false" ]]; then
			status="NEW"
		fi
		local stats
		stats="$(fct_diff_stats "$baseline" "$head" "$skill_name")"
		echo "| $skill_name | $status | $stats |"
		count=$((count + 1))
	done
	echo ""
	echo "Total: $count skill(s) changed."

	# Check for new skills not in map
	local new_skills
	new_skills="$(fct_detect_new_skills)"
	if [[ -n "$new_skills" ]]; then
		echo ""
		echo "New skills detected (not in skill map):"
		for s in $new_skills; do
			echo "  - $s"
		done
	fi
}

# --- MODE: verbose (show diffs) ---
fct_mode_verbose() {
	local baseline head changed_files
	baseline="$(fct_read_baseline)"
	head="$(fct_current_head)"

	fct_mode_default

	echo ""
	echo "=== Diffs (first 40 lines each) ==="

	changed_files="$(fct_detect_changes "$baseline" "$head")"
	declare -A shown_skills
	while IFS= read -r file; do
		[[ -z "$file" ]] && continue
		local skill_name
		skill_name="$(fct_skill_from_path "$file")"
		if [[ -z "${shown_skills[$skill_name]:-}" ]]; then
			shown_skills["$skill_name"]=1
			echo ""
			echo "--- $skill_name ---"
			if [[ -z "$baseline" ]]; then
				git -C "$GIT_ROOT" diff "$(git -C "$GIT_ROOT" rev-list --max-parents=0 HEAD)".."$head" -- "${GIT_PREFIX}skills/$skill_name/" 2>/dev/null | head -40
			else
				git -C "$GIT_ROOT" diff "$baseline".."$head" -- "${GIT_PREFIX}skills/$skill_name/" 2>/dev/null | head -40
			fi
		fi
	done <<<"$changed_files"
}

# --- MODE: prompt (generate agent prompt) ---
fct_mode_prompt() {
	local baseline head changed_files
	baseline="$(fct_read_baseline)"
	head="$(fct_current_head)"

	if [[ -z "$baseline" ]]; then
		echo "ERROR: No baseline commit. Run --lock first." >&2
		exit 1
	fi

	changed_files="$(fct_detect_changes "$baseline" "$head")"

	if [[ -z "$changed_files" ]]; then
		echo "No changes to sync."
		return
	fi

	declare -A changed_skills
	while IFS= read -r file; do
		[[ -z "$file" ]] && continue
		local skill_name
		skill_name="$(fct_skill_from_path "$file")"
		changed_skills["$skill_name"]=1
	done <<<"$changed_files"

	cat <<'PROMPT_HEADER'
You are applying upstream delta updates to distilled reference files.

RULES:
- Read the git diff for each skill
- Read the current distilled reference file
- Apply ONLY the changes (do not re-distill from scratch)
- Use harness-agnostic language
- Preserve all existing content that was not changed upstream
- For new skills, create from scratch using the reference file template

PROMPT_HEADER

	echo "## Changed Skills"
	echo ""
	for skill_name in $(echo "${!changed_skills[@]}" | tr ' ' '\n' | sort); do
		local ref_name=""
		for r in "${!SKILL_MAP[@]}"; do
			if [[ "${SKILL_MAP[$r]}" == "$skill_name" ]]; then
				ref_name="$r"
				break
			fi
		done

		if [[ -n "$ref_name" ]]; then
			echo "### $skill_name (MODIFIED)"
			echo "- Source: $SOURCE_PATH/skills/$skill_name/SKILL.md"
			echo "- Distilled: $REFERENCES_DIR/$ref_name.md"
			echo "- Diff: \`git -C \"$GIT_ROOT\" diff $baseline..$head -- \"${GIT_PREFIX}skills/$skill_name/\"\`"
			echo ""
		else
			echo "### $skill_name (NEW)"
			echo "- Source: $SOURCE_PATH/skills/$skill_name/SKILL.md"
			echo "- Distilled: $REFERENCES_DIR/$skill_name.md (create new)"
			echo "- Action: Create from scratch using the reference file template"
			echo ""
		fi
	done

	echo "## After Applying"
	echo ""
	echo "Run: \`$SCRIPT_DIR/sync-upstream.sh --lock\`"
}

# --- MODE: lock (update UPSTREAM.lock) ---
fct_mode_lock() {
	local head
	head="$(fct_current_head)"
	local version="unknown"

	if [[ -f "$SOURCE_PATH/package.json" ]]; then
		version="$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' "$SOURCE_PATH/package.json")"
	fi

	cat >"$LOCK_FILE" <<EOF
## superpowers upstream lock
## Records which source commit was used to generate/update the references.
## Do not edit manually. Updated by scripts/sync-upstream.sh after a successful sync.

upstream_repo=$SOURCE_PATH
upstream_commit=$head
upstream_version=$version
synced_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

	echo "UPSTREAM.lock updated:"
	echo "  commit:  $(fct_short_hash "$head")"
	echo "  version: $version"
	echo "  time:    $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}

# --- Main ---
case "${1:-}" in
--prompt)
	fct_mode_prompt
	;;
--lock)
	fct_mode_lock
	;;
--verbose)
	fct_mode_verbose
	;;
--help | -h)
	echo "Usage: sync-upstream.sh [--prompt|--lock|--verbose|--help]"
	echo ""
	echo "  (default)   Show what changed since last sync"
	echo "  --prompt    Generate agent prompt to apply delta updates"
	echo "  --lock      Update UPSTREAM.lock to current HEAD"
	echo "  --verbose   Show full diffs for changed skills"
	;;
"")
	fct_mode_default
	;;
*)
	echo "Unknown option: $1" >&2
	echo "Run with --help for usage." >&2
	exit 1
	;;
esac
