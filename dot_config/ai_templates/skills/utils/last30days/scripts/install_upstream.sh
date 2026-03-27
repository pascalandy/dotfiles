#!/usr/bin/env bash

set -Eeuo pipefail

readonly FCT_REPO_URL="https://github.com/mvanhorn/last30days-skill.git"
readonly FCT_ROOT="${HOME}/.local/share/last30days-skill"

fct_sparse_set() {
	git -C "${FCT_ROOT}" sparse-checkout set --no-cone \
		"/README.md" \
		"/LICENSE" \
		"/SKILL.md" \
		"/agents/openai.yaml" \
		"/fixtures" \
		"/fixtures/**" \
		"/scripts" \
		"/scripts/**" \
		"/variants/open" \
		"/variants/open/**"
}

fct_main() {
	mkdir -p "$(dirname "${FCT_ROOT}")"

	if [[ -d "${FCT_ROOT}/.git" ]]; then
		git -C "${FCT_ROOT}" remote set-url origin "${FCT_REPO_URL}"
		fct_sparse_set
		git -C "${FCT_ROOT}" checkout main
		git -C "${FCT_ROOT}" pull --ff-only --depth=1 origin main
	else
		git clone --depth=1 --filter=blob:none --sparse "${FCT_REPO_URL}" "${FCT_ROOT}"
		fct_sparse_set
	fi

	printf 'Installed upstream checkout at %s\n' "${FCT_ROOT}"
}

fct_main "$@"
