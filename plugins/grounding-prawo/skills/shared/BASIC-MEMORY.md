# Basic Memory w pracy nad sprawą

Basic Memory (projekt `legal`) to wiki spraw wspólna dla wszystkich postępowań i sesji: teczki spraw,
postępowania, zdarzenia, osoby, nieprawidłowości, zweryfikowane orzeczenia i lekcje. Pliki w teczce sprawy
(`shared/ARTEFAKTY-SPRAWY.md`) trzymają pracę nad jednym pismem; wiki trzyma to, co ma przetrwać sesję i przydać się
w innej sprawie. Każdy skill pracujący nad sprawą czyta wiki na wejściu i aktualizuje ją na wyjściu - sekcja MOST
skilla podaje, co dokładnie.

Narzędzia: MCP `basic-memory` (lokalnie) albo `pilot-basic-memory_*` w portalu `lex`; zawsze z `project="legal"`.
Zapis tylko narzędziami MCP (`write_note`, `edit_note`), nigdy plikiem do katalogu danych. Konektor niedostępny:
pracuj dalej, a w `_PRZEBIEGI.md` zapisz „Basic Memory: NOT_CHECKED” i zaległy zapis do wykonania.

## Teczka sprawy

Każda sprawa ma folder `sprawy/<katalog teczki>/` z notatką `Teczka — <katalog teczki>` (`type: sprawa`, schemat
`_schemat/Schemat — sprawa`; frontmatter (poza pluginem) `teczka: legal/<katalog>`, `status`, `sygnatury` tylko z dokumentów).
Brak teczki przy pierwszej pracy nad sprawą: załóż ją przed analizą lub pismem. Sekcje:

| Sekcja | Wpis |
|---|---|
| `## Stan` | `- [stan] ... (data, źródło)` |
| `## Terminy` | `- [termin] ... @due:RRRR-MM-DD` |
| `## Decyzje użytkownika` | `- [decyzja] ...` |
| `## Lekcje` | `- [lekcja] ...` (pełna lista w `_wiedza.md`) |
| `## Pisma` / `## Relacje` | `- pismo [[...]]`, `- postepowanie [[postepowania/...]]` |

Pisma: `sprawy/<katalog>/pisma/` (`type: pismo`, `status: szkic | do-podpisu | zlozone`, `dotyczy` = postępowanie):
wersja, ścieżka pliku, stan pętli doskonalenia (runda, otwarte uwagi, pytania do autora), wynik kontroli.

## Odczyt na wejściu

1. `read_note` teczki i `build_context` z niej (postępowania, pisma); `search_notes` po sygnaturze i nazwiskach.
2. Decyzje użytkownika i lekcje z teczki obowiązują w tej pracy, tak jak `_wiedza.md`.
3. Przed szukaniem orzeczenia w MCP sprawdź `orzeczenia/`; przed analizą przepisu `ustawy/` i `zagadnienia/`.
4. Ustalenie wiki to relacja do sprawdzenia w aktach (`potwierdzone_dokumentem`), nie dowód ani źródło brzmienia przepisu.

## Zapis na wyjściu

Zapisuj po każdej istotnej zmianie (`edit_note`, append albo replace_section), nie na koniec sesji:

| Zmiana | Gdzie |
|---|---|
| nowa wersja pisma, runda pętli, wynik kontroli | notatka pisma |
| decyzja użytkownika, termin, stan sprawy | teczka: `## Decyzje użytkownika`, `## Terminy`, `## Stan` |
| lekcja do kolejnych pism (zarzut, który wracał, uwaga autora do formy) | teczka `## Lekcje` + `_wiedza.md` |
| zweryfikowane orzeczenie przydatne w innych sprawach | `orzeczenia/` (`type: orzeczenie`, `sygnatura`, `zrodlo_url`), relacja z teczką |
| nowy fakt z akt spoza wiki | zgłoszenie do ingestu (`_metodologia/Metodologia ingestu`, jeden dokument naraz); wiki nie przepisuj hurtem |

Fakty o przebiegu postępowań należą do notatek `postepowania/`, nie do teczki. Każdy wpis ma źródło
(`— źródło: [[<dokument>]] (s. N)` albo `(relacja <kto>, <data>)`). Język i oznaczenia: `_metodologia/Zasady języka wiki`.
