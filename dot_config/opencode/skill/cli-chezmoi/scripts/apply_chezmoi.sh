#!/usr/bin/env bash
#
# ==============================================================================
# Apply Chezmoi Changes
# ==============================================================================
# Why: A consistent way to apply dotfiles changes with verbose output.
# ==============================================================================

# ==============================================================================
# Script metadata
# ==============================================================================
readonly SCRIPT_VERSION="0.1.0"
readonly SCRIPT_DESCRIPTION="Applies chezmoi changes to the home directory."

readonly SCRIPT_PATH="${BASH_SOURCE[0]}"
readonly SCRIPT_NAME="${SCRIPT_PATH##*/}"

# ==============================================================================
# Runtime options
# ==============================================================================
VERBOSE=0
NO_COLOR="${NO_COLOR:-}"

# ==============================================================================
# Execution mode helpers
# ==============================================================================
IS_SOURCED=0
if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then
	IS_SOURCED=1
fi
readonly IS_SOURCED

fct_exit() {
	local code="${1:-0}"
	if [[ "${IS_SOURCED}" -eq 1 ]]; then
		return "${code}"
	fi
	exit "${code}"
}

# ==============================================================================
# Strict mode
# ==============================================================================
fct_enable_strict_mode() {
	set -euo pipefail
	set -o errtrace
}

# ==============================================================================
# Logging
# ==============================================================================
fct_timestamp() {
	date '+%Y-%m-%d %H:%M:%S%z'
}

fct_ansi() {
	local code="${1}"
	if [[ -t 2 && -z "${NO_COLOR}" ]]; then
		printf '\033[%sm' "${code}"
	fi
}

fct_log() {
	local level="${1}"
	shift
	local message="$*"
	local ts
	ts="$(fct_timestamp)"
	local plain="${ts} [${SCRIPT_NAME}] ${level}: ${message}"
	local rendered="${plain}"
	if [[ -t 2 && -z "${NO_COLOR}" ]]; then
		local prefix=""
		local reset=""
		reset="$(fct_ansi '0')"
		case "${level}" in
		DEBUG) prefix="$(fct_ansi '36')" ;;
		INFO) prefix="$(fct_ansi '32')" ;;
		WARN) prefix="$(fct_ansi '33')" ;;
		ERROR) prefix="$(fct_ansi '31')" ;;
		*) prefix="" ;;
		esac
		rendered="${prefix}${plain}${reset}"
	fi
	printf '%s\n' "${rendered}" >&2
}

log_debug() { [[ "${VERBOSE}" -eq 1 ]] && fct_log "DEBUG" "$@"; }
log_info() { fct_log "INFO" "$@"; }
log_error() { fct_log "ERROR" "$@"; }

# ==============================================================================
# Error handling
# ==============================================================================
die() {
	local message="${1:-Unknown error}"
	local exit_code="${2:-1}"
	log_error "${message}"
	fct_exit "${exit_code}"
}

# ==============================================================================
# Usage / version
# ==============================================================================
usage() {
	cat <<EOF
${SCRIPT_NAME} v${SCRIPT_VERSION}
${SCRIPT_DESCRIPTION}

Usage:
  ${SCRIPT_NAME} [options]

Options:
  -h, --help         Show this help and exit
  -V, --version      Show version and exit
  -v, --verbose      Enable debug logging
EOF
}

show_version() {
	printf '%s\n' "${SCRIPT_NAME} v${SCRIPT_VERSION}"
}

# ==============================================================================
# Argument parsing
# ==============================================================================
fct_parse_arguments() {
	while [[ $# -gt 0 ]]; do
		case "$1" in
		-h | --help)
			usage
			fct_exit 0
			;;
		-V | --version)
			show_version
			fct_exit 0
			;;
		-v | --verbose)
			VERBOSE=1
			shift
			;;
		*) die "Unknown option: $1" 2 ;;
		esac
	done
}

# ==============================================================================
# Dependency checking
# ==============================================================================
fct_require_command() {
	local cmd="${1}"
	if ! command -v "${cmd}" >/dev/null 2>&1; then
		die "Missing required command: ${cmd}." 4
	fi
}

fct_check_dependencies() {
	fct_require_command "chezmoi"
}

# ==============================================================================
# Cleanup & traps
# ==============================================================================
cleanup() {
	local exit_status=$?
	set +e
	return "${exit_status}"
}

fct_setup_traps() {
	trap 'cleanup' EXIT
	trap 'log_error "Command failed at line $LINENO"; exit 1' ERR
}

# ==============================================================================
# Main logic
# ==============================================================================
fct_execute_this() {
	log_info "Applying chezmoi changes..."
	chezmoi apply -v
}

main() {
	fct_enable_strict_mode
	fct_setup_traps
	fct_parse_arguments "$@"
	fct_check_dependencies
	fct_execute_this
	log_info "Done."
}

if [[ "${IS_SOURCED}" -eq 0 ]]; then
	main "$@"
fi
