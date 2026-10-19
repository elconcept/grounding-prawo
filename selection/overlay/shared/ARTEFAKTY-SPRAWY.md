# ARTEFAKTY-SPRAWY - jakie pliki zostawia praca nad sprawą

Reguła kanoniczna dla każdego skilla, który analizuje akta, draftuje albo kontroluje pismo w teczce sprawy.
Cel: mało plików, pełny ślad. Kolejny przebieg niczego nie dubluje - dopisuje do plików, które już istnieją.

`<sprawa>` oznacza teczkę sprawy `legal/sprawy/<katalog_sprawy>/`. Używaj istniejącej teczki, nie zakładaj
drugiej kopii. Wspólny katalog odbioru to `legal/output/`; nazwa pliku musi identyfikować sprawę i pismo
(np. `20261018_NC_pismo_przewodnie_BSWP_v7.docx`), aby identyczne tytuły w różnych sprawach nie nadpisywały się.

Pismo istnieje w dwóch miejscach i w dwóch formatach:
- `<sprawa>/drafty/<pismo>/` - wyłącznie Markdown: kolejne wersje `_v1`, `_v2`, `_v3`... (historia, nic nie jest nadpisywane);
- `legal/output/` - wyłącznie DOCX: dokładnie jeden plik dla każdego pisma, dokument roboczy autora.

## Rodzaje plików

| Rodzaj | Gdzie | Zasada |
|---|---|---|
| **Wersja pisma (snapshot)** | `<sprawa>/drafty/<pismo>/rrrrMMdd_<nazwa>_vN.md` | Stan pisma na początku pracy, po akceptacji redline i ze zmianami autora. Każda sesja pracy nad pismem dodaje jedną wersję z podbitym `vN`. Tylko MD; w `drafty/` nie ma DOCX. |
| **DOCX pisma** | `legal/output/rrrrMMdd_<nazwa>_vN.docx` | Jeden plik na pismo, tylko DOCX. Po sesji zawiera zmiany tej sesji jako redline względem snapshotu `vN`. Bez sidecara `.md` i bez starszych wersji. |
| **Pliki inkrementalne** (prefiks `_`) | `drafty/<pismo>/_*.md` (dla pisma), `analiza/_*.md` (dla sprawy) | Tworzone raz, potem tylko uzupełniane dopiskiem przebiegu. Nigdy kopia, `_v2` ani nowy plik z datą. |
| **Pliki jednorazowe** | `_robocze/` | Workspace modelu: wyciągi, JSON-y, wyniki skryptów, redline'y, notatki. Nikt ich nie czyta - model zbiera z nich esencję do plików inkrementalnych. |
| **Wynik soczewki / skilla kontroli** | `<sprawa>/_robocze/rrrrMMdd_hhmm_<skill>_<wersja>.md` | Każdy przebieg skilla oceniającego pismo (Marko, recenzja, pierwsze wrażenie sędziego, atak przeciwnika, fidelity, karta ocen) zapisany od razu, w katalogu sprawy. `hhmm` to rzeczywisty czas zapisu (`date +%Y%m%d_%H%M`), nie szacunek. |

## Zestaw standardowy

| Plik | Co zawiera | Kto pisze |
|---|---|---|
| `analiza/_dokumenty.md` | indeks akt: plik, strona, rodzaj, status odczytu (OCR), luki | `the-ocr`, `akta-przeszukiwalne-pl`, `patron-przeglad-tabelaryczny` |
| `analiza/_brief.md` | stan sprawy w skrócie: strony, cel, żądania, terminy | `prawny-router-v3`, `analiza-sadowa-v6` |
| `analiza/_chronologia.md` | oś zdarzeń z cytatem i stroną; niespójności | `chronologia-sprawy-v1`, `chronologia-stanowiska-pl` |
| `analiza/_dowody-i-przepisy.md` | dowody, przepisy (z potwierdzeniem źródła), tezy orzeczeń | `analizator-dowodow-v3`, `analizator-przepisow-v2`, `orzeczenia-sadowe-v2` |
| `analiza/_podsumowanie.md` | wnioski analizy i ryzyka | `analiza-sadowa-v6`, `case-risk` |
| `drafty/<pismo>/rrrrMMdd_<nazwa>_vN.md` | snapshot pisma z początku sesji; wszystkie wersje tworzą historię | skille pism |
| `legal/output/rrrrMMdd_<nazwa>_vN.docx` | jedyny DOCX pisma: snapshot `vN` + redline zmian sesji | skille pism |
| `drafty/<pismo>/_SUBSUMPCJA.md` | rejestr stały: teza - przesłanka - dowód - kotwica (format: `szturm-na-draft-pl/references/rejestr-staly.md`) | `subsumpcja-pl`, `szturm-na-draft-pl` |
| `drafty/<pismo>/_PRZEBIEGI.md` | rejestr przebiegów: data, cel, wynik, decyzje autora, wskaźnik do `_robocze/` | każdy skill kontroli |
| `drafty/<pismo>/_FINDINGS.md` | lista nieprawidłowości ze stałymi ID (`F-12`); pozycja zmienia status, nie jest duplikowana | skille kontroli |
| `_wiedza.md` (korzeń teczki) | lekcje do doskonalenia kolejnych pism: co działało, jakie zarzuty wracały, wzorce orzeczeń | każdy skill na koniec przebiegu |

