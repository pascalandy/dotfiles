#!/usr/bin/env bash

set -Eeuo pipefail

log() {
	printf '%s - %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1"
}

log_info() {
	log "INFO: $1"
}

log_warn() {
	log "WARN: $1"
}

log_error() {
	log "ERROR: $1"
}

fct_copy_dir() {
	local src_dir="$1"
	local dst_dir="$2"
	local sync_mode="${3:-delete}"
	local -a extra_args=("${@:4}")
	local -a rsync_args

	rsync_args=(-a --exclude '.DS_Store')

	if [[ "$sync_mode" == "delete" ]]; then
		rsync_args+=(--delete)
	fi

	if [[ "${#extra_args[@]}" -gt 0 ]]; then
		rsync_args+=("${extra_args[@]}")
	fi

	if [[ ! -d "$src_dir" ]]; then
		log_error "Source directory does not exist: $src_dir"
		return 1
	fi

	if [[ "$src_dir" == "$dst_dir" ]]; then
		log_info "Source and destination are identical, skipping: $src_dir"
		return 0
	fi

	mkdir -p "$dst_dir"
	log_info "Syncing $src_dir -> $dst_dir (mode: $sync_mode)"
	rsync "${rsync_args[@]}" "$src_dir/" "$dst_dir/"
}

fct_copy_file() {
	local src_file="$1"
	local dst_file="$2"
	local dst_parent

	if [[ ! -f "$src_file" ]]; then
		log_warn "Source file does not exist: $src_file"
		return 0
	fi

	dst_parent="$(dirname "$dst_file")"
	mkdir -p "$dst_parent"

	if [[ -f "$dst_file" ]] && cmp -s "$src_file" "$dst_file"; then
		log_info "File already up to date: $dst_file"
		return 0
	fi

	log_info "Copying file $src_file -> $dst_file"
	cp "$src_file" "$dst_file"
}

fct_sync_agent_assets() {
	local commands_src="$1"
	local skills_src="$2"

	# Pi
	fct_copy_dir "$commands_src" "$HOME/.pi/agent/prompts"
	fct_copy_dir "$skills_src" "$HOME/.pi/agent/skills"

	# Claude Code
	fct_copy_dir "$commands_src" "$HOME/.claude/commands"
	fct_copy_dir "$skills_src" "$HOME/.claude/skills"

	# Codex
	fct_copy_dir "$commands_src" "$HOME/.codex/prompts"
	fct_copy_dir "$skills_src" "$HOME/.codex/skills"

	# Gemini
	fct_copy_dir "$commands_src" "$HOME/.gemini/commands"

	# Amp
	fct_copy_dir "$commands_src" "$HOME/.config/amp/commands"
	fct_copy_dir "$skills_src" "$HOME/.config/amp/skills"

	# Agents
	fct_copy_dir "$commands_src" "$HOME/.config/agents/commands"
	fct_copy_dir "$skills_src" "$HOME/.config/agents/skills"

	# Factory
	fct_copy_dir "$commands_src" "$HOME/.factory/commands"
	fct_copy_dir "$skills_src" "$HOME/.factory/skills"

	# OpenCode
	# Keep OpenCode-specific commands/skills managed directly by chezmoi.
	# Shared ai_templates assets should merge in without deleting extra entries.
	fct_copy_dir "$commands_src" "$HOME/.config/opencode/command" "merge"
	fct_copy_dir "$skills_src" "$HOME/.config/opencode/skill" "merge" --exclude 'skill-creator'
}

fct_render_ai_templates() {
	local render_root="$1"

	mkdir -p "$render_root"
	log_info "Rendering chezmoi target state for ~/.config/ai_templates"

	chezmoi archive --format tar \
		"$HOME/.config/ai_templates" |
		tar -xf - -C "$render_root"
}

fct_cleanup() {
	local render_root_path="${1:-}"

	if [[ -n "$render_root_path" && -d "$render_root_path" ]]; then
		rm -rf "$render_root_path"
	fi
}

fct_main() {
	local repo_root
	local tree_src
	local tree_dst
	local ai_templates_root
	local render_root
	local commands_src
	local skills_src

	repo_root="$HOME/.local/share/chezmoi"
	tree_src="$HOME/Documents/_my_docs/42_tree_of_my_dir_files/z_archive/tree_my_docs.txt"
	tree_dst="$repo_root/backup_tree_my_docs.txt"
	ai_templates_root="$repo_root/dot_config/ai_templates"
	render_root="$(mktemp -d)"
	trap 'fct_cleanup "${render_root:-}"' EXIT

	log_info "Starting post-apply backup script"

	fct_copy_file "$tree_src" "$tree_dst"

	if [[ ! -d "$ai_templates_root" ]]; then
		log_error "Source of truth not found: $ai_templates_root"
		exit 1
	fi

	log_info "Using ai_templates as source of truth"
	log_info "Rendering target-safe names from: $ai_templates_root"
	log_info "Ignoring archived skills under: $ai_templates_root/skills_archived"

	fct_render_ai_templates "$render_root"

	commands_src="$render_root/.config/ai_templates/commands"
	skills_src="$render_root/.config/ai_templates/skills"

	if [[ ! -d "$commands_src" ]]; then
		log_error "Rendered commands directory not found: $commands_src"
		exit 1
	fi

	if [[ ! -d "$skills_src" ]]; then
		log_error "Rendered skills directory not found: $skills_src"
		exit 1
	fi

	log_info "Rendered commands source: $commands_src"
	log_info "Rendered skills source: $skills_src"

	fct_sync_agent_assets "$commands_src" "$skills_src"

	log_info "Post-apply backup script completed successfully"
}

fct_main "$@"
