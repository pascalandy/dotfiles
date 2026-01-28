set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

# test all locally
ci:
    just gitleaks
    just shellcheck
    just shfmt
    chezmoi apply -n -v

# chezmoi
gitleaks:
    gitleaks detect --config .gitleaks.toml

gitleaks-staged:
    gitleaks protect --staged --verbose

shellcheck:
    git ls-files -z '*.sh' 'dot_local/bin/executable_*' | xargs -0 -r shellcheck

shellcheck-staged:
    git diff --name-only --staged -z -- '*.sh' 'dot_local/bin/executable_*' | xargs -0 -r shellcheck

shfmt:
    git ls-files -z '*.sh' 'dot_local/bin/executable_*' | xargs -0 -r shfmt -d

shfmt-staged:
    git diff --name-only --staged -z -- '*.sh' 'dot_local/bin/executable_*' | xargs -0 -r shfmt -d

shfmt-fix:
    git ls-files -z '*.sh' 'dot_local/bin/executable_*' | xargs -0 -r shfmt -w

shfmt-fix-staged:
    git diff --name-only --staged -z -- '*.sh' 'dot_local/bin/executable_*' | xargs -0 -r shfmt -w

# staged checks
lint-staged:
    just gitleaks-staged
    just shellcheck-staged
    just shfmt-staged

# formatting
fmt:
    just shfmt-fix

# chezmoi
cm-status:
    chezmoi status

cm-diff:
    chezmoi diff

# chezmoi apply
cma:
    chezmoi apply

cm-apply-verbose:
    chezmoi apply -v

cm-apply-dry:
    chezmoi apply -n -v

cm-managed:
    chezmoi managed

cm-quick-check:
    git status -sb
    chezmoi status

cm-add path:
    chezmoi add {{path}}

cm-edit path:
    chezmoi edit {{path}}

default:
    @just --list
