# Feature Video

> Record browser interactions demonstrating a feature, stitch screenshots into an MP4, upload natively to GitHub, and embed in the PR description as an inline video player.

## When to Use

- A PR needs a visual demo for reviewers
- User asks to demo a feature, create a PR video, record a walkthrough, or show what changed visually
- Adding a video to a pull request description

## Inputs

- PR number, "current" (current branch's PR), or path to an existing `.mp4` file (upload-only resume mode)
- Optional: base URL (defaults to `http://localhost:3000`)

## Prerequisites

- Local development server running (e.g., `bin/dev`, `npm run dev`, `rails server`)
- `agent-browser` CLI installed (load the `agent-browser` skill for details)
- `ffmpeg` installed (for video conversion)
- `gh` CLI authenticated with push access to the repo
- Git repository on a feature branch (PR optional — skill can create a draft or record-only)
- One-time GitHub browser auth (see Step 6 auth check)

## Methodology

### Step 1: Parse Arguments & Resolve PR

Parse input:
- First argument: PR number, "current", or path to existing `.mp4` (upload-only resume mode)
- Second argument: base URL (defaults to `http://localhost:3000`)

**Upload-only resume mode:** If first argument ends in `.mp4` and the file exists, skip Steps 2–5 and go directly to Step 6 using that file. Resolve PR from current branch.

If explicit PR number provided, verify it exists:
```bash
gh pr view [number] --json number -q '.number'
```

If no explicit PR number (or "current"), check for a PR on the current branch:
```bash
gh pr view --json number -q '.number'
```

If no PR exists, ask the user to choose (use interactive question tool):
```
No PR found for the current branch.

1. Create a draft PR now and continue (recommended)
2. Record video only -- save locally and upload later when a PR exists
3. Cancel
```

- Option 1: Create draft PR: `gh pr create --draft --title "[branch-name-humanized]" --body "Draft PR for video walkthrough"`, then continue with new PR number
- Option 2: Set `RECORD_ONLY=true`. Run Steps 2–5 (record + encode), skip Steps 6–7, report local video path and RUN_ID at end

### Step 1b: Verify Required Tools

Check before proceeding — fail early with clear message:

```bash
command -v ffmpeg
command -v agent-browser
command -v gh
```

If any tool missing, stop and report:
- `ffmpeg`: `brew install ffmpeg` (macOS) or equivalent
- `agent-browser`: load the `agent-browser` skill for installation instructions
- `gh`: `brew install gh` (macOS) or https://cli.github.com

Do not proceed to Step 2 until all tools available.

### Step 2: Gather Feature Context

**If PR available**, get PR details and changed files:
```bash
gh pr view [number] --json title,body,files,headRefName -q '.'
gh pr view [number] --json files -q '.files[].path'
```

**If record-only mode**, detect default branch and derive context:
```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name') && git diff --name-only "$DEFAULT_BRANCH"...HEAD && git log --oneline "$DEFAULT_BRANCH"...HEAD
```

Map changed files to routes/pages to demonstrate. Examine the project's routing configuration (e.g., `routes.rb`, `next.config.js`, `app/` directory structure) to determine which URLs correspond to changed files.

### Step 3: Plan the Video Flow

Create a shot list before recording:

1. **Opening shot**: Homepage or starting point (2–3 seconds)
2. **Navigation**: How user gets to the feature
3. **Feature demonstration**: Core functionality (main focus)
4. **Edge cases**: Error states, validation, etc. (if applicable)
5. **Success state**: Completed action/result

Present proposed flow to user for confirmation before recording (use interactive question tool if available):

```
Proposed Video Flow for PR #[number]: [title]

1. Start at: /[starting-route]
2. Navigate to: /[feature-route]
3. Demonstrate:
   - [Action 1]
   - [Action 2]
   - [Action 3]
4. Show result: [success state]

Estimated duration: ~[X] seconds

1. Start recording
2. Modify the flow (describe changes)
3. Add specific interactions to demonstrate
```

### Step 4: Record the Walkthrough

Generate a unique run ID using current timestamp:
```bash
date +%s
```

Substitute the concrete timestamp value into ALL subsequent paths — do not use a variable that may not persist across terminal commands.

Create output directories with the concrete RUN_ID value:
```bash
mkdir -p .context/compound-engineering/feature-video/[RUN_ID]/screenshots
mkdir -p .context/compound-engineering/feature-video/[RUN_ID]/videos
```

Execute the planned flow, numbering screenshots sequentially for correct frame ordering:

```bash
agent-browser open "[base-url]/[start-route]"
agent-browser wait 2000
agent-browser screenshot .context/compound-engineering/feature-video/[RUN_ID]/screenshots/01-start.png
```

```bash
agent-browser snapshot -i
agent-browser click @e1
agent-browser wait 1000
agent-browser screenshot .context/compound-engineering/feature-video/[RUN_ID]/screenshots/02-navigate.png
```

```bash
agent-browser snapshot -i
agent-browser click @e2
agent-browser wait 1000
agent-browser screenshot .context/compound-engineering/feature-video/[RUN_ID]/screenshots/03-feature.png
```

```bash
agent-browser wait 2000
agent-browser screenshot .context/compound-engineering/feature-video/[RUN_ID]/screenshots/04-result.png
```

### Step 5: Create Video

Stitch screenshots into MP4 using the same RUN_ID:

```bash
ffmpeg -y -framerate 0.5 -pattern_type glob -i ".context/compound-engineering/feature-video/[RUN_ID]/screenshots/*.png" \
  -c:v libx264 -pix_fmt yuv420p -vf "scale=1280:-2" \
  ".context/compound-engineering/feature-video/[RUN_ID]/videos/feature-demo.mp4"
```

Notes:
- `-framerate 0.5` = 2 seconds per frame (adjust for faster/slower playback)
- `-2` in scale ensures height is divisible by 2 (required for H.264)

### Step 6: Authenticate & Upload to GitHub

Upload produces a `user-attachments/assets/` URL that GitHub renders as a native inline video player.

#### Check for Existing Session

```bash
agent-browser close
agent-browser --engine chrome --session-name github open https://github.com/settings/profile
agent-browser get title
```

If page title contains user's GitHub username or "Profile": session valid → skip to "Upload the video".
If redirects to login page: session expired → proceed to "Auth setup".

#### Auth Setup (One-Time)

```bash
agent-browser close
agent-browser --engine chrome --headed --session-name github open https://github.com/login
```

Prompt the user to log in manually (handles 2FA, SSO, OAuth):
```
GitHub login required for video upload.

A Chrome window has opened to github.com/login. Please log in manually
(this handles 2FA/SSO/OAuth automatically). Reply when done.
```

After login, verify:
```bash
agent-browser open https://github.com/settings/profile
```

The `github` session is now saved and reusable.

#### Upload the Video

Navigate to PR page and scroll to comment form:
```bash
agent-browser open "https://github.com/[owner]/[repo]/pull/[number]"
agent-browser scroll down 5000
```

Save any existing textarea content (may contain unsent draft):
```bash
agent-browser eval "document.getElementById('new_comment_field').value"
```
Store as `SAVED_TEXTAREA`.

Upload via hidden file input. Use caller-provided path (upload-only resume mode) or current run's video:
```bash
agent-browser upload '#fc-new_comment_field' [VIDEO_FILE_PATH]
```

Where `[VIDEO_FILE_PATH]` is:
- The `.mp4` path passed as first argument (upload-only resume)
- `.context/compound-engineering/feature-video/[RUN_ID]/videos/feature-demo.mp4` (normal flow)

Wait for GitHub to process (typically 3–5 seconds), then read textarea:
```bash
agent-browser wait 5000
agent-browser eval "document.getElementById('new_comment_field').value"
```

**Validate extracted URL.** Value MUST contain `user-attachments/assets/` to confirm successful upload.

If validation fails:
1. Check `agent-browser get url` — if `github.com/login`, session expired → re-run auth setup
2. If still on PR page: wait additional 5 seconds and re-read textarea
3. If still fails after retry: report failure and local video path for manual upload

Restore original textarea content (or clear if empty). Produce a JS string literal from SAVED_TEXTAREA — escape backslashes, double quotes, and newlines:
```bash
agent-browser eval "const ta = document.getElementById('new_comment_field'); ta.value = [SAVED_TEXTAREA_AS_JS_STRING]; ta.dispatchEvent(new Event('input', { bubbles: true }))"
```

### Step 7: Update PR Description

Get current PR body:
```bash
gh pr view [number] --json body -q '.body'
```

Append a Demo section (or replace existing one). Video URL renders as inline player when on its own line:

```markdown
## Demo

https://github.com/user-attachments/assets/[uuid]

*Automated video walkthrough*
```

Update the PR:
```bash
gh pr edit [number] --body "[updated body with demo section]"
```

### Step 8: Cleanup

Ask user before removing temporary files.

**If video successfully uploaded**, remove entire run directory:
```bash
rm -r .context/compound-engineering/feature-video/[RUN_ID]
```

**If record-only mode or upload failed**, remove only screenshots, preserve video for later upload:
```bash
rm -r .context/compound-engineering/feature-video/[RUN_ID]/screenshots
```

Present completion summary:
```
Feature Video Complete

PR: #[number] - [title]
Video: [VIDEO_URL]

Shots captured:
1. [description]
2. [description]
3. [description]
4. [description]

PR description updated with demo section.
```

---

## Usage Examples

```bash
# Record video for current branch's PR
/feature-video

# Record video for specific PR
/feature-video 847

# Record with custom base URL
/feature-video 847 http://localhost:5000

# Record for staging environment
/feature-video current https://staging.example.com
```

## Tips

- Keep it short: 10–30 seconds is ideal for PR demos
- Focus on the change: don't include unrelated UI
- Show before/after: if fixing a bug, show broken state first (if possible)
- The `--session-name github` session expires when GitHub invalidates cookies (typically weeks). If upload fails with a login redirect, re-run auth setup
- GitHub DOM selectors (`#fc-new_comment_field`, `#new_comment_field`) may change if GitHub updates its UI. If upload silently fails, inspect the PR page for updated selectors

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ffmpeg: command not found` | ffmpeg not installed | `brew install ffmpeg` (macOS) or equivalent |
| `agent-browser: command not found` | agent-browser not installed | Load the `agent-browser` skill |
| Textarea empty after upload wait | Session expired or GitHub processing slow | Check session validity (Step 6). If valid, increase wait time and retry |
| Textarea empty, URL is `github.com/login` | Session expired | Re-run auth setup (Step 6) |
| `gh pr view` fails | No PR for current branch | Step 1 handles this — create draft PR or record-only mode |
| Video file too large | Exceeds GitHub 10MB (free) or 100MB (paid) limit | Re-encode: lower framerate (`-framerate 0.33`), reduce resolution (`scale=960:-2`), or increase CRF (`-crf 28`) |
| Upload URL lacks `user-attachments/assets/` | Wrong upload method or GitHub change | Verify file input selector by inspecting PR page |

## Quality Gates

- All required tools verified before proceeding (Step 1b)
- Screenshot files numbered sequentially before stitching
- Upload URL validated to contain `user-attachments/assets/` before updating PR
- Original textarea content restored after upload

## Outputs

- MP4 video in `.context/compound-engineering/feature-video/[RUN_ID]/videos/`
- PR description updated with `## Demo` section containing inline video URL
- Completion summary with PR number, video URL, and shot list

## Feeds Into

- PR review process (reviewers can watch the demo inline)

## Harness Notes

Interactive question prompts vary by harness:
- Claude Code: `AskUserQuestion`
- Codex: `request_user_input`
- Gemini: `ask_user`
- Fallback: present numbered options and wait for user's next message

Shell variables do not persist across separate command blocks. Always substitute the concrete RUN_ID value (e.g., `1711234567`) into all paths — do not rely on variable expansion across blocks.
