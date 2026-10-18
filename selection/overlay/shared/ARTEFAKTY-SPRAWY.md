# ARTEFAKTY-SPRAWY - jakie pliki zostawia praca nad sprawą

Reguła kanoniczna dla każdego skilla, który analizuje akta, draftuje albo kontroluje pismo w teczce sprawy.
Cel: mało plików, pełny ślad. Kolejny przebieg niczego nie dubluje - dopisuje do plików, które już istnieją.

## Trzy rodzaje plików

| Rodzaj | Gdzie | Zasada |
|---|---|---|
| **Wersja wynikowa** pisma | `drafty/<pismo>/rrrrMMdd_<nazwa>_vN.md` oraz, tylko dla najnowszej wersji, odpowiadający mu `.docx` | Każdy przebieg tworzy historyczne źródło `.md` z podbitym `vN`. W katalogu pisma pozostaje dokładnie jeden wynikowy DOCX: najnowszy. |
| **Kopia do odbioru** | `<sprawa>/output/rrrrMMdd_<nazwa>_vN.docx` | Kopia wyłącznie najnowszego DOCX. Dla tego pisma nie przechowuj tu Markdown ani starszych wersji DOCX. |
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
| `drafty/<pismo>/rrrrMMdd_<nazwa>_vN.md` | wersja pisma; wszystkie wersje tworzą historię | skille pism |
| `drafty/<pismo>/rrrrMMdd_<nazwa>_vN.docx` | najnowsza wersja pisma; dokładnie jeden wynikowy DOCX | skille pism |
| `output/rrrrMMdd_<nazwa>_vN.docx` | kopia najnowszej wersji do odbioru; bez sidecara `.md` | skille pism |
| `drafty/<pismo>/_SUBSUMPCJA.md` | rejestr stały: teza - przesłanka - dowód - kotwica (format: `szturm-na-draft-pl/references/rejestr-staly.md`) | `subsumpcja-pl`, `szturm-na-draft-pl` |
| `drafty/<pismo>/_PRZEBIEGI.md` | rejestr przebiegów: data, cel, wynik, decyzje autora, wskaźnik do `_robocze/` | każdy skill kontroli |
| `drafty/<pismo>/_FINDINGS.md` | lista nieprawidłowości ze stałymi ID (`F-12`); pozycja zmienia status, nie jest duplikowana | skille kontroli |
| `_wiedza.md` (korzeń teczki) | lekcje do doskonalenia kolejnych pism: co działało, jakie zarzuty wracały, wzorce orzeczeń | każdy skill na koniec przebiegu |

Nowy plik inkrementalny wolno założyć tylko wtedy, gdy przebieg daje inny rodzaj informacji, który będzie
uzupełniany dalej (np. `_MAPA_KRZYWD.md`, `_PYTANIA.md`); uzasadnij jednym zdaniem w `_PRZEBIEGI.md`.

Format dopisku: sekcja z datą i numerem przebiegu (`## Przebieg 3 - 2026-10-03`) na końcu pliku albo
pozycja ze stałym ID zmieniająca status. Brak szumu: jeden plik na rodzaj informacji.

## Wersjonowanie pisma i publikacja do `output`

Każda runda korzysta z **ostatniego DOCX autora**, a nie z dokumentu
sprzed jego poprawek. Runda rozpoczyna się od wykonanej na **kopii**
automatycznej akceptacji pozostawionych zmian śledzonych (przypięty
`redline-docx-pl`, adeu `accept-all`); użytkownik nie musi osobno
zatwierdzać zmian własnego pisma, które poprzednia runda pozostawiła
w śledzeniu. Nie nadpisuj oryginalnego wejścia.

1. Po akceptacji dotychczasowego redline odczytaj pełną bazę i przeprowadź
   nowy przegląd.
2. Zapisz kompletny wynikowy tekst nowej wersji jako
   `drafty/<pismo>/rrrrMMdd_<nazwa>_vN.md`. Wszystkie historyczne MD pozostają
   nietknięte.
3. Utwórz **jeden DOCX wynikowy z aktywnymi Track Changes** pokazującymi
   poprawki tej rundy. Zweryfikuj śledzenie i odczyt treści; nie dodawaj
   drugiego DOCX bez redline.
4. Skopiuj nowy DOCX do `<sprawa>/output/`. Po sprawdzeniu kopii usuń
   starszy DOCX **tego samego pisma** z katalogu draftów i output.
   Nie naruszaj innych pism, załączników ani oryginału dostarczonego przez
   autora.

Stan końcowy: historia pełnych wersji `*.md`, jeden wynikowy
`*.docx` z redline oraz jego kopia w `output/`. Na początku następnej
rundy zaakceptuj ten redline w kopii roboczej.

Wyjątek: cudze dokumenty i negocjowane redline kontrahenta wymagają
osobnej decyzji przed zaakceptowaniem wszystkich zmian.

## Zakazy

- Pliki logu, recapu, „summary", „issues", raportu tury poza `_robocze/` - zamiast tego dopisek do pliku inkrementalnego.
- Katalogi `PRZEBIEG_*`, `RUN/`, `out/` w `analiza/` i `drafty/`. Katalog narzędzia: `_robocze/rrrrMMdd_<pismo>__<narzędzie>/`.
- Kopie „(2)", `_kopia`, `__dup`, `.md.md` - duplikaty się usuwa.
- Historyczne DOCX wersji pisma w `drafty/<pismo>/` oraz jakiekolwiek pliki `.md` pisma w `output/`.

## Koniec przebiegu

1. Esencja z `_robocze/` jest w plikach inkrementalnych (ustalenia, decyzje, pytania, stan kotwic).
2. Nowe pliki poza `_robocze/`: historyczny `.md`, DOCX najnowszej wersji i jego kopia w `output/`
   (+ ewentualnie nowy plik inkrementalny z uzasadnieniem). Starsze wynikowe DOCX tego pisma usunięte.
3. `_PRZEBIEGI.md` ma wpis przebiegu; lekcje o ogólnej wartości trafiły do `_wiedza.md`.
4. Sprawa bez folderu (rozmowa bez plików): wynik w odpowiedzi, a pliki zakładaj dopiero na prośbę użytkownika.
