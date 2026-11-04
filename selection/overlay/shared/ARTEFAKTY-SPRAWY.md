# ARTEFAKTY-SPRAWY - jakie pliki zostawia praca nad sprawą

Reguła kanoniczna dla każdego skilla, który analizuje akta, draftuje albo kontroluje pismo w teczce sprawy.
Cel: mało plików, pełny ślad. Kolejny przebieg niczego nie dubluje - dopisuje do plików, które już istnieją.

`<sprawa>` oznacza teczkę sprawy `legal/sprawy/<katalog_sprawy>/`. Używaj istniejącej teczki, nie zakładaj
drugiej kopii. Wspólny katalog odbioru to `legal/output/`; nazwa pisma musi identyfikować sprawę i pismo
(np. `II_W_1342_26_wniosek_o_sprostowanie_protokolu`), aby identyczne tytuły w różnych sprawach nie nadpisywały się.

**Wersje zamiast zmian śledzonych (decyzja autora, 4.11.2026).** Mechanizm redline dla własnego pisma jest wycofany.
Każda zmiana pisma to nowy plik DOCX z wyższym sufiksem wersji; poprzednie wersje zostają bez zmian.

Pismo istnieje w tych miejscach:
- `legal/output/<nazwa>/` - folder pisma. Zawiera wszystkie wersje `<nazwa>_v1.docx`, `<nazwa>_v2.docx`, ...
  (nazwa bez daty i godziny), kopie wszystkich załączników, spis `_ZALACZNIKI.md` i raporty kontroli (`_*.md`, `_*.json`).
  Bieżące pismo to wersja z najwyższym `N`. Złożona wersja PDF (`<nazwa>.pdf`) może leżeć obok. Żadne pismo nie leży
  luzem w korzeniu `output/`;
- `<sprawa>/pisma/<nazwa>.docx` - kopia bieżącej wersji w teczce sprawy, odświeżana po każdej nowej wersji;
- `<sprawa>/drafty/<pismo>/` - źródło Markdown nowego pisma (`rrrrMMdd_hhmm_<nazwa>_v1.md`) i, opcjonalnie,
  snapshoty tekstu kolejnych wersji (`nastepna --drafty`). Historią pisma są wersje DOCX w folderze pisma.

Plik pisma luzem w `output/`, `.md` w folderze pisma (poza `_*.md`), DOCX bez `_vN` albo z nazwą innego pisma
i niezaakceptowane zmiany śledzone w najnowszej wersji to błąd do naprawy w tym samym przebiegu.

## Teczka sprawy - ustal przed pierwszym zapisem

Zanim zapiszesz pierwszy plik pisma, wskaż teczkę: `ls legal/sprawy/`, notatki Basic Memory (`legal`, `sprawy/`,
`relacje/<autor>/` z rejestrem pism) i sygnatury lub numery z treści pisma (np. numer procedury, sygnatura,
organ). Pismo dotyczące sprawy, która ma teczkę, idzie do jej `drafty/<pismo>/`, także gdy jest pismem do innego
organu (np. wniosek do MOPS o dane z procedury, na którą powołuje się sprawa karna).

Gdy teczka nie wynika jednoznacznie z materiału, zapytaj autora przed zapisem (narzędzie pytań interaktywnych,
jeśli jest): podaj 2-3 najbardziej prawdopodobne teczki z uzasadnieniem w jednym zdaniu i opcję „nowa teczka”
z proponowaną nazwą katalogu. Do odpowiedzi nie zapisuj niczego w `legal/output/` ani w `legal/` poza `_robocze/`.
Nowa teczka powstaje dopiero po decyzji autora; jej nazwę wpisz do rejestru pism w Basic Memory.

## Rodzaje plików

