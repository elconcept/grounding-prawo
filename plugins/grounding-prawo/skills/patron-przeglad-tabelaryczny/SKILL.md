---
name: patron-przeglad-tabelaryczny
description: Masowa ekstrakcja danych z pakietu dokumentów (umowy, NDA, SPA, najmy, umowy o pracę, kredytowe, korespondencja) do tabeli - kolumna po kolumnie, z cytatem i stroną w każdej komórce oraz flagą ryzyka - i eksport do CSV/Excela. Użyj, gdy trzeba przejrzeć wiele dokumentów według tych samych pytań, zrobić due diligence, change of control review albo zestawienie warunków umów.
---

## Pamięć sesji — przed pracą i przed odpowiedzią końcową

Przeczytaj `shared/BASIC-MEMORY.md` i `shared/ZASADY-PLUGINU.md`. Na wejściu odczytaj kontekst sprawy z projektu `legal`; przed odpowiedzią końcową zapisz lub zaktualizuj recap tej sesji w projekcie `main` i sprawdź odczytem zapis. Nowe dokumenty i ustalenia zapisuj w `legal` po każdym zakończonym etapie. Podaj status pamięci i identyfikator notatki; nie zgłaszaj zapisu bez potwierdzenia MCP.

# Przegląd tabelaryczny

Ścieżki względem katalogu tego skilla. Skrypty: `scripts/doc_to_text.py` (tekst ze znacznikami
stron), `scripts/tabular_to_csv.py` (składanie tabeli). Szablony kolumn:
`references/szablony-kolumn.json`.

## 1. Kolumny
Szablony (id - liczba kolumn): `coc-dd` Change of Control (8), `commercial-agreement` (18),
`credit-agreement` (21), `ediscovery` (7), `supply-agreement` (14), `spa` (13), `nda` (9),
`commercial-lease` (20), `lpa` (20), `shareholder-agreement` (20), `employment-agreement` (16).

```bash
python3 -c "import json,sys; print(json.dumps(next(w for w in json.load(open('references/szablony-kolumn.json')) if w['id']==sys.argv[1]), ensure_ascii=False, indent=1))" nda
```

Prompty szablonów są po angielsku i pod common law (np. security of tenure, liquidated damages).
Przy umowach polskich dostosuj pytania przed uruchomieniem (kara umowna, prawo właściwe,
sąd polubowny, wypowiedzenie z kodeksu cywilnego itd.).

Własna kolumna: `{"index": N, "name": "...", "format": "...", "prompt": "..."}`, dla formatu
`tag` także `"tags": [...]`. Prompt kolumny opisuje tylko CO wyciągnąć, nigdy JAK sformatować
odpowiedź - format dokleja się osobno (tabela niżej). Zapisz kolumny do `kolumny.json`
(lista albo obiekt z polem `kolumny`).

## 2. Tekst dokumentów
```bash
python3 scripts/doc_to_text.py teczka/*.pdf teczka/*.docx teczka/*.md --out-dir teksty/
```
Numer strony w cytacie to kolejny `[Page N]`, nie numer ze stopki dokumentu.

Markdown po OCR (odczyt-dokumentow, Chandra/Datalab, LlamaParse) jest przyjmowany bezpośrednio: strony
rozpoznawane po `## Page N`, `[Page N]`, `<!-- page N -->`, `{N}------` i `\f`, frontmatter (poza pluginem)
pomijany. Przy parze `umowa.pdf` + `umowa.md` brany jest `.md` (`--no-md` wyłącza). Plik bez
znaczników stron to jedna strona (skrypt ostrzega); własny separator: `--page-sep hr` albo regex.

## 3. Ekstrakcja - jeden dokument naraz
Przeczytaj `teksty/<dokument>.txt` i dla wszystkich kolumn zapisz do `wyniki/<dokument>.jsonl`
po jednej linii JSON na kolumnę (minifikowany obiekt, w kolejności kolumn):

```
{"document": "<plik>", "column_index": N, "column": "<nazwa>", "summary": "...", "flag": "green|grey|yellow|red", "reasoning": "..."}
```

