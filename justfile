set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

# Show available recipes
default:
    @just --list

# -----------------------------------------------------------------------------
# Quality checks
# -----------------------------------------------------------------------------
# Run the main local checks before applying or committing dotfile changes.
ci:
    just gitleaks
    just shellcheck
    just shfmt
    just test-all
    chezmoi apply -n -v

test-all:
    just test-transcript
    just test-banana
    just test-map-fs
    just test-tavily

test-transcript:
    uv run --with pytest --with httpx --with tiktoken --with yt-dlp --with rich pytest dot_config/ai_templates/skills/utils/transcript-sk/scripts/tests/ -v

test-banana:
    uv run --with pytest --with openai --with typer --with rich --with pillow pytest dot_config/ai_templates/skills/utils/nano-banana-sk/scripts/tests/ -v

test-map-fs:
    uv run --with pytest --with typer --with rich --with pyyaml --with tomli-w pytest dot_config/ai_templates/skills/utils/map-filesystem-abstract/scripts/tests/ -v

test-tavily:
    uv run --with pytest --with httpx --with rich --with respx pytest dot_config/ai_templates/skills/utils/tavily/scripts/tests/ -v

# Run gitleaks across the repository.
gitleaks:
    gitleaks detect --config .gitleaks.toml

# Run gitleaks only on staged changes.
gitleaks-staged:
    gitleaks protect --staged --verbose

# Lint all tracked shell scripts with shellcheck.
shellcheck:
    git ls-files -z '*.sh' 'dot_local/bin/executable_*' | xargs -0 -r shellcheck

# Lint only staged shell scripts with shellcheck.
shellcheck-staged:
    git diff --name-only --staged -z -- '*.sh' 'dot_local/bin/executable_*' | xargs -0 -r shellcheck

# Show shfmt diffs for all tracked shell scripts.
shfmt:
    git ls-files -z '*.sh' 'dot_local/bin/executable_*' | xargs -0 -r shfmt -d

# Show shfmt diffs for staged shell scripts only.
shfmt-staged:
    git diff --name-only --staged -z -- '*.sh' 'dot_local/bin/executable_*' | xargs -0 -r shfmt -d

# Format all tracked shell scripts with shfmt.
shfmt-fix:
    git ls-files -z '*.sh' 'dot_local/bin/executable_*' | xargs -0 -r shfmt -w

# Format staged shell scripts with shfmt.
shfmt-fix-staged:
    git diff --name-only --staged -z -- '*.sh' 'dot_local/bin/executable_*' | xargs -0 -r shfmt -w

# Run staged-only security, lint, and formatting checks.
lint-staged:
    just gitleaks-staged
    just shellcheck-staged
    just shfmt-staged

# Format all tracked shell scripts in-place.
fmt:
    just shfmt-fix

# -----------------------------------------------------------------------------
# Chezmoi workflow
# -----------------------------------------------------------------------------
# Important:
# - Edit managed dotfiles in chezmoi source, not directly in $HOME.
# - Use `just cm-edit ~/.zshrc` or edit files under ~/.local/share/chezmoi.
# - `cm-status` and `cm-diff` exclude scripts on purpose.
#   Chezmoi run scripts often show `R` (= will run), which is normal and does
#   not mean the repo is drifting.
# - Use `cm-apply-dry` before `cm-apply-verbose` when you want a safe preview.

# Show real chezmoi drift, excluding run scripts.
cm-status:
    chezmoi status -x scripts

# Diff managed files against target state, excluding run scripts.
cm-diff:
    chezmoi diff -x scripts

# Apply chezmoi source to the home directory target.
cma:
    chezmoi apply

# Apply chezmoi source with verbose output.
cm-apply-verbose:
    chezmoi apply -v

# Preview an apply without changing the home directory.
cm-apply-dry:
    chezmoi apply -n -v

# List all files currently managed by chezmoi.
cm-managed:
    chezmoi managed

# Show git status plus real chezmoi drift.
cm-quick-check:
    git status -sb
    chezmoi status -x scripts

# Show git status plus chezmoi status and diff.
cm-audit:
    git status -sb
    chezmoi status -x scripts
    chezmoi diff -x scripts

# Add an existing home-directory file to chezmoi management.
cm-add path:
    chezmoi add {{path}}

# Open the chezmoi source file for a managed target path.
cm-edit path:
    chezmoi edit {{path}}

readd:
    chezmoi re-add ~/.pi/agent/settings.json
    chezmoi re-add ~/.opencode/agent/settings.json
# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

