---
title: Supply Chain Security - Minimum Release Age Protection
type: feat
  - status/close
date: 2025-04-01
---

# Supply Chain Security - Minimum Release Age Protection

## Overview

Implement supply chain security measures for package managers that lack native age-based protection. **npm and UV are already configured** with 7-day minimum age restrictions. This plan implements defense-in-depth for the remaining tools: **pip/pipx (priority #3), Go (priority #4), Cargo (priority #5), and Bun (already created as reference)**.

## Current State (Already Configured)

These tools already have supply chain protection:

1. **npm** - `min-release-age=7` in `~/.npmrc` ✅
2. **uv** - `exclude-newer = "7 days"` in `~/.config/uv/uv.toml` ✅

## Problem Frame

Supply chain attacks on open-source packages are increasing. Attackers compromise maintainer accounts or inject malicious code into popular packages. npm and uv have native 7-day minimum age protections, but other tools (pip, Go, Cargo, Bun) lack this feature. This plan implements defense-in-depth via lockfiles, version pinning, and explicit version requirements.

## Requirements Trace

- **R1.** npm protection must be verified and documented (EXISTING)
- **R2.** uv protection must be verified and documented (EXISTING)
- **R3.** pip/pipx must enforce explicit versions (NEW - 3rd priority)
- **R4.** Go must enforce version pinning (NEW - 4th priority)
- **R5.** Cargo must enforce locked installs (NEW - 5th priority)
- **R6.** Bun must enforce lockfile discipline (NEW - reference implementation already created)
- **R7.** All configurations must be managed via chezmoi
- **R8.** Unified verification tool must confirm all protections

## Scope Boundaries

- **In scope:** pip/pipx, Go, Cargo, Bun (new implementations)
- **Already done:** npm, uv (verification only)
- **Out of scope:** Homebrew (no native age restriction), Docker images, system package managers

## Context & Research

### Existing Protection (Reference Implementation)

**npm:**
- Config: `~/.npmrc` with `min-release-age=7`
- Native feature: rejects packages newer than 7 days
- Status: Already configured, needs verification

**uv:**
- Config: `~/.config/uv/uv.toml` with `exclude-newer = "7 days"`
- Native feature: rejects packages newer than 7 days
- Status: Already configured, needs verification
- **This is the gold standard** - other tools should reference this

### Tools Without Native Protection

**pip/pipx:**
- No native age restriction
- Defense: explicit version requirements + virtualenv enforcement
- Will show banner: "UV has 7-day protection, pip does not"

**Go:**
- No native age restriction
- Defense: version pinning (@v1.2.3 syntax)
- Will show banner comparing to UV's protection

**Cargo:**
- No native age restriction
- Defense: `--locked` flag for reproducible builds
- Will show banner comparing to UV's protection

**Bun:**
- No native age restriction
- Defense: frozen lockfile enforcement
- Reference implementation already created

## Key Technical Decisions

1. **npm/uv are the reference** - Other tools show limitation banners comparing to these
2. **Priority order:** pip/pipx (#3) → Go (#4) → Cargo (#5) → Bun (reference already done)
3. **Defense-in-depth** - No tool without native age support can match npm/uv automatically
4. **Clear messaging** - Every wrapper shows what protection exists vs what's missing
5. **Unified verification** - `supply-chain-check` shows comparison table

## Implementation Units

- [ ] **Unit 1: npm Verification (EXISTING)**

**Goal:** Verify npm protection is active and document it

**Requirements:** R1

**Dependencies:** None

**Files:**
- Verify: `dot_npmrc` exists with `min-release-age=7`
- Create: Documentation reference

**Approach:**
- Confirm `~/.npmrc` contains `min-release-age=7`
- Document as reference implementation
- Show in verification tool

**Verification:**
- `cat ~/.npmrc | grep min-release-age` shows `min-release-age=7`

- [ ] **Unit 2: uv Verification (EXISTING - GOLD STANDARD)**

**Goal:** Verify uv protection is active and document it as the gold standard

**Requirements:** R2

**Dependencies:** None

**Files:**
- Verify: `dot_config/uv/uv.toml` exists with `exclude-newer = "7 days"`
- Create: `dot_local/bin/executable_uv-tool-safe` (for tool installs)

**Approach:**
- Confirm `~/.config/uv/uv.toml` contains `exclude-newer = "7 days"`
- Create `uv-tool-safe` wrapper for `uv tool install` commands
- Document as the gold standard other tools reference

**Verification:**
- `cat ~/.config/uv/uv.toml | grep exclude-newer` shows `exclude-newer = "7 days"`
- UV is marked as "GOLD STANDARD" in all documentation

- [ ] **Unit 3: pip/pipx Configuration (NEW - 3rd Priority)**

**Goal:** Enforce explicit version requirements for pip/pipx with clear UV comparison

**Requirements:** R3

**Dependencies:** Units 1-2 (reference implementations)

**Files:**
- Create: `dot_config/pip/pip.conf`
- Create: `dot_local/bin/executable_pip-install-safe`
- Create: `dot_local/bin/executable_pipx-install-safe`
- Modify: `dot_zshrc` (add pip/pipx aliases)

**Approach:**
- Create `pip.conf` with `require-virtualenv = true`
- Create wrapper scripts that:
  - Reject bare package names without versions
  - Show prominent limitation banner:
    ```
    ⚠️  pip/pipx does NOT have automatic age protection
    UV has exclude-newer = "7 days" (packages older than 7 days only)
    pip requires explicit versions for defense-in-depth
    ```
  - Require `package==version` syntax
  - Recommend UV for new Python projects

**Patterns to follow:**
- Bun example's limitation banner style
- Clear comparison to UV's superior protection

**Test scenarios:**
- `pip-install-safe requests` fails (no version specified)
- `pip-install-safe requests==2.31.0` succeeds
- Shows banner explaining UV has better protection

**Verification:**
- pip config exists at `~/.config/pip/pip.conf`
- Both wrapper scripts show clear limitation warnings referencing UV

- [ ] **Unit 4: Go Configuration (NEW - 4th Priority)**

**Goal:** Enforce version-pinned Go installs with UV comparison

**Requirements:** R4

**Dependencies:** Units 1-2 (reference implementations)

**Files:**
- Create: `dot_config/go/README.md` (documentation)
- Create: `dot_local/bin/executable_go-install-safe`
- Modify: `dot_zshrc` (add Go alias)

**Approach:**
- Create documentation explaining Go's lack of age restrictions
- Create `go-install-safe` wrapper that:
  - Requires explicit versions (@v1.2.3 syntax)
  - Shows limitation banner:
    ```
    ⚠️  Go does NOT have automatic age protection
    UV has exclude-newer = "7 days" (packages older than 7 days only)
    Go requires explicit version pinning for defense-in-depth
    ```
  - Suggests waiting 7 days after release (like UV's protection)

**Patterns to follow:**
- Bun example's limitation banner style
- Reference UV as the gold standard

**Test scenarios:**
- `go-install-safe` without version fails with helpful message
- `go-install-safe pkg@v1.2.3` executes `go install pkg@v1.2.3`
- Shows banner referencing UV's superior protection

**Verification:**
- Documentation exists and references UV
- `go-install-safe` shows clear limitation warning

- [ ] **Unit 5: Cargo Configuration (NEW - 5th Priority)**

**Goal:** Configure Cargo to enforce locked installs with UV comparison

**Requirements:** R5

**Dependencies:** Units 1-2 (reference implementations)

**Files:**
- Create: `dot_cargo/config.toml`
- Create: `dot_local/bin/executable_cargo-install-safe`
- Modify: `dot_zshrc` (add Cargo alias)

**Approach:**
- Create `~/.cargo/config.toml` with alias: `i = "install --locked"`
- Create `cargo-install-safe` wrapper that:
  - Enforces `--locked` flag
  - Shows limitation banner:
    ```
    ⚠️  Cargo does NOT have automatic age protection
    UV has exclude-newer = "7 days" (packages older than 7 days only)
    Cargo uses --locked for reproducible builds (defense-in-depth)
    ```
  - Requires explicit versions

**Patterns to follow:**
- Bun example's limitation banner style
- Reference UV as the gold standard

**Test scenarios:**
- `cargo i package` uses `--locked` flag
- `cargo-install-safe` shows limitation banner
- `cargo-install-safe` fails if no Cargo.lock present

**Verification:**
- Cargo config exists at `~/.cargo/config.toml`
- `cargo-install-safe` shows clear limitation warning

- [ ] **Unit 6: Bun Configuration (NEW - Reference Implementation)**

**Goal:** Configure Bun for reproducible installs with lockfile enforcement

**Requirements:** R6

**Dependencies:** Units 1-2 (reference implementations)

**Files:**
- Create: `dot_config/bun/bunfig.toml`
- Create: `dot_local/bin/executable_bun-install-safe`
- Modify: `dot_zshrc` (add Bun alias)

**Approach:**
- Create `bunfig.toml` with `install.lockfile = true` and `install.frozen = true`
- Create `bun-install-safe` wrapper with prominent limitation banner:
  ```
  ⚠️  Bun does NOT have automatic age protection
  npm has min-release-age=7
  UV has exclude-newer = "7 days"
  Bun uses frozen lockfiles for defense-in-depth
  ```
- Document that Bun lacks native age restrictions

**Patterns to follow:**
- Already created as reference implementation

**Test scenarios:**
- `bun install` respects lockfile when present
- `bun-install-safe` shows limitation banner
- `bun-install-safe` fails if no lockfile exists

**Verification:**
- Bun config file exists at `~/.config/bun/bunfig.toml`
- `bun-install-safe` shows clear limitation warning

- [ ] **Unit 7: Unified Verification Tool**

**Goal:** Create a single command to verify all supply chain protections

**Requirements:** R7, R8

**Dependencies:** Units 1-6

**Files:**
- Create: `dot_local/bin/executable_supply-chain-check`

**Approach:**
- Script checks all protections and shows comparison:
  ```
  Supply Chain Protection Status
  ==============================
  
  ✅ NATIVE AGE PROTECTION (Gold Standard):
     • npm:  min-release-age=7 days
     • uv:   exclude-newer = "7 days"  ← BEST PROTECTION
  
  ⚠️  DEFENSE-IN-DEPTH (No native age support):
     • pip:   Explicit versions required
     • Go:    Version pinning required
     • Cargo: --locked flag required
     • Bun:   Frozen lockfile required
  ```
- Exit code 0 if npm+uv protection active (critical), non-zero if missing

**Patterns to follow:**
- Existing scripts in `dot_local/bin/`
- Use `set -euo pipefail`

**Test scenarios:**
- Script runs without errors
- Correctly identifies npm+uv as gold standard
- Shows clear comparison table
- Exit code reflects npm+uv status (most critical)

**Verification:**
- Script executable and in PATH
- Output clearly shows which tools have native protection vs defense-in-depth

- [ ] **Unit 8: Documentation Update**

**Goal:** Document the supply chain security setup

**Requirements:** R8

**Dependencies:** Units 1-7

**Files:**
- Modify: `README.md`

**Approach:**
- Add "Supply Chain Security" section to README
- Lead with npm and uv as having native protection
- Show comparison table: Native (npm/uv) vs Defense-in-depth (pip/Go/Cargo/Bun)
- Document the `supply-chain-check` command
- Explain why npm/uv are the gold standard

**Patterns to follow:**
- Existing README structure

**Test scenarios:**
- Documentation is accurate and complete
- npm/uv clearly positioned as having native protection
- Links to relevant external resources

**Verification:**
- README updated with new section
- Section clearly explains the two-tier protection model

## System-Wide Impact

- **Shell startup:** New aliases/functions added to `.zshrc` (minimal impact)
- **Tool behavior:** Users see clear comparison to npm/uv's native protection
- **Documentation:** Users educated on which tools have automatic vs manual protection

## Risks & Dependencies

- **Risk:** Users might not understand the difference between native and defense-in-depth
  - **Mitigation:** Clear comparison table + verification tool shows the distinction
- **Risk:** Wrapper scripts might be bypassed
  - **Mitigation:** Documentation recommends npm/uv for critical installs
- **Risk:** pip/Go/Cargo/Bun limitations might be forgotten
  - **Mitigation:** Every wrapper shows the limitation banner

## Documentation / Operational Notes

- Update README with "Supply Chain Security" section
- Add `supply-chain-check` to `just ci` workflow
- Document the two-tier model: Native (npm/uv) vs Defense-in-depth (others)
- Note: Only npm and uv have automatic age-based protection

## Sources & References

- npm: https://docs.npmjs.com/cli/v10/commands/npm-install#min-release-age
- uv: https://docs.astral.sh/uv/reference/settings/#exclude-newer (GOLD STANDARD)
- pip: https://pip.pypa.io/en/stable/topics/configuration/
- Go Modules: https://go.dev/ref/mod
- Cargo: https://doc.rust-lang.org/cargo/reference/config.html
- Bun: https://bun.sh/docs/runtime/bunfig
