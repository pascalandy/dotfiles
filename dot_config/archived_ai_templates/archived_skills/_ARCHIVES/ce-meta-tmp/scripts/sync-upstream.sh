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
META_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOCK_FILE="$META_DIR/UPSTREAM.lock"
REFERENCES_DIR="$META_DIR/references"

# Source project location
SOURCE_PATH="/Users/andy16/Documents/github_local/SKILLS_MONO/vendors/everyinc-compound-engineering-plugin"
SKILLS_SUBDIR="plugins/compound-engineering/skills"

# Detect git root and prefix for the source (it may be a subdirectory of a larger repo)
GIT_ROOT=""
GIT_PREFIX=""
fct_detect_git_layout() {
	GIT_ROOT="$(git -C "$SOURCE_PATH" rev-parse --show-toplevel 2>/dev/null)" || {
		echo "ERROR: $SOURCE_PATH is not inside a git repository." >&2
		exit 1
	}
	GIT_PREFIX="$(git -C "$SOURCE_PATH" rev-parse --show-prefix 2>/dev/null)" || true
}

# Skill map: reference_name -> source_directory_name
declare -A SKILL_MAP=(
	["agent-browser"]="agent-browser"
	["agent-native-architecture"]="agent-native-architecture"
	["agent-native-audit"]="agent-native-audit"
	["andrew-kane-gem-writer"]="andrew-kane-gem-writer"
	["ce-brainstorm"]="ce-brainstorm"
	["ce-compound"]="ce-compound"
	["ce-compound-refresh"]="ce-compound-refresh"
	["ce-ideate"]="ce-ideate"
	["ce-plan"]="ce-plan"
	["ce-review"]="ce-review"
	["ce-work"]="ce-work"
	["ce-work-beta"]="ce-work-beta"
	["changelog"]="changelog"
	["claude-permissions-optimizer"]="claude-permissions-optimizer"
	["deploy-docs"]="deploy-docs"
	["dhh-rails-style"]="dhh-rails-style"
	["document-review"]="document-review"
	["dspy-ruby"]="dspy-ruby"
	["every-style-editor"]="every-style-editor"
	["feature-video"]="feature-video"
	["frontend-design"]="frontend-design"
	["gemini-imagegen"]="gemini-imagegen"
	["git-clean-gone-branches"]="git-clean-gone-branches"
	["git-commit"]="git-commit"
	["git-commit-push-pr"]="git-commit-push-pr"
	["git-worktree"]="git-worktree"
	["lfg"]="lfg"
	["onboarding"]="onboarding"
	["orchestrating-swarms"]="orchestrating-swarms"
	["proof"]="proof"
	["rclone"]="rclone"
	["report-bug-ce"]="report-bug-ce"
	["reproduce-bug"]="reproduce-bug"
	["resolve-pr-feedback"]="resolve-pr-feedback"
	["setup"]="setup"
	["slfg"]="slfg"
	["test-browser"]="test-browser"
	["test-xcode"]="test-xcode"
	["todo-create"]="todo-create"
	["todo-resolve"]="todo-resolve"
	["todo-triage"]="todo-triage"
)

fct_read_lock() {
	local commit=""
	if [[ -f "$LOCK_FILE" ]]; then
		commit="$(sed -n 's/^upstream_commit=//p' "$LOCK_FILE")"
	fi
	if [[ -z "$commit" ]]; then
		echo "WARNING: No UPSTREAM.lock found or no commit recorded. Showing all changes." >&2
		commit=""
	fi
	echo "$commit"
}

fct_current_head() {
	git -C "$GIT_ROOT" rev-parse HEAD
}

