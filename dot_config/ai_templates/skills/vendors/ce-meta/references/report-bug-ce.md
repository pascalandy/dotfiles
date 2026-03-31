# Report Bug (compound-engineering)

> Gather structured bug information and file a GitHub issue against the compound-engineering plugin.

## When to Use

- A user encounters unexpected behavior from any compound-engineering agent, command, skill, or MCP server
- Installation problems with the plugin
- User explicitly requests to report a bug in compound-engineering

## Inputs

- Optional: brief description of the bug (passed as argument)
- Answers to structured interview questions (collected interactively)
- Auto-detected environment information

## Methodology

### Step 1: Gather Bug Information

Prompt the user with the following questions. Use a blocking question mechanism (prompt and wait for reply before continuing):

**Question 1: Bug Category**
- What type of issue are you experiencing?
- Options: Agent not working, Command not working, Skill not working, MCP server issue, Installation problem, Other

**Question 2: Specific Component**
- Which specific component is affected?
- Ask for the name of the agent, command, skill, or MCP server

**Question 3: What Happened (Actual Behavior)**
- Ask: "What happened when you used this component?"
- Collect a clear description of the actual behavior

**Question 4: What Should Have Happened (Expected Behavior)**
- Ask: "What did you expect to happen instead?"
- Collect a clear description of expected behavior

**Question 5: Steps to Reproduce**
- Ask: "What steps did you take before the bug occurred?"
- Collect reproduction steps

**Question 6: Error Messages**
- Ask: "Did you see any error messages? If so, please share them."
- Capture any error output

---

### Step 2: Collect Environment Information

Automatically gather environment details. Do not block on failures — note "unknown" and continue.

**OS info (all platforms):**
```bash
uname -a
```

**Plugin version:** Read the plugin manifest or installed plugin metadata. Common locations:
- Claude Code: `~/.claude/plugins/installed_plugins.json`
- Codex: `.codex/plugins/` or project config
- Other platforms: check the platform's plugin registry

**Agent CLI version:** Run the platform's version command:
- Claude Code: `claude --version`
- Codex: `codex --version`
- Other platforms: use the appropriate CLI version flag

If any of these fail, record "unknown" and continue.

---

### Step 3: Format the Bug Report

Compose the report using this exact template:

```markdown
## Bug Description

**Component:** [Type] - [Name]
**Summary:** [Brief description from argument or collected info]

## Environment

- **Plugin Version:** [from plugin manifest/registry]
- **Agent Platform:** [e.g., Claude Code, Codex, Copilot, Pi, Kilo]
- **Agent Version:** [from CLI version command]
- **OS:** [from uname]

## What Happened

[Actual behavior description]

## Expected Behavior

[Expected behavior description]

## Steps to Reproduce

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Error Messages

[Any error output]

## Additional Context

[Any other relevant information]

---
*Reported via `/report-bug-ce` skill*
```

---

### Step 4: Create GitHub Issue

Run in terminal to create the issue:

```bash
gh issue create \
  --repo EveryInc/compound-engineering-plugin \
  --title "[compound-engineering] Bug: [Brief description]" \
  --body "[Formatted bug report from Step 3]" \
  --label "bug,compound-engineering"
```

If labels do not exist, create without labels:
```bash
gh issue create \
  --repo EveryInc/compound-engineering-plugin \
  --title "[compound-engineering] Bug: [Brief description]" \
  --body "[Formatted bug report]"
```

---

### Step 5: Confirm Submission

After the issue is created:
1. Display the issue URL to the user
2. Thank them for reporting the bug
3. Let them know the maintainer (Kieran Klaassen) will be notified

---

### Error Handling

- If `gh` CLI is not installed or not authenticated: prompt the user to install/authenticate first, then retry
- If issue creation fails: display the formatted report so the user can manually create the issue
- If required information is missing: re-prompt for that specific field only

---

### Privacy Notice

This skill does NOT collect:
- Personal information
- API keys or credentials
- Private code from projects
- File paths beyond basic OS info

Only technical information about the bug is included in the report.

## Quality Gates

- All 6 interview questions answered (or explicitly skipped with a note)
- Environment info collected (or recorded as "unknown")
- Bug report formatted using the exact template
- GitHub issue created successfully or formatted report surfaced to user

## Outputs

```
Bug report submitted successfully!

Issue: https://github.com/EveryInc/compound-engineering-plugin/issues/[NUMBER]
Title: [compound-engineering] Bug: [description]

Thank you for helping improve the compound-engineering plugin!
The maintainer will review your report and respond as soon as possible.
```

## Feeds Into

- Maintainer triage and fix workflow
- `reproduce-bug` (if investigation is needed)
