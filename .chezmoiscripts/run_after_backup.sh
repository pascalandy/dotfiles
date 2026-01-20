#!/usr/bin/env bash

# Exit on error, treat unset variables as error, exit on pipe failure
set -euo pipefail

# Function to log messages
log() {
	echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

fct_copy_dir() {
	local src_dir="$1"
	local dst_dir="$2"

	if [[ ! -d "$src_dir" ]]; then
		log "Error: Source directory $src_dir does not exist"
		return 1
	fi

	mkdir -p "$dst_dir"
	log "Copying from $src_dir to $dst_dir"
	rsync -a --delete "$src_dir"/ "$dst_dir"/
}

fct_copy_file() {
	local src_file="$1"
	local dst_file="$2"
	local dst_parent

	if [[ ! -f "$src_file" ]]; then
		log "Warning: Source file $src_file does not exist"
		return 0
	fi

	dst_parent="$(dirname "$dst_file")"
	mkdir -p "$dst_parent"

	if [[ -f "$dst_file" ]] && cmp -s "$src_file" "$dst_file"; then
		log "File up to date: $dst_file"
		return 0
	fi

	log "Copying file from $src_file to $dst_file"
	cp "$src_file" "$dst_file"
}

log "Starting post-apply backup script"

# Backup tree file to repo
TREE_SRC="$HOME/Documents/_my_docs/42_tree_of_my_dir_files/z_archive/tree_my_docs.txt"
TREE_DST="$HOME/.local/share/chezmoi/backup_tree_my_docs.txt"
fct_copy_file "$TREE_SRC" "$TREE_DST"

# Sync opencode commands and skills to all AI coding tools
OPENCODE_SRC="$HOME/.local/share/chezmoi/dot_config/opencode"
OPENCODE_COMMAND_SRC="$OPENCODE_SRC/command"
OPENCODE_SKILL_SRC="$OPENCODE_SRC/skill"

# Claude Code
fct_copy_dir "$OPENCODE_COMMAND_SRC" "$HOME/.claude/commands"
fct_copy_dir "$OPENCODE_SKILL_SRC" "$HOME/.claude/skills"

# Codex
fct_copy_dir "$OPENCODE_COMMAND_SRC" "$HOME/.codex/prompts"
fct_copy_dir "$OPENCODE_SKILL_SRC" "$HOME/.codex/skills"

# Gemini
fct_copy_dir "$OPENCODE_COMMAND_SRC" "$HOME/.gemini/commands"

# Amp
fct_copy_dir "$OPENCODE_COMMAND_SRC" "$HOME/.config/amp/commands"
fct_copy_dir "$OPENCODE_SKILL_SRC" "$HOME/.config/amp/skills"

# Agents
fct_copy_dir "$OPENCODE_COMMAND_SRC" "$HOME/.config/agents/commands"
fct_copy_dir "$OPENCODE_SKILL_SRC" "$HOME/.config/agents/skills"

# OpenCode
fct_copy_dir "$OPENCODE_COMMAND_SRC" "$HOME/.config/opencode/command"
fct_copy_dir "$OPENCODE_SKILL_SRC" "$HOME/.config/opencode/skill"

log "Post-apply backup script completed successfully"