fct_changed_skills() {
	local baseline="$1"
	local head="$2"
	local skills_path="${GIT_PREFIX}${SKILLS_SUBDIR}/"
	local changed_files

	if [[ -z "$baseline" ]]; then
		# No baseline -- list all skill directories
		for ref_name in "${!SKILL_MAP[@]}"; do
			local src_dir="${SKILL_MAP[$ref_name]}"
			if [[ -d "$SOURCE_PATH/$SKILLS_SUBDIR/$src_dir" ]]; then
				echo "NEW $ref_name"
			fi
		done
		return
	fi

	changed_files="$(git -C "$GIT_ROOT" diff --name-only "$baseline".."$head" -- "$skills_path" 2>/dev/null)" || {
		echo "ERROR: Could not compute diff between $baseline and $head" >&2
		return 1
	}

	if [[ -z "$changed_files" ]]; then
		return 0
	fi

	# Extract unique skill directories from changed file paths
	local seen_skills=()
	while IFS= read -r file; do
		# Strip the prefix to get relative path under skills/
		local rel="${file#"$skills_path"}"
		local skill_dir="${rel%%/*}"
		# Check if we already saw this skill
		local already_seen=false
		for s in "${seen_skills[@]+"${seen_skills[@]}"}"; do
			if [[ "$s" == "$skill_dir" ]]; then
				already_seen=true
				break
			fi
		done
		if [[ "$already_seen" == "false" ]]; then
			seen_skills+=("$skill_dir")
		fi
	done <<<"$changed_files"

	# Classify each changed skill
	for skill_dir in "${seen_skills[@]}"; do
		local ref_name=""
		for rn in "${!SKILL_MAP[@]}"; do
			if [[ "${SKILL_MAP[$rn]}" == "$skill_dir" ]]; then
				ref_name="$rn"
				break
			fi
		done

		if [[ -z "$ref_name" ]]; then
			echo "NEW_UNMAPPED $skill_dir"
			continue
		fi

		if [[ ! -f "$REFERENCES_DIR/$ref_name.md" ]]; then
			echo "NEW $ref_name"
		else
			# Get insertion/deletion counts
			local stats
			stats="$(git -C "$GIT_ROOT" diff --stat "$baseline".."$head" -- "${skills_path}${skill_dir}/" 2>/dev/null | tail -1)"
			local insertions=0
			local deletions=0
			insertions="$(echo "$stats" | sed -n 's/.*\([0-9][0-9]*\) insertion.*/\1/p')" || true
			deletions="$(echo "$stats" | sed -n 's/.*\([0-9][0-9]*\) deletion.*/\1/p')" || true
			echo "CHANGED $ref_name +${insertions:-0}/-${deletions:-0}"
		fi
	done

	# Check for removed skills
	for ref_name in "${!SKILL_MAP[@]}"; do
		local src_dir="${SKILL_MAP[$ref_name]}"
		if [[ ! -d "$SOURCE_PATH/$SKILLS_SUBDIR/$src_dir" ]] && [[ -f "$REFERENCES_DIR/$ref_name.md" ]]; then
			echo "REMOVED $ref_name"
		fi
	done
}

