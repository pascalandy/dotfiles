#!/usr/bin/env bash
#
# speed.sh - Adjust video playback speed with audio pitch correction.
#
# Usage: speed.sh -i <input> -r <ratio> -o <output>
#
# Accepts ratios from 0.5 to 2.0 (native atempo range).
# For extreme speed changes, use the Edit sub-skill (chains atempo filters).
# If the input has no audio stream, the output remains silent.

set -euo pipefail

fct_usage() {
	cat <<EOF
Usage: $(basename "$0") -i <input> -r <ratio> -o <output>

  -i  Input video file
  -r  Speed ratio (0.5 to 2.0)
        >1 = faster (2.0 = 2x speed)
        <1 = slower (0.5 = half speed)
  -o  Output file

Example:
  $(basename "$0") -i video.mp4 -r 2.0 -o fast.mp4
  $(basename "$0") -i video.mp4 -r 0.5 -o slow.mp4
EOF
	exit "${1:-0}"
}

log_error() { echo "ERROR: $*" >&2; }

fct_parse_arguments() {
	[[ $# -eq 0 ]] && fct_usage 0
	while getopts "i:r:o:h" opt; do
		case "${opt}" in
		i) INPUT="${OPTARG}" ;;
		r) RATIO="${OPTARG}" ;;
		o) OUTPUT="${OPTARG}" ;;
		h) fct_usage 0 ;;
		*) fct_usage 1 ;;
		esac
	done

	: "${INPUT:?Missing -i input}"
	: "${RATIO:?Missing -r ratio}"
	: "${OUTPUT:?Missing -o output}"

	[[ -f "${INPUT}" ]] || {
		log_error "Input file not found: ${INPUT}"
		exit 1
	}

	# Validate ratio is within atempo's native range
	local in_range
	in_range=$(awk -v r="${RATIO}" 'BEGIN{print (r >= 0.5 && r <= 2.0) ? "1" : "0"}')
	if [[ "${in_range}" != "1" ]]; then
		log_error "Ratio ${RATIO} out of range [0.5, 2.0]. For extreme speed changes, use Edit sub-skill."
		exit 1
	fi
}

fct_main() {
	fct_parse_arguments "$@"

	# Video pts multiplier is the reciprocal of the speed ratio
	local pts has_audio
	pts=$(awk -v r="${RATIO}" 'BEGIN{printf "%.6f", 1.0 / r}')

	has_audio=$(ffprobe -v error -select_streams a:0 \
		-show_entries stream=codec_type \
		-of default=noprint_wrappers=1:nokey=1 \
		"${INPUT}" 2>/dev/null || true)

	if [[ "${has_audio}" == "audio" ]]; then
		ffmpeg -hide_banner -y \
			-i "${INPUT}" \
			-filter_complex "[0:v]setpts=${pts}*PTS[v];[0:a]atempo=${RATIO}[a]" \
			-map "[v]" -map "[a]" \
			"${OUTPUT}"
	else
		ffmpeg -hide_banner -y \
			-i "${INPUT}" \
			-vf "setpts=${pts}*PTS" \
			-an \
			"${OUTPUT}"
	fi

	echo "Wrote ${OUTPUT}"
}

fct_main "$@"
