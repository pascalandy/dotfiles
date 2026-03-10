# Search, API, and Admin Utilities

Use this reference for search, API calls, org-level queries, gists, codespaces, extensions, aliases, keys, rulesets, attestations, and general admin tasks.

## Search

```bash
gh search code "TODO"
gh search code "TODO" --repo owner/repo
gh search commits "fix bug"
gh search issues "label:bug state:open"
gh search prs "is:open is:pr review:required"
gh search repos "stars:>1000 language:python"
gh search repos "topic:api" --limit 50
gh search repos "language:rust" --sort stars --order desc
gh search repos "stars:>100" --json name,description,stargazersCount
gh search prs "is:open" --web
```

## API requests

Use `gh api` when first-class commands are missing or too limited.

```bash
gh api /user
gh api /repos/owner/repo --jq '.stargazers_count'
gh api /user/repos --paginate
gh api /user --include
gh api /user --silent

gh api --method POST /repos/owner/repo/issues \
  --field title="Issue title" \
  --field body="Issue body"

gh api graphql -f query='{
  viewer {
    login
    repositories(first: 5) {
      nodes { name }
    }
  }
}'
```

## Organizations

```bash
gh org list
gh org list --user username
gh org list --json login,name,description
```

If the user needs deeper org inspection not covered here, use `gh api` against the relevant REST or GraphQL endpoint.

## Gists

```bash
gh gist list
gh gist list --limit 20
gh gist view abc123
gh gist view abc123 --files
gh gist create script.py --desc "My script"
gh gist create script.py --public
echo "print(\"hello\")" | gh gist create
gh gist edit abc123
gh gist rename abc123 --filename old.py new.py
gh gist clone abc123
gh gist delete abc123
```

## Codespaces

```bash
gh codespace list
gh codespace create --repo owner/repo
gh codespace create --repo owner/repo --branch develop
gh codespace view
gh codespace ssh
gh codespace ssh --command "cd /workspaces && ls"
gh codespace code
gh codespace code --web
gh codespace stop
gh codespace delete
gh codespace logs
gh codespace ports
gh codespace rebuild
gh codespace edit --machine standardLinux
gh codespace jupyter
gh codespace cp file.txt :/workspaces/file.txt
gh codespace cp :/workspaces/file.txt ./file.txt
```

## Extensions and aliases

```bash
gh extension list
gh extension search github
gh extension install owner/extension-repo
gh extension install owner/extension-repo --branch develop
gh extension upgrade extension-name
gh extension remove extension-name
gh extension create my-extension
gh extension exec extension-name -- --help

gh alias list
gh alias set prview 'pr view --web'
gh alias set co 'pr checkout' --shell
gh alias delete prview
gh alias import ./aliases.sh
```

## Keys, rulesets, attestations

```bash
gh ssh-key list
gh ssh-key add ~/.ssh/id_ed25519.pub --title "My laptop"
gh ssh-key delete 12345

gh gpg-key list
gh gpg-key add ~/.gnupg/public.key
gh gpg-key delete 12345

gh ruleset list
gh ruleset view 123
gh ruleset check --repo owner/repo --branch main

gh attestation trusted-root
gh attestation download owner/repo --artifact-id 123456
gh attestation verify owner/repo
```

## Browse, status, completion

```bash
gh browse
gh browse 123
gh browse --repo owner/repo --settings
gh browse --actions
gh browse --no-browser

gh status
gh status --repo owner/repo --json

gh completion -s bash
gh completion -s zsh
gh completion -s fish
```

## Guidance

- Prefer `gh search ... --json` when results will be post-processed.
- Prefer `gh api graphql` for cross-resource or nested queries.
- For org-wide admin work, confirm whether the target is user, org, repo, or enterprise scope.
- Codespaces, rulesets, and attestations change over time; verify advanced syntax with local help.
