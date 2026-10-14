# Document Analysis & Classification

This skill defines the methodology for analyzing documents, extracting metadata, classifying topics/tags, and generating summaries for ingestion into a Knowledge Base.

## When to Use This Skill

Use this skill when:
- Processing a new document from the inbox
- Reclassifying an existing document
- Generating or updating document summaries
- Determining topic and tag assignments

## Analysis Process Overview

```
┌─────────────────┐
│  Read Document  │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Detect Type &   │
│ Parse Content   │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Extract Signals │
│ (structure,     │
│  entities,      │
│  themes)        │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Check Existing  │
│ Taxonomy        │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Classify:       │
│ - Primary topic │
│ - All topics    │
│ - Tags          │
│ - Doc type      │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Generate        │
│ Summary         │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Propose         │
│ Filename        │
└─────────────────┘
```

## File Type Specific Analysis

### Markdown (.md)

**Parsing approach:**
1. Check for existing YAML frontmatter (preserve useful fields)
2. Extract document structure (headers, hierarchy)
3. Identify code blocks and their languages
4. Note links (internal references, external URLs)

**Signal extraction:**
- H1/H2 headers often indicate main topics
- Code block languages hint at technology topics
- Link domains suggest context (github = code, arxiv = research)
- Conversation patterns (Q&A format) indicate `conversation` doc type

**Special handling for AI conversation artifacts:**
- Look for patterns: "Human:", "Assistant:", "User:", "Codex:", etc.
- Extract the *subject* of the conversation, not just "this is a conversation"
- Identify conclusions, decisions, or outcomes reached
- Note any code produced or problems solved

### Plain Text (.txt)

**Parsing approach:**
1. Detect if it's structured (log file, data) or prose
2. Look for implicit structure (blank line paragraphs, indentation)
3. Check for timestamps, patterns suggesting specific formats

**Signal extraction:**
- First few lines often indicate purpose
- Repeated patterns suggest data/logs vs narrative
- Email-like headers indicate correspondence

### HTML (.html, .htm)

**Parsing approach:**
1. Extract `<title>`, `<meta>` tags for initial signals
2. Strip scripts, styles, navigation, footers
3. Convert semantic HTML to markdown-like structure
4. Preserve links with their text and URLs

**Signal extraction:**
- `<title>` is often a good document title
- `<meta name="description">` provides summary hints
- `<article>`, `<main>` tags isolate primary content
- Header hierarchy (h1-h6) indicates structure
- `<time>` tags may indicate publication date

**Conversion rules:**
- Headers → Markdown headers
- Lists → Markdown lists
- Tables → Markdown tables (if simple) or note "complex table present"
- Images → Note presence, extract alt text
- Links → Preserve as markdown links

### CSV (.csv)

**Parsing approach:**
1. Read header row for column names
2. Sample 5-10 data rows for type inference
3. Count total rows
4. Detect delimiter if non-standard

**Signal extraction (schema-based classification):**

| Column Patterns | Likely Domain |
|-----------------|---------------|
| `user_id`, `email`, `created_at` | User/account data |
| `amount`, `price`, `total`, `revenue` | Financial/sales data |
| `timestamp`, `event`, `action` | Event logs |
| `lat`, `lng`, `latitude`, `longitude` | Geographic data |
| `name`, `description`, `category` | Product/catalog data |
| `date`, `metric`, `value` | Time series/analytics |

**Output format:**
- Create markdown wrapper with frontmatter
- Include schema description in summary
- Note row count, column types
- Keep original CSV alongside wrapper

**Example wrapper:**
```markdown
---
id: abc-123
title: "Q4 2024 Sales Transactions"
source_type: csv
schema:
  columns: [transaction_id, customer_id, amount, date, product_sku]
  row_count: 15847
  domain: "E-commerce sales transaction records"
# ... rest of frontmatter
---

# Q4 2024 Sales Transactions

## Schema

| Column | Type | Description |
|--------|------|-------------|
| transaction_id | string | Unique transaction identifier |
| customer_id | string | Customer reference |
| amount | decimal | Transaction amount in USD |
| date | date | Transaction date |
| product_sku | string | Product identifier |

## Overview

This dataset contains 15,847 sales transactions from Q4 2024...

## Data File

Original data: [sales-q4-2024.csv](./sales-q4-2024.csv)
```

