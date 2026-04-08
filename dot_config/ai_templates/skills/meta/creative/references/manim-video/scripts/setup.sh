#!/usr/bin/env bash
set -euo pipefail
G="\033[0;32m"
R="\033[0;31m"
N="\033[0m"
ok() { echo -e "  ${G}+${N} $1"; }
fail() { echo -e "  ${R}x${N} $1"; }
echo ""
echo "Manim Video Skill — Setup Check"
echo ""
errors=0
if command -v uv &>/dev/null; then
	ok "uv $(uv --version 2>&1 | awk '{print $2}')"
else
	fail "uv not found (install: https://docs.astral.sh/uv/getting-started/installation/)"
	errors=$((errors + 1))
fi
if command -v manim &>/dev/null; then
	ok "Manim $(manim --version 2>&1 | head -1)"
else
	fail "Manim not installed: uv tool install manim"
	errors=$((errors + 1))
fi
if command -v pdflatex &>/dev/null; then
	ok "LaTeX (pdflatex)"
else
	fail "LaTeX not found (macOS: brew install --cask mactex-no-gui)"
	errors=$((errors + 1))
fi
if command -v ffmpeg &>/dev/null; then
	ok "ffmpeg"
else
	fail "ffmpeg not found"
	errors=$((errors + 1))
fi
echo ""
if [ $errors -eq 0 ]; then
	echo -e "${G}All prerequisites satisfied.${N}"
else
	echo -e "${R}$errors prerequisite(s) missing.${N}"
fi
echo ""