| Rodzaj | Gdzie | Zasada |
|---|---|---|
| **Wersja pisma (DOCX)** | `legal/output/<nazwa>/<nazwa>_vN.docx` | Każda zmiana pisma to nowy plik z `N` o jeden wyższym; starsze wersje zostają. Bez zmian śledzonych. W folderze tylko DOCX, PDF, załączniki i pliki `_*`. |
| **Źródło i snapshot (MD)** | `<sprawa>/drafty/<pismo>/rrrrMMdd_hhmm_<nazwa>_vN.md` | Źródło nowego pisma (`_v1`) i opcjonalne snapshoty tekstu kolejnych wersji. W `drafty/` nie ma DOCX. |
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
| `drafty/<pismo>/rrrrMMdd_hhmm_<nazwa>_vN.md` | źródło nowego pisma i snapshoty tekstu wersji | skille pism |
| `legal/output/<nazwa>/<nazwa>_vN.docx` | kolejne wersje pisma; bieżąca = najwyższe `N` | skille pism |
| `legal/output/<nazwa>/_ZALACZNIKI.md` + kopie załączników | spis i kopie załączników z udziału `dokumentacja` | skille pism |
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

1. **Nowa wersja.** Weź najnowszą wersję `legal/output/<nazwa>/<nazwa>_vN.docx` (z ręcznymi zmianami autora w Wordzie)
   i utwórz `<nazwa>_v(N+1).docx` (`wersja_pisma.py nastepna`). W nowej wersji przyjmij zmiany śledzone, jeśli autor
   je zostawił (komentarze zostają); poprzednia wersja zostaje nietknięta. Wyjątek: redline kontrahenta albo innego
   autora w cudzym dokumencie wymaga osobnej decyzji użytkownika (`redline-docx-pl`). Plik otwarty w Wordzie
   (`~$` obok) - poproś autora o zamknięcie.
2. **Praca** odbywa się na kopiach w `_robocze/` (tekst, `edits.json`). Rundy pętli doskonalenia nie tworzą
   kolejnych wersji w `output/`: jedna sesja = jedna nowa wersja.
3. **Zmiany.** Zmiany sesji nanosisz na nową wersję bez śledzenia (`wersja_pisma.py zmien`: `adeu apply`
   i natychmiastowe przyjęcie, kontrola pominiętych edycji, pustych akapitów i tekstu). Nowa wersja to kopia
   poprzedniej z naniesionymi zmianami, nie nowy render z MD: render gubi ręczne zmiany autora w Wordzie.
4. **Teczka.** Skopiuj bieżącą wersję do `<sprawa>/pisma/<nazwa>.docx`.

Nowe pismo: pierwszą treść zapisz jako `drafty/<pismo>/rrrrMMdd_hhmm_<nazwa>_v1.md`, a DOCX wygenerowany z niej
jako `legal/output/<nazwa>/<nazwa>_v1.docx` (`wersja_pisma.py nowe`). Załączniki skopiuj z udziału `dokumentacja`
do folderu pisma i wypisz w `_ZALACZNIKI.md` (pismo bez załączników: „brak załączników”).

Raport porównania wersji dla autora (gdy o niego prosi): `adeu diff` dwóch wersji do `_robocze/`; to raport,
nie plik pisma.

### Redakcja zmian w DOCX

- Wstawka ma krój i rozmiar otaczającego tekstu (Georgia 10 pt według `FORMAT-PISMA.md`). Tekst wstawiony na
  początku akapitu nie dziedziczy formatowania i spada do domyślnej czcionki dokumentu (np. Aptos 12 pt);
  `zmien` nadaje mu czcionkę z sąsiedniego runu - nie omijaj tego kroku.
- Zmiany nie dodają pustych akapitów ani łamań wiersza; usunięcie akapitu usuwa też jego znacznik.
  `zmien` zatrzymuje się, gdy przybyło pustych akapitów.
- Punkty listy: numer, jedna spacja, tekst (`1. tekst`, `a) tekst`) - bez tabulatora i wcięcia wiszącego.
- Edycja dotyczy treści po etykiecie (`Stan protokołu:`, `Opuszczenie:`), żeby etykieta zachowała pogrubienie.

