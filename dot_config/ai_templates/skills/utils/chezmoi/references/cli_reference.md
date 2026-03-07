# Chezmoi CLI Reference

## Core Commands

| Command                | Description                                 |
| ---------------------- | ------------------------------------------- |
| `chezmoi init`         | Initialize chezmoi or clone a dotfiles repo |
| `chezmoi add $FILE`    | Add a file to chezmoi management            |
| `chezmoi edit $FILE`   | Edit the source file for a managed dotfile  |
| `chezmoi apply`        | Apply changes from source to home directory |
| `chezmoi diff`         | Show differences between source and home    |
| `chezmoi status`       | Show status of managed files                |
| `chezmoi managed`      | List all managed files                      |
| `chezmoi unmanaged`    | List files in home not managed by chezmoi   |
| `chezmoi cd`           | Launch a shell in the source directory      |
| `chezmoi forget $FILE` | Stop managing a file (keeps it in home)     |
| `chezmoi remove $FILE` | Remove file from both chezmoi and home      |

## Source Directory

Default location: `~/.local/share/chezmoi`

## File Naming Conventions in Source

- `dot_` prefix: Represents a hidden file (starting with `.`) in home.
- `executable_` prefix: File will be made executable.
- `private_` prefix: File will have restricted permissions (0600 or 0700).
- `readonly_` prefix: File will be read-only.
- `exact_` prefix: Directory will be managed exactly (files not in source will be deleted from home).
- `.tmpl` suffix: File is a template.

## Templates

Chezmoi uses `text/template` (Go templates).

- Use `chezmoi data` to see available variables.
- Use `chezmoi execute-template` to test a template.
