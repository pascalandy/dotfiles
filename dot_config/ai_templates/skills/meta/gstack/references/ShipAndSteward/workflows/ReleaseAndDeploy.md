# Release And Deploy

Use this workflow when the request is about preparing a branch for release, deploying it, or monitoring the rollout after it lands.

| Request Pattern | Load This Skill | Why |
|---|---|---|
| ship, open PR, push, prepare release, create branch and PR | `../../ship/SKILL.md` | Run the release-preparation workflow |
| merge and deploy, land approved PR, verify production | `../../land-and-deploy/SKILL.md` | Handle the post-approval deployment path |
| watch rollout, canary check, post-deploy monitoring | `../../canary/SKILL.md` | Monitor production health after release |
| configure deploy workflow before first use | `../../setup-deploy/SKILL.md` | Prepare deployment metadata and commands |

Expected artifact: a release decision, deployment result, or rollout verification.
