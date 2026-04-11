#!/usr/bin/env bash

# Exit on error, treat unset variables as error, exit on pipe failure
set -euo pipefail

# Function to log messages
log() {
	echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log "Starting pre-apply sync script"

# =============================================================================
# BREWFILE SYNC CONFIGURATION
# =============================================================================
# SYNC_BREWFILE: Master switch to enable/disable Brewfile syncing
#   - Set to 'true' to enable, 'false' to completely disable
#
# 72-HOUR RATE LIMITING:
#   Even when SYNC_BREWFILE=true, the script will only actually run 'brew bundle dump'
#   once every 72 hours. This prevents:
#     - Unnecessary git noise from frequent Brewfile changes
#     - Slowing down every chezmoi apply with brew operations
#     - Hitting API rate limits or brew analytics
#
#   How it works:
#     - A timestamp file (.last_brewfile_sync) tracks last successful sync
#     - Script compares current time vs last sync time
#     - Only syncs if 72+ hours have passed OR no timestamp exists
#
#   To force immediate sync:
#     rm ~/.local/share/chezmoi/.last_brewfile_sync
# =============================================================================

SYNC_BREWFILE=true

# Timestamp file for tracking last Brewfile sync
BREWFILE_TIMESTAMP="$HOME/.local/share/chezmoi/.last_brewfile_sync"
BREWFILE_DST="$HOME/.local/share/chezmoi/dot_Brewfile"
# 72 hours in seconds
SYNC_INTERVAL=$((72 * 60 * 60))

# Sync VS Code: config back to chezmoi source (only if changed)
VSCODE_USER="$HOME/Library/Application Support/Code/User"
VSCODE_DST="$HOME/.local/share/chezmoi/private_Library/private_Application Support/private_Code/User"
VSCODE_EXT_DST="$HOME/.local/share/chezmoi/dot_config/vscode/extensions.txt"

if [[ -f "$VSCODE_USER/settings.json" ]]; then
	if ! diff -q "$VSCODE_USER/settings.json" "$VSCODE_DST/settings.json" >/dev/null 2>&1; then
		log "Syncing VS Code: settings.json to chezmoi source"
		cp "$VSCODE_USER/settings.json" "$VSCODE_DST/settings.json"
		log "VS Code: settings.json synced"
	else
		log "VS Code: settings.json unchanged, skipping"
	fi
fi

if [[ -f "$VSCODE_USER/keybindings.json" ]]; then
	if ! diff -q "$VSCODE_USER/keybindings.json" "$VSCODE_DST/keybindings.json" >/dev/null 2>&1; then
		log "Syncing VS Code: keybindings.json to chezmoi source"
		cp "$VSCODE_USER/keybindings.json" "$VSCODE_DST/keybindings.json"
		log "VS Code: keybindings.json synced"
	else
		log "VS Code: keybindings.json unchanged, skipping"
	fi
fi

# Update extensions list (only if changed)
if command -v code >/dev/null 2>&1; then
	TEMP_EXT=$(mktemp)
	code --list-extensions >"$TEMP_EXT"
	if ! diff -q "$TEMP_EXT" "$VSCODE_EXT_DST" >/dev/null 2>&1; then
		log "Updating VS Code: extensions list"
		cp "$TEMP_EXT" "$VSCODE_EXT_DST"
		log "VS Code: extensions list updated"
	else
		log "VS Code: extensions list unchanged, skipping"
	fi
	rm -f "$TEMP_EXT"
fi

# Update Brewfile (only if SYNC_BREWFILE=true AND 72h have passed since last sync)
# See header comment for full explanation of the rate limiting logic
should_sync_brewfile=false

if [[ "$SYNC_BREWFILE" == true ]]; then
	# Check if enough time has passed since last sync
	if [[ -f "$BREWFILE_TIMESTAMP" ]]; then
		last_sync=$(cat "$BREWFILE_TIMESTAMP")
		current_time=$(date +%s)
		time_diff=$((current_time - last_sync))
		if [[ $time_diff -ge $SYNC_INTERVAL ]]; then
			should_sync_brewfile=true
			log "Last Brewfile sync was $((time_diff / 3600))h ago (threshold: 72h)"
		else
			log "Brewfile sync skipped - last sync was $((time_diff / 3600))h ago (threshold: 72h)"
		fi
	else
		# No timestamp file exists, should sync
		should_sync_brewfile=true
		log "No previous Brewfile sync timestamp found"
	fi
else
	log "SYNC_BREWFILE=false, skipping Brewfile update"
fi

if [[ "$should_sync_brewfile" == true ]]; then
	if command -v brew >/dev/null 2>&1; then
		log "Updating Brewfile to chezmoi source"
		brew bundle dump --file "$BREWFILE_DST" --force
		date +%s >"$BREWFILE_TIMESTAMP"
		log "Brewfile updated successfully"
	else
		log "Warning: brew command not found, skipping Brewfile update"
	fi
fi

log "Pre-apply sync script completed successfully"
