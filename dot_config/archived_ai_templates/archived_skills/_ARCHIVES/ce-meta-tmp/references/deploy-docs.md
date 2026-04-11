# deploy-docs

> Validate and prepare the compound-engineering plugin documentation site for GitHub Pages deployment.

## When to Use

- Before deploying documentation to GitHub Pages.
- After adding or modifying HTML pages, agents, or skills.
- When verifying that all JSON config files are valid and all expected pages exist.
- When setting up GitHub Pages for the first time.

## Inputs

- Access to the repository containing `plugins/compound-engineering/docs/`.
- `jq` available in the environment (for JSON validation).
- Git repository with a working tree.

## Methodology

### Step 1: Validate Documentation

Run the following checks in the terminal:

```bash
# Count components
echo "Agents: $(ls plugins/compound-engineering/agents/*.md | wc -l)"
echo "Skills: $(ls -d plugins/compound-engineering/skills/*/ 2>/dev/null | wc -l)"

# Validate JSON
cat .claude-plugin/marketplace.json | jq . > /dev/null && echo "✓ marketplace.json valid"
cat plugins/compound-engineering/.claude-plugin/plugin.json | jq . > /dev/null && echo "✓ plugin.json valid"

# Check all HTML files exist
for page in index agents commands skills mcp-servers changelog getting-started; do
  if [ -f "plugins/compound-engineering/docs/pages/${page}.html" ] || [ -f "plugins/compound-engineering/docs/${page}.html" ]; then
    echo "✓ ${page}.html exists"
  else
    echo "✗ ${page}.html MISSING"
  fi
done
```

### Step 2: Check for Uncommitted Changes

```bash
git status --porcelain plugins/compound-engineering/docs/
```

If there are uncommitted changes, warn the user to commit first before deploying.

### Step 3: Deployment Instructions

Provide the following instructions based on the user's situation:

#### First-time Setup

1. Create `.github/workflows/deploy-docs.yml` with the GitHub Pages workflow (see Workflow File Content below).
2. Go to repository Settings > Pages.
3. Set Source to "GitHub Actions".

#### Deploying

After merging to `main`, the docs will auto-deploy. Or trigger manually:

1. Go to the Actions tab.
2. Select "Deploy Documentation to GitHub Pages".
3. Click "Run workflow".

#### Workflow File Content

```yaml
name: Deploy Documentation to GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - 'plugins/compound-engineering/docs/**'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: 'plugins/compound-engineering/docs'
      - uses: actions/deploy-pages@v4
```

### Step 4: Report Status

Produce a deployment readiness summary:

```
## Deployment Readiness

✓ All HTML pages present
✓ JSON files valid
✓ Component counts match

### Next Steps
- [ ] Commit any pending changes
- [ ] Push to main branch
- [ ] Verify GitHub Pages workflow exists
- [ ] Check deployment at https://everyinc.github.io/compound-engineering-plugin/
```

## Quality Gates

- [ ] Agent and skill counts are non-zero and match expectations.
- [ ] `marketplace.json` parses as valid JSON.
- [ ] `plugin.json` parses as valid JSON.
- [ ] All expected HTML pages exist: `index`, `agents`, `commands`, `skills`, `mcp-servers`, `changelog`, `getting-started`.
- [ ] No uncommitted changes in the docs directory (or user has acknowledged and committed).
- [ ] GitHub Pages workflow file exists at `.github/workflows/deploy-docs.yml`.
- [ ] Repository Pages source is set to "GitHub Actions".

## Outputs

- Validation report showing which checks passed and which failed.
- Deployment readiness summary with actionable next steps.
- GitHub Actions workflow file content (to create if missing).

## Feeds Into

- Live documentation site at the GitHub Pages URL.
- `changelog` — document what shipped in each deployment.
