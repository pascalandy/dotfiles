# Auth and Config

Use this reference for login, token handling, host and account switching, git credential setup, and CLI config.

## Authentication

### Login

```bash
# default github.com login
gh auth login

# web flow
gh auth login --web

# custom host (GitHub Enterprise)
gh auth login --hostname enterprise.internal

# read token from stdin
gh auth login --with-token < token.txt
```

### Status and current account

```bash
gh auth status
gh auth status --active
gh auth status --hostname github.com
gh auth token
```

### Switch accounts or hosts

```bash
gh auth switch
gh auth switch --hostname github.com --user monalisa
```

### Refresh scopes

```bash
gh auth refresh
gh auth refresh --scopes write:org,read:public_key
gh auth refresh --remove-scopes delete_repo
gh auth refresh --reset-scopes
```

### Logout

```bash
gh auth logout
gh auth logout --hostname github.com --user monalisa
```

## Git credential integration

```bash
gh auth setup-git
gh auth setup-git --hostname enterprise.internal
```

Use this when the user wants HTTPS git pushes and pulls to reuse GitHub CLI credentials.

## Config

```bash
gh config list
gh config get editor
gh config set editor vim
gh config set git_protocol ssh
gh config set prompt disabled
gh config set pager "less -R"
gh config clear-cache
```

## Common troubleshooting sequence

1. `gh --version`
2. `gh auth status`
3. `gh config list`
4. `gh auth token` only if the user explicitly needs token-aware automation
5. `gh <command> --help` for version-specific syntax

## Safety notes

- Prefer environment variables or stdin for tokens instead of putting secrets in shell history.
- Confirm the host when working with GitHub Enterprise.
- If a command fails because of missing scopes, use `gh auth refresh --scopes ...` before you redo the entire login flow.
