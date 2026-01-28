set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

# test all locally
ci:
    just gitleaks
    just shellcheck
    just shfmt

default:
    @just --list

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
