# Relacja w repozytorium `elconcept/legal` (katalog `relacje/`)

Relacja zdarzeń, log zeznań, rejestr pism, pytania otwarte i lista zgłoszeń są plikami Markdown w repozytorium
GitHub **`elconcept/legal`**, w katalogu **`relacje/` w korzeniu projektu**. Zastępuje to dawny zapis w Basic Memory.
Na dysku sprawy i w projekcie claude.ai zostają tylko pisma (`.md` + `.docx`) i pliki inkrementalne pism
(`_PRZEBIEGI.md`, `_MAPA_KRZYWD.md`, `_HARDGATE.md`).

## 1. Dostęp: sprawdź przed pierwszym pytaniem, w tej kolejności

1. **Integracja z GitHub.** Sprawdź, czy masz działający dostęp do `elconcept/legal`: narzędzia GitHub MCP
   (np. odczyt pliku i zapis pliku w repo) albo `gh` (`gh auth status`, potem
   `gh api repos/elconcept/legal --jq '.permissions.push'`). Użyj pierwszej działającej drogi.
   Zapis wymaga uprawnienia `push`; sam odczyt to dostęp ograniczony (traktuj jak brak zapisu).
2. **Lokalna kopia repo** (tylko gdy punkt 1 zawiódł). Znajdź katalog, w którym `git remote -v` wskazuje
   `elconcept/legal` (bieżący katalog i jego rodzice, `legal/` obok repo pluginu, `/workspace/legal`).
   Przed pracą `git pull --rebase`; po zapisie commit i `git push`, gdy zdalny dostęp działa; bez niego commit
   zostaje lokalnie i powiedz o tym autorowi.
3. **Brak jednego i drugiego.** Powiedz autorowi wprost, **zanim zadasz pierwsze pytanie**:
   - nie masz dostępu do istniejących relacji, logu, rejestru pism ani listy zgłoszeń z repozytorium `elconcept/legal`;
   - dlatego nie możesz wznowić wcześniejszej relacji, sprawdzić, co zostało złożone, ani wykonać AUDYTU-B względem
     zapisanych wcześniej zeznań; pracujesz tylko na tym, co autor poda w tej rozmowie;
   - prosisz o wklejenie istniejącej relacji i wszystkich złożonych zawiadomień (jeśli są);
   - wynik oddasz jako Markdown do zapisania, oznaczony `NIEZAPISANE`, z nazwami plików.
   Nie twórz pozoru kontynuacji i nie wymyślaj zawartości plików, których nie przeczytałeś.

Tryb dostępu (GitHub / lokalna kopia / brak) podaj autorowi jednym zdaniem na początku sesji.

## 2. Katalog autora

`relacje/<autor-slug>/` (slug z imienia i nazwiska autora relacji, bez polskich znaków, np. `relacje/jan-kowalski/`).
Jedna osoba ma jeden katalog, nawet gdy relacja obejmuje kilka spraw i pism. Relacja innej osoby (np. osoby bliskiej)
ma własny katalog. Nie zakładaj slugu z pamięci: wylistuj `relacje/` i dopasuj istniejący katalog.

