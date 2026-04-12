---
name: Chezmoi Secrets
description: How chezmoi handles API keys and credentials — keyring integration, alternative backends, best practices, and `.env` migration
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-to-configure-chezmoi
---

Chezmoi treats secrets as *data pulled in at apply time*, never as content committed to the source tree. The model: you write a `.tmpl` file that references a secret by name, chezmoi resolves the name against a backend (keyring, 1Password, Bitwarden, Pass, Vault, or a plain `chezmoi.toml` entry), and the real value is substituted only when `chezmoi apply` runs on your machine.

This means:

- Secrets never land in git history.
- Two machines with different credentials render the same source tree into different applied copies.
- Losing a machine does not leak anything from the repo.

## 1. Keyring backend (macOS Keychain)

The default on macOS. Chezmoi's `keyring` template function reads directly from the system keychain.

### Store a secret

```bash
chezmoi secret keyring set --service=exa --user=api_key
# prompts for the value (hidden input)
```

### Use it in a template

```bash
# Source file: dot_config/example/config.json.tmpl
{
  "exa_api_key": "{{ keyring "exa" "api_key" }}"
}
```

On apply, chezmoi reads `exa/api_key` from the keychain and substitutes the value.

### Retrieve for verification

```bash
chezmoi secret keyring get --service=exa --user=api_key
```

### Delete

```bash
chezmoi secret keyring delete --service=exa --user=api_key
```

## 2. Alternative backends

Chezmoi supports several other secret stores. Pick based on what is already in your environment.

| Backend | Template function | When to use |
|---|---|---|
| **`chezmoi.toml` data** | `{{ .some_key }}` | Quick setup, low security. The value lives in plaintext under `~/.config/chezmoi/chezmoi.toml`. Good for low-risk config that is annoying to keep elsewhere. |
| **macOS Keychain** | `keyring` | macOS-only. No extra tooling. Default for this repo. |
| **1Password CLI** | `onepasswordRead`, `onepassword` | You already use 1Password and want one canonical place for all secrets. |
| **Bitwarden CLI** | `bitwarden`, `bitwardenFields` | You prefer Bitwarden. |
| **Pass (Unix password store)** | `pass` | GPG-backed, Linux-native. |
| **HashiCorp Vault** | `vault` | Team or multi-machine setup where Vault already exists. |

Full reference for each function is in [[upstream-links]].

### Fallback pattern with `chezmoi.toml`

If you want the template to work without any secret backend at all, define the value under `[data]` in `~/.config/chezmoi/chezmoi.toml`:

```toml
[data]
exa_api_key = "your-exa-api-key-here"
openrouter_api_key = "sk-or-v1-..."
```

Then reference it:

```bash
"exa_api_key": "{{ .exa_api_key }}"
```

This is the simplest setup and the easiest to debug, but the value is plaintext on disk. Fine for low-risk keys, wrong for production credentials.

## 3. Best practices

- **`.tmpl` extension is mandatory.** Any file using `keyring`, `onepasswordRead`, or any other secret function must have the `.tmpl` suffix. Without it, chezmoi does not process the placeholders and the literal function call gets written to the applied copy.
- **`private_` prefix for sensitive files.** Files containing secrets should also use the `private_` prefix so the applied copy has mode 600 or 700.
- **Never commit raw secrets.** The whole point of the keyring pattern is that `git log` contains *template calls*, not values. If you ever see a real secret in `git diff`, stop the commit.
- **Use `gitleaks` as a pre-commit hook.** A secret-scanner catches accidents before they land. The [`lefthook`](../../how-my-chezmoi-is-configured.md) setup in this repo runs `gitleaks protect --staged` on every commit.
- **Put secrets behind a single abstraction.** If one team or tool owns several keys, group them under one service name (`--service=openrouter --user=api_key` rather than inventing a service per key). It keeps the keychain clean.

## 4. Troubleshooting

### Is the secret actually stored?

```bash
chezmoi secret keyring get --service=exa --user=api_key
```

If this errors, the value is not in the keychain under that service/user combination. Use `set` to store it.

### Does the template resolve?

```bash
chezmoi apply -n -v
```

Dry run, verbose. If a template fails to resolve, chezmoi prints the error and the file it was trying to render. Fix the template or store the missing secret.

### What does chezmoi actually see?

```bash
chezmoi data | jq '.chezmoi.config'
```

Shows the config chezmoi is operating with. Useful when the template reads from `.data` rather than `keyring`.

## 5. Migrating from `.env` to keyring

When moving a secret from an environment file into the keychain:

```bash
# 1. Read the current value (do not echo to history)
grep EXA_API_KEY .env

# 2. Store in keyring
chezmoi secret keyring set --service=exa --user=api_key
# paste the value when prompted

# 3. Update the template to use the keyring function
# e.g. in opencode.json.tmpl:
#   "exa_api_key": "{{ keyring "exa" "api_key" }}"

# 4. Delete .env and any fallback plaintext copies
trash .env

# 5. Apply and verify
chezmoi apply -v
chezmoi cat ~/.config/example/config.json
```

Step 5 is important: always confirm the rendered output is what you expect before relying on it.

## Related

- [[cli]]
- [[templates]]
- [[naming-conventions]]
- [[upstream-links]]
- [[how-my-chezmoi-is-configured]]
