#!/usr/bin/env bash
#
# probe.sh - Thin ffprobe wrapper that prints format + streams as clean JSON.
#
# Usage: probe.sh <file>

set -euo pipefail

fct_usage() {
	cat <<EOF
Usage: $(basename "$0") <file>

Prints ffprobe format + streams as JSON.

Example:
  $(basename "$0") video.mp4 | jq '.streams[0]'
EOF
	exit "${1:-0}"
}

log_error() { echo "ERROR: $*" >&2; }

fct_main() {
	[[ $# -eq 0 ]] && fct_usage 0
	[[ "${1:-}" == "-h" ]] && fct_usage 0

	local file="${1}"
	[[ -f "${file}" ]] || {
		log_error "File not found: ${file}"
		exit 1
	}

	ffprobe -v quiet -print_format json -show_format -show_streams "${file}"
}

fct_main "$@"
