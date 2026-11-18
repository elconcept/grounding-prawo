# Test scenarios — original route [1]–[11] (no substituted router)

These are static mapping checks. They do not assert execution of a model, remote tool or legal-source verification.

| Input cue | Category | Source PRIMARY | Unchanged routing nuance |
|---|---|---|---|
| Analyze a contract's clauses | [1] | `analizator-umow-v1` | A contract as background of a dispute → [10] |
| Analyze an already supplied appellate judgment | [2] | `analiza-sadowa-v6` | "apelacyjny" names a court, not a requested pleading |
| Draft an appeal against a ruling | [3] | `pisma-procesowe-v3` | An appellate judgment as a document stays [2] |
| Single-purpose request for justification | [4] | `pisma-proste-v2` | Multi-topic pleading → [3] |
| Find a judgment of Supreme Court | [5] | `orzeczenia-sadowe-v2` | Searching a judgment vs analyzing supplied text |
| Evaluate recordings as evidence | [6] | `analizator-dowodow-v3` | Mentioning recordings as story context → [10] |
| Explain where to start | [7] | `przewodnik-prawny-v2` | LAIK fallback retains original |
| Questions for cross-examination | [8] | `przesluchanie-swiadkow-v2-min90` | Expert mentioned incidentally → [10] |
| Analyze Article X scope | [9] | `analizator-przepisow-v2` | Requires real versioned source check |
| Arrest/RODO case classification | [10] | `prawo-polskie-v2` | Domain facade unchanged |
| Audit a legal opinion from another AI | [11] | `analizator-przepisow-v2` | `references/AUDYT-KLUCZA-ODPOWIEDZI.md` K0–K6 |
| Victim crime notification | source exception | `zawiadomienie-o-przestepstwie` external | No automatic pleading-guilt threshold, no unverified PRIMARY read |
