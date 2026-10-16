---
name: patron-analiza-akt-karnych
description: Ustrukturyzowana 6-punktowa analiza obrończa akt sprawy karnej - zarzut, dowody (sprzeczności, luki, opinie biegłych), wyrok I instancji, apelacja, wyrok II instancji i dalsza linia obrony (kasacja, wznowienie, areszt). Użyj, gdy użytkownik ma akta sprawy karnej i prosi o analizę, streszczenie pod kątem obrony albo wskazanie słabych punktów oskarżenia.
---

> **Pliki przebiegu (reguła kanoniczna):** zapisuj według `shared/ARTEFAKTY-SPRAWY.md` - nowym plikiem jest
> tylko wersja wynikowa (`drafty/<pismo>/rrrrMMdd_<nazwa>_vN.*`); logi, raporty, ustalenia i recapy przebiegu
> dopisuj do istniejących plików inkrementalnych (`_PRZEBIEGI.md`, `_SUBSUMPCJA*.md`, `_FINDINGS.md` …), a pliki
> jednorazowe zostawiaj w `_robocze/` sprawy.

# Analiza akt sprawy karnej (6 punktów)

Pracuj WYŁĄCZNIE na dokumentach sprawy. Nie zmyślaj faktów, nazwisk ani sygnatur - czego nie ma
w aktach, napisz wprost „brak w aktach”. To projekt do redakcji przez obrońcę, nie gotowe pismo.

**Dyscyplina cytatu:** każde przywołanie treści akt to dosłowny cytat + dokument (nazwa pliku) +
strona („str. N”, jeśli znana). Bez tego nie przypisuj twierdzenia aktom. Orzeczenia i przepisy
podawaj z sygnaturą lub numerem artykułu dosłownie (sprawdzenie: skill `patron-prawo-pl-zrodla`).

Przygotowanie: tekst akt ze znacznikami stron (`doc_to_text.py` ze skilla
`patron-przeglad-tabelaryczny`). Przy obszernych aktach zacznij od spisu dokumentów (co, data, strony).

## Struktura
1. **Zarzut** - dokładna treść zarzutu lub aktu oskarżenia: kwalifikacja prawna, opis czynu,
   data, miejsce, kwota, znamiona. Cytat z aktu oskarżenia + strona.
2. **Dowody** - dowody oskarżenia i obrony (zeznania, dokumenty, opinie biegłych, protokoły).
   Dla każdego: co dowodzi i z czego to wynika (cytat + strona). Wyraźnie oznacz
   **SPRZECZNOŚCI i LUKI** (zeznanie vs protokół, opinia vs opinia, brak dowodu na znamię).
   Opinie biegłych oceń pod kątem art. 201 k.p.k. (niepełność, niejasność, sprzeczność,
   przekroczenie granic opiniowania).
3. **Wyrok I instancji** - rozstrzygnięcie, ustalenia faktyczne, ocena dowodów. Wychwyć
   naruszenia: swobodna vs dowolna ocena dowodów (art. 7 k.p.k.), pominięcie całokształtu
   okoliczności (art. 410), braki uzasadnienia (art. 424), wątpliwości rozstrzygnięte na
   niekorzyść oskarżonego (art. 5 § 2). Cytat z uzasadnienia + strona.
4. **Apelacja** - podniesione zarzuty i ich podstawy (art. 438 k.p.k.: obraza prawa
   materialnego lub procesowego, błąd w ustaleniach faktycznych, rażąca niewspółmierność kary).
   Oceń, na ile trafiają w ustalenia z pkt 3.
5. **Wyrok II instancji** - rozstrzygnięcie sądu odwoławczego, które zarzuty uwzględniono,
   które oddalono i dlaczego (cytat + strona).
6. **Wskazania / dalsza linia obrony** - niewykorzystane sprzeczności i luki, możliwe dalsze
   środki (kasacja, wznowienie), ryzyka. Przy tymczasowym aresztowaniu oceń przesłanki
   art. 249 i 258 k.p.k. (realne uzasadnienie, indywidualizacja, dowolność ocen).

Wynik w czacie; plik (`analiza-akt.md`, Word przez pandoc) tylko na prośbę. Na końcu zaproponuj
weryfikację cytatów (skill `patron-weryfikacja-cytatow`) przed użyciem fragmentów w piśmie.

---
Źródło: Patron (MateMatic Solutions, AGPL-3.0) - `backend/src/lib/builtinWorkflows.ts`
(builtin-analiza-akt-karne, ADR-0130).

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** akta sprawy karnej po OCR
- **Wynik zapisz w:** analiza obrończa w `analiza/_podsumowanie.md` (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `pisma-procesowe-v3`, `analizator-dowodow-v3`
- **Basic Memory (`legal`):** czytaj teczkę sprawy (`build_context`) i notatki wiki po sygnaturze i nazwiskach; zapisz stan sprawy i terminy w teczce, nowe fakty z akt zgłoś do ingestu (protokół: `shared/BASIC-MEMORY.md`)
- **Mapa ścieżek:** skill `prowadnik-grounding-prawo`.
