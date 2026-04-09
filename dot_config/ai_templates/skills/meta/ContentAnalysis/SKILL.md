---
name: ContentAnalysis
description: Content-adaptive wisdom extraction from videos, podcasts, articles, and YouTube -- dynamic sections built from what the content actually contains, not static templates. USE WHEN extract wisdom, content analysis, analyze content, analyze video, analyze podcast, extract insights, key takeaways, what did I miss, extract from YouTube, insight report, summarize content, what's interesting.
keywords: [content-analysis, extract-wisdom, youtube, podcast, video, article, insights, takeaways, wisdom, extraction, dynamic-sections, content-extraction]
---

# ContentAnalysis

> Content-adaptive wisdom extraction -- dynamic sections built from what the content actually contains, not static templates.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

---

## The Problem

Traditional content extraction follows a fixed template: IDEAS, QUOTES, HABITS, FACTS, REFERENCES. Every piece of content gets the same headers regardless of what it actually contains. A programming interview gets a "HABITS" section. A geopolitical analysis gets "FACTS" that are really just opinions. The output feels mechanical and misses the real gems because the sections were decided before the content was even read.

- **Static sections miss domain-specific wisdom** -- a security talk has threat model insights, not generic "ideas"
- **Forced categories create padding** -- filling a HABITS section when the content has none
- **Uniform tone reads like a committee report** -- compressed info nuggets instead of genuine observations
- **No depth control** -- the same exhaustive output whether you want a quick hit or a deep dive

The fundamental issue: the extraction format should serve the content, not the other way around.

---

## The Solution

ContentAnalysis detects what wisdom domains actually exist in the content and builds custom sections around them. A programming interview gets "Programming Philosophy" and "Developer Workflow Tips." A business podcast gets "Contrarian Business Takes" and "Money Philosophy." A security talk gets "Threat Model Insights" and "Defense Strategies."

**Core capabilities:**

1. **Dynamic section detection** -- Reads the content first, identifies wisdom domains, then builds sections around what is actually there
2. **Five depth levels** -- From Instant (one killer section) to Comprehensive (10-15 sections with themes and connections)
3. **Conversational voice** -- Bullets that sound like someone telling a friend about it, not a book report
4. **Quality standards** -- Every bullet earns its place; no padding, no inventory lists, no committee language
5. **Closing sections** -- One-Sentence Takeaway, If You Only Have 2 Minutes, References and Rabbit Holes (depth-dependent)

The sections adapt because the content dictates them.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Skill router | `references/ROUTER.md` | Minimal routing table that dispatches requests to the right sub-skill |
| ExtractWisdom skill | `references/ExtractWisdom/MetaSkill.md` | Dynamic content extraction methodology, tone rules, depth levels, quality standards |
| Extract workflow | `references/ExtractWisdom/workflows/Extract.md` | Step-by-step extraction workflow |

**Summary:**
- **Sub-skills:** 1 (ExtractWisdom)
- **Workflows:** 1 (Extract)
- **Dependencies:** None (works standalone)

---

## What Makes This Different

This sounds similar to the original extract_wisdom which also pulls insights from content. The difference:

The original extract_wisdom uses static sections -- IDEAS, QUOTES, HABITS, FACTS, REFERENCES -- for every piece of content. ContentAnalysis reads the content first, figures out what wisdom domains are present, and builds sections around what it finds. A talk about AI agents gets "Self-Modifying Software" and "The Agent Spectrum" instead of generic IDEAS. The tone follows a conversational voice standard (Level 3) that produces bullets people actually want to read, not compressed information nuggets. Depth levels let you choose between a 30-second skim and a comprehensive deep dive.

- Dynamic sections adapted to each piece of content, not static templates
- Five depth levels from Instant to Comprehensive
- Conversational tone that reads like someone telling you about it
- Every bullet passes the "Would I tweet this?" test
- Section names read like magazine headlines, not category labels

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| "extract wisdom from [URL]" | Routes to ExtractWisdom -- Full-depth extraction with 5-12 dynamic sections |
| "analyze this video" | Routes to ExtractWisdom -- Content scan, section detection, extraction with closing sections |
| "extract wisdom (fast)" | Routes to ExtractWisdom -- Fast-depth: 3 sections, 3 bullets each, no closing sections |
| "extract wisdom at comprehensive level" | Routes to ExtractWisdom -- Maximum depth: 10-15 sections plus Themes and Connections |
| "key takeaways from this podcast" | Routes to ExtractWisdom -- Full extraction with emphasis on actionable insights |
| "what did I miss in this article" | Routes to ExtractWisdom -- Full extraction focused on non-obvious insights |

---

## Example Usage

### Full Extraction (Default)

```
User: "extract wisdom from [YouTube URL about AI agents]"

AI responds:
# EXTRACT WISDOM: Building AI Agents That Actually Work
> A deep dive into agent engineering with [speaker] -- from self-modifying
> software to the economics of building with AI

---

## The Death of 80% of Apps

- He wasn't trying to build self-modifying software. He just let the agent
  see its own source code and it started fixing itself.
- Most apps are just a UI on a database. Agents can generate those on the fly.
  The app store as we know it is already dead.
- ...

## Money Stops Mattering

- Past a certain point, money stops mattering. A cheeseburger is a cheeseburger
  no matter how rich you are.
- Every VC is offering hundreds of millions. He genuinely doesn't care.
- ...

[... more dynamic sections ...]

---

## One-Sentence Takeaway

The best agents aren't programmed -- they're given access to their own source
code and a reason to improve.

## If You Only Have 2 Minutes

- Self-modifying software happened by accident, not design
- 80% of current apps will be replaced by agent-generated UIs
- ...

## References & Rabbit Holes

- **Claude Code** -- The agent framework he built everything on
- **MCP protocol** -- The tool integration layer that makes agents practical
```

### Fast Extraction

```
User: "extract wisdom (fast) from this podcast episode"

AI responds:
# EXTRACT WISDOM: [Title]
> [One-line description]

## [Dynamic Section 1]
- [3 tight bullets]

## [Dynamic Section 2]
- [3 tight bullets]

## [Dynamic Section 3]
- [3 tight bullets]
```

---

## Configuration

No configuration required. The skill works out of the box with sensible defaults (Full depth level). All extraction uses built-in Level 3 conversational voice standards.

---

## Customization

### Recommended Customization

No customization needed -- the skill adapts dynamically to each piece of content.

### Optional Customization

| Customization | Where | Impact |
|--------------|-------|--------|
| Default depth level | Invoke with depth keyword | Changes from Full to another level per request |
| Section preferences | Modify ExtractWisdom SKILL.md | Always-include or always-exclude section types |

---

## Credits

- **Original concept:** Daniel Miessler -- developed as the next generation of [extract_wisdom](https://github.com/danielmiessler/fabric) within the [PAI](https://github.com/danielmiessler/Personal_AI_Infrastructure) system
- **Inspired by:** The limitations of static content extraction templates

---

## Related Work

- **Fabric extract_wisdom** -- The original static-section content extractor that inspired this dynamic approach

---

## Changelog

### 1.0.0
- Initial release
- Dynamic section detection based on content analysis
- Five depth levels: Instant, Fast, Basic, Full, Comprehensive
- Level 3 conversational voice standard
- Closing sections: One-Sentence Takeaway, If You Only Have 2 Minutes, References and Rabbit Holes
- Comprehensive-level Themes and Connections synthesis
