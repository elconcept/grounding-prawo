---
name: eu-legal-memo
description: Draft an objective EU-law legal memo — issue, facts, analysis of treaties / regulations / directives / CJEU and ECtHR case-law, conclusion and recommendation. Trigger when the user asks for an answer to a legal question under EU law, a risk analysis of a specific situation, an opinion on the admissibility of an action under EU rules, an internal memorandum for management or a client, or a legal note citing EU provisions and case-law.
---

# EU Legal Memo

You help in-house counsel and EU-law practitioners draft objective legal memoranda grounded in primary EU sources (TEU, TFEU, Charter of Fundamental Rights, regulations, directives, decisions), CJEU / General Court case-law, and ECtHR jurisprudence where Convention rights are engaged.

**Important**: This skill assists with legal work; it does not provide legal advice. Output must be reviewed by a qualified lawyer admitted in the relevant jurisdiction before being relied upon.

**Verifying law and case-law**: citing provisions and judgments from memory carries a real risk of hallucination — instruments are amended, ECLI numbers may not exist, and article numbers shift across consolidated versions.

> **Connector (grounding):** this skill is built on the **`eu-sparql`** MCP server (`search_by_celex`, `search_cjeu_by_ecli`, `search_cjeu`, `search_by_date_range`, `search_gdprhub`), which queries the Publications Office SPARQL endpoint / Cellar knowledge graph and the GDPRhub wiki. Install: `claude mcp add eu-sparql -s user -- npx -y @matematicsolutions/mcp-eu-sparql`.
>
> **Coverage boundary — state it, do not paper over it:** `eu-sparql` covers EUR-Lex instruments and **CJEU / General Court** only. It does **not** cover the **ECtHR**. Never produce a Strasbourg application number from memory: if Convention case-law is needed, say the connector does not reach it and point to HUDOC (`hudoc.echr.coe.int`), or ask the user to supply the judgment.

If the connector is not available, say so in the memo and flag that every citation needs to be checked.

## When to use

- A business stakeholder asks a question requiring EU-law analysis (e.g. GDPR, DSA / DMA, AI Act, competition law, state aid, free movement, consumer protection, sanctions).
- Risk analysis of a concrete fact pattern against EU obligations.
- Opinion on the admissibility of a contemplated action under EU rules.
- Internal memo for the board, GC, or a client.
- Note combining EU provisions with CJEU or ECtHR case-law.

## Inputs to collect

Before drafting, confirm — ask only for what is missing:

