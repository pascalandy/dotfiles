# Chezmoi Secrets Management

## 1. Keyring Integration (macOS Keychain)

Chezmoi has built-in macOS Keychain support via the `keyring` template function:

```bash
# Store a secret
chezmoi secret keyring set --service=exa --user=api_key

# Retrieve (for verification)
chezmoi secret keyring get --service=exa --user=api_key

# Delete if needed
chezmoi secret keyring delete --service=exa --user=api_key
```

**In templates** (`.tmpl` files):
```json
"EXA_API_KEY": "{{ keyring "exa" "api_key" }}"
```

## 2. Alternative Methods Chezmoi Supports

**A. Chezmoi.toml data (simpler, less secure)**
```toml
# ~/.config/chezmoi/chezmoi.toml
[data]
exa_api_key = "your-key"
```
Template: `"{{ .exa_api_key }}"`

**B. 1Password CLI** (`chezmoi secret onepassword`)
**C. Bitwarden CLI** (`chezmoi secret bitwarden`)
**D. Pass (Unix password store)**
**E. Vault, AWS Secrets Manager, etc.**

## 3. Security Best Practices

- **Use `.tmpl` extension** for any file with secrets
- **Never commit raw secrets** - chezmoi's `keyring` function retrieves at apply time
- **Use `private_` prefix** for sensitive files (e.g., `private_dot_ssh/config.tmpl`)
- **Enable pre-commit hooks** - use `gitleaks` in your `lefthook` setup

## 4. Troubleshooting

```bash
# Test if a keyring value exists
chezmoi secret keyring get --service=exa --user=api_key

# Dry-run to see if templates resolve
chezmoi apply --dry-run --verbose

# Check what data chezmoi sees
chezmoi data | jq '.chezmoi.config'
```

## 5. Migration from .env to Keyring

```bash
# 1. Read current value
cat .env | grep EXA_API_KEY

# 2. Store in keyring
chezmoi secret keyring set --service=exa --user=api_key

# 3. Update template to use keyring function
# 4. Remove .env from repo
# 5. Apply to test
chezmoi apply -v
```