## Topic Classification Strategy

### Step 1: Check Existing Taxonomy

Before creating new topics, read `meta/taxonomy.md` to understand:
- What topics already exist
- Their descriptions and scope
- Common tags associated with each

### Step 2: Extract Candidate Topics

From the document, identify:
1. **Explicit subjects**: What is this document *about*?
2. **Domain**: What field/area does it belong to?
3. **Project/context**: Is it related to a specific project?

### Step 3: Match or Create

- If content fits existing topic: use it
- If content spans multiple topics: pick primary, list all
- If no topic fits: propose new topic with description

### Topic Naming Guidelines

- Use kebab-case: `machine-learning`, `project-alpha`
- Be specific enough to be useful: `python` not `programming`
- Be general enough to group related docs: `web-development` not `react-hooks`
- Avoid overly generic topics: not just `notes` or `misc`

## Tag Assignment Strategy

Tags are more specific than topics. Use tags for:

1. **Technologies**: `pytorch`, `react`, `postgresql`
2. **Concepts**: `optimization`, `authentication`, `caching`
3. **Time periods**: `q4-2024`, `2024`
4. **Status/type markers**: `draft`, `archived`, `decision`
5. **People/orgs**: `acme-corp`, `team-alpha` (if relevant)

**Tag guidelines:**
- Lowercase, kebab-case
- Prefer existing tags over creating new ones
- 3-7 tags is typical; don't over-tag
- Tags should aid retrieval — ask "would someone search for this?"

## Document Type Classification

| Type | Indicators |
|------|------------|
| `conversation` | Q&A format, multiple speakers, chat-like |
| `article` | Long-form prose, thesis/body/conclusion structure |
| `notes` | Informal, bullet points, fragments, meeting context |
| `data` | CSV, structured records, schemas |
| `presentation` | Slides, visual-heavy, bullet-point heavy |
| `reference` | Documentation, specifications, manuals |
| `report` | Analysis, findings, recommendations |

## Summary Generation Guidelines

Summaries should be **detailed and substantive**:

### For prose documents (articles, notes, conversations):
- What is the main subject/question addressed?
- What conclusions or decisions were reached?
- What key points or arguments were made?
- What actions or next steps were identified?
- 3-5 sentences minimum; more for longer documents

### For data files:
- What domain does this data represent?
- What is the scope (time period, entity count)?
- What could this data be used for?
- Any notable characteristics (sparse, complete, etc.)?

### For conversations:
- What was the user trying to accomplish?
- What solution or approach was discussed?
- What was the outcome?
- Any code or artifacts produced?

**Avoid vague summaries** like "This document discusses various topics." Be specific about *what* topics and *what* was said about them.

## Entity Extraction

Extract notable entities for the `key_entities` field:

- **People**: Names mentioned (authors, subjects)
- **Organizations**: Companies, teams, institutions
- **Technologies**: Specific tools, frameworks, languages
- **Projects**: Named projects or initiatives
- **Concepts**: Key technical or domain concepts

Only include entities that are *significant* to the document, not every noun.

## Filename Generation

Generate descriptive, URL-safe filenames:

1. Based on title or main subject
2. Lowercase kebab-case
3. No dates (those go in frontmatter)
4. 3-6 words typical
5. End with appropriate extension

**Examples:**
- "Conversation about React performance" → `react-performance-optimization.md`
- "Q3 Sales Report" → `q3-sales-analysis-report.md`
- "random_notes_final_v2.txt" → `project-alpha-planning-notes.md`

## Quality Checklist

Before finalizing classification, verify:

- [ ] Title is descriptive and accurate
- [ ] Summary captures substance, not just structure
- [ ] Primary topic is the best fit
- [ ] All relevant topics are listed
- [ ] Tags aid discoverability
- [ ] Document type matches format/purpose
- [ ] Filename is descriptive
- [ ] Key entities are truly significant
