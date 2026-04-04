# Extract Workflow

Extract dynamic, content-adaptive wisdom from any content source.

## Input Sources

| Source | Method |
|--------|--------|
| YouTube URL | Use available tools to fetch the transcript (browser, transcript API, etc.) |
| Article URL | Use available tools to fetch the page content |
| File path | Read the file directly |
| Pasted text | Use directly |

## Execution Steps

### Step 1: Get the Content

Obtain the full text/transcript. For YouTube, use whatever transcript-fetching tool is available in your environment. For articles, fetch the page content. Save to a working file if large.

### Step 2: Deep Read

Read the entire content. Don't extract yet. Notice:
- What domains of wisdom are present?
- What made you stop and think?
- What's genuinely novel vs. commonly known?
- What would you highlight if you were telling a friend about this?
- What quotes land perfectly?

### Step 3: Determine Depth Level

Check the user's request for depth keywords. Default to **Full** if none specified.

| Keyword | Depth Level |
|---------|-------------|
| "instant", "one section" | Instant (1 section, 8 bullets) |
| "fast", "quick", "skim" | Fast (3 sections, 3 bullets each) |
| "basic", "overview" | Basic (3 sections, 5 bullets each) |
| (default / no keyword) | Full (5-12 sections, 3-15 bullets each) |
| "comprehensive", "deep", "everything" | Comprehensive (10-15 sections, 8-15 bullets each) |

### Step 4: Select Dynamic Sections

Based on the deep read, pick sections per depth level. Rules:
- Section names must be conversational, not academic
- Each must have at least 3 quality bullets to justify existing
- Always include "Quotes That Hit Different" if source has quotable moments
- Always include "First-Time Revelations" if genuinely new ideas exist
- Be SPECIFIC -- "Agentic Engineering Philosophy" not "Technology Insights"
- Name sections like a magazine editor -- headlines, not categories

### Step 5: Extract Per Section

For each section, extract bullets per depth level. Apply tone rules from the SKILL.md:
- 8-16 words per sentence, flexible for clarity
- Specific details, not vague summaries
- Speaker's words when they're good
- No hedging language
- Every bullet worth telling someone about

### Step 6: Add Closing Sections

Include closing sections based on depth level:

| Level | Closing Sections |
|-------|-----------------|
| **Instant** | None |
| **Fast** | None |
| **Basic** | One-Sentence Takeaway only |
| **Full** | One-Sentence Takeaway + If You Only Have 2 Minutes + References & Rabbit Holes |
| **Comprehensive** | All three above + Themes & Connections |

1. **One-Sentence Takeaway** (15-20 words) -- the single most important thing
2. **If You Only Have 2 Minutes** (5-7 essential points) -- the cream of the cream
3. **References & Rabbit Holes** -- people, projects, books, tools mentioned worth following up on
4. **Themes & Connections** (Comprehensive only) -- 3-5 throughlines connecting multiple sections

### Step 7: Quality Check

Run the quality checklist from the SKILL.md before delivering:
- Sections are specific to THIS content, not generic
- No bullet sounds like it was written by a committee
- Every bullet has a specific detail, quote, or insight
- Section names are conversational and headline-worthy
- Section count matches depth level
- Closing sections match depth level
- No bullet starts with "The speaker" or "It was noted that"
- No more than 3 bullets per section start with "He" or the speaker's name
- No bullet exceeds 25 words
- No inventory sections
- Reading the output makes you want to consume the original content

### Step 8: Output

Present the complete extraction in the format specified in the SKILL.md.
