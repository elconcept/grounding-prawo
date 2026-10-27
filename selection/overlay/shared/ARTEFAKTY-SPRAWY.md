# ARTEFAKTY-SPRAWY - jakie pliki zostawia praca nad sprawą

Reguła kanoniczna dla każdego skilla, który analizuje akta, draftuje albo kontroluje pismo w teczce sprawy.
Cel: mało plików, pełny ślad. Kolejny przebieg niczego nie dubluje - dopisuje do plików, które już istnieją.

`<sprawa>` oznacza teczkę sprawy `legal/sprawy/<katalog_sprawy>/`. Używaj istniejącej teczki, nie zakładaj
drugiej kopii. Wspólny katalog odbioru to `legal/output/`; nazwa pliku musi identyfikować sprawę i pismo
(np. `II_W_1342_26_wniosek_o_sprostowanie_protokolu.docx`), aby identyczne tytuły w różnych sprawach nie nadpisywały się.

Pismo istnieje w dwóch miejscach i w dwóch formatach:
- `legal/output/<nazwa>.docx` - JEDEN plik pisma, **bez daty, godziny i `_vN` w nazwie**, przez cały czas życia pisma.
  Każda sesja pracuje na tym samym pliku: zmiany wchodzą do niego wyłącznie jako zmiany śledzone (redline).
  W `output/` model nie tworzy kolejnych wersji, kopii ani plików pośrednich, niczego nie usuwa i nie zmienia nazw;
- `<sprawa>/drafty/<pismo>/rrrrMMdd_hhmm_<nazwa>_vN.md` - snapshoty poprzednich stanów pisma (Markdown). Różnią się
  nazwą dzięki prefiksowi daty i godziny (`date +%Y%m%d_%H%M`) i sufiksowi `_vN`; nic nie jest nadpisywane.

Wersja `.md` w `output/`, DOCX z datą lub `_vN` w nazwie albo drugi DOCX tego samego pisma to błąd do naprawy
w tym samym przebiegu (przeniesienie przez `mv` do `<sprawa>/_robocze/rrrrMMdd_archiwum_output/`, nie usunięcie).

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
| **Wersja pisma (snapshot)** | `<sprawa>/drafty/<pismo>/rrrrMMdd_hhmm_<nazwa>_vN.md` | Stan pisma na początku sesji, po przyjęciu zmian śledzonych i ze zmianami autora. Każda sesja dodaje jeden snapshot z podbitym `vN` i rzeczywistą godziną. Tylko MD; w `drafty/` nie ma DOCX. |
| **DOCX pisma** | `legal/output/<nazwa>.docx` | Jeden plik na pismo przez całe jego życie, bez daty i `_vN`. Po sesji zawiera zmiany tej sesji jako zmiany śledzone. Bez sidecara `.md`, bez kopii i bez starszych wersji. |
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
| `drafty/<pismo>/rrrrMMdd_hhmm_<nazwa>_vN.md` | snapshot pisma z początku sesji; wszystkie wersje tworzą historię | skille pism |
| `legal/output/<nazwa>.docx` | jedyny DOCX pisma: stan z początku sesji + zmiany sesji jako zmiany śledzone | skille pism |
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

1. **Przyjęcie zmian w pliku pisma.** Weź `legal/output/<nazwa>.docx`. Niezaakceptowane zmiany śledzone (także
   propozycje DECYZJA_AUTORA z poprzedniej sesji, których autor nie odrzucił) przyjmij **w tym samym pliku**,
   z zachowaniem komentarzy (`wersja_pisma.py start`). Odrzucenie zmiany jest decyzją autora podejmowaną w Wordzie
   przed sesją; model nie pyta o nie ponownie. Wyjątek: redline kontrahenta albo innego autora w cudzym dokumencie
   wymaga osobnej decyzji użytkownika. Plik otwarty w Wordzie (`~$` obok) - poproś autora o zamknięcie.
2. **Snapshot.** Pełny tekst pliku po kroku 1 (ze wszystkimi ręcznymi zmianami autora) zapisz jako
   `<sprawa>/drafty/<pismo>/rrrrMMdd_hhmm_<nazwa>_vN.md`, z numerem o jeden wyższym od ostatniej wersji w katalogu
   i rzeczywistą godziną zapisu. Robi to `start`.
3. **Praca** odbywa się na kopiach w `_robocze/` (tekst, `edits.json`). Rundy pętli doskonalenia nie tworzą
   plików w `output/` ani kolejnych snapshotów: snapshot opisuje stan z początku sesji.
4. **Redline.** Zmiany sesji nakładasz na ten sam plik jako zmiany śledzone (`w:ins`/`w:del`) przez
   `wersja_pisma.py redline` (`adeu apply`). Plik w `output/` zostaje pod tą samą nazwą. Jeżeli zmian śledzonych
   nie da się utworzyć, etap jest NIEZAKOŃCZONY, a plik zostaje bez zmian. DOCX wygenerowany od nowa z MD
   (renderer, pandoc, python-docx) nie jest redline i nie może zastąpić pliku pisma.

