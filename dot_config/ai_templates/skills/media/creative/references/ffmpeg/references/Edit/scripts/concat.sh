#!/usr/bin/env bash
#
# concat.sh - Concatenate videos using the concat demuxer with stream copy.
#
# Usage: concat.sh <output> <file1> <file2> [file3 ...]
#
# All inputs must share the same codec, resolution, frame rate, and pixel format.
# For mixed sources, use the concat filter documented in references/trim-concat.md.

set -euo pipefail

fct_usage() {
	cat <<EOF
Usage: $(basename "$0") <output> <file1> <file2> [file3 ...]

Example:
  $(basename "$0") merged.mp4 a.mp4 b.mp4 c.mp4
EOF
	exit "${1:-0}"
}

log_error() { echo "ERROR: $*" >&2; }

fct_main() {
	[[ $# -lt 3 ]] && fct_usage 1
	[[ "${1:-}" == "-h" ]] && fct_usage 0

	local output="${1}"
	shift
	local inputs=("$@")

	for f in "${inputs[@]}"; do
		[[ -f "${f}" ]] || {
			log_error "Input file not found: ${f}"
			exit 1
		}
	done

	local list_file
	list_file=$(mktemp -t concat-list.XXXXXX.txt)
	trap 'rm -f "${list_file}"' EXIT

	for f in "${inputs[@]}"; do
		local abs
		abs="$(cd "$(dirname "${f}")" && pwd)/$(basename "${f}")"
		printf "file '%s'\n" "${abs}" >>"${list_file}"
	done

	ffmpeg -hide_banner -y \
		-f concat -safe 0 \
		-i "${list_file}" \
		-c copy \
		"${output}"

	echo "Wrote ${output}"
}

fct_main "$@"
