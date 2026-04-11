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
		rsync_args+=(--delete --delete-excluded --force)
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

fct_compile_assets() {
	local src_dir="$1"
	local compile_dir="$2"

	mkdir -p "$compile_dir"

	# If src has subdirectories (categories), compile them
	# If src is flat, copy everything directly
	local has_categories=false
	for category in meta pa-sdlc specs utils; do
		if [[ -d "$src_dir/$category" ]]; then
			has_categories=true
			break
		fi
	done

	if [[ "$has_categories" == true ]]; then
		# Compile from category subdirectories
		for category in meta pa-sdlc specs utils; do
			if [[ -d "$src_dir/$category" ]]; then
				cp -r "$src_dir/$category/"* "$compile_dir/" 2>/dev/null || true
			fi
		done
	else
		# Flat structure - copy everything directly
		cp -r "$src_dir/"* "$compile_dir/" 2>/dev/null || true
	fi
}

fct_sync_agent_assets() {
	local commands_src="$1"
	local skills_src="$2"
	local compiled_commands_dir
	local compiled_skills_dir

	# Create compiled directories (clean slate sources)
	compiled_commands_dir="$(mktemp -d)"
	compiled_skills_dir="$(mktemp -d)"
	fct_compile_assets "$commands_src" "$compiled_commands_dir"
	fct_compile_assets "$skills_src" "$compiled_skills_dir"

	# OpenCode
	fct_copy_dir "$compiled_commands_dir" "$HOME/.config/opencode/commands" "delete"
	fct_copy_dir "$compiled_skills_dir" "$HOME/.config/opencode/skills" "delete"

	# Pi
	fct_copy_dir "$compiled_commands_dir" "$HOME/.pi/agent/prompts" "delete"
	fct_copy_dir "$compiled_skills_dir" "$HOME/.pi/agent/skills" "delete"

	# Claude Code
	fct_copy_dir "$compiled_commands_dir" "$HOME/.claude/commands" "delete"
	fct_copy_dir "$compiled_skills_dir" "$HOME/.claude/skills" "delete"

	# Codex
	fct_copy_dir "$compiled_commands_dir" "$HOME/.codex/prompts" "delete"
	fct_copy_dir "$compiled_skills_dir" "$HOME/.codex/skills" "delete"

	# Gemini
	fct_copy_dir "$compiled_commands_dir" "$HOME/.gemini/commands" "delete"
	fct_copy_dir "$compiled_skills_dir" "$HOME/.gemini/skills" "delete"

	# Amp
	fct_copy_dir "$compiled_commands_dir" "$HOME/.config/amp/commands" "delete"
	fct_copy_dir "$compiled_skills_dir" "$HOME/.config/amp/skills" "delete"

	# Agents
	fct_copy_dir "$compiled_commands_dir" "$HOME/.config/agents/commands" "delete"
	fct_copy_dir "$compiled_skills_dir" "$HOME/.config/agents/skills" "delete"

	# Factory
	fct_copy_dir "$compiled_commands_dir" "$HOME/.factory/commands" "delete"
	fct_copy_dir "$compiled_skills_dir" "$HOME/.factory/skills" "delete"

	# Cleanup compiled directories
	rm -rf "$compiled_commands_dir" "$compiled_skills_dir"
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
