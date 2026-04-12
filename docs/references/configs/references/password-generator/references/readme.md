---
name: Password Generator README
description: Password generator usage and options documentation
tags:
  - area/ea
  - kind/doc
  - status/stable
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Password Generator

Generate secure, readable passwords with structured format and clipboard integration.

## Usage

```bash
uv run scripts/password_generator.py
uv run scripts/password_generator.py --length 32
uv run scripts/password_generator.py --count 3 --copy
```

## Options

| Option           | Default | Description                                           |
| ---------------- | ------- | ----------------------------------------------------- |
| `--length`       | 28      | Total password length including underscores (min: 10) |
| `--count`        | 10      | Number of passwords to generate (max: 100)            |
| `--copy`         | auto    | Force clipboard copying                               |
| `--no-clipboard` | -       | Disable clipboard copying                             |

## Output Format

```
part1_part2_part3
```

- **part1**: 4 characters
- **part2**: Variable length (fills remaining)
- **part3**: 4 characters
- **Separator**: underscore (`_`)

## Character Set

Safe characters excluding visually ambiguous ones (I, O, l, o):

- Uppercase: A-HJ-NP-Z
- Lowercase: a-kmnp-z
- Digits: 0-9

## Clipboard Support

Automatically copies last generated password using:

- macOS: `pbcopy`
- Linux: `xclip`

## CLI Integration

The `passgen` command is available system-wide via a wrapper script at `~/.local/bin/passgen`.

> **Warning:** The CLI wrapper depends on this script being at the expected path:
> ```bash
> ~/.local/share/chezmoi/docs/configs/password-generator/scripts/password_generator.py
> ```
> 
> If you move this script, update the wrapper at `dot_local/bin/executable_passgen`.

## Related

- [[source]]
- [[LOG]]
