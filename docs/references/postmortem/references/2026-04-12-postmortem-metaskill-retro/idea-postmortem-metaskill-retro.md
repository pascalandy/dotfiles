---
name: Postmortem - Building the Postmortem Meta-Skill
description: Reverse-engineered session from 2026-04-12 analyzing the creation of the postmortem meta-skill
tags:
  - area/ea
  - kind/project
  - status/stable
date_created: 2026-04-12
date_updated: 2026-04-12
sources: []
---

# Postmortem: Building the Postmortem Meta-Skill

Reverse-engineered session from 2026-04-12.

## What We Did

1. User asked to create a meta-skill for postmortem/lessons-learned, using the meta-skill-creator pattern and sourcing from 15 ranked skills in opensrc.
2. Agent loaded the meta-skill-creator skill, read the reference "thinking" meta-skill for pattern, and read 6 of the top source skills in full (ce-compound, postmortem-writing, ce-compound-refresh, compound-docs, gstack/retro, learnings-researcher).
3. Agent designed a 5-sub-skill structure (Capture, IncidentReview, Retro, Refresh, Research) and presented it for approval via ExitSpecMode.
4. User approved. Agent started creating files.
5. User interrupted: "no refresh, it's really about capturing feedbacks." Agent pivoted to 4 sub-skills (removed Refresh), created all 13 files at the export path.
6. User then triggered the thinking skill (appears accidental), interrupted it, and revealed their own postmortem process -- a simple conversation-reverse-engineering approach with 8 memory types and structured extraction.
7. User asked: "what are the advantages of the metaskill we just created? I want to make sure we're not overcomplicating things."

---

## Elements Worth Remembering

### 1. The user's actual postmortem process is simpler and better for personal use

**MEMORY TYPE:** observation

The user's process: reverse-engineer the conversation, classify memories into 8 types (observation, decision, learning, error, action, thought, project_status, command_summary), extract learnings/errors/discoveries/fixes/feedback. Conversation-centric knowledge extraction. It works. The 13-file meta-skill solves a heavier problem -- team-scale engineering knowledge bases with YAML schemas, git retros, formal incident reviews. For personal knowledge capture, the user's approach is better.

### 2. "It's really about capturing feedbacks" was a scope correction I should have caught earlier

**MEMORY TYPE:** learning

The input file was titled "postmortem & lessons learned skills" and the top-ranked skill was ce-compound (scoring 46/50) which is about capturing solved problems. The user's intent was always about capturing feedback/lessons, not maintaining a knowledge base. I included Refresh (a maintenance sub-skill) because the source skills had it, not because the user asked for it. The user's correction was sharp: the meta-skill should focus on capture, not lifecycle management. Lesson: distinguish between "what the source material can do" and "what the user actually wants."

### 3. The meta-skill-creator pattern produces high-quality structure

**MEMORY TYPE:** learning

The three-layer pattern (Collection SKILL.md -> ROUTER.md -> MetaSkill.md sub-skills) with strict naming (only root is SKILL.md, sub-skills are MetaSkill.md to avoid scanner collisions) is solid. The thinking meta-skill at `~/.local/share/chezmoi/dot_config/ai_templates/skills/meta/thinking/` was an excellent reference. The pattern forces clear separation of concerns and progressive disclosure. This pattern is reusable.

### 4. Over-research is a real risk -- 6 source skills was too many

**MEMORY TYPE:** error

Read 6 full source skills including the 1468-line gstack/retro SKILL.md. Excessive. ce-compound, postmortem-writing, and learnings-researcher would have sufficed. retro and compound-docs added marginal value per token. ce-compound-refresh was cut entirely. Better: deep-read top 3, skim the rest for specific techniques.

### 5. ExitSpecMode worked well for plan approval

**MEMORY TYPE:** learning

Using ExitSpecMode to present the 5-sub-skill plan with optionNames (5 vs 4 vs 3 sub-skills) was effective. The user approved the 5-sub-skill option. The plan was saved to `docs/plans/2026-04-12-postmortem-meta-skill-structure.md`. This is a good pattern: present structure, get approval, then build.

### 6. User preference: metaskills should justify their complexity

**MEMORY TYPE:** observation

The user explicitly asked "what are the advantages" and "I want to make sure we're not overcomplicating things." This signals a preference for lean skills that earn their file count. A meta-skill with 13 files needs to deliver clear value over a simpler approach. If the simpler approach (user's own postmortem process) handles the use case, the meta-skill is overhead.

### 7. The postmortem meta-skill lives alongside the thinking meta-skill

**MEMORY TYPE:** project_status

Export path: `/Users/andy16/.local/share/chezmoi/dot_config/ai_templates/skills/meta/postmortem/`. This sits next to the existing `thinking/` meta-skill. Both follow the same pattern (SKILL.md -> ROUTER.md -> MetaSkill.md). The postmortem skill has 4 sub-skills: Capture, IncidentReview, Retro, Research.

---

## What Went Wrong

- Included Refresh sub-skill despite it not matching the user's intent ("capturing feedbacks"). User had to correct scope mid-build.
- Over-research: read 6 massive source skills when 3 would have sufficed. Burned tokens on the 1468-line retro skill.
- Built before fully understanding the user's actual workflow. The user already had a simpler, effective postmortem process that I didn't discover until the end.

## What We Discovered

- The user has a personal postmortem process: reverse-engineer conversation, classify memories (8 types), extract learnings/errors/fixes/feedback. This is the actual workflow, not the 13-file meta-skill.
- The source skills split into two distinct domains: conversation-centric knowledge capture (what the user does) vs codebase-centric engineering documentation (what the meta-skill does). These are complementary, not competing.
- The best source skills for postmortem are ce-compound (capture), postmortem-writing (formal incident review), and learnings-researcher (search). The retro skill is impressive but git-centric and heavy.

## Fixes Applied

- Removed Refresh sub-skill after user's correction ("no refresh, it's really about capturing feedbacks").
- Renamed the incident sub-skill to "IncidentReview" to avoid collision with the parent "postmortem" name.

## Feedback for the Agent

- Ask about the user's current process BEFORE designing a replacement. The user already had a working postmortem approach that I didn't discover until the very end.
- When a user says "it's really about X," treat that as a scope signal. Stop including things that aren't about X.
- Don't let source material drive scope. The source skills had Refresh, but the user wanted capture-focused. User intent > source availability.
- Be more aggressive about token budget. Reading 6 full source skills (one 1468 lines) was wasteful. Skim first, deep-read selectively.

## Feedback for the User

- Your postmortem process (reverse-engineer, classify, extract) is clean and effective. Don't replace it with the meta-skill for personal knowledge capture.
- The meta-skill earns its keep if you ever need: formal incident postmortems with templates, git-based engineering retros, or a searchable docs/solutions/ knowledge base. Those are team-scale concerns.
- Consider whether the meta-skill should be trimmed further -- Research could be a section inside Capture rather than its own sub-skill, reducing the file count from 13 to 10.
- The meta-skill at `/Users/andy16/.local/share/chezmoi/dot_config/ai_templates/skills/meta/postmortem/` is ready to use as-is. It won't interfere with your simpler personal process. They coexist.

## Related

- [[index]]
- [[log]]
