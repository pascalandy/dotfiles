# Safety And Control

Use this workflow when the request is about reducing operational risk, constraining edits, or preparing sensitive sessions before release or debugging work.

| Request Pattern | Load This Skill | Why |
|---|---|---|
| be careful, warn before destructive commands, safety mode | `../../careful/SKILL.md` | Add warning guardrails |
| freeze this directory, restrict edits to one scope | `../../freeze/SKILL.md` | Hard-bound the edit surface |
| activate both safety systems together | `../../guard/SKILL.md` | Combine destructive-command warnings and edit boundaries |
| remove freeze, unlock the workspace | `../../unfreeze/SKILL.md` | Remove the active edit restriction |
| import browser cookies for authenticated testing | `../../setup-browser-cookies/SKILL.md` | Prepare browser session state safely |

Expected artifact: an active or removed safety control, or a prepared authenticated browser session.
