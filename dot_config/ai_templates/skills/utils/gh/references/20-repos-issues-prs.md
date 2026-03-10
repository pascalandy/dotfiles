# Repositories, Issues, and Pull Requests

Use this reference for everyday repository work: repo setup, issue workflows, PR creation and review, merges, and labels.

## Repositories

### Create, clone, and view

```bash
gh repo create my-repo --public
gh repo create org/my-repo --private --description "My awesome project"
gh repo clone owner/repo
gh repo view owner/repo
gh repo view owner/repo --json name,description,defaultBranchRef
```

### List, edit, and delete

```bash
gh repo list owner --limit 50
gh repo edit owner/repo --description "New description"
gh repo edit owner/repo --default-branch main
gh repo rename new-name
gh repo delete owner/repo --yes
```

### Fork, sync, and set a default repo

```bash
gh repo fork owner/repo --clone
gh repo sync
gh repo sync --branch main
gh repo set-default owner/repo
gh repo set-default --unset
```

### Handy repo extras

```bash
gh repo autolink list
gh repo autolink add --key-prefix JIRA- --url-template https://jira.example.com/browse/<num>
gh repo deploy-key list
gh repo deploy-key add ~/.ssh/id_ed25519.pub --title "CI key" --read-only
gh repo gitignore python
gh repo license mit
```

## Issues

### Create, list, and view

```bash
gh issue create --title "Bug: login not working" --body "Steps to reproduce..."
gh issue create --repo owner/repo --title "Issue title"
gh issue list
gh issue list --state all --limit 50
gh issue list --assignee @me
gh issue list --labels bug,high-priority
gh issue view 123 --comments
gh issue view 123 --json title,body,state,labels
```

### Edit, comment, and close

```bash
gh issue edit 123 --title "New title"
gh issue edit 123 --add-label bug,high-priority
gh issue comment 123 --body "Looking into this now"
gh issue close 123 --comment "Fixed in PR #456"
gh issue reopen 123
```

### Other issue actions

```bash
gh issue status
gh issue pin 123
gh issue unpin 123
gh issue lock 123 --reason off-topic
gh issue unlock 123
gh issue transfer 123 --repo owner/new-repo
gh issue delete 123 --yes
gh issue develop 123 --branch fix/issue-123 --base main
```

## Pull requests

### Create, list, and view

```bash
gh pr create --title "Feature: add new functionality" --body "This PR adds..."
gh pr create --draft --base main --head feature-branch
gh pr create --reviewer user1,user2 --labels enhancement

gh pr list
gh pr list --state all --author @me
gh pr list --base main --limit 50
gh pr list --json number,title,state,author,headRefName

gh pr view 123
gh pr view 123 --comments
gh pr view 123 --json title,body,state,files
```

### Checkout, diff, and checks

```bash
gh pr checkout 123
gh pr diff 123
gh pr diff 123 --name-only
gh pr checks 123
gh pr checks 123 --watch --interval 5
```

### Edit, comment, and review

```bash
gh pr edit 123 --title "New title"
gh pr edit 123 --add-reviewer user1,user2
gh pr edit 123 --ready
gh pr comment 123 --body "Looks good overall"
gh pr review 123 --approve --body "LGTM"
gh pr review 123 --request-changes --body "Please fix these issues"
gh pr review 123 --comment --body "A few thoughts"
```

### Merge, close, reopen, and sync branches

```bash
gh pr merge 123 --merge
gh pr merge 123 --squash --delete-branch
gh pr merge 123 --rebase
gh pr close 123 --comment "Closing for now"
gh pr reopen 123
gh pr update-branch 123
gh pr update-branch 123 --merge
```

### Other PR actions

```bash
gh pr ready 123
gh pr lock 123 --reason off-topic
gh pr unlock 123
gh pr revert 123
gh pr status
gh pr status --repo owner/repo
```

## Labels

```bash
gh label list
gh label create bug --color d73a4a --description "Something isn't working"
gh label edit bug --name bug-report --color ff0000
gh label delete bug
gh label clone owner/repo
gh label clone owner/repo --repo target/repo
```

## Common workflows

### Create a PR from an issue

```bash
gh issue develop 123 --branch feature/issue-123
# make changes, commit, push
gh pr create --title "Fix #123" --body "Closes #123"
```

### Bulk issue or PR edits

```bash
gh issue list --search "label:stale" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --comment "Closing as stale"

gh pr list --search "review:required" --json number --jq '.[].number' | \
  xargs -I {} gh pr edit {} --add-label needs-review
```

## Guidance

- Set a default repo with `gh repo set-default` before a long repo-specific session.
- Prefer `--json` for reporting, dashboards, or follow-up scripts.
- Before you merge, confirm the strategy: merge, squash, or rebase.
- Before bulk edits to labels, assignees, or reviewers, verify the target repo.
