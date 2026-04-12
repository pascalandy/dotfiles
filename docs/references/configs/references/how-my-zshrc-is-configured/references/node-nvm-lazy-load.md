---
name: node-nvm-lazy-load
description: The two-part pattern used to keep shell startup fast while still exposing global node CLIs
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Node.js Lazy Loading via nvm

## The problem this solves

Sourcing `$NVM_DIR/nvm.sh` at every shell start adds hundreds of milliseconds. But globally installed node CLIs (for example, `claude`) need to be on `PATH` immediately, before anyone has typed `nvm` or `node`.

## The pattern

### Part 1: eagerly prepend the default node's bin to PATH

```zsh
if [[ -d "$NVM_DIR/versions/node" ]]; then
    _NODE_DEFAULT=$(ls "$NVM_DIR/versions/node" 2>/dev/null | sort -V | tail -1)
    [[ -n "$_NODE_DEFAULT" ]] && export PATH="$NVM_DIR/versions/node/$_NODE_DEFAULT/bin:$PATH"
    unset _NODE_DEFAULT
fi
```

This runs at shell start. It picks the highest-versioned node directory under `$NVM_DIR/versions/node/` and prepends its `bin/` to `PATH`, exposing `node`, `npm`, `npx`, and any globally installed CLIs — without sourcing nvm.

### Part 2: lazy-load real nvm on first call

```zsh
_nvm_lazy_load() {
    unset -f nvm node npm npx
    [[ -f "$NVM_DIR/nvm.sh" ]] && source "$NVM_DIR/nvm.sh"
    [[ -f "$NVM_DIR/bash_completion" ]] && source "$NVM_DIR/bash_completion"
}

nvm()  { _nvm_lazy_load; nvm  "$@"; }
node() { _nvm_lazy_load; node "$@"; }
npm()  { _nvm_lazy_load; npm  "$@"; }
npx()  { _nvm_lazy_load; npx  "$@"; }
```

On first invocation of any of the wrapper functions:
1. The wrappers unset themselves so their names go back to resolving against the real binaries / nvm shell functions
2. `nvm.sh` and its completion are sourced
3. The original call is re-issued against the now-real command

Subsequent calls go straight to nvm-managed functions.

## Consequences and trade-offs

- Shell start is fast — `nvm.sh` is never sourced unless node tooling is actually used
- Global CLIs under the default node version work immediately
- Version switching via `nvm use ...` works, but only kicks in after the first `nvm`/`node`/`npm`/`npx` call in the session
- The "default" node is whatever `ls | sort -V | tail -1` picks — i.e. the highest installed version, not necessarily whatever `nvm alias default` points to