Nowe pismo: pierwszą treść zapisz jako `drafty/<pismo>/rrrrMMdd_hhmm_<nazwa>_v1.md`, a DOCX wygenerowany z niej
(bez śledzenia zmian) jako `legal/output/<nazwa>.docx` (`wersja_pisma.py nowe`).

### Redakcja zmian w DOCX

- Wstawka ma krój i rozmiar otaczającego tekstu (Georgia 10 pt według `FORMAT-PISMA.md`). Tekst wstawiony na
  początku akapitu nie dziedziczy formatowania i spada do domyślnej czcionki dokumentu (np. Aptos 12 pt);
  `redline` nadaje mu czcionkę z sąsiedniego runu - nie omijaj tego kroku.
- Zmiany nie dodają pustych akapitów ani łamań wiersza; usunięcie akapitu usuwa też jego znacznik.
  `redline` zatrzymuje się, gdy po akceptacji przybyło pustych akapitów.
- Punkty listy: numer, jedna spacja, tekst (`1. tekst`, `a) tekst`) - bez tabulatora i wcięcia wiszącego.
- Edycja dotyczy treści po etykiecie (`Stan protokołu:`, `Opuszczenie:`), żeby etykieta zachowała pogrubienie.

### Polecenia (skrypt `shared/format-pisma/wersja_pisma.py`, silnik `redline-docx-pl`)

Skrypt wykonuje kroki 1, 2, 4 i weryfikację; pomiń go tylko wtedy, gdy nie działa, i opisz przyczynę.
`<S>` to katalog `shared/` zainstalowanego pluginu.

```bash
# nowe pismo: v1.md -> legal/output/<nazwa>.docx (renderer, nazwa bez daty i _vN)
python3 -I <S>/format-pisma/wersja_pisma.py nowe --md <sprawa>/drafty/<pismo>/rrrrMMdd_hhmm_<nazwa>_v1.md --output legal/output
# kroki 1-2: przyjęcie zmian w pliku pisma (komentarze zostają) i snapshot rrrrMMdd_hhmm_<nazwa>_vN.md
python3 -I <S>/format-pisma/wersja_pisma.py start --docx legal/output/<nazwa>.docx --drafty <sprawa>/drafty/<pismo>
# krok 4: zmiany sesji jako zmiany śledzone w tym samym pliku (edits.json albo pełny tekst nowej wersji)
python3 -I <S>/format-pisma/wersja_pisma.py redline --docx legal/output/<nazwa>.docx \
        --edits <sprawa>/_robocze/<katalog>/edits.json --author "Imię Nazwisko"
# bramka końcowa katalogu output (kod 1 = naruszenie, napraw przed odpowiedzią)
python3 -I <S>/format-pisma/wersja_pisma.py sprawdz --output legal/output
```

Autor zmian śledzonych to autor pisma (`podpis`), nie nazwa konta. Przyjęcie zmian na początku sesji i nałożenie
zmian na plik pisma to kroki cyklu własnego pisma: nie wymagają potwierdzenia z tierów `redline-docx-pl`.

Stan końcowy dla jednego pisma: w `<sprawa>/drafty/<pismo>/` wszystkie snapshoty `.md` i żadnego DOCX;
w `legal/output/` dokładnie jeden DOCX tego pisma, bez daty i `_vN` w nazwie, i żadnego `.md`. Nie naruszaj
innych pism, załączników ani dokumentów dostarczonych przez autora.

## Zakazy

- Pliki logu, recapu, „summary", „issues", raportu tury poza `_robocze/` - zamiast tego dopisek do pliku inkrementalnego.
- Katalogi `PRZEBIEG_*`, `RUN/`, `out/` w `analiza/` i `drafty/`. Katalog narzędzia: `_robocze/rrrrMMdd_<pismo>__<narzędzie>/`.
- Kopie „(2)", `_kopia`, `__dup`, `.md.md` - duplikaty się usuwa.
- Jakiekolwiek DOCX w `drafty/<pismo>/`, pliki `.md` w `legal/output/`, więcej niż jeden DOCX tego samego pisma w `legal/output/`
  oraz data lub `_vN` w nazwie DOCX pisma.
- Usuwanie, kopiowanie i zmiana nazwy pliku pisma w `legal/output/` w toku pracy; nowa wersja pisma jako nowy plik.

## Koniec przebiegu

1. Esencja z `_robocze/` jest w plikach inkrementalnych (ustalenia, decyzje, pytania, stan kotwic).
2. Nowe pliki poza `_robocze/`: snapshot `.md` w `drafty/<pismo>/` (+ ewentualnie nowy plik inkrementalny
   z uzasadnieniem). Plik pisma w `legal/output/` ten sam co na początku sesji, ze zmianami sesji jako redline.
   `wersja_pisma.py sprawdz --output legal/output` daje `PASS`; w odpowiedzi podaj liczbę `w:ins`/`w:del`
   z wyniku `redline`, a nie słowo „redline” bez liczb.
3. `_PRZEBIEGI.md` ma wpis przebiegu; lekcje o ogólnej wartości trafiły do `_wiedza.md`.
4. Sprawa bez folderu (rozmowa bez plików): wynik w odpowiedzi, a pliki zakładaj dopiero na prośbę użytkownika.
