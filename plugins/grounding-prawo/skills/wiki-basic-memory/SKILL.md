---
name: wiki-basic-memory
description: 'Wiki spraw w Basic Memory: ingest PDF strona po stronie przez model (Markdown do Basic Memory, PDF do R2), pytania i syntezy, kontrola jakości (odnośniki, duplikaty, sprzeczności, luki).'
---

## Pamięć sesji — przed pracą i przed odpowiedzią końcową

Przeczytaj `shared/BASIC-MEMORY.md`, `shared/ZASADY-PLUGINU.md` oraz katalog `shared/INDEKS-SKILLI.md`. Przy redakcji pisma wczytaj `shared/STYLE.md`; przy zapisie plików `shared/ARTEFAKTY-SPRAWY.md`. Na wejściu odczytaj kluczowe trwałe ustalenia z `model-memory`, ostatni recap z `main` i sprawę z `legal`; po etapach zapisuj recap sesji w `main/sesje/` i sprawdź odczytem. Do `model-memory` dodawaj wyłącznie nowe, wartościowe key takeaways; nigdy logu sesji. Nowe dokumenty i ustalenia zapisuj w `legal` po każdym zakończonym etapie. Podaj status pamięci i identyfikator notatki; nie zgłaszaj zapisu bez potwierdzenia MCP.

# Pytania i utrzymanie wiki

Przeczytaj `shared/WIKI.md` i `shared/BASIC-MEMORY.md`. Wybierz gałąź: pytanie,
synteza lub kontrola jakości. Korzystaj z istniejących narzędzi Basic Memory przez
portal Lex; odkryj aktualny schemat narzędzia przed wywołaniem. Projekt podawaj jawnie.

Odpowiedź zakończ źródłami i zakresem rzeczywiście sprawdzonego materiału.
Przy kontroli jakości podaj znalezione problemy, wykonane poprawki i pozostałe braki.

## MODUŁY SCALONE

Ten skill obejmuje funkcje dawnych osobnych skilli. Wczytaj moduł, gdy zadanie go dotyczy; reguły tego skilla obowiązują także w module.

| Moduł | Zastosowanie | Plik |
|---|---|---|
| `ingest-wiki` | ingest PDF do Basic Memory strona po stronie przez model; oryginał PDF do R2 | `modules/ingest-wiki/MODULE.md` |

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** pytanie do wiki, synteza lub kontrola jakości
- **Wynik zapisz w:** istniejąca notatka tematyczna, źródło Markdown w `legal/dokumenty` i recap sesji (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `analizator-dowodow-v3`, `chronologia-sprawy-v1`
- **Basic Memory (`legal`):** źródła odpowiedzi, synteza, sprzeczności i wykryte braki (protokół: `shared/BASIC-MEMORY.md`)
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
