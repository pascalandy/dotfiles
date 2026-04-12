# byterover details

This file is for occasional lookup. Keep it out of the critical path unless the task actually needs setup, debugging, or knowledge-base maintenance details.

## Important Non-Obvious Facts

- `brv query` is local retrieval from `.brv/context-tree/`
- `brv curate` is the command that uses the configured provider for AI-assisted curation
- Before suggesting unfamiliar `brv` subcommands or flags, run `brv <command> --help`

## Provider Setup

`brv curate` requires a configured provider. `brv query` does not.

Default provider:

```bash
brv providers connect byterover
```

Other providers:

```bash
brv providers list
brv providers connect openai --api-key sk-xxx --model gpt-4.1
```

Useful verification commands:

```bash
brv model
brv providers list --format json
brv query "nonsense query that will not match"
```

The last command is a quick behavioral check that `brv query` is retrieval rather than provider-backed generation.

Provider config is stored at:

```text
~/Library/Application Support/brv/providers.json
```

## Curate History

```bash
brv curate view
brv curate view cur-1739700001000
brv curate view detail
brv curate view --since 1h --status completed
brv curate view --help
```

## Review Commands

```bash
brv review pending
brv review approve <taskId>
brv review reject <taskId>
brv review approve <taskId> --file <path> --file <path>
brv review reject <taskId> --file <path>
brv review pending --format json
```

File paths are relative to the context tree.

## Project Locations

Use this when you need to find a registered project's context tree path:

```bash
brv locations -f json
```

JSON fields include:
- `projectPath`
- `contextTreePath`
- `isCurrent`
- `isActive`
- `isInitialized`

## Version Control

`brv vc` provides git-style version control for the knowledge base.

Common commands:

```bash
brv vc init
brv vc status
brv vc add .
brv vc commit -m "add authentication patterns"
brv vc log
brv vc branch
brv vc checkout -b feature/auth
brv vc merge feature/auth
brv vc remote
brv vc fetch
brv vc pull
brv vc push
```

Remote sync requires `brv login` and a configured remote.

## Data Handling

- Knowledge is stored as Markdown under `.brv/context-tree/`
- `brv curate -f` only accepts files from the current project
- Maximum 5 files per curate command
- No data is sent to ByteRover servers unless you explicitly run `brv vc push`

## Error Handling

Show this troubleshooting guidance when these errors occur:

"Not authenticated" | Run `brv login --help` for more details.
"No provider connected" | Run `brv providers connect byterover`.
"Connection failed" / "Instance crashed" | User should kill the `brv` process.
"Token has expired" / "Token is invalid" | Run `brv login` again.
"Billing error" / "Rate limit exceeded" | User should check credits or wait before retrying.

Handle these directly and retry after fixing:

"Missing required argument(s)." | Run `brv <command> --help`.
"Maximum 5 files allowed" | Reduce to 5 or fewer `-f` flags.
"File does not exist" | Verify the path and use a project-relative file.
"File type not supported" | Use supported text, image, PDF, or office files only.

## Quick Diagnosis

```bash
brv status
```
