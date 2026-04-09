---
name: deploy-docs
description: Validate and prepare documentation for GitHub Pages deployment
disable-model-invocation: true
---

# Deploy Documentation Command

Validate the documentation site and prepare it for GitHub Pages deployment.

## Step 1: Validate Documentation

Run checks that match the current repository's docs layout.

```bash
# Replace placeholders with paths from this repo before running.

test -d "[docs-path]" && echo "✓ docs directory exists" || echo "✗ docs directory missing"
test -f "[manifest-path]" && jq . "[manifest-path]" > /dev/null && echo "✓ metadata valid" || echo "! metadata file optional or invalid"
test -f "[index-page]" && echo "✓ index page exists" || echo "✗ index page missing"
```

## Step 2: Check for Uncommitted Changes

```bash
git status --porcelain "[docs-path]"
```

If there are uncommitted changes, warn the user to commit first.

## Step 3: Deployment Instructions

Since GitHub Pages deployment requires a workflow file with special permissions, provide these instructions:

### First-time Setup

1. Create `.github/workflows/deploy-docs.yml` with the GitHub Pages workflow
2. Go to repository Settings > Pages
3. Set Source to "GitHub Actions"

### Deploying

After merging to `main`, the docs will auto-deploy. Or:

1. Go to Actions tab
2. Select "Deploy Documentation to GitHub Pages"
3. Click "Run workflow"

### Workflow File Content

```yaml
name: Deploy Documentation to GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - '[docs-path]/**'
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
          path: '[docs-path]'
      - uses: actions/deploy-pages@v4
```

## Step 4: Report Status

Provide a summary:

```
## Deployment Readiness

✓ Required docs assets present
✓ Metadata files valid
✓ Deployment workflow ready

### Next Steps
- [ ] Commit any pending changes
- [ ] Push to main branch
- [ ] Verify GitHub Pages workflow exists
- [ ] Check deployment at [site-url]
```
