#!/usr/bin/env bash
#
# convert.sh - Transcode a video to web-safe H.264 MP4.
#
# Usage: convert.sh -i <input> -o <output.mp4>
#
# Produces H.264 + AAC with yuv420p pixel format and +faststart flag
# for broad browser and player compatibility.

set -euo pipefail

fct_usage() {
	cat <<EOF
Usage: $(basename "$0") -i <input> -o <output.mp4>

  -i  Input file (any common video format)
  -o  Output file (.mp4)

Example:
  $(basename "$0") -i input.avi -o output.mp4
EOF
	exit "${1:-0}"
}

log_error() { echo "ERROR: $*" >&2; }

fct_parse_arguments() {
	[[ $# -eq 0 ]] && fct_usage 0
	while getopts "i:o:h" opt; do
		case "${opt}" in
		i) INPUT="${OPTARG}" ;;
		o) OUTPUT="${OPTARG}" ;;
		h) fct_usage 0 ;;
		*) fct_usage 1 ;;
		esac
	done

	: "${INPUT:?Missing -i input}"
	: "${OUTPUT:?Missing -o output}"

	[[ -f "${INPUT}" ]] || {
		log_error "Input file not found: ${INPUT}"
		exit 1
	}
}

fct_main() {
	fct_parse_arguments "$@"

	ffmpeg -hide_banner -y \
		-i "${INPUT}" \
		-c:v libx264 -preset medium -crf 23 \
		-pix_fmt yuv420p \
		-c:a aac -b:a 128k \
		-movflags +faststart \
		"${OUTPUT}"

	echo "Wrote ${OUTPUT}"
}

fct_main "$@"
