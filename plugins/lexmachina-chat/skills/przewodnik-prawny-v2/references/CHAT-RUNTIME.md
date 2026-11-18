# CHAT-RUNTIME — przewodnik-prawny-v2 2.11, adapter 0.6.1

## Responsibility and precedence

- `prawny-router-v3` is the **only** case classifier, with original 11 categories, PRIMARY/SECONDARY/FALLBACK; `prawo-polskie-v2` is the original domain façade with 16 DR mapping. The guide is a **fallback/session host**, not a router replacement. It may manage the conversation once activated by the router or explicit user intent.
- Original source: `../SKILL.upstream.md`; original substantive core from `# Przewodnik Prawny v2 — Gospodarz Sesji` is byte-identical. Historical `model-memory`, `Basic Memory`, `Repertorium`, `show_widget`, `view`, `present_files` are runtime requests, never proof of available tools.
- Source rendering is subordinate to the actual user's task and host capabilities; don't create empty interaction or multiple unnecessary questions. Known facts, case posture, participant roles and preferences carry across stages.

## Preserved guide state machine

`PROWADZENIE` — when genuinely needed, ask one missing question at a time, warn of hard procedural deadlines first. Do not restart known matters.
`Q&A` — answer the asked question with verifiable sources; if not accessible, distinguish partial analysis from unverified legal citations.
`MENU` — list only actually available functionality; planned LexMachina targets marked `PENDING`.
`SUROWA ANALIZA` — requested-only mode, independent of PRAWNIK/LAIK, source excerpts with provenance and no interpretation/strategy.
`KROK A` document; `B` decision; `C` new matter; `D` drafting; `E` legal term; `F` incoming-pleading audit; `G` deadlines first; `H` adapted explanation; `I` contextual next steps. Keep KROK-F/M reference logic.

## Availability and cross-skill handoff

Read `skills/shared/<file>` from the **same plugin version**. Each mention of `view <skill>/SKILL.md` means *actual* installed skill read: `INSTALLED_READ` when found here, `EXTERNAL_READ` if explicitly read from another plugin, `PENDING` for approved future migration, `NOT_AVAILABLE` when inaccessible. Use the exact existing native skill. Do not simulate a skill from a name or from an old manifest. `przewodnik` is now `IN_BUNDLE`; contract in `CHAT-HANDOFF.md`.

## Source and evidence protection

For statute and rulings distinguish original authored text, indexed metadata, partial snippet and full legal text on the legally relevant date. A statutorily cited term must use the actual appropriate procedural regime. `VERIFIED` only after source read, otherwise `NOT_CHECKED`. Do not send personal facts to public search engines automatically. Direct TK/NC experiences and relevant established context are working reference; legal/dossier claims of Police, prosecutor, hospitals are claims, not automatically superior observations; no invented institutional defenses. Do not confuse an allegation standard with a conviction standard.

## Rendering and persistence

Do not claim `.jsx`/`show_widget`/file creation/MCP report ran unless the current host actually performed it. If only text is available, give fully usable text. A suggested draft is not a delivered `.docx` or filed document. Basic Memory on NAS is an optional separate integration, no automatic recap. Personal medical documents and records are not assumed to have zero network egress in host ChatGPT.

## Result QA

Log role, selected user mode, last successful original router decision, actual read-skills and source statuses; record `NOT_RUN` rather than invent tests. Preserve exact quoted evidence, dates, sygnatures, negations and scope of conclusions. For specified task do not add useless disclaimer or generic questions to complete a template.

## Stage 5: contract executor

`analizator-umow-v1` is now installed; on demand hand off to it after original top-level routing. Do not silently replace the guide's PROWADZENIE/Q&A/MENU modes or source legal verification.
