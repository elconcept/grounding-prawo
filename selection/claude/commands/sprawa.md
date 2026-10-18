---
description: Otwórz pracę nad sprawą - kontekst z teczki, Basic Memory i wybór ścieżki skilli grounding-prawo.
argument-hint: <katalog sprawy albo sygnatura> [cel, np. "odpowiedź na wezwanie"]
---

Otwierasz pracę nad sprawą: $ARGUMENTS

1. Ustal katalog teczki w `sprawy/` (dopasuj sygnaturę do nazwy katalogu; przy wątpliwości zapytaj jednym pytaniem).
2. Przeczytaj w tej kolejności: `<teczka>/analiza/_brief.md` (albo `_brief.md`),
   `_wiedza.md` teczki (lekcje z poprzednich pism - obowiązują), `analiza/_dokumenty.md` (spis dokumentów w `../dokumentacja`),
   ostatnie wpisy `_PRZEBIEGI.md`.
3. Basic Memory (projekt `legal`): `read_note` teczki `sprawy/<katalog>/Teczka — <katalog>`. **Brak teczki = załóż ją teraz**
   (`write_note`, `directory: sprawy/<katalog>`, `type: sprawa`, układ jak w `shared/BASIC-MEMORY.md` i `_schemat/Schemat — sprawa`), powiąż
   z notatkami `postepowania/` (szukaj po sygnaturze). `## Stan` teczki to bieżący stan sprawy. Potem `build_context` z teczki
   i `search_notes` po nazwiskach. Ustalenia wiki to relacja do sprawdzenia w aktach, nie dowód. Nowa sprawa bez katalogu:
   załóż `sprawy/<katalog>/` i teczkę razem.
4. Wywołaj skill `grounding-prawo:prawny-router-v3` i wybierz ścieżkę A-E (mapa celów: `shared/SCIEZKI-PRACY.md`).
5. Odpowiedz krótko: stan sprawy (z datą źródła), najbliższy termin, czego brakuje w aktach, proponowana ścieżka i pierwszy skill.
   Nie zaczynaj pisać pisma, zanim użytkownik potwierdzi cel.
