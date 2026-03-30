# Setup Deploy

> Configure deployment settings for land-and-deploy by detecting your platform, production URL, health check endpoints, and deploy commands, then persisting everything to CLAUDE.md.

## When to Use

- User asks "setup deploy", "configure deployment", "set up land-and-deploy"
- About to use land-and-deploy for the first time on a project
- Deploy configuration in CLAUDE.md is missing or stale
- Deploy platform has changed

## Inputs

- The project repository (for platform detection)
- CLAUDE.md (read/write — this is where config is persisted)
- Access to platform CLIs (`fly`, `vercel`, `render`) if installed
- The production URL if not auto-detectable

## Methodology

### Step 1: Check existing configuration

Search CLAUDE.md for an existing `## Deploy Configuration` section.

If found: show it to the user and ask:
- A) Reconfigure from scratch (overwrite existing)
- B) Edit specific fields
- C) Done — looks correct

If C, stop.

### Step 2: Detect platform

Run detection across all known platform config files:

```bash
# Platform config files
[ -f fly.toml ]       && echo "PLATFORM:fly"
[ -f render.yaml ]    && echo "PLATFORM:render"
[ -f vercel.json ] || [ -d .vercel ] && echo "PLATFORM:vercel"
[ -f netlify.toml ]   && echo "PLATFORM:netlify"
[ -f Procfile ]       && echo "PLATFORM:heroku"
[ -f railway.json ] || [ -f railway.toml ] && echo "PLATFORM:railway"

# GitHub Actions deploy workflows
find .github/workflows -name '*.yml' -o -name '*.yaml' | xargs grep -liE "deploy|release|production|cd" 2>/dev/null

# Project type
grep -q '"bin"' package.json 2>/dev/null && echo "PROJECT_TYPE:cli"
ls *.gemspec 2>/dev/null && echo "PROJECT_TYPE:library"
```

### Step 3: Platform-specific setup

#### Fly.io (fly.toml detected)

1. Extract app name from `fly.toml`
2. Check if `fly` CLI is installed; if so, run `fly status --app {app}`
3. Infer URL: `https://{app}.fly.dev`
4. Deploy status command: `fly status --app {app}`
5. Health check: `https://{app}.fly.dev` (or `/health` if app has it)
6. Confirm production URL with user — Fly apps often use custom domains

#### Render (render.yaml detected)

1. Extract service name and type from render.yaml
2. Infer URL: `https://{service-name}.onrender.com`
3. Render auto-deploys on push to connected branch — no deploy command needed
4. Health check: poll the inferred URL for the new version after merge

#### Vercel (vercel.json or .vercel detected)

1. Check for `vercel` CLI; if installed, run `vercel ls --prod`
2. Auto-deploys on push: preview on PR, production on merge to main
3. Health check: production URL from Vercel project settings

#### Netlify (netlify.toml detected)

1. Extract site info from netlify.toml
2. Auto-deploys on push
3. Health check: production URL

#### GitHub Actions only (no platform config file)

1. Read the detected workflow file to understand what it deploys
2. Extract deploy target if mentioned
3. Ask user for production URL

#### Nothing detected — ask the user

Gather information via questions:
1. How are deploys triggered? (auto on push / GitHub Actions / deploy script / manual / library)
2. What is the production URL?
3. How can the agent check if a deploy succeeded? (HTTP health check URL / CLI command / GitHub Actions status / just check the URL loads)
4. Any pre-merge or post-merge hooks? (build commands, migration scripts)

### Step 4: Confirm before writing

Always show the detected configuration and ask the user to confirm before writing.

### Step 5: Write to CLAUDE.md

Find and replace `## Deploy Configuration` section if it exists, or append to the end:

```markdown
## Deploy Configuration (configured by /setup-deploy)
- Platform: {platform}
- Production URL: {url}
- Deploy workflow: {workflow file or "auto-deploy on push"}
- Deploy status command: {command or "HTTP health check"}
- Merge method: {squash/merge/rebase}
- Project type: {web app / API / CLI / library}
- Post-deploy health check: {health check URL or command}

### Custom deploy hooks
- Pre-merge: {command or "none"}
- Deploy trigger: {command or "automatic on push to main"}
- Deploy status: {command or "poll production URL"}
- Health check: {URL or command}
```

This is idempotent — running setup-deploy again overwrites cleanly.

### Step 6: Verify

After writing:
1. If health check URL configured, probe it: `curl -sf "{url}" -o /dev/null -w "%{http_code}"`
2. If deploy status command configured, run it and check output

Report results. A temporarily unreachable health check doesn't block — configuration is still valid.

## Quality Gates

- [ ] Platform correctly identified (or user-confirmed for manual)
- [ ] Production URL confirmed with user
- [ ] Health check mechanism established (URL or command)
- [ ] Configuration written to CLAUDE.md under `## Deploy Configuration`
- [ ] No secrets (API keys, tokens) written to CLAUDE.md
- [ ] Health check verification ran (even if temporarily unreachable)

## Outputs

- `CLAUDE.md` updated with `## Deploy Configuration` section containing platform, URL, health check, deploy commands, merge method, and custom hooks

```
DEPLOY CONFIGURATION — COMPLETE
Platform:      fly.io
URL:           https://myapp.fly.dev
Health check:  https://myapp.fly.dev/health
Status cmd:    fly status --app myapp
Merge method:  squash

Saved to CLAUDE.md. /land-and-deploy will use these settings automatically.
```

## Feeds Into

- >land-and-deploy (reads CLAUDE.md config written by this skill)
- >ship (uses deploy configuration for post-merge verification)

## Important Rules

- **Never expose secrets.** Don't print full API keys, tokens, or passwords. Don't write them to CLAUDE.md.
- **Confirm with the user.** Always show the detected configuration and ask for confirmation before writing.
- **CLAUDE.md is the source of truth.** All configuration lives there — not in a separate config file.
- **Idempotent.** Running setup-deploy multiple times overwrites the previous config cleanly.
- **Platform CLIs are optional.** If `fly` or `vercel` CLI isn't installed, fall back to URL-based health checks.

## Harness Notes

No browser required. Reads/writes CLAUDE.md. Platform CLIs (`fly`, `vercel`, etc.) are optional — falls back to URL-based health checks if not installed. Never expose secrets in CLAUDE.md or terminal output.
