#!/usr/bin/env bash
#
# normalize-audio.sh - Two-pass EBU R128 loudness normalization.
#
# Usage: normalize-audio.sh <input> <output> [target_lufs]
#
# First pass measures loudness; second pass applies the correction with
# linear normalization (preserves dynamics perfectly).
#
# Default target: -16 LUFS (streaming standard).
# Use -23 for broadcast.

set -euo pipefail

fct_usage() {
	cat <<EOF
Usage: $(basename "$0") <input> <output> [target_lufs]

  target_lufs defaults to -16 (streaming standard)
              use -23 for broadcast

Example:
  $(basename "$0") in.mp4 out.mp4
  $(basename "$0") in.mp4 out.mp4 -23
EOF
	exit "${1:-0}"
}

log_error() { echo "ERROR: $*" >&2; }
log_info() { echo "INFO:  $*"; }

fct_main() {
	[[ $# -lt 2 ]] && fct_usage 1
	[[ "${1:-}" == "-h" ]] && fct_usage 0

	local input="${1}"
	local output="${2}"
	local target="${3:--16}"

	[[ -f "${input}" ]] || {
		log_error "Input file not found: ${input}"
		exit 1
	}

	log_info "Pass 1: measuring loudness..."

	# First pass — measure integrated loudness, true peak, and LRA
	local measure
	measure=$(ffmpeg -hide_banner -i "${input}" \
		-af "loudnorm=I=${target}:TP=-1.5:LRA=11:print_format=json" \
		-f null - 2>&1 | awk '/^{/,/^}/')

	local I TP LRA thresh offset
	I=$(echo "${measure}" | grep -o '"input_i"[^,]*' | cut -d'"' -f4)
	TP=$(echo "${measure}" | grep -o '"input_tp"[^,]*' | cut -d'"' -f4)
	LRA=$(echo "${measure}" | grep -o '"input_lra"[^,]*' | cut -d'"' -f4)
	thresh=$(echo "${measure}" | grep -o '"input_thresh"[^,]*' | cut -d'"' -f4)
	offset=$(echo "${measure}" | grep -o '"target_offset"[^,]*' | cut -d'"' -f4)

	if [[ -z "${I}" || -z "${TP}" || -z "${LRA}" ]]; then
		log_error "Could not parse loudnorm measurement output"
		log_error "${measure}"
		exit 1
	fi

	log_info "  Input I: ${I} LUFS"
	log_info "  Input TP: ${TP} dBTP"
	log_info "  Input LRA: ${LRA} LU"

	log_info "Pass 2: applying normalization (target: ${target} LUFS)..."

	ffmpeg -hide_banner -y \
		-i "${input}" \
		-af "loudnorm=I=${target}:TP=-1.5:LRA=11:\
measured_I=${I}:measured_TP=${TP}:measured_LRA=${LRA}:\
measured_thresh=${thresh}:offset=${offset}:linear=true:print_format=summary" \
		-c:v copy \
		"${output}"

	log_info "Wrote ${output}"
}

fct_main "$@"
