# FFmpeg Meta-Skill Acceptance Checklist

Use this as the final audit trail for `.agents/skills/meta/ffmpeg`.

## Job Breakdown

- [x] Inventory the five source skills in `.agents/skills/ffmpeg-5x-skills`
- [x] Confirm the export is a single meta-skill rooted at `.agents/skills/meta/ffmpeg`
- [x] Map source `01_claude-code-video-toolkit.md` into the `Create` sub-skill
- [x] Map source `02_ffmpeg-cli.md` into the `Quick` sub-skill
- [x] Map source `03_ffmpeg-analyse-video.md` into the `Analyse` sub-skill
- [x] Map source `04_ffmpeg-patterns.md` into the `Edit` sub-skill references
- [x] Map source `05_ffmpeg-video-editor.md` into the `Edit` sub-skill router, scripts, and cookbook

## Acceptance Criteria

- [x] Root `SKILL.md` exists and includes the router bridge to `references/ROUTER.md`
- [x] `references/ROUTER.md` routes cleanly across `Create`, `Quick`, `Analyse`, and `Edit`
- [x] `Create` preserves the toolkit-root rule, progress-reporting rule, and long-running polling rule
- [x] `Create` exposes setup, project init, asset generation, chain video, sync/render, and progress workflows
- [x] `Quick` exposes all eight one-shot wrapper scripts: cut, merge, extract-audio, thumb, gif, convert, speed, watermark
- [x] `Quick` scripts are present, executable, and `shellcheck` clean
- [x] `Analyse` preserves the four-stage pipeline: probe, extract, delegate, synthesise
- [x] `Analyse` keeps the frame-reader prompt template as a standalone reference file
- [x] `Edit` exposes the command cookbook plus helper scripts for probing, concat, and loudnorm
- [x] `Edit` reference files cover transcode, trim/concat, video filters, audio filters, speed/reverse, transitions, color grading, chroma key, compositing, hardware acceleration, batch processing, probing, and preset profiles

## Corrections Made During Audit

- [x] Fixed the broken relative path to `cost-estimates.md` in `references/Create/workflows/01-setup.md`
- [x] Fixed the broken relative path to `subagent-prompt-template.md` in `references/Analyse/workflows/03-delegate-batches.md`
- [x] Corrected the Analyse workflow so it no longer suggests using `ffprobe` on extracted JPEGs for exact timestamps
- [x] Tightened `references/Quick/scripts/extract-audio.sh` so its help and validation match its actual MP3-only behavior
- [x] Hardened `references/Quick/scripts/speed.sh` so it works on silent inputs instead of failing on missing audio
- [x] Updated `references/Quick/MetaSkill.md` so the speed script behavior matches the implementation

## Verification Performed

- [x] Read every source skill and every exported sub-skill entrypoint
- [x] Read every Create and Analyse workflow file for routing and reference integrity
- [x] Read every Quick and Edit helper script for behavior and UX consistency
- [x] Ran `shellcheck` across all exported shell scripts with no findings
- [x] Confirmed the helper scripts are executable on disk
- [x] Smoke-tested `extract-audio.sh` and `speed.sh` on generated media, including a silent-video edge case

## Client-Facing Standard

- [x] No placeholder text or TODO markers remain in the exported meta-skill
- [x] The exported structure is coherent enough to hand to a client without broken internal references in the audited paths
- [x] The known defects found during audit were fixed in-place rather than left as follow-up notes
