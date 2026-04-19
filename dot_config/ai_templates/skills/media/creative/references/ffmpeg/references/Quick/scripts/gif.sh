#!/usr/bin/env bash
#
# gif.sh - Convert a video segment to a high-quality GIF using the two-pass palette method.
#
# Usage: gif.sh -i <video> -s <start> -e <end> -o <out.gif> [-w <width>] [-f <fps>]

set -euo pipefail

WIDTH=480
FPS=15

fct_usage() {
	cat <<EOF
Usage: $(basename "$0") -i <video> -s <start> -e <end> -o <out.gif> [-w <width>] [-f <fps>]

  -i  Input video file
  -s  Start timestamp (HH:MM:SS or seconds)
  -e  End timestamp (HH:MM:SS or seconds)
  -o  Output GIF file
  -w  Width in pixels (default: 480)
  -f  Frames per second (default: 15)

Example:
  $(basename "$0") -i video.mp4 -s 00:00:10 -e 00:00:15 -o clip.gif
EOF
	exit "${1:-0}"
}

log_error() { echo "ERROR: $*" >&2; }

fct_parse_arguments() {
	[[ $# -eq 0 ]] && fct_usage 0
	while getopts "i:s:e:o:w:f:h" opt; do
		case "${opt}" in
		i) INPUT="${OPTARG}" ;;
		s) START="${OPTARG}" ;;
		e) END="${OPTARG}" ;;
		o) OUTPUT="${OPTARG}" ;;
		w) WIDTH="${OPTARG}" ;;
		f) FPS="${OPTARG}" ;;
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

	local palette
	palette=$(mktemp -t palette.XXXXXX.png)
	trap 'rm -f "${palette}"' EXIT

	# Pass 1: build palette
	ffmpeg -hide_banner -y \
		-ss "${START}" -to "${END}" \
		-i "${INPUT}" \
		-vf "fps=${FPS},scale=${WIDTH}:-1:flags=lanczos,palettegen" \
		"${palette}"

	# Pass 2: render gif using palette
	ffmpeg -hide_banner -y \
		-ss "${START}" -to "${END}" \
		-i "${INPUT}" \
		-i "${palette}" \
		-filter_complex "fps=${FPS},scale=${WIDTH}:-1:flags=lanczos[x];[x][1:v]paletteuse" \
		"${OUTPUT}"

	echo "Wrote ${OUTPUT}"
}

fct_main "$@"