| Plik | Zasada zapisu |
|---|---|
| `relacja-zdarzen.md` | pełna narracja w 1. osobie według czasu zdarzeń; po każdej odpowiedzi redagowana w odpowiednim miejscu osi czasu (nadpisanie pliku z aktualnym `sha`); stałe ID `E001…`, bez renumeracji; nagłówek YAML: `typ: relacja`, `autor`, `wersja`, `status_wywiadu`, `ostatni_wpis_logu` |
| `log-zeznan.md` | tylko dopisywany (odczyt, dopisek na końcu lub w sekcji sesji, zapis z `sha`); wpis jako linia `- [rodzaj] Lnnn (Exxx) [rodzaj słownie]: treść — źródło #Snnn`; korekta to nowy wpis z odnośnikiem; wpisów nie usuwa się ani nie zmienia |
| `rejestr-pism.md` | linie `- [Pn] pismo; ścieżka; epizody; STATUS (źródło statusu); organ; wersja relacji #status`; zmiana sekcji przy zmianie pisma |
| pytania otwarte | **konwencja repo `legal` (`reguly/RELACJE.md`):** otwarte pytania wszystkich autorów są w jednym pliku `DO_DECYZJI.md` w korzeniu repo, pogrupowane, z ID z logu; nowe pytanie dopisujesz tam. Odpowiedź autora zapisz dosłownie w logu, a pytanie przenieś z datą do `relacje/PYTANIA_ZAMKNIETE.md` (pytań nie usuwasz). Gdy repo nie ma `DO_DECYZJI.md`, prowadź `relacje/<autor-slug>/pytania-otwarte.md` (sekcja „Zamknięte” z ID odpowiedzi). Pytanie to pełne zdanie ze znakiem zapytania, które nazywa osobę, zdarzenie, datę i to, czego brakuje, tak by autor odpowiedział bez sięgania do akt |
| `zgloszenia.md` | źródło prawdy o złożeniu: `## Złożone zawiadomienia` (wpis `- [Z001] data; organ; pismo; ścieżka; epizody E…; czyny; sygnatura; etap; źródło #Snnn`), tabela `## Zgłoszone czyny i sygnatury`, `## Postępowania przed sądem` (po odcięciu, `zgloszenia.md` §4a), `## Do ustalenia`. Wpisy nie są usuwane, zmiana = nowy wpis lub korekta. Zasady: `references/zgloszenia.md` §1–§2 |
| `wersje/RRRRMMDD_relacja_vN.md` | niezmienna kopia relacji na koniec sesji, przy przerwie i przed oddaniem pism; kolejny wolny numer `N` (także przy kilku sesjach dziennie); pełny tekst albo bezstratna łatka wsteczna (`diff -u`) z sumą kontrolną źródła |
| `archiwum/…` | dokumenty przeniesione przy migracji (stare gałęzie pism, analizy), bez zmian treści |

Każdy plik główny zaczyna się nagłówkiem YAML z `typ` (`relacja`, `log_zeznan`, `rejestr_pism`,
`pytania_otwarte`, `zgloszenia`), `autor` i `zaktualizowano` (data). Nie ma zewnętrznego schematu ani walidatora:
sprawdź ręcznie, że plik ma nagłówek YAML i oczekiwane sekcje.

Rodzaje wpisów logu: `nowy_epizod`, `szczegol`, `korekta`, `rozbieznosc`, `brak_pamieci`, `brak_materialu`,
`decyzja_autora`, `ustalenie_z_dokumentu`, `porzadkowanie`, `pytanie_otwarte`, `skutek`. Sesje: `#S001`, `#S002`…

## 3. Operacje na plikach

- **Odczyt:** GitHub MCP (odczyt zawartości pliku) albo `gh api repos/elconcept/legal/contents/<ścieżka>`
  (zwraca `sha`), albo `cat` w lokalnej kopii.
- **Zapis przez GitHub:** utwórz lub zaktualizuj plik z komunikatem commita; przy aktualizacji podaj `sha`
  odczytanego pliku. Błąd 409/422 (zmieniony `sha`) = ktoś zapisał w międzyczasie: odczytaj ponownie, scal,
  zapisz. Przy kilku plikach naraz użyj jednego commita (np. `push_files`), jeśli narzędzie to umożliwia.
- **Zapis lokalny:** `git pull --rebase`, edycja, `git add relacje/<autor-slug>`, `git commit`, `git push`.
  Commituj tylko `relacje/<autor-slug>/`, nie cudze zmiany w innych katalogach.
- **Komunikat commita:** `relacje/<autor-slug>: <co> (#Snnn)`, np. `relacje/jan-kowalski: log, relacja E007 (#S004)`.
- **Potwierdzenie:** po zapisie odczytaj plik (lub `git show HEAD --stat`) i sprawdź, że ostatni wpis logu i `sha`
  się zgadzają. Nie deklaruj zapisu bez odczytu potwierdzającego.
