# Actions, Projects, and Releases

Use this reference for CI/CD workflows, workflow runs, caches, secrets, variables, project boards, and releases.

## Actions: runs

```bash
gh run list
gh run list --workflow ci.yml --branch main --limit 20
gh run list --json databaseId,status,conclusion,headBranch

gh run view 123456789
gh run view 123456789 --log
gh run view 123456789 --job 987654321
gh run view 123456789 --web

gh run watch 123456789
gh run watch 123456789 --interval 5

gh run rerun 123456789
gh run rerun 123456789 --job 987654321
gh run cancel 123456789
gh run delete 123456789

gh run download 123456789
gh run download 123456789 --name build --dir ./artifacts
```

## Actions: workflows

```bash
gh workflow list
gh workflow view ci.yml
gh workflow view ci.yml --yaml
gh workflow view ci.yml --web
gh workflow enable ci.yml
gh workflow disable ci.yml
gh workflow run ci.yml
gh workflow run ci.yml --ref develop
```

If the workflow takes inputs, confirm the current CLI syntax with local help:

```bash
gh workflow run --help
```

## Actions: cache, secrets, variables

```bash
gh cache list
gh cache list --branch main --limit 50
gh cache delete 123456789
gh cache delete --all

gh secret list
gh secret set MY_SECRET
echo "$MY_SECRET" | gh secret set MY_SECRET
gh secret set MY_SECRET --env production
gh secret set MY_SECRET --org orgname
gh secret delete MY_SECRET
gh secret delete MY_SECRET --env production

gh variable list
gh variable set MY_VAR "some-value"
gh variable set MY_VAR "value" --env production
gh variable set MY_VAR "value" --org orgname
gh variable get MY_VAR
gh variable delete MY_VAR
gh variable delete MY_VAR --env production
```

## Projects

```bash
gh project list
gh project list --owner owner
gh project view 123
gh project view 123 --format json
gh project create --title "My Project"
gh project create --title "Project" --owner orgname
gh project edit 123 --title "New Title"
gh project close 123
gh project delete 123

gh project field-list 123
gh project field-create 123 --title "Status" --data-type SINGLE_SELECT
gh project field-delete 123 --id FIELD_ID

gh project item-list 123
gh project item-add 123 --owner owner --url https://github.com/owner/repo/issues/456
gh project item-edit --id ITEM_ID --project-id PROJECT_ID --field-id FIELD_ID --single-select-option-id OPTION_ID
gh project item-delete --id ITEM_ID --project-id PROJECT_ID
```

Project syntax evolves faster than many other `gh` areas. Prefer local `--help` before using advanced field/item mutations.

## Releases

```bash
gh release list
gh release view
gh release view v1.0.0
gh release view v1.0.0 --web

gh release create v1.0.0 --notes "Release notes here"
gh release create v1.0.0 --notes-file notes.md --title "Version 1.0.0"
gh release create v1.0.0 --target main --draft
gh release create v1.0.0 --prerelease

gh release upload v1.0.0 ./file.tar.gz
gh release upload v1.0.0 ./file1.tar.gz ./file2.tar.gz

gh release download v1.0.0
gh release download v1.0.0 --pattern "*.tar.gz" --dir ./downloads
gh release download v1.0.0 --archive zip

gh release edit v1.0.0 --notes "Updated notes"
gh release delete-asset v1.0.0 file.tar.gz
gh release delete v1.0.0 --yes
gh release verify v1.0.0
```

## Common workflows

### Run workflow and watch it

```bash
gh workflow run ci.yml --ref main
RUN_ID=$(gh run list --workflow ci.yml --branch main --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$RUN_ID"
```

### Trigger run, then fetch artifacts

```bash
gh workflow run ci.yml --ref main
RUN_ID=$(gh run list --workflow ci.yml --branch main --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$RUN_ID"
gh run download "$RUN_ID" --dir ./artifacts
```

## Guidance

- Be extra careful with secrets, environment scopes, and org scopes.
- Prefer watching or viewing runs before rerunning them blindly.
- For project field/item mutations, confirm the exact flag names with local help.
- For releases, clarify whether the user wants draft, prerelease, or full release.