- `summary`: sama wyciągnięta wartość, a po każdym twierdzeniu faktycznym cytat
  `[[page:N||quote:dosłowny fragment do 25 słów]]`. Bez wyjaśnień. Cytat wąski - tylko słowa
  wspierające twierdzenie; nie używaj jednego długiego cytatu dla kilku twierdzeń.
- Brak informacji: „Not Found” (albo „Brak w dokumencie”), flaga `grey`.
- `flag`: green - standardowe/korzystne, yellow - wymaga uwagi, red - problematyczne/niekorzystne,
  grey - neutralne/brak.
- `reasoning`: krótkie uzasadnienie; może zawierać cytaty. Markdown w wartościach dozwolony
  (nowa linia jako `\n`).

| format | `summary` |
|---|---|
| text | tekst z cytatami |
| bulleted_list | wyłącznie lista markdown, każdy punkt od `* ` |
| number | jedna liczba, bez jednostek |
| percentage | jedna wartość, np. 42% |
| monetary_amount | kwota z walutą, np. 1 234,56 zł |
| currency | kody walut w `[[...]]`, np. `[[PLN]]` |
| yes_no | `[[Yes]]` albo `[[No]]`; cytat uzasadniający w `reasoning` |
| date | sama data (1 stycznia 2024 r.; zakres - dwie daty); cytat w `reasoning` |
| tag | dokładnie jeden tag z listy w `[[...]]`; cytat w `reasoning` |

Ekstrakcja nie wymaga głębokiego rozumowania. Przy więcej niż kilku dokumentach deleguj ją do
subagentów - po jednym na dokument, z tańszym modelem - przekazując ścieżkę tekstu,
`kolumny.json`, powyższe reguły i ścieżkę pliku JSONL. Jedno przejście obejmuje do ~120 000
znaków; dłuższy dokument dziel na części i scal wyniki (wartość z cytatem ma pierwszeństwo
przed „Not Found”).

## 4. Kontrola cytatów
```bash
python3 ../patron-weryfikacja-cytatow/scripts/verify_citations.py wyniki/<dokument>.jsonl --tabular --source teksty/<dokument>.txt
```
Komórkę z cytatem NIEZWERYFIKOWANY popraw albo zmień jej flagę na yellow z adnotacją
w `reasoning`.

## 5. Tabela
```bash
python3 scripts/tabular_to_csv.py wyniki/*.jsonl --columns kolumny.json -o przeglad.csv
python3 scripts/tabular_to_csv.py wyniki/*.jsonl --columns kolumny.json --markdown --plain -o przeglad.md
```
CSV ma BOM UTF-8 (Excel poprawnie pokaże polskie znaki). `--with-reasoning` dodaje kolumny
uzasadnień, `--plain` usuwa znaczniki cytatów.

W czacie podsumuj: dokumenty z flagami red i yellow i dlaczego; kolumny z największą liczbą
„Not Found”. Tabela to materiał do przeglądu przez prawnika - czerwone i żółte komórki oraz te
z niezweryfikowanym cytatem wymagają przeczytania fragmentu źródłowego.

---
Źródło: Patron (MateMatic Solutions, AGPL-3.0) - `backend/src/routes/tabular.ts`
(EXTRACTION_SYSTEM, formatPromptSuffix, queryTabularAllColumns),
`frontend/src/app/components/workflows/builtinWorkflows.ts`, `lib/tabular/grounding.ts`
(ADR-0010, ADR-0080).

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** wiele dokumentów tego samego rodzaju (umowy, korespondencja) po OCR
- **Wynik zapisz w:** tabela CSV/Excel w `_robocze/`; esencja i flagi ryzyka w `analiza/_dokumenty.md` (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `chronologia-sprawy-v1`, `analizator-umow-v1`, `case-risk`
- **Basic Memory (`legal`):** czytaj teczkę sprawy (`build_context`) i notatki wiki po sygnaturze i nazwiskach; zapisz stan sprawy i terminy w teczce, nowe fakty z akt zgłoś do ingestu (protokół: `shared/BASIC-MEMORY.md`)
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