- **Wyszukiwanie korekt i rozbieżności:** w `log-zeznan.md` szukaj linii z `[korekta]` i `[rozbieznosc]`
  (`grep -n '\[korekta\]\|\[rozbieznosc\]'` w lokalnej kopii albo wyszukiwanie kodu GitHub).

## 4. Kolejność zapisu po każdej odpowiedzi autora

1. Wpis do `log-zeznan.md` (zawsze, także „nie pamiętam” i decyzje autora).
2. Redakcja `relacja-zdarzen.md` w miejscu osi czasu.
3. Aktualizacja pytań otwartych (`DO_DECYZJI.md` albo `pytania-otwarte.md`, §2).
4. `rejestr-pism.md`, gdy zmienia się pismo albo jego status.
5. `zgloszenia.md`, gdy autor wprost mówi o złożeniu, dacie, organie, sygnaturze, etapie albo decyzji organu.
6. Potwierdzenie odczytem.

Odpowiedzi zbiorcze (autor wkleja listę odpowiedzi z ID) zapisuj jako osobne wpisy logu. Etykieta podana przez autora
może nie pasować do pytania: przypisz odpowiedź po treści i zapisz to we wpisie. Zapisy łącz w jeden commit na odpowiedź
(albo na kilka odpowiedzi, gdy autor odpowiada serią), nie rzadziej niż przy przerwie i końcu sesji.

## 5. Gdy zapis się nie powiedzie

Nie twórz zastępczej relacji w plikach sprawy. Zapisz odpowiedź autora i proponowane zmiany w
`<sprawa>/_robocze/relacje-zalegle.md` (plik, treść do dopisania), w odpowiedzi podaj `NIEZAPISANE` z przyczyną
(brak sieci, brak uprawnień, konflikt). Przy następnym wejściu najpierw uzupełnij repozytorium i usuń zaległość.
Poza repo i teczką sprawy podaj Markdown do zapisania z nazwami plików, jasno informując, że nic nie zapisano.

## 6. Wejście i wyszukiwanie

- Start: wylistuj `relacje/`, wskaż katalog autora, odczytaj `relacja-zdarzen.md`, `log-zeznan.md`,
  `rejestr-pism.md`, `zgloszenia.md` oraz pytania otwarte autora z `DO_DECYZJI.md` (albo `pytania-otwarte.md`).
- Brak któregokolwiek z plików głównych albo brak `zgloszenia.md`: najpierw poproś o złożone zawiadomienia
  i dopiero potem twórz brakujące (`references/zgloszenia.md` §6).
- Zastane pliki w `relacje/<autor-slug>/` w starym układzie (np. `20261113_relacja_….md`, odpowiedzi na rundy pytań)
  są materiałem wejściowym: przeczytaj, zaimportuj do logu jako wpis „import zastanej relacji” i **nie usuwaj ich**
  (historia git jest kopią zapasową). Przeniesienie do `archiwum/` tylko na prośbę autora.

## 7. Migracja z plików awaryjnych (`relacja/_RELACJA_ZDARZEN.md`, `_LOG_ZEZNAN.md`, `_REJESTR_PISM.md`, `wersje/`)

1. Przenieś relację, log (każdy wiersz jako wpis, treść bez zmian), rejestr i wszystkie wersje do `relacje/<autor-slug>/`.
2. Sprawdź kompletność: log przeniesiony jest prefiksem logu docelowego, ostatnie ID się zgadza; wersje mają sumy kontrolne.
3. Dokumenty jedyne w swoim rodzaju (gałęzie pism, analizy, handoffy) przenieś do `archiwum/` albo teczki sprawy.
4. Dopiero po odczycie potwierdzającym usuń pliki awaryjne z teczki sprawy; pisma zostają.
5. Zapisz migrację jako wpis logu `porzadkowanie`.
