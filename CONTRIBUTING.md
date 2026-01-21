# Contributing

Thanks for the interest in improving these dotfiles. This repo is personal,
but contributions are welcome for portability, documentation, and safe
defaults.

## Guidelines

- Avoid machine-specific state, caches, or generated files.
- Do not commit secrets. Use templates and `private_` files when needed.
- Keep scripts in `dot_local/bin/` and ensure they are executable.
- Follow conventions in `AGENTS.md`.

## Development

1. Fork and clone the repo.
2. Install chezmoi.
3. Review changes with `chezmoi diff` before applying.
4. Run `gitleaks detect` and `shellcheck` on scripts.

## Pull Requests

- Keep changes small and focused.
- Explain why the change is needed and how it was tested.

## License

By contributing, you agree your changes are licensed under the MIT License.