fct_detect_new_skills() {
	# Scan source for directories not in SKILL_MAP
	local count=0
	for dir in "$SOURCE_PATH/$SKILLS_SUBDIR"/*/; do
		[[ -d "$dir" ]] || continue
		local dirname
		dirname="$(basename "$dir")"
		local found=false
		for rn in "${!SKILL_MAP[@]}"; do
			if [[ "${SKILL_MAP[$rn]}" == "$dirname" ]]; then
				found=true
				break
			fi
		done
		if [[ "$found" == "false" ]]; then
			echo "  UNMAPPED: $dirname (not in SKILL_MAP)"
			count=$((count + 1))
		fi
	done
	if [[ "$count" -eq 0 ]]; then
		echo "  None found."
	fi
}

fct_show_default() {
	local baseline="$1"
	local head="$2"

	echo "============================================"
	echo "  CE-META UPSTREAM SYNC STATUS"
	echo "============================================"
	echo ""
	if [[ -n "$baseline" ]]; then
		echo "Baseline: ${baseline:0:12}"
	else
		echo "Baseline: (none -- first sync)"
	fi
	echo "Current:  ${head:0:12}"
	echo ""

	local changes
	changes="$(fct_changed_skills "$baseline" "$head")"

	if [[ -z "$changes" ]]; then
		echo "No changes detected since last sync."
		echo ""
		echo "New source directories not in SKILL_MAP:"
		fct_detect_new_skills
		return
	fi

	echo "CHANGES:"
	echo "--------"
	printf "%-10s %-35s %s\n" "Status" "Skill" "Delta"
	printf "%-10s %-35s %s\n" "------" "-----" "-----"
	while IFS= read -r line; do
		local status="${line%% *}"
		local rest="${line#* }"
		local name="${rest%% *}"
		local delta="${rest#* }"
		if [[ "$delta" == "$name" ]]; then
			delta=""
		fi
		printf "%-10s %-35s %s\n" "$status" "$name" "$delta"
	done <<<"$changes"

	echo ""
	echo "New source directories not in SKILL_MAP:"
	fct_detect_new_skills
}

fct_show_verbose() {
	local baseline="$1"
	local head="$2"
	local skills_path="${GIT_PREFIX}${SKILLS_SUBDIR}/"

	fct_show_default "$baseline" "$head"

	echo ""
	echo "DIFFS (first 40 lines each):"
	echo "============================"

	local changes
	changes="$(fct_changed_skills "$baseline" "$head")"
	[[ -z "$changes" ]] && return

	while IFS= read -r line; do
		local status="${line%% *}"
		local rest="${line#* }"
		local name="${rest%% *}"

		if [[ "$status" == "CHANGED" ]] && [[ -n "$baseline" ]]; then
			local src_dir="${SKILL_MAP[$name]:-$name}"
			echo ""
			echo "--- $name ---"
			git -C "$GIT_ROOT" diff "$baseline".."$head" -- "${skills_path}${src_dir}/" 2>/dev/null | head -40
			echo "..."
		fi
	done <<<"$changes"
}

fct_generate_prompt() {
	local baseline="$1"
	local head="$2"

	local changes
	changes="$(fct_changed_skills "$baseline" "$head")"

	if [[ -z "$changes" ]]; then
		echo "No changes to sync."
		return
	fi

	cat <<'PROMPT_HEADER'
# CE-META Upstream Sync -- Delta Update Prompt

You are updating distilled reference files to reflect upstream changes.
For each CHANGED skill: read the git diff, read the current distilled reference, apply ONLY the delta changes (do not re-distill from scratch). Preserve manual improvements.
For each NEW skill: create from scratch using the standard reference template.
For each REMOVED skill: delete the reference file and remove from SKILL.md routing table.

Use harness-agnostic language throughout.

PROMPT_HEADER

	echo "## Changes to Apply"
	echo ""

	while IFS= read -r line; do
		local status="${line%% *}"
		local rest="${line#* }"
		local name="${rest%% *}"
		local src_dir="${SKILL_MAP[$name]:-$name}"

		case "$status" in
		CHANGED)
			echo "### CHANGED: $name"
			echo "- Source: $SOURCE_PATH/$SKILLS_SUBDIR/$src_dir/SKILL.md"
			echo "- Distilled: $REFERENCES_DIR/$name.md"
			echo "- Action: Read the diff below, apply delta to the distilled file"
			echo ""
			if [[ -n "$baseline" ]]; then
				echo '```diff'
				git -C "$GIT_ROOT" diff "$baseline".."$head" -- "${GIT_PREFIX}${SKILLS_SUBDIR}/${src_dir}/" 2>/dev/null || true
				echo '```'
			fi
			echo ""
			;;
		NEW)
			echo "### NEW: $name"
			echo "- Source: $SOURCE_PATH/$SKILLS_SUBDIR/$src_dir/SKILL.md"
			echo "- Distilled: $REFERENCES_DIR/$name.md (create new)"
			echo "- Action: Read the source and create from scratch using the reference template"
			echo ""
			;;
		NEW_UNMAPPED)
			echo "### NEW (UNMAPPED): $name"
			echo "- Source: $SOURCE_PATH/$SKILLS_SUBDIR/$name/"
			echo "- Action: Add to SKILL_MAP in sync-upstream.sh, then create reference file"
			echo ""
			;;
		REMOVED)
			echo "### REMOVED: $name"
			echo "- Distilled: $REFERENCES_DIR/$name.md (delete)"
			echo "- Action: Remove file and remove from SKILL.md routing table"
			echo ""
			;;
		esac
	done <<<"$changes"

	echo "## After Applying All Changes"
	echo ""
	echo "Run: \`./scripts/sync-upstream.sh --lock\` to update UPSTREAM.lock to current HEAD."
}

fct_update_lock() {
	local head
	head="$(fct_current_head)"
	local version="2.59.0"

	# Try to read version from package.json
	if [[ -f "$SOURCE_PATH/package.json" ]]; then
		local pkg_version
		pkg_version="$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' "$SOURCE_PATH/package.json" | head -1)" || true
		if [[ -n "$pkg_version" ]]; then
			version="$pkg_version"
		fi
	fi

	cat >"$LOCK_FILE" <<EOF
## ce-meta upstream lock
## Records which source commit was used to generate/update the references.
## Do not edit manually. Updated by scripts/sync-upstream.sh after a successful sync.

upstream_repo=$SOURCE_PATH
upstream_commit=$head
upstream_version=$version
synced_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

	echo "UPSTREAM.lock updated:"
	echo "  commit:  ${head:0:12}"
	echo "  version: $version"
	echo "  time:    $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}

# --- Main ---

fct_detect_git_layout

baseline="$(fct_read_lock)"
head="$(fct_current_head)"

case "${1:-}" in
--prompt)
	fct_generate_prompt "$baseline" "$head"
	;;
--lock)
	fct_update_lock
	;;
--verbose)
	fct_show_verbose "$baseline" "$head"
	;;
--help | -h)
	echo "Usage: sync-upstream.sh [--prompt|--lock|--verbose|--help]"
	echo ""
	echo "  (default)   Show what changed since last sync"
	echo "  --prompt    Generate an agent prompt to apply delta updates"
	echo "  --lock      Update UPSTREAM.lock to current HEAD"
	echo "  --verbose   Show full diffs for changed skills"
	;;
"")
	fct_show_default "$baseline" "$head"
	;;
*)
	echo "Unknown option: $1" >&2
	echo "Usage: sync-upstream.sh [--prompt|--lock|--verbose|--help]" >&2
	exit 1
	;;
esac
