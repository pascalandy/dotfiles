#!/usr/bin/env bash

# Exit on error, treat unset variables as error, exit on pipe failure
set -euo pipefail

# Function to log messages
log() {
	echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log "Starting post-apply backup script"

# file to test the backup
TREE_SRC="$HOME/Documents/_my_docs/42_tree_of_my_dir_files/z_archive/tree_my_docs.txt"
TREE_DST="$HOME/.local/share/chezmoi/backup_tree_my_docs.txt"

# Backup tree file to repo
if [[ -f "$TREE_SRC" ]]; then
	log "Copying tree file from $TREE_SRC to $TREE_DST"
	cp "$TREE_SRC" "$TREE_DST"
	log "Tree file copied successfully"
else
	log "Error: Source tree file $TREE_SRC does not exist"
	exit 1
fi



log "Post-apply backup script completed successfully"
