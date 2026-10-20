# Ocena skilli z enhance-workflows

Ocena dotyczy użycia w repo rozwijającym `grounding-prawo` oraz w publikowanym
pluginie prawniczym. Skille deweloperskie pozostają w `.agents/skills`; nie są
dołączane do marketplace pluginu.

| Skill | Decyzja | Uzasadnienie |
|---|---|---|
| `feature-factory` | włączony do repo | Kompletny, przenośny workflow ograniczonej zmiany z testami i audytem. |
| `peer-agent-collaboration` | przeniesiony do globalnych skilli HolyClaude (2026-10-20) | Rozszerzony o tryb delegowania: drogi model planuje, darmowe modele OpenCode wykonują (`~/.agents/bin/delegate`). |
| `whitepaper-audit` | włączony tylko do repo | Deterministyczny audyt dokumentacji technicznej. Nie służy do audytu pism prawnych. |
| `release` | włączony do repo | Dostarcza sprawdzalny mechanizm planowania wersji i kompatybilności. |
| `rag-eval` | P0: adaptacja później | Model gold-setów jest trafny, ale upstream nie zawiera deklarowanego `eval_sweep.py` i zakłada klasyczny vector store. Potrzebny adapter do Repertorium, SAOS, LEGAL-CITE i testów odpowiedzi negatywnych. |
| `skill-studio` | nie włączono | Wymaga instalacji własnego CLI; kopiowanie samego skilla tworzyłoby niedziałające polecenia. Może być uruchamiany bezpośrednio z submodułu po świadomej instalacji. |
| `tdd` | nie włączono | Zakłada Claude `Task`, trzy role subagentów i ścieżki `~/.claude/skills`; jest zbyt sztywny dla wielohostowego repo. Zwykłe TDD pokrywa `feature-factory`. |
| `retrospective` | nie włączono | Zakłada transkrypty Claude i automatyczne edycje pamięci, skilli oraz instrukcji. W tym repo wnioski mają być proponowane i zatwierdzane. |
| `repo-prep` | nie włączono | Narzędzie jednorazowe; nie uzasadnia stałej obecności jako skill projektu. |
| `balanced` | nie dodano do pluginu | Funkcje pokrywają `adversarial-legal-review-pl`, `atak-przeciwnika-pl`, `subsumpcja-pl` i `case-risk`, które dodatkowo wymagają oparcia w aktach. |
| `whitepaper-audit` dla pism | nie dodano do pluginu | Audyt pism już łączą `szturm-na-draft-pl`, `citation-grounding-pl`, `deliverable-fidelity-pl`, `ocena-outputu-pl` i soczewki procesowe. |
| `qmd-search` | eksperyment przed decyzją | Basic Memory już zapewnia wyszukiwanie tekstowe i semantyczne. Dodanie drugiego indeksu wymaga benchmarku na polskich aktach. |
| `decision-toolkit` | nie dodano do pluginu | Jest ogólnym generatorem dashboardów; oceny strategii prawnej pokrywają istniejące skille z rygorem dowodowym. |
| `deep-research` | nie dodano do pluginu | Zakłada osobny OpenAI Deep Research API i długi blokujący proces; research prawny jest kierowany przez konektory źródłowe i istniejące skille. |

## Zakres przyszłego `legal-retrieval-eval`

Minimalny gold set powinien osobno mierzyć: trafność przepisu, trafność orzeczenia,
pozyskanie rzeczywistej treści, wybór właściwego fragmentu uzasadnienia, entailment
odpowiedzi przez źródła oraz poprawną odmowę, gdy źródło nie zawiera odpowiedzi.
Koszt i latency należy raportować oddzielnie od jakości. Dane z konkretnych spraw
mogą wejść do zestawu dopiero po świadomej decyzji o zakresie i miejscu przechowywania.

## Persistent memory

`claude-legal-persistent-memory-pl` pozostaje źródłem porównawczym. Nie uruchamiamy
drugiego automatycznego dziennika obok Basic Memory, dopóki test nie wykaże wyższej
odzyskiwalności ustaleń bez duplikowania notatek i bez rozbieżnych źródeł prawdy.