### Polecenia (skrypt `shared/format-pisma/wersja_pisma.py`, silnik adeu z `redline-docx-pl`)

Skrypt wykonuje kroki 1 i 3 oraz weryfikację; pomiń go tylko wtedy, gdy nie działa, i opisz przyczynę.
`<S>` to katalog `shared/` zainstalowanego pluginu.

```bash
# nowe pismo: v1.md -> legal/output/<nazwa>/<nazwa>_v1.docx
python3 -I <S>/format-pisma/wersja_pisma.py nowe --md <sprawa>/drafty/<pismo>/rrrrMMdd_hhmm_<nazwa>_v1.md --output legal/output
# krok 1: kopia najnowszej wersji jako _v(N+1), zmiany śledzone przyjęte w kopii (opcjonalnie snapshot MD)
python3 -I <S>/format-pisma/wersja_pisma.py nastepna --pismo legal/output/<nazwa> [--drafty <sprawa>/drafty/<pismo>]
# krok 3: zmiany sesji naniesione i przyjęte w nowej wersji (edits.json albo pełny tekst nowej wersji)
python3 -I <S>/format-pisma/wersja_pisma.py zmien --docx legal/output/<nazwa>/<nazwa>_v<N+1>.docx \
        --edits <sprawa>/_robocze/<katalog>/edits.json
# bramka końcowa katalogu output (kod 1 = naruszenie, napraw przed odpowiedzią)
python3 -I <S>/format-pisma/wersja_pisma.py sprawdz --output legal/output
```

`zmien` działa tylko na najnowszej wersji; starsze wersje są historią i się ich nie zmienia. Utworzenie wersji
i naniesienie zmian to kroki cyklu własnego pisma: nie wymagają potwierdzenia z tierów `redline-docx-pl`.

Stan końcowy dla jednego pisma: folder `legal/output/<nazwa>/` z wersjami `_v1` … `_vN`, najnowsza bez zmian
śledzonych, załączniki obecne zgodnie z `_ZALACZNIKI.md`; kopia `_vN` w `<sprawa>/pisma/<nazwa>.docx`.
Nie naruszaj innych pism, załączników ani dokumentów dostarczonych przez autora.

## Zakazy

- Pliki logu, recapu, „summary", „issues", raportu tury poza `_robocze/` - zamiast tego dopisek do pliku inkrementalnego.
- Katalogi `PRZEBIEG_*`, `RUN/`, `out/` w `analiza/` i `drafty/`. Katalog narzędzia: `_robocze/rrrrMMdd_<pismo>__<narzędzie>/`.
- Kopie „(2)", `_kopia`, `__dup`, `.md.md` - duplikaty się usuwa.
- Jakiekolwiek DOCX w `drafty/<pismo>/`, pliki `.md` w folderze pisma (poza `_*.md`), pismo luzem w korzeniu
  `legal/output/` i data w nazwie DOCX pisma.
- Zmiany śledzone (redline) we własnym piśmie; nadpisanie, usunięcie albo zmiana nazwy wcześniejszej wersji.

## Koniec przebiegu

1. Esencja z `_robocze/` jest w plikach inkrementalnych (ustalenia, decyzje, pytania, stan kotwic).
2. Nowe pliki poza `_robocze/`: nowa wersja `<nazwa>_vN.docx` w folderze pisma (+ ewentualnie snapshot `.md`
   i nowy plik inkrementalny z uzasadnieniem). `wersja_pisma.py sprawdz --output legal/output` daje `PASS`;
   w odpowiedzi podaj nazwę nowej wersji i liczbę naniesionych zmian z wyniku `zmien`.
3. `_PRZEBIEGI.md` ma wpis przebiegu; lekcje o ogólnej wartości trafiły do `_wiedza.md`.
4. Sprawa bez folderu (rozmowa bez plików): wynik w odpowiedzi, a pliki zakładaj dopiero na prośbę użytkownika.