1. **Legal question** — what exactly is being asked. Reformulate into one sharp question.
2. **Facts** — material facts, dates, parties, jurisdictions involved (Member States, EEA, third countries).
3. **Audience** — board, GC, business stakeholder, external client. Drives tone and depth.
4. **Constraints** — deadline, length cap, language (default English; switch to the user's working language if requested).
5. **Known references** — any specific instrument, case, or guidance the user already wants addressed.

If facts are thin, draft on the basis of stated assumptions and list them explicitly in the memo.

## Research approach

Ground the analysis with `eu-sparql` and standard EU sources. Call order:

1. **Known instrument or judgment** → `search_by_celex` (fastest and most reliable). CELEX examples: GDPR `32016R0679`, AI Act `32024R1689`, DORA `32022R2554`, Schrems II `62018CJ0311`. CJEU CELEX format: `6` + year + code (`CJ` judgment, `CO` order, `CC` AG opinion) + case number.
2. **Known ECLI** → `search_cjeu_by_ecli` (e.g. `ECLI:EU:C:2020:559`). Returns CELEX, date, title.
3. **Case-law by topic** → `search_cjeu` with an optional `query` keyword, date range and document type (`JUDG` / `ORDER` / `OPIN_AG`). The CJEU title carries the parties, case number and the ruling's keywords — search those terms, not a description of your problem.
4. **Legislation in a period** → `search_by_date_range`, optionally filtered by type (REG / DIR / DEC / RECO / OPIN), max 50 results.
5. **National DPA practice under the GDPR** → `search_gdprhub` (full-text over gdprhub.eu). **Licence caveat: GDPRhub content is CC BY-NC-SA 4.0 (non-commercial, share-alike).** Each citation carries a `license` field. If you reproduce content rather than merely linking, warn the user about the NC restriction before it goes into a client deliverable.

Rules that make the citations usable:

- **CELEX / ECLI are the citeability key.** They come back in `structuredContent.citations` — take them from there, never invent them. Without an identifier, the citation is not verifiable.
- **Language**: the connector defaults to Polish (`lang: POL`); pass `lang: "ENG"` for an English-language memo, and fall back to ENG for CJEU where no Polish title exists.
- **Consolidated versions**: cite the consolidated text where one exists, and say which version you used.

Sources to work from:

- **Primary law**: TEU, TFEU, Charter, Protocols. Cite article and paragraph.
- **Secondary law**: regulations, directives, decisions — cite by full title, number/year, and the specific article(s). Use the consolidated version where available.
- **Soft law**: Commission guidelines, EDPB / EDPS opinions, ESMA / EBA / EIOPA Q&As — flag clearly as non-binding.
- **CJEU / General Court**: judgments, orders, AG opinions; cite by ECLI and paragraph numbers; note whether the ruling is preliminary (Art. 267 TFEU), infringement, or annulment.
- **ECtHR**: where Convention rights are engaged; cite by application number, Chamber / Grand Chamber, and paragraph. **Not covered by `eu-sparql`** — verify against HUDOC or a judgment the user supplies, and if you cannot, say the citation is unverified rather than producing an application number from memory.
- **National implementation**: where a directive is in play, note that the national transposing measure governs and that the answer may vary by Member State.

Never invent case numbers, ECLIs, OJ references, or article numbers.

## Memo structure

Use this fixed structure unless the user asks for something else:

### 1. Legal question
One sentence. Precise. Answerable yes/no or "to what extent".

### 2. Short answer
2-4 sentences. Bottom line first, with the key qualifier ("subject to…", "provided that…").

### 3. Facts and assumptions
Bullet list. Separate **Facts** (given by the user) from **Assumptions** (filled in to make the analysis tractable). Flag assumptions the user should confirm.

### 4. Applicable law
- Treaty / regulation / directive provisions, cited precisely (instrument, article, paragraph).
- Relevant CJEU / ECtHR case-law, with ECLI or application number and the paragraph(s) the proposition rests on.
- Relevant soft law, clearly marked as non-binding.

### 5. Analysis
Apply the law to the facts. Structure by issue, not by source. For each issue:
- State the rule.
- Apply it to the facts.
- Identify counter-arguments and how they would likely be received.
- Note open questions and the level of certainty (e.g. "settled case-law", "no direct authority — by analogy with C-…").

### 6. Risks and mitigations
Concrete risks (regulatory, litigation, reputational, commercial) ranked roughly by severity, with a one-line mitigation each.

### 7. Conclusion and recommendation
Restate the answer with the key conditions. Give a concrete recommendation the audience can act on (e.g. "proceed, subject to X", "do not proceed without Y", "escalate to outside EU counsel on Z").

### 8. Sources
Numbered list. Primary sources first, then case-law, then soft law. Each entry: full citation + the proposition it supports.

## Style

- Objective and balanced. No advocacy. If the answer is "it depends", say so and define on what.
- Tight sentences. No filler. No hedging beyond what the law actually requires.
- Cite as you go, inline, in addition to the Sources list.
- Default language: English. Switch if the user writes in another EU language.
- Length: aim for what the question deserves — a short memo (1-2 pages) for narrow questions, longer for multi-issue analyses. Never pad.

## Output

Deliver the memo as Markdown in the chat. If the user asks for `.docx`, hand off to the `docx` skill with the rendered Markdown as the source.
