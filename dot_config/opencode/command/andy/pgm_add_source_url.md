---
description: add_source into pg-memory sources table
---

## ORCHESTRATION PLAN

Follow these steps exactly. Do not skip any step.

### Step 1: Get URL from user

Ask: "What URL do you want to ingest?"

### Step 2: Load skills

Load these skills:

- `dufuddle` - for scraping
- `pg-memory` - for database insertion

### Step 3: Scrape with dufuddle

Run dufuddle with `--json` to get structured data:

```bash
bun run .opencode/skill/dufuddle/scripts/dufuddle.ts --json "<URL>"
```

Capture the JSON output which contains:

- `title` - article title
- `content` - full markdown content
- `author` - author name (may be null)
- `published` - publication date (may be null)
- `site` - site name
- `domain` - domain name
- `wordCount` - word count

### Step 4: Ask all metadata questions together

Present options as numbered choices. **Sort by highest probability first.** Show your recommended answer in parentheses.

```
Please provide the following information:

1. SOURCE NAME: What name should I use for this source?
   1) [Extracted site name] (from site name) (recommended)
   2) Enter custom name

   Your choice [1-2]: (1)
   If 2, provide custom name:

2. SOURCE TYPE: What type of source is this?
   1) blog_post - Blog articles (recommended)
   2) documentation - Official project docs
   3) article - General web articles
   4) podcast - Podcast episode transcripts
   5) video - YouTube/video transcripts
   6) coding - Code examples, repos, snippets

   Your choice [1-6]: (1)

3. TAGS: What tags should I add? (lowercase, hyphens for multi-word)

   Suggested based on content: [will be shown after scraping]

   1) Accept suggested tags (recommended)
   2) Add more tags
   3) Replace with different tags

   Your choice [1-3]: (1)
   If 2 or 3, provide tags:

4. IMPORTANCE: How important is this source?

   | Score | Label | Criteria |
   |-------|-------|----------|
   | 7 | Perfect | Nothing to change, flawless |
   | 6 | Excellent | Life-changing, would enthusiastically recommend |
   | 5 | Good | Would recommend with minor caveats |
   | 4 | Fine | No strong feelings, wouldn't discourage |
   | 3 | Meh | Wouldn't recommend, but not upset I tried |
   | 2 | Disappointing | Regret it, would warn others |
   | 1 | Avoid | Harmful, offensive, or a complete waste |
   | 0 | Unrated | Not yet evaluated |

   Your choice [0-7]: (5)

---
Please answer in this format:
1. [number 1-2] [optional: custom name if 2]
2. [number 1-6]
3. [number 1-3] [optional: your tags if 2 or 3]
4. [number 0-7]
```

### Step 5: Parse user responses

Extract the answers from the user's batch response:

- Source name from answer 1 (use extracted site name if option 1, or custom name if option 2)
- Source type from answer 2 (map number to type name)
- Tags from answer 3 (suggest tags based on content if they chose option 1)
- Importance from answer 4

### Step 6: Validate and format data

Before building the INSERT:

1. **Format `published_at`**: Convert dufuddle's `published` to PostgreSQL TIMESTAMPTZ format:
   - If ISO format (e.g., `2025-01-15T10:30:00Z`): use as-is
   - If date only (e.g., `2025-01-15`): append `T00:00:00Z`
   - If null/empty: use `NULL`

2. **Validate tags**: Ensure all tags are:
   - Lowercase
   - Use hyphens for multi-word (e.g., `web-development`, not `web development`)
   - No special characters except hyphens

3. **Build metadata JSONB**: Include bonus info from dufuddle:
   ```json
   {
     "wordCount": 1500,
     "site": "vercel.com",
     "domain": "vercel.com"
   }
   ```

### Step 7: Show INSERT preview

Show the user the exact INSERT statement you will run.

**CRITICAL:** The `content` field must contain the ACTUAL markdown content, not a file path or reference.

