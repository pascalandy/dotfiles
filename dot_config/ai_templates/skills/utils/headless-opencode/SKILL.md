---
name: headless-opencode
description: "Use whenever the user wants to run OpenCode in headless/non-interactive mode: `opencode run`, `opencode serve`, scripted automation, JSON output, or attaching to a running server. Prefer this skill over interactive TUI guidance when the task should finish in one terminal command or needs programmatic/automated execution."
---

# Headless OpenCode

Run OpenCode CLI in non-interactive headless mode for scripting, automation, CI/CD, or quick answers without the TUI.

**Important:** Always use --agents, never --models. Agents are defined in `dot_config/opencode/opencode.json.tmpl`. 

### Use specific agent

**Core agents:**
```bash
opencode run --agent 1-kimi "Your prompt"    # Kimi 2.5 Turbo (default)
opencode run --agent 2-opus "Your prompt"      # Claude Opus 4-6
opencode run --agent 3-gpt "Your prompt"     # GPT-5.4
opencode run --agent 4-sonnet "Your prompt"  # Claude Sonnet 4-6
```

**Specialized agents:**
```bash
opencode run --agent worker "Your prompt"     # GPT-5.4 general worker
opencode run --agent worker1 "Your prompt"    # Claude Sonnet (thinking)
opencode run --agent worker2 "Your prompt"    # GLM 5.1
opencode run --agent worker3 "Your prompt"    # agt mini (GPT-5.4-mini)
opencode run --agent glm "Your prompt"        # GLM 5.1
opencode run --agent gptmini "Your prompt"    # GPT-5.4 mini
opencode run --agent gpthigh "Your prompt"    # GPT-5.4 high reasoning
opencode run --agent gptxhigh "Your prompt"   # GPT-5.4 xhigh reasoning
opencode run --agent gemini "Your prompt"     # Gemini 3.1 Pro
opencode run --agent flash "Your prompt"      # Gemini 3 Flash
```

### Continue last session

```bash
opencode run --continue "Now add error handling examples"
```

The session resumes with the same agent that started it. To switch agents, fork the session:

```bash
opencode run --continue --fork --agent 2-opus "Now add error handling examples"
```

### Attach files

```bash
opencode run --file src/main.py --file README.md "Review these files"
```

### JSON output for programmatic use

```bash
opencode run --format json "List all functions in this file"
```

### Named session

```bash
opencode run --title "Code Review Session" "Review this PR"
```

## Common flags reference

````shell
opencode run --help
````

## Output handling

- Default: formatted text to stdout
- `--format json`: raw JSON events for parsing
- Progress and diagnostics may appear on stderr
- Keep stderr visible for debugging; use `--format json` for clean machine-readable output
