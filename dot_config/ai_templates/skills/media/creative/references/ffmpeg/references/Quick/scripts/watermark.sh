#!/usr/bin/env bash
#
# watermark.sh - Overlay a static image watermark in the bottom-right corner.
#
# Usage: watermark.sh -i <video> -w <watermark.png> -o <output>
#
# Places the watermark with a 10px margin from the bottom-right corner.
# For other positions or animated watermarks, use the Edit sub-skill.

set -euo pipefail

fct_usage() {
	cat <<EOF
Usage: $(basename "$0") -i <video> -w <watermark.png> -o <output>

  -i  Input video file
  -w  Watermark image (PNG with transparency recommended)
  -o  Output file

Example:
  $(basename "$0") -i video.mp4 -w logo.png -o output.mp4
EOF
	exit "${1:-0}"
}

log_error() { echo "ERROR: $*" >&2; }

fct_parse_arguments() {
	[[ $# -eq 0 ]] && fct_usage 0
	while getopts "i:w:o:h" opt; do
		case "${opt}" in
		i) INPUT="${OPTARG}" ;;
		w) WATERMARK="${OPTARG}" ;;
		o) OUTPUT="${OPTARG}" ;;
		h) fct_usage 0 ;;
		*) fct_usage 1 ;;
		esac
	done

	: "${INPUT:?Missing -i input}"
	: "${WATERMARK:?Missing -w watermark}"
	: "${OUTPUT:?Missing -o output}"

	[[ -f "${INPUT}" ]] || {
		log_error "Input file not found: ${INPUT}"
		exit 1
	}
	[[ -f "${WATERMARK}" ]] || {
		log_error "Watermark file not found: ${WATERMARK}"
		exit 1
	}
}

fct_main() {
	fct_parse_arguments "$@"

	ffmpeg -hide_banner -y \
		-i "${INPUT}" \
		-i "${WATERMARK}" \
		-filter_complex "[0:v][1:v]overlay=W-w-10:H-h-10" \
		-c:a copy \
		"${OUTPUT}"

	echo "Wrote ${OUTPUT}"
}

fct_main "$@"
