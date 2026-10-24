---
description: Kontrola gotowego pisma (ścieżka C) - soczewki grounding-prawo, każdy wynik zapisany w _robocze/rrrrMMdd_hhmm_.
argument-hint: <ścieżka pisma .md/.docx> [soczewki: pelna | szybka | marko,sedzia,atak,fidelity,ocena,cytaty,styl]
---

Pismo do kontroli: $ARGUMENTS

Zestawy soczewek (skille z prefiksem `grounding-prawo:`):
- `pelna` (domyślnie): `szturm-na-draft-pl` (orkiestrator); jeśli pismo nie ma `.docx` - ręcznie: `ekstraktor-cytatow-pl` →
  `citation-grounding-pl` → `subsumpcja-pl` → `pierwsze-wrazenie-sedziego-pl` → `atak-przeciwnika-pl` → `adversarial-legal-review-pl`
  → `deliverable-fidelity-pl` → `ocena-outputu-pl` (karta 1-5).
- `szybka`: `pisz-po-polsku` → `pierwsze-wrazenie-sedziego-pl` → `ocena-outputu-pl`.
- pojedyncze: `marko` = `marko-pl-content`, `sedzia` = `pierwsze-wrazenie-sedziego-pl`, `atak` = `atak-przeciwnika-pl`,
  `fidelity` = `deliverable-fidelity-pl`, `ocena` = `ocena-outputu-pl`, `cytaty` = `ekstraktor-cytatow-pl` + `citation-grounding-pl`,
  `styl` = `pisz-po-polsku`.

Zasady:
1. Każda soczewka w osobnym przebiegu; wynik jednej nie zwalnia z następnej.
2. Wynik każdej soczewki zapisz od razu w `<teczka>/_robocze/$(date +%Y%m%d_%H%M)_<soczewka>_<wersja>.md` (rzeczywisty czas, nie szacunek).
3. Kontrola to pętla, nie raport (`shared/ZASADY-PLUGINU.md`, „Pętla doskonalenia pisma”): uwagi, które możesz naprawić, wdroż
   w nowej wersji `_vN+1`; o fakty, dowody i decyzje strategiczne pytaj użytkownika od razu (narzędzie pytań interaktywnych) i wdroż
   odpowiedź; potem uruchom soczewki ponownie na nowej wersji. Powtarzaj, aż pełna runda nie da uwag 🔴/🟠 (`GOTOWE`) albo
   użytkownik przerwie (`NIEGOTOWE` z listą otwartych uwag).
4. Po każdej rundzie: dopisek do `drafty/<pismo>/_PRZEBIEGI.md` i notatki pisma w Basic Memory (wersja, otwarte uwagi, pytania).
   Werdykt `PASS` / `FAIL` / `NOT_CHECKED` / `NEEDS_REVIEW`. Nie ogłaszaj gotowości przy niezweryfikowanym cytacie albo poprawce
   wprowadzonej po ostatniej soczewce.
