# Upstream

Single source of truth for provenance. Do not duplicate this information elsewhere in the skill.

## Sources

- **CLI**: https://github.com/run-llama/liteparse
- **Skill**: https://github.com/run-llama/llamaparse-agent-skills

## Original metadata

- **Author**: LlamaIndex
- **License**: MIT
- **Version**: 0.1.0

## Local modifications

- Restructured the original single `SKILL.md` into a hierarchical meta-skill (`Preferences`, `Parse`, `Screenshot`, `Setup`).
- Added per-language configs `Preferences/config.en.json` and `Preferences/config.fr.json` as the single source of truth for user defaults (`ocrLanguage`, `dpi`, `outputFormat`, `outputSuffix=_lykra.md`).
