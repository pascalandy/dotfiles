# changelog

> Create a witty, engaging changelog from recent PR merges to the main branch for an internal development team.

## When to Use

- After merges to main and a team update is needed.
- On a daily schedule (last 24 hours of changes).
- On a weekly schedule (last 7 days of changes).
- After major releases or deployments.
- User requests a changelog, release summary, or change digest.

## Inputs

- Access to the repository's git history and PR list via the `gh` CLI.
- Optional argument: `daily`, `weekly`, or a custom number of days.
- Default: last 24 hours of merges to the main branch.

## Methodology

### Step 1: Determine Time Period

- **Daily**: Look at PRs merged in the last 24 hours.
- **Weekly**: Look at PRs merged in the last 7 days.
- **Custom**: User-specified time window.
- Always specify the time period in the output title (e.g., "Daily" vs "Weekly").
- Default: last day's changes from the main branch.

### Step 2: PR Analysis

Gather data from the repository. Use the `gh` CLI to look up PRs and their descriptions. For each PR, collect:

1. New features that have been added.
2. Bug fixes that have been implemented.
3. Any other significant changes or improvements.
4. References to specific issues and their details.
5. Names of contributors who made the changes.
6. PR labels to identify feature type (feature, bug, chore, etc.).
7. Breaking changes — highlight them prominently.
8. PR numbers for traceability.
9. Links between PRs and issues (include issue context when present).

### Step 3: Prioritize Content

Order content in the changelog by these priorities:

1. **Breaking changes** (if any) — MUST appear at the top.
2. User-facing features.
3. Critical bug fixes.
4. Performance improvements.
5. Developer experience improvements.
6. Documentation updates.

### Step 4: Draft Changelog

Apply these formatting guidelines:

1. Keep it concise and to the point.
2. Highlight the most important changes first.
3. Group similar changes together (all new features, all bug fixes).
4. Include issue references where applicable.
5. Mention the names of contributors, giving them credit for their work.
6. Add a touch of humor or playfulness to make it engaging.
7. Use emojis sparingly to add visual interest.
8. Keep total message under 2000 characters for Discord.
9. Use consistent emoji for each section.
10. Format code/technical terms in backticks.
11. Include PR numbers in parentheses (e.g., "Fixed login bug (#123)").

Include deployment notes when relevant:
- Database migrations required.
- Environment variable updates needed.
- Manual intervention steps post-deploy.
- Dependencies that need updating.

### Step 5: Format Output

Produce output using this exact structure:

```
# 🚀 [Daily/Weekly] Change Log: [Current Date]

## 🚨 Breaking Changes (if any)

[List any breaking changes that require immediate attention]

## 🌟 New Features

[List new features here with PR numbers]

## 🐛 Bug Fixes

[List bug fixes here with PR numbers]

## 🛠️ Other Improvements

[List other significant changes or improvements]

## 🙌 Shoutouts

[Mention contributors and their contributions]

## 🎉 Fun Fact of the Day

[Include a brief, work-related fun fact or joke]
```

### Step 6: Style Review

Review the changelog against the team's write style guide (e.g., `EVERY_WRITE_STYLE.md` if present in the repo). Run style checks in parallel using subagents to go through each guideline point-by-point.

### Step 7: Handle Edge Cases

- **No changes in the time period**: Output a "quiet day" message: "🌤️ Quiet day! No new changes merged."
- **Unable to fetch PR details**: List the PR numbers for manual review.
- **Message exceeds 2000 characters**: Trim lower-priority sections (Developer DX, Documentation) first; never trim Breaking Changes or critical bug fixes.

### Step 8: Audience Adjustment (Optional)

Adjust tone and detail level based on the target channel:

| Channel | Focus |
|---------|-------|
| **Dev team** | Include technical details, performance metrics, code snippets |
| **Product team** | Focus on user-facing changes and business impact |
| **Leadership** | Highlight progress on key initiatives and blockers |

### Step 9: Discord Posting (Optional)

Post the changelog to Discord by posting to a webhook URL:

```bash
# Set your Discord webhook URL
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"

# Post using curl
curl -H "Content-Type: application/json" \
  -d "{\"content\": \"{{CHANGELOG}}\"}" \
  $DISCORD_WEBHOOK_URL
```

To get a webhook URL: Discord server → Server Settings → Integrations → Webhooks → New Webhook.

Always validate message length before posting (max 2000 chars).

## Quality Gates

- [ ] Time period is correctly determined and stated in the title.
- [ ] Breaking changes appear at the top (if any).
- [ ] Content is ordered by priority (features → bugs → improvements).
- [ ] All contributors are named and credited.
- [ ] PR numbers included for every entry.
- [ ] Total length ≤ 2000 characters for Discord.
- [ ] Style guide review completed.
- [ ] Deployment notes included when relevant.
- [ ] No changes message used when the time period is empty.

## Outputs

- A formatted changelog inside `<change_log>` tags, containing only the content (no thought process, no raw data).
- Recommended schedule: daily at 6 AM NY time for previous day; weekly on Mondays for the previous week.

## Feeds Into

- Internal team communication (Discord, Slack, email digest).
- PR descriptions or release notes.
- `ce:compound` — capture patterns in what changed.