Nowy plik inkrementalny wolno założyć tylko wtedy, gdy przebieg daje inny rodzaj informacji, który będzie
uzupełniany dalej (np. `_MAPA_KRZYWD.md`, `_PYTANIA.md`); uzasadnij jednym zdaniem w `_PRZEBIEGI.md`.

Format dopisku: sekcja z datą i numerem przebiegu (`## Przebieg 3 - 2026-10-03`) na końcu pliku albo
pozycja ze stałym ID zmieniająca status. Brak szumu: jeden plik na rodzaj informacji.

## Cykl pracy nad pismem

Każda sesja pracy nad istniejącym pismem (redakcja, szturm, kontrola z poprawkami) ma ten sam przebieg:

1. **Akceptacja redline.** Weź DOCX pisma z `legal/output/`. Jeżeli ma niezaakceptowane zmiany śledzone
   (także propozycje DECYZJA_AUTORA z poprzedniej sesji, których autor nie odrzucił), przyjmij wszystkie
   (`redline-docx-pl`, przypięty `adeu accept-all`) w kopii roboczej `<sprawa>/_robocze/`. Odrzucenie zmiany
   jest decyzją autora podejmowaną w Wordzie przed sesją; model nie pyta o nie ponownie. Wyjątek: redline
   kontrahenta albo innego autora w cudzym dokumencie wymaga osobnej decyzji użytkownika.
2. **Snapshot.** Pełny tekst zaakceptowanej kopii (ze wszystkimi zmianami wprowadzonymi przez autora
   ręcznie) zapisz jako `<sprawa>/drafty/<pismo>/rrrrMMdd_<nazwa>_vN.md` z numerem o jeden wyższym od
   ostatniej wersji w katalogu. Porównaj zapis z ekstrakcją DOCX; snapshot jest bazą całej sesji.
3. **Praca** odbywa się na snapshot i kopiach w `_robocze/`. Kolejne rundy (np. pętla szturmu) nakładają
   swoje zmiany na redline z poprzedniej rundy, a nie na nową bazę.
4. **Redline.** Sesja kończy się jednym DOCX: zaakceptowana kopia z kroku 1 i wszystkie zmiany sesji jako
   zmiany śledzone (`w:ins`/`w:del`) z komentarzem przy każdej. Zweryfikuj strukturę pliku, a nie komunikat
   narzędzia. Zapisz go w `legal/output/rrrrMMdd_<nazwa>_vN.docx` (`vN` = numer snapshotu) i dopiero po
   sprawdzeniu nowego pliku usuń z `legal/output/` poprzedni DOCX tego samego pisma. Jeżeli śledzenia zmian
   nie da się utworzyć, etap jest NIEZAKOŃCZONY, a poprzedni DOCX zostaje.

Nowe pismo: pierwszą treść zapisz jako `drafty/<pismo>/rrrrMMdd_<nazwa>_v1.md`, a wygenerowany z niej DOCX
(bez śledzenia zmian) jako jedyny DOCX pisma w `legal/output/`.

Stan końcowy dla jednego pisma: w `<sprawa>/drafty/<pismo>/` wszystkie wersje `.md` i żadnego DOCX;
w `legal/output/` dokładnie jeden DOCX tego pisma i żadnego `.md`. Nie naruszaj innych pism, załączników
ani dokumentów dostarczonych przez autora.

## Zakazy

- Pliki logu, recapu, „summary", „issues", raportu tury poza `_robocze/` - zamiast tego dopisek do pliku inkrementalnego.
- Katalogi `PRZEBIEG_*`, `RUN/`, `out/` w `analiza/` i `drafty/`. Katalog narzędzia: `_robocze/rrrrMMdd_<pismo>__<narzędzie>/`.
- Kopie „(2)", `_kopia`, `__dup`, `.md.md` - duplikaty się usuwa.
- Jakiekolwiek DOCX w `drafty/<pismo>/`, pliki `.md` w `legal/output/` oraz więcej niż jeden DOCX tego samego pisma w `legal/output/`.

## Koniec przebiegu

1. Esencja z `_robocze/` jest w plikach inkrementalnych (ustalenia, decyzje, pytania, stan kotwic).
2. Nowe pliki poza `_robocze/`: snapshot `.md` w `drafty/<pismo>/` i jedyny DOCX pisma z redline sesji w
   `legal/output/` (+ ewentualnie nowy plik inkrementalny z uzasadnieniem). Poprzedni DOCX tego pisma usunięty.
3. `_PRZEBIEGI.md` ma wpis przebiegu; lekcje o ogólnej wartości trafiły do `_wiedza.md`.
4. Sprawa bez folderu (rozmowa bez plików): wynik w odpowiedzi, a pliki zakładaj dopiero na prośbę użytkownika.