# OpenCode QA smoke tests.
#
# Usage:
# - `just opencode-qa`      -> run the full QA sweep
# - `just qa-gemini-or`     -> test Gemini 3.1 Pro via OpenRouter
# - `just qa-flash-or`      -> test Gemini 3 Flash via OpenRouter
# - `just qa-gpt`           -> test a single agent
#
# Each recipe asks the target agent to reply with exactly `OK`.
alias ocqa := opencode-qa
opencode-qa:
    just qa-default || true
    just qa-grok || true
    just qa-mini || true
    just qa-glm || true
    just qa-flash-or || true

# OTHER OPTIONS ..
# just qa-build || true
# just qa-gemini-or || true
# just qa-gpt || true

# Run the default opencode QA check.
qa-default:
    opencode run "reply with exactly OK"

# Run the build agent opencode QA check.
qa-build:
    opencode run --agent build "reply with exactly OK"

# Run the grok agent opencode QA check.
qa-grok:
    opencode run --agent grok "reply with exactly OK"

# Run the mini-zen agent opencode QA check.
qa-mini:
    opencode run --agent mini-zen "reply with exactly OK"

# Run the gpt agent opencode QA check.
qa-gpt:
    opencode run --agent gpt "reply with exactly OK"

# Run the glm-zen agent opencode QA check.
qa-glm:
    opencode run --agent glm-zen "reply with exactly OK"

# Run the Gemini 3 Flash via OpenRouter opencode QA check.
qa-flash-or:
    opencode run --agent flash-or "reply with exactly OK"

# Run the Gemini 3.1 Pro via OpenRouter opencode QA check.
qa-gemini-or:
    opencode run --agent gemini-or "reply with exactly OK"

# Transcribe a YouTube URL. Wrap the URL in quotes. Extra CLI args are forwarded.
alias ttr := transcript
transcript url *args:
    uv run ~/.local/share/chezmoi/dot_config/ai_templates/skills/utils/transcript-sk/scripts/transcript.py {{quote(url)}} {{args}}

# Update all opensrc repositories listed in sources.json.
update-oss:
    cat opensrc/sources.json | jq -r '.repos[].name' | sed 's|github.com/||' | xargs opensrc

# -----------------------------------------------------------------------------
# git
# -----------------------------------------------------------------------------

c:
    opencode run --agent mini-zen "load skill commit, and commit"

# -----------------------------------------------------------------------------
# System maintenance
# -----------------------------------------------------------------------------

# Update Cli Apps
uca:
    just brew-daily
    just uv-daily
    just npm-daily
    just bun-globals-full
    amp update
    claude update
    pi update
    qmd update
    qmd embed
    qmd cleanup
    qmd status

uca-qmd-update:
    echo "hello"

# Update Cli Apps
uca-full:
    brew-full
    uv-full
    npm-full
    bun-globals-full

# Homebrew routine maintenance for daily-use formulas.
brew-daily:
    brew update
    brew upgrade codex chezmoi git go neovim fzf fd bat yq zoxide yt-dlp
    brew upgrade oven-sh/bun/bun || true
    brew cleanup
    brew autoremove
    type -a chezmoi git go nvim fzf fd bat yq zoxide yt-dlp bun
    brew outdated

# Homebrew full refresh for all formulas and casks.
brew-full:
    brew update
    brew upgrade --formula
    brew upgrade --cask
    brew cleanup
    brew autoremove
    brew doctor
    brew outdated

# Upgrade all installed uv tools and show the current tool list.
uv-daily:
    uv tool upgrade --all
    uv tool list

# Upgrade all installed uv tools, show the current tool list, and prune cache.
uv-full:
    uv tool upgrade --all
    uv tool list
    uv cache prune

# Update global npm packages for the active Node version and list them.
npm-daily:
    find "$(npm root -g)" -name '.DS_Store' -delete
    npm outdated -g --depth=0 || true
    npm update -g
    npm list -g --depth=0

# Run a fuller maintenance pass for global npm packages.
npm-full:
    find "$(npm root -g)" -name '.DS_Store' -delete
    npm outdated -g --depth=0 || true
    npm update -g
    npm cache verify
    npm doctor
    npm list -g --depth=0

# List Bun global packages from Bun's global install directory.
bun-globals:
    cd "$HOME/.bun/install/global" && bun pm ls

# Upgrade managed Bun global packages explicitly and list them.
bun-globals-full:
    bun add -g @biomejs/biome@latest @google/gemini-cli@latest @googleworkspace/cli@latest @kilocode/cli@latest @mariozechner/pi-coding-agent@latest @tobilu/qmd@latest agent-browser@latest defuddle-cli@latest opencode-ai@latest oxlint@latest typescript@latest typescript-language-server@latest
    cd "$HOME/.bun/install/global" && bun pm ls
