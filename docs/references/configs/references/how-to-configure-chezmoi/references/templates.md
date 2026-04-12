---
name: Chezmoi Templates
description: How chezmoi renders `.tmpl` files using Go `text/template` and how to debug them
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-to-configure-chezmoi
---

Chezmoi uses Go's standard `text/template` package to render any source file whose name ends in `.tmpl`. Templates let you inject OS-specific paths, user data, and secrets into configuration files without committing machine-specific values.

## The basics

Any `.tmpl` file is a normal file with `{{ }}` placeholders interpolated at apply time.

```bash
# Source file: dot_zshenv.tmpl
export EDITOR={{ .editor }}
export HOSTNAME={{ .chezmoi.hostname }}
```

`chezmoi apply` renders this to `~/.zshenv` with real values substituted.

## Where data comes from

Templates have access to three kinds of data:

1. **Built-in chezmoi data** — info chezmoi computes automatically: OS, hostname, architecture, username, home directory, kernel, etc.
2. **Custom data from `chezmoi.toml`** — anything you add under a `[data]` table in `~/.config/chezmoi/chezmoi.toml`.
3. **Template functions** — helpers like `keyring`, `onepasswordRead`, `env`, `promptStringOnce`, `include`, `joinPath`, etc.

To see everything available right now:

```bash
chezmoi data
```

This prints a JSON blob of every variable and function the current templates can use. The output is large; pipe it into `jq` or `less`.

## Template functions you will actually use

| Function | Purpose | Example |
|---|---|---|
| `.chezmoi.os` | Current OS (`darwin`, `linux`, `windows`) | `{{ if eq .chezmoi.os "darwin" }}...{{ end }}` |
| `.chezmoi.hostname` | Hostname of the current machine | `export HOSTNAME={{ .chezmoi.hostname }}` |
| `.chezmoi.homeDir` | Current user's home directory | `{{ .chezmoi.homeDir }}/bin` |
| `.<key>` | Custom data from `chezmoi.toml` | `"apiKey": "{{ .exa_api_key }}"` |
| `keyring` | Read from OS keyring | `"{{ keyring "exa" "api_key" }}"` |
| `env` | Read an environment variable | `{{ env "USER" }}` |
| `promptStringOnce` | Ask once during first apply | `{{ promptStringOnce "name" "Your name" }}` |

For the full list, see [[upstream-links]] → Template functions.

## Debugging a template

Three commands make template work tractable:

### 1. Preview what a template would render

```bash
chezmoi cat ~/.zshenv
```

`chezmoi cat` shows the rendered output chezmoi would write to a target. It does not modify anything. Use this before `chezmoi apply` to confirm a template is producing the expected text.

### 2. Test an expression in isolation

```bash
chezmoi execute-template '{{ .chezmoi.os }}-{{ .chezmoi.hostname }}'
```

Evaluates one expression against the current data and prints the result. Great for confirming a function works before wiring it into a file.

### 3. Dry-run the whole apply

```bash
chezmoi apply -n -v
```

Dry run, verbose. Shows every file that would change without writing anything.

## Conditional content

Go templates support `if`, `else`, `range`, and comparisons. The most common pattern in dotfiles is OS branching:

```bash
{{ if eq .chezmoi.os "darwin" }}
export HOMEBREW_PREFIX=/opt/homebrew
{{ else if eq .chezmoi.os "linux" }}
export HOMEBREW_PREFIX=/home/linuxbrew/.linuxbrew
{{ end }}
```

## Common mistakes

- **Missing `.tmpl` suffix.** You write `{{ keyring "foo" "bar" }}` in a plain file. The braces get written literally to the applied copy. Always rename to `.tmpl` when you add a placeholder.
- **Spaces around delimiters.** `{{-` and `-}}` trim whitespace. `{{ foo }}` does not. If you see extra blank lines in the rendered output, that is probably why.
- **Referring to data that does not exist.** Templates fail hard on undefined keys. Run `chezmoi data | jq '.<your-key>'` to confirm a key exists before referencing it.
- **Escaping in JSON templates.** When the template output is JSON, wrap the interpolation in quotes: `"apiKey": "{{ .key }}"`, not `"apiKey": {{ .key }}`.

## Related

- [[cli]]
- [[naming-conventions]]
- [[secrets]]
- [[upstream-links]]
