#!/usr/bin/env bash

# Exit on error, treat unset variables as error, exit on pipe failure
set -euo pipefail

# Function to log messages
log() {
	echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log "Starting pre-apply sync script"

# Sync VS Code config back to chezmoi source (only if changed)
VSCODE_USER="$HOME/Library/Application Support/Code/User"
VSCODE_DST="$HOME/.local/share/chezmoi/private_Library/private_Application Support/private_Code/User"
VSCODE_EXT_DST="$HOME/.local/share/chezmoi/dot_config/vscode/extensions.txt"

if [[ -f "$VSCODE_USER/settings.json" ]]; then
	if ! diff -q "$VSCODE_USER/settings.json" "$VSCODE_DST/settings.json" >/dev/null 2>&1; then
		log "Syncing VS Code settings.json to chezmoi source"
		cp "$VSCODE_USER/settings.json" "$VSCODE_DST/settings.json"
		log "VS Code settings.json synced"
	else
		log "VS Code settings.json unchanged, skipping"
	fi
fi

if [[ -f "$VSCODE_USER/keybindings.json" ]]; then
	if ! diff -q "$VSCODE_USER/keybindings.json" "$VSCODE_DST/keybindings.json" >/dev/null 2>&1; then
		log "Syncing VS Code keybindings.json to chezmoi source"
		cp "$VSCODE_USER/keybindings.json" "$VSCODE_DST/keybindings.json"
		log "VS Code keybindings.json synced"
	else
		log "VS Code keybindings.json unchanged, skipping"
	fi
fi

# Update extensions list (only if changed)
if command -v code >/dev/null 2>&1; then
	TEMP_EXT=$(mktemp)
	code --list-extensions >"$TEMP_EXT"
	if ! diff -q "$TEMP_EXT" "$VSCODE_EXT_DST" >/dev/null 2>&1; then
		log "Updating VS Code extensions list"
		cp "$TEMP_EXT" "$VSCODE_EXT_DST"
		log "VS Code extensions list updated"
	else
		log "VS Code extensions list unchanged, skipping"
	fi
	rm -f "$TEMP_EXT"
fi

# Update Brewfile
if command -v brew >/dev/null 2>&1; then
	log "Updating Brewfile to chezmoi source"
	brew bundle dump --file "$HOME/.local/share/chezmoi/dot_Brewfile" --force
	log "Brewfile updated successfully"
else
	log "Warning: brew command not found, skipping Brewfile update"
fi

log "Pre-apply sync script completed successfully"
