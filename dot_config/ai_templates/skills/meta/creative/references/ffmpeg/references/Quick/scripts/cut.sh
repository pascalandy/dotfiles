#!/usr/bin/env bash
#
# cut.sh - Cut a video segment using stream copy (fast, lossless).
#
# Usage: cut.sh -i <input> -s <start> -e <end> -o <output>
#   -i  Input file
#   -s  Start timestamp (e.g. 00:01:30 or 90)
#   -e  End timestamp (e.g. 00:02:45 or 165)
#   -o  Output file
#
# Cut points snap to the nearest keyframe. For frame-accurate cuts,
# use the Edit sub-skill's precise trim pattern.

set -euo pipefail

fct_usage() {
	cat <<EOF
Usage: $(basename "$0") -i <input> -s <start> -e <end> -o <output>

  -i  Input file
  -s  Start timestamp (HH:MM:SS or seconds)
  -e  End timestamp (HH:MM:SS or seconds)
  -o  Output file

Example:
  $(basename "$0") -i video.mp4 -s 00:01:30 -e 00:02:45 -o clip.mp4
EOF
	exit "${1:-0}"
}

log_error() { echo "ERROR: $*" >&2; }

fct_parse_arguments() {
	[[ $# -eq 0 ]] && fct_usage 0
	while getopts "i:s:e:o:h" opt; do
		case "${opt}" in
		i) INPUT="${OPTARG}" ;;
		s) START="${OPTARG}" ;;
		e) END="${OPTARG}" ;;
		o) OUTPUT="${OPTARG}" ;;
		h) fct_usage 0 ;;
		*) fct_usage 1 ;;
		esac
	done

	: "${INPUT:?Missing -i input}"
	: "${START:?Missing -s start}"
	: "${END:?Missing -e end}"
	: "${OUTPUT:?Missing -o output}"

	[[ -f "${INPUT}" ]] || {
		log_error "Input file not found: ${INPUT}"
		exit 1
	}
}

fct_main() {
	fct_parse_arguments "$@"

	ffmpeg -hide_banner -y \
		-ss "${START}" -to "${END}" \
		-i "${INPUT}" \
		-c copy \
		-avoid_negative_ts make_zero \
		"${OUTPUT}"

	echo "Wrote ${OUTPUT}"
}

fct_main "$@"
