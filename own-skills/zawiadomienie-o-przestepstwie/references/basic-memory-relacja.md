# Relacja w Basic Memory (baza danych sprawy)

Obowiązuje od v0.7. Relacja zdarzeń, log zeznań, rejestr pism i pytania otwarte są
prowadzone w Basic Memory, projekt `legal`, a nie w plikach katalogu sprawy ani w projekcie
claude.ai. Na dysku i w projekcie zostają tylko pisma (`.md` + `.docx`) i pliki inkrementalne
pism (`_PRZEBIEGI.md`, `_MAPA_KRZYWD.md`, `_HARDGATE.md`). Dostęp do serwera i zasady potwierdzania
zapisu: `shared/BASIC-MEMORY.md`. Projekt zawsze podawaj jawnie (`project="legal"`).

## Katalog autora

`relacje/<autor-slug>/` (slug z imienia i nazwiska autora relacji, bez polskich znaków,
np. `relacje/jan-kowalski/`). Jedna osoba ma jeden katalog, nawet gdy relacja obejmuje kilka spraw
i kilka pism. Relacja innej osoby (np. osoby bliskiej) ma własny katalog.

| Notatka | `note_type` | Zasada zapisu |
|---|---|---|
| `Relacja zdarzeń — <Autor>` | `relacja` | pełna narracja w 1. osobie według czasu zdarzeń; po każdej odpowiedzi redagowana w odpowiednim miejscu osi czasu (`write_note` z `overwrite=True` i `expected_checksum` albo `edit_note replace_section`); stałe ID `E001…`, bez renumeracji; frontmatter: `autor`, `wersja`, `status_wywiadu`, `ostatni_wpis_logu` |
| `Log zeznań — <Autor>` | `log_zeznan` | tylko dopisywany (`edit_note` `append` albo `insert_before_section "## Relacje"`); wpis jako obserwacja `- [rodzaj] Lnnn (Exxx) [rodzaj słownie]: treść — źródło #Snnn`; korekta to nowy wpis z odnośnikiem; wpisów nie usuwa się ani nie zmienia |
| `Rejestr pism — <Autor>` | `rejestr_pism` | obserwacje `- [Pn] pismo; ścieżka; epizody; STATUS (źródło statusu); organ; wersja relacji #status`; zmiana sekcji przy zmianie pisma |
| `Pytania otwarte — <Autor>` | `pytania_otwarte` | bieżąca lista wszystkich otwartych pytań z ID logu; pytanie zamknięte przenieś do sekcji „Zamknięte” z ID odpowiedzi |
| `Zgłoszenia — <Autor>` | `zgloszenia` | źródło prawdy o złożeniu: sekcja `## Złożone zawiadomienia` (wpis `- [Z001] data; organ; pismo; ścieżka; epizody E…; czyny; sygnatura; etap; źródło #Snnn`), tabela `## Zgłoszone czyny i sygnatury` (czyn, `Z-ID`, organ, sygnatura, etap, źródło), `## Postępowania przed sądem` (po odcięciu, `zgloszenia.md` §4a), `## Do ustalenia` (wzmianki bez wprost potwierdzonego złożenia). Wpisy nie są usuwane, zmiana = nowy wpis lub korekta. Zasady: `zgloszenia.md` §1–§2 |
| `wersje/…` | `relacja_wersja` | niezmienna kopia relacji na koniec sesji, przy przerwie i przed oddaniem pism; tytuł zawiera numer wersji i datę; pełny tekst albo bezstratna łatka wsteczna (`diff -u` od nowszej wersji) z sumą kontrolną źródła |
| `archiwum/…` | `archiwum` | dokumenty przeniesione z plików przy migracji (np. stare gałęzie pism, analizy), bez zmian treści |

Rodzaje wpisów logu (kategoria obserwacji): `nowy_epizod`, `szczegol`, `korekta`, `rozbieznosc`,
`brak_pamieci`, `brak_materialu`, `decyzja_autora`, `ustalenie_z_dokumentu`, `porzadkowanie`,
`pytanie_otwarte`, `skutek`. Sesje: `#S001`, `#S002`… Schematy notatek: `_schemat/` w `legal`
(`Schemat — relacja`, `Schemat — log zeznań`, `Schemat — rejestr pism`); kontrola `schema_validate`.

## Kolejność zapisu po każdej odpowiedzi autora

1. Wpis do logu (zawsze, także „nie pamiętam” i decyzje autora).
2. Redakcja relacji w miejscu osi czasu.
3. Aktualizacja pytań otwartych.
4. Rejestr pism, gdy zmienia się pismo albo jego status.
5. `Zgłoszenia`, gdy autor wprost mówi o złożeniu, dacie, organie, sygnaturze, etapie albo decyzji organu sądu.
6. Potwierdzenie odczytem (`read_note`, co najmniej `include_content=False` i checksum).

Odpowiedzi zbiorcze (autor wkleja listę odpowiedzi z ID) zapisuj jako osobne wpisy logu.
Etykieta podana przez autora może nie pasować do pytania: przypisz odpowiedź po treści i zapisz to w wpisie.

## Gdy Basic Memory jest niedostępna

Nie twórz zastępczej relacji w plikach sprawy. Zapisz odpowiedź autora i proponowane zmiany
w `_robocze/pamiec-zalegle.md` folderu sprawy (projekt, tytuł notatki, treść) i w odpowiedzi
podaj `NIEZAPISANE` z przyczyną. Przy następnym wejściu najpierw uzupełnij bazę i usuń zaległość.
Poza repo/katalogiem sprawy i bez Basic Memory podaj Markdown do zapisu, jasno informując, że nic
nie zapisano (`references/ciaglosc-sesji.md`).

## Wejście i wyszukiwanie

- Start: `list_directory(project="legal", dir_name="relacje")`, potem `read_note` relacji, logu,
  rejestru i pytań autora.
- Kontekst: `build_context(project="legal", url="relacje/<autor-slug>/*")`.
- Korekty i rozbieżności: `search_notes(project="legal", note_types=["log_zeznan"], categories=["korekta"])`.
- Lokalna procedura projektu (gdy istnieje): `_metodologia/Workflow — relacja pokrzywdzonego i zawiadomienia`.
- Zgłoszenia: `read_note` `Zgłoszenia — <Autor>`; przy braku notatki albo braku któregokolwiek z pięciu plików
  systemu najpierw poproś o złożone zawiadomienia i dopiero potem twórz brakujące (`zgloszenia.md` §6).
- Schemat `Schemat — zgłoszenia` w `_schemat/` (`legal`): utwórz, gdy brak, przed pierwszym zapisem zgłoszeń; kontrola `schema_validate`.

## Migracja z plików (`relacja/_RELACJA_ZDARZEN.md`, `_LOG_ZEZNAN.md`, `_REJESTR_PISM.md`, `wersje/`)

1. Przenieś relację, log (każdy wiersz jako obserwacja, treść bez zmian), rejestr i wszystkie wersje.
2. Sprawdź kompletność: log z pliku jest prefiksem logu w bazie, ostatnie ID się zgadza; wersje mają sumy kontrolne.
3. Dokumenty jedyne w swoim rodzaju (gałęzie pism, analizy, handoffy) przenieś do `archiwum/` albo teczki sprawy.
4. Dopiero po odczycie potwierdzającym usuń pliki relacji z dysku i z projektu; pisma zostają.
5. Zapisz migrację jako wpis logu `porzadkowanie`.
