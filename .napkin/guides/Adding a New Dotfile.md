---
date: "2026-03-29"
tags:
  - guide
---
# Adding a New Dotfile

## Prerequisites
- File exists in home directory (`~/`) and needs to be managed by chezmoi
- You understand the chezmoi naming conventions (see [[Repository Topology]])

## Steps
1. **Verify the file is not already managed**
   ```bash
   chezmoi managed | grep <filename>
   ```

2. **Add the file to chezmoi**
   ```bash
   chezmoi add ~/.config/someapp/config.json
   ```
   
3. **Edit in source if needed**
   - File appears under `~/.local/share/chezmoi/` with appropriate prefix
   - `dot_` prefix for files starting with `.`
   - `private_` prefix for sensitive files (600/700 permissions)
   - `executable_` prefix for scripts needing execute permission
   - `.tmpl` extension if using chezmoi templates (`{{ .variable }}`)

4. **Apply and verify**
   ```bash
   just cm-apply-dry    # Preview changes
   just cm-apply-verbose # Apply with output
   ```

5. **Run quality checks**
   ```bash
   just ci
   ```

## Common problems
- **"File already managed"** — Check if it's already in chezmoi source
- **Template variables not processed** — Ensure file has `.tmpl` extension
- **Wrong permissions** — Use `private_` prefix for sensitive files, `executable_` for scripts

## Related
- [[Repository Topology]]
- [[Testing Dotfile Changes]]
- [[Chezmoi Apply Automation]]