```sql
INSERT INTO sources (
  user_id, name, title, source_type, source_url, content,
  author, published_at, importance, provider_id, model_id, tags, metadata
)
VALUES (
  'pascalandy',
  'Vercel',
  'AI SDK 6: Agents, Tool Execution...',
  'blog_post',
  'https://vercel.com/blog/ai-sdk-6',
  $content$
# AI SDK 6

Full markdown content here (NOT a file path)...
$content$,
  'Vercel Team',
  '2025-01-15T00:00:00Z',
  5,
  'manual',
  'none',
  '["ai", "sdk", "vercel"]',
  '{"wordCount": 1500, "site": "vercel.com", "domain": "vercel.com"}'
)
RETURNING id, name, title, importance, LENGTH(content) as content_length;
```

**Note:** Use `$content$...$content$` dollar quoting for the content field to handle special characters and quotes safely.

### Step 8: Get approval

Ask: "Does this look correct? Type 'go' to insert."

### Step 9: Execute INSERT

Run the INSERT statement via psql:

```bash
psql forzr -c "<INSERT_STATEMENT>"
```

### Step 10: Verify insertion

Run verification query:

```sql
SELECT id, name, title, source_type, importance, LENGTH(content) as content_length, ingested_at
FROM sources
WHERE user_id = 'pascalandy'
ORDER BY ingested_at DESC
LIMIT 1;
```

Confirm `content_length` is substantial (thousands of characters, not 20-30).

### Step 11: Display raw content

Retrieve and display the full markdown content that was stored:

```sql
SELECT content
FROM sources
WHERE user_id = 'pascalandy'
ORDER BY ingested_at DESC
LIMIT 1;
```

Display the raw markdown output to the user so they can verify the content was stored correctly.

### Step 12: Report success

Show user a summary:

```
Source added successfully!

- ID: 019400a0-1234-7abc-8def-0123456789ab
- Name: Vercel
- Title: AI SDK 6: Agents, Tool Execution...
- Type: blog_post
- Importance: 5/7
- Content length: 15,234 characters
- Word count: 1,500
- Ingested at: 2025-01-15 14:30:00-05
```

---

## FIELD REFERENCE

| Field          | Required | Source           | Description                                                           |
| -------------- | -------- | ---------------- | --------------------------------------------------------------------- |
| `user_id`      | YES      | Hardcoded        | Always `'pascalandy'`                                                 |
| `name`         | YES      | User (from site) | Source name (e.g., "Vercel", "Syntax")                                |
| `title`        | NO       | dufuddle         | Article/page title                                                    |
| `source_type`  | YES      | User (inferred)  | `documentation`, `podcast`, `blog_post`, `video`, `article`, `coding` |
| `source_url`   | NO       | User input       | Original URL                                                          |
| `content`      | YES      | dufuddle         | Full markdown content                                                 |
| `author`       | NO       | dufuddle         | Author name                                                           |
| `published_at` | NO       | dufuddle         | Publication date (TIMESTAMPTZ)                                        |
| `importance`   | NO       | User             | 0-7 scale (default: 0)                                                |
| `provider_id`  | YES      | Hardcoded        | Always `'manual'` for this command                                    |
| `model_id`     | YES      | Hardcoded        | Always `'none'` for this command                                      |
| `tags`         | NO       | User (inferred)  | JSON array of lowercase tags                                          |
| `metadata`     | NO       | dufuddle         | JSON object with wordCount, site, domain                              |

---

## CRITICAL RULES

1. **NEVER store file paths in content** - The `content` field must contain the actual text, not `$(cat file)` or `/tmp/something.md`
2. **ALWAYS verify content_length** - If less than 100 characters, something went wrong
3. **ALWAYS use --json flag** with dufuddle to get structured data
4. **ALWAYS show preview** before inserting
5. **ALWAYS get user approval** before INSERT
6. **ALWAYS use numbered choices** - Present options as `1) ... 2) ... 3) ...` for quick selection
7. **ALWAYS show recommended answer** - Put `(recommended)` next to best option and `(X)` at the end
8. **ALWAYS sort by probability** - Most likely option first
9. **ALWAYS use lowercase tags** - With hyphens for multi-word tags
10. **ALWAYS use dollar quoting** - Use `$content$...$content$` for the content field
11. **ALWAYS format dates** - Convert to PostgreSQL TIMESTAMPTZ format
12. **ALWAYS show raw content** - Display the stored markdown after insertion
