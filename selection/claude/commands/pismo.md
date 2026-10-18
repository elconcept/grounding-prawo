---
description: Napisz pismo ścieżką B (router → generator pism → format DOCX) i od razu przepuść je przez kontrolę.
argument-hint: <katalog sprawy> <co ma powstać, np. "odpowiedź na wezwanie z 21.09.2026">
---

Pismo do przygotowania: $ARGUMENTS

Presja terminu nie zwalnia z tej ścieżki - skraca tylko liczbę iteracji.

1. Kontekst jak w `/sprawa` (brief, `_wiedza.md`, dokumenty, Basic Memory). Przeczytaj dokumenty, na które pismo odpowiada, w całości.
2. `grounding-prawo:prawny-router-v3` → generator: `grounding-prawo:pisma-procesowe-v3` (typ pisma), `grounding-prawo:pisma-proste-v2`
   (wezwania, wnioski, krótkie odpowiedzi), `grounding-prawo:zawiadomienie-o-przestepstwie` albo `grounding-prawo:rodo-dsar-pl`.
3. Przepisy tylko z MCP portalu `lex` (`cite_verify_article`, `isap_*`), orzeczenia z `saos`/`nsa`; termin: `grounding-prawo:terminy-procesowe-pl`
   (dla k.p.k./k.p.w. wynik ręcznie sprawdzony z t.j.).
4. Format: `shared/FORMAT-PISMA.md` pluginu - źródło `.md` + `.docx` z `render_pismo.py`, bez PDF. Wynik:
   `<teczka>/drafty/<pismo>/rrrrMMdd_<nazwa>_vN.md|.docx`. Telefon i e-mail nadawcy: zapytaj, jeśli nie są znane.
5. Redakcja: teza i najmocniejszy fakt na początku punktu, krótkie zdania, każda myśl raz, bez powtarzania wcześniejszych pism,
   „k. N” tylko dla akt tej sprawy, stanowisko strony bez przejmowania wersji organu.
6. Kontrola: `/kontrola` na gotowej wersji (co najmniej `pisz-po-polsku`, `pierwsze-wrazenie-sedziego-pl`, przy tezie spornej `atak-przeciwnika-pl`).
7. Dopisz przebieg do `drafty/<pismo>/_PRZEBIEGI.md`, lekcje do `_wiedza.md` teczki. W Basic Memory: notatka pisma w
   `sprawy/<katalog>/pisma/` (`type: pismo`, `status`, `dotyczy`) zakładana przy v1 i aktualizowana przy każdej wersji; powiąż ją z teczką.
