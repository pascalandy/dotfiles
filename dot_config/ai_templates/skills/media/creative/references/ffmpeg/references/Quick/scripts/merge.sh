#!/usr/bin/env bash
#
# merge.sh - Concatenate videos using the concat demuxer.
#
# Usage: merge.sh -o <output> <file1> <file2> [file3 ...]
#
# All inputs must share the same codec, resolution, and frame rate.
# For mixed-codec merges, use the Edit sub-skill.

set -euo pipefail

fct_usage() {
	cat <<EOF
Usage: $(basename "$0") -o <output> <file1> <file2> [file3 ...]

  -o  Output file

Example:
  $(basename "$0") -o merged.mp4 part1.mp4 part2.mp4 part3.mp4
EOF
	exit "${1:-0}"
}

log_error() { echo "ERROR: $*" >&2; }

fct_parse_arguments() {
	[[ $# -eq 0 ]] && fct_usage 0
	while getopts "o:h" opt; do
		case "${opt}" in
		o) OUTPUT="${OPTARG}" ;;
		h) fct_usage 0 ;;
		*) fct_usage 1 ;;
		esac
	done
	shift $((OPTIND - 1))

	: "${OUTPUT:?Missing -o output}"
	[[ $# -ge 2 ]] || {
		log_error "Need at least 2 input files"
		exit 1
	}

	INPUTS=("$@")
	for f in "${INPUTS[@]}"; do
		[[ -f "${f}" ]] || {
			log_error "Input file not found: ${f}"
			exit 1
		}
	done
}

fct_main() {
	fct_parse_arguments "$@"

	local list_file
	list_file=$(mktemp -t merge-list.XXXXXX.txt)
	trap 'rm -f "${list_file}"' EXIT

	for f in "${INPUTS[@]}"; do
		# Absolute path to survive the concat demuxer's working directory
		local abs
		abs="$(cd "$(dirname "${f}")" && pwd)/$(basename "${f}")"
		printf "file '%s'\n" "${abs}" >>"${list_file}"
	done

	ffmpeg -hide_banner -y \
		-f concat -safe 0 \
		-i "${list_file}" \
		-c copy \
		"${OUTPUT}"

	echo "Wrote ${OUTPUT}"
}

fct_main "$@"
