#!/usr/bin/env bash
#
# extract-audio.sh - Extract the audio track from a video as MP3 at 192 kbps.
#
# Usage: extract-audio.sh -i <video> -o <output.mp3>

set -euo pipefail

fct_usage() {
	cat <<EOF
Usage: $(basename "$0") -i <video> -o <output.mp3>

  -i  Input video file
  -o  Output audio file (.mp3)

Example:
  $(basename "$0") -i video.mp4 -o audio.mp3
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
	[[ "${OUTPUT}" == *.mp3 ]] || {
		log_error "This quick script outputs MP3 only. Use an .mp3 path, or use the Edit sub-skill for WAV/M4A outputs."
		exit 1
	}
}

fct_main() {
	fct_parse_arguments "$@"

	ffmpeg -hide_banner -y \
		-i "${INPUT}" \
		-vn \
		-acodec libmp3lame -b:a 192k \
		"${OUTPUT}"

	echo "Wrote ${OUTPUT}"
}

fct_main "$@"
