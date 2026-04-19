#!/usr/bin/env bash
#
# thumb.sh - Extract a single frame from a video at a specific timestamp.
#
# Usage: thumb.sh -i <video> -t <timestamp> -o <out.jpg>

set -euo pipefail

fct_usage() {
	cat <<EOF
Usage: $(basename "$0") -i <video> -t <timestamp> -o <out.jpg>

  -i  Input video file
  -t  Timestamp (HH:MM:SS or seconds)
  -o  Output image file (.jpg, .png)

Example:
  $(basename "$0") -i video.mp4 -t 00:00:15 -o frame.jpg
EOF
	exit "${1:-0}"
}

log_error() { echo "ERROR: $*" >&2; }

fct_parse_arguments() {
	[[ $# -eq 0 ]] && fct_usage 0
	while getopts "i:t:o:h" opt; do
		case "${opt}" in
		i) INPUT="${OPTARG}" ;;
		t) TIMESTAMP="${OPTARG}" ;;
		o) OUTPUT="${OPTARG}" ;;
		h) fct_usage 0 ;;
		*) fct_usage 1 ;;
		esac
	done

	: "${INPUT:?Missing -i input}"
	: "${TIMESTAMP:?Missing -t timestamp}"
	: "${OUTPUT:?Missing -o output}"

	[[ -f "${INPUT}" ]] || {
		log_error "Input file not found: ${INPUT}"
		exit 1
	}
}

fct_main() {
	fct_parse_arguments "$@"

	ffmpeg -hide_banner -y \
		-ss "${TIMESTAMP}" \
		-i "${INPUT}" \
		-frames:v 1 \
		-q:v 2 \
		"${OUTPUT}"

	echo "Wrote ${OUTPUT}"
}

fct_main "$@"
