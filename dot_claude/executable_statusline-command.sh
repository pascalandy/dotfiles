#!/usr/bin/env bash
set -euo pipefail

# StatusLine for Claude Code — mirrors key Powerlevel10k prompt segments
# Segments: directory | git branch+status | active virtual env

parts=()

# 1. Short directory (last 2 components, ~ for home)
dir="${PWD/#$HOME/~}"
# Keep last 2 path components for brevity
if [[ "$dir" == "~" ]]; then
	parts+=("~")
else
	parts+=("${dir##*/}")
fi

# 2. Git info (branch + dirty indicator)
if git_branch="$(git symbolic-ref --short HEAD 2>/dev/null)"; then
	git_part="$git_branch"
	if ! git diff --quiet HEAD 2>/dev/null; then
		git_part="${git_part}*"
	fi
	parts+=("$git_part")
elif git_hash="$(git rev-parse --short HEAD 2>/dev/null)"; then
	parts+=("@${git_hash}")
fi

# 3. Python virtualenv
if [[ -n "${VIRTUAL_ENV:-}" ]]; then
	parts+=("venv:${VIRTUAL_ENV##*/}")
fi

# 4. Kubernetes context (if kubectl available)
if command -v kubectl &>/dev/null; then
	if kctx="$(kubectl config current-context 2>/dev/null)"; then
		parts+=("k8s:${kctx}")
	fi
fi

# Join with separator
printf '%s' "${parts[*]}"
