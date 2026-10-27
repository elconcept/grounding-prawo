# the-ocr

**Uwaga na integracje:** główne polecenie `the-ocr` zachowuje oryginalny
interfejs i tryb działania. Obsługuje PDF, JPG, JPEG i PNG, a dotychczasowe
flagi (`-o`, `--markdown`, `--json`, `--keep-geometry`, `--archive`,
`--from-json`, `--force-provider` itd.) mają poprzednią semantykę.
Domyślne uruchomienie `the-ocr dokument.pdf` **nie zostało zmienione**
— nadal tworzy przeszukiwalny PDF według poprzedniego kontraktu.

**Tylko ingest do wiki Basic Memory** używa osobnej komendy
`the-ocr-ingest-page`, której wejściem jest wyłącznie PDF i która zapisuje
kandydat Markdown jednej strony. Nie ma automatycznego przechodzenia
do kolejnej strony — ocenę wykonuje LLM.

```bash
the-ocr skan.jpg                         # stary interfejs bez zmian
the-ocr dokument.pdf --markdown          # stary interfejs bez zmian
the-ocr-ingest-page akta.pdf --page 1 --force-provider google_vision
the-ocr-ingest-page akta.pdf --page 2 --force-provider datalab
the-ocr-ingest-page akta.pdf --page 2 --fixme
the-ocr-ingest-page akta.pdf --searchable-pdf --from-json reviewed.json
```

Szczegóły workflow modelu: [docs/INGEST-LLM.md](docs/INGEST-LLM.md).

Prywatny pipeline OCR dla polskich dokumentów. Z PDF albo obrazu robi **wierny przeszukiwalny PDF A4**,
a na życzenie także Markdown i kanoniczny JSON z bboxami. Rozpoznają tekst zewnętrzni providerzy
(Datalab, LlamaParse, Azure Document Intelligence, Google Cloud Vision; opcjonalnie lokalny RapidOCR),
warstwę tekstu stawia OCRmyPDF 17 przez własny silnikowy plugin. Ten plik jest jedynym aktualnym opisem
projektu; `Resources/` to wyłącznie materiały referencyjne i historyczne.

Używają go: CLI `the-ocr`, Paperless-ngx (`paperless-stack`, parser `paperless_theocr`), serwer
REST/MCP `elconcept/mcp-ocr` (submoduł) i plugin `grounding-prawo` (skill `odczyt-dokumentow`).

## Przebieg

```text
wejście PDF / JPG / PNG
  -> [--archive] kopia oryginału do archiwum (krok 0, także gdy OCR zawiedzie)
  -> przygotowanie stron
       PDF: usunięcie starej niewidzialnej warstwy OCR (Tr 3, także w Form XObject),
            wektorowe dopasowanie stron do A4 (bez rasteryzacji)
       obraz: obrót wg EXIF, proporcjonalnie na stronę A4
  -> łańcuch providerów: Datalab -> LlamaParse -> Azure DI -> Google Vision (pierwszy poprawny wynik wygrywa)
  -> kanoniczny dokument (doc-intel-contract-pl 1.2.0) + geometria słów
  -> OCRmyPDF --mode redo + plugin the-ocr (generate_ocr, renderer fpdf2): warstwa tekstu na oryginalnych stronach
  -> kontrola: liczba stron, tekst do wyciągnięcia, >= 80% słów providera w PDF
  -> publikacja atomowa z rollbackiem: <stem>.pdf [+ <stem>.md, <stem>.json]
```

Tesseract nie rozpoznaje tekstu; jego binarka musi istnieć tylko dlatego, że sprawdza ją OCRmyPDF.
Żadne współrzędne słów nie są wymyślane: blok z ramką, ale bez słów, trafia do warstwy całym tekstem
w swojej ramce; blok bez geometrii trafia tylko do JSON/Markdown (`gating.ungroundable`).

## Instalacja i uruchomienie

Wymagania: Python 3.11+, binarki `tesseract` i `gs` (Ghostscript) na PATH.

```bash
uv sync                       # albo: pip install .        (lokalny RapidOCR: pip install ".[local]")
uv run the-ocr dokument.pdf                    # PDF nadpisany w miejscu (wynik zweryfikowany przed podmianą)
uv run the-ocr skan.jpg                        # skan.pdf obok obrazu, obraz zostaje
uv run the-ocr dokument.pdf -o wynik/ocr.pdf   # wejście nietknięte
uv run the-ocr dokument.pdf --markdown --json  # dodatkowo .md i .json obok PDF
uv run the-ocr dokument.pdf --archive          # kopia oryginału przed OCR
uv run the-ocr dokument.pdf --keep-geometry    # bez dopasowania do A4
uv run the-ocr dokument.pdf --force-provider azure   # tylko jeden provider (diagnostyka)
uv run the-ocr dokument.pdf --words            # JSON z edytowalnymi słowami (do poprawek)
uv run the-ocr dokument.pdf --from-json dokument.json  # warstwa z poprawionego JSON, bez OCR
```

Gotowa binarka (bez Pythona) jest w [wydaniach](#wydania-binarne); na hoście autora `the-ocr` jest na PATH
([niżej](#instalacja-binarki-na-hoście)).

## Flagi CLI

| Flaga | Działanie |
|---|---|
| `INPUT` | PDF, JPG, JPEG lub PNG |
| `-o`, `--output PLIK` | PDF wynikowy w innym miejscu; wejście nietknięte |
| `--json` | dodatkowo `<wynik>.json` (kanoniczny JSON kontraktu) |
| `--words` | jak `--json`, ale z edytowalną geometrią słów `blocks[].words[]` - wejście dla `--from-json` |
| `--from-json PLIK` | **żaden provider OCR nie jest wywoływany**: warstwa tekstu powstaje z (poprawionego) JSON ze słowami ([niżej](#poprawki-ręczne-bez-ponownego-ocr---from-json)) |
| `--archive` | kopia oryginału przed OCR do `$THE_OCR_ARCHIVE_DIR` albo `~/archive`; obraz wejściowy usuwany po sukcesie |
| `--archive-dir KATALOG` | jak `--archive`, do wskazanego katalogu |
| `--keep-geometry` | bez dopasowania stron do A4 |
| `--layer auto\|redo\|skip\|force` | tryb warstwy OCRmyPDF (niżej); domyślnie `auto` |
| `--force-provider NAZWA` | tylko ten provider: `datalab`, `llamaparse`, `azure`, `google_vision`, `rapidocr` (aliasy: `azure-di`, `google-vision`); wyklucza się z `--from-json` |
| `--optimize 0\|1\|2\|3` | `--optimize` OCRmyPDF; domyślnie `1` ([niżej](#flagi-ocrmypdf)) |
| `--clean-final` | `--clean-final` OCRmyPDF; tylko z `--layer force` |
| `--pdfa` | wynik jako PDF/A-2b (`--output-type pdfa` OCRmyPDF) |

Kody wyjścia: `0` sukces, `1` błąd wejścia/zapisu/flag albo wadliwy JSON dla `--from-json`, `2` żaden provider nie dał wyniku (wejście nietknięte;
przy `--archive` kopia zostaje w archiwum). Kolejne próby providerów są wypisywane na stderr.

## Tryby warstwy tekstu (`--layer`)

| Tryb | OCRmyPDF | Skutek |
|---|---|---|
| `auto` | `redo`, a dla PDF z formularzem AcroForm `skip` | domyślnie: oryginalna treść stron bez rasteryzacji |
| `redo` | usuwa starą warstwę OCR, zachowuje wektory i widoczny tekst | wymiana wadliwego OCR |
| `skip` | strony z tekstem zostają bez zmian | PDF mieszane (natywne + skany) |
| `force` | **rasteryzuje** każdą stronę, potem warstwa | tylko świadomie: wektory i tekst natywny stają się obrazem |

## Poprawki ręczne bez ponownego OCR (`--from-json`)

```bash
the-ocr pismo.pdf --words                  # 1. OCR; obok pismo.json ze słowami (blocks[].words[])
#                                            2. poprawić w pismo.json words[].text (i text bloku dla .md)
the-ocr pismo.pdf --from-json pismo.json   # 3. nowa warstwa z JSON; żaden provider nie jest wołany
```

`--from-json` przygotowuje strony tak samo jak zwykły przebieg (usunięcie starej warstwy, A4), wczytuje JSON
(`OCRDocument.from_dict`: schemat, liczba stron, bboxy w `0..1`, słowa w ramce bloku) i stawia warstwę przez
OCRmyPDF. Można go uruchamiać na już przetworzonym PDF (stara warstwa jest usuwana) albo na oryginale - ważne,
by użyć tych samych `--keep-geometry` co przy pierwszym OCR, bo bboxy są względne wobec przygotowanej strony.
Działają z nim `-o`, `--markdown`, `--json` (zapisuje JSON ze słowami, więc nie gubi poprawek), `--layer`,
`--optimize`, `--clean-final`, `--pdfa`, `--archive`. Błędny JSON = kod `1` i wejście nietknięte.
Tak samo robi `reapply` w mcp-ocr.

## Flagi OCRmyPDF

Warstwę stawia OCRmyPDF, ale **rozpoznawanie robi provider przed OCRmyPDF** na przygotowanych stronach,
więc dostępne są tylko opcje, które nie przesuwają treści strony względem bboxów providera:

| Flaga OCRmyPDF | W the-ocr | Uwagi |
|---|---|---|
| `--mode force/redo/skip` | `--layer` | patrz [tryby](#tryby-warstwy-tekstu---layer) |
| `--optimize 0-3` | `--optimize` | `1` (domyślnie) bezstratnie; `2`/`3` stratnie, potrzebują `pngquant` i `jbig2enc` (bez nich OCRmyPDF pomija ten krok) |
| `--clean-final` | `--clean-final` | obraz strony po `unpaper` (domyślne argumenty OCRmyPDF: bez prostowania i przesuwania treści); wymaga `--layer force` (OCRmyPDF odrzuca go z `redo`) i binarki `unpaper` |
| `--output-type pdfa` | `--pdfa` | PDF/A-2b |
| `--clean` | brak | czyści tylko obraz dla Tesseracta, który tu nie działa - bez efektu |
| `--deskew`, `--rotate-pages`, `--remove-background` | brak | obracają/zmieniają obraz po OCR providera, więc warstwa rozjechałaby się z tekstem; `redo` ich nie przyjmuje |
| `--language`, `--tesseract-*`, `--sidecar`, `--jobs` itp. | brak | dotyczą Tesseracta albo są ustawione na stałe |

Inne potrzeby: `the_ocr.pdf.searchable_pdf.build_document_searchable_pdf(..., mode=, optimize=, clean_final=, pdfa=)`.

## Konfiguracja

Zmienne procesu mają pierwszeństwo. Potem czytany jest **pierwszy znaleziony** plik `.env`:

1. `$THE_OCR_ENV_FILE` (jawna ścieżka),
2. `.env` obok binarki (wydanie) albo w katalogu uruchomienia (uruchomienie ze źródeł),
3. `~/.config/the-ocr/.env` (`$XDG_CONFIG_HOME/the-ocr/.env`; Windows: `%APPDATA%\the-ocr\.env`).

Ścieżki względne w `.env` (np. `GOOGLE_VISION_CREDENTIALS`) liczą się od katalogu, w którym naprawdę leży ten
`.env` - dowiązanie symboliczne jest rozwiązywane, więc `.env` podlinkowany do repo widzi `.secrets/` repo.
Wzór: `env.example`. W tym prywatnym repo prawdziwe klucze są
świadomie w `.env` i `.secrets/` (synchronizacja między hostami autora; darmowe tiery).

| Zmienna | Znaczenie |
|---|---|
| `DATALAB_API_KEY` (albo `DATALAB_API_KEY_EU`/`_US`), `DATALAB_REGION_ORDER`, `DATALAB_API_URL[_EU/_US]` | Datalab |
| `LLAMA_CLOUD_API_KEY` (albo `_EU`/`_US`), `LLAMA_CLOUD_REGION_ORDER`, `LLAMA_CLOUD_REGION`, `LLAMA_CLOUD_BASE_URL[_EU/_US]` | LlamaParse |
| `AZURE_DOCUMENT_ENDPOINT` + `AZURE_DOCUMENT_KEY`, albo `AZURE_DOCUMENT_RESOURCE` [+ `AZURE_DOCUMENT_RESOURCE_GROUP`] z zalogowanym `az` | Azure DI |
| `AZURE_DOCUMENT_PAGES_PER_REQUEST` | stron na żądanie Azure (domyślnie 2 = limit F0) |
| `GOOGLE_VISION_API_KEY`, albo `GOOGLE_VISION_CREDENTIALS` (JSON konta usługi, ścieżka względem katalogu `.env`), albo ADC `gcloud` / `GOOGLE_APPLICATION_CREDENTIALS` (+ `GOOGLE_CLOUD_PROJECT`) | Google Vision |
| `THE_OCR_ENV_FILE` | jawna ścieżka pliku `.env` |
| `THE_OCR_RAPIDOCR_DPI` | rozdzielczość renderu dla RapidOCR (domyślnie 200) |
| `THE_OCR_CHAIN` | kolejność łańcucha, np. `azure,google_vision,rapidocr` |
| `THE_OCR_ARCHIVE_DIR` | katalog archiwum dla `--archive` |

## Providerzy

Provider bez kluczy jest pomijany. Następny jest próbowany przy błędzie sieci/API, pustym wyniku,
brakujących stronach albo braku geometrii. Nie ma głosowania ani łączenia wyników.

- **Datalab** - `/api/v1/convert` (`output_format=json`, `mode=accurate`, `word_bboxes=true`,
  `add_block_ids=true`, `extras=new_block_types`, `disable_image_extraction=true`); asynchroniczny
  `request_check_url`, odrzucenie `metadata.failed_pages`; regiony wg `DATALAB_REGION_ORDER` (EU, potem US).
- **LlamaParse** - `items`, `markdown_full`, `metadata`; bboxy elementów z `items.pages[]`, nigdy z promptu;
  regiony wg `LLAMA_CLOUD_REGION_ORDER`.
- **Azure Document Intelligence** - REST `prebuilt-read` (API `2024-11-30`): linie jako bloki, słowa z wielokątów
  i offsetów. F0 analizuje 2 strony na żądanie, więc PDF idzie paczkami i jest składany; paczka z brakującą stroną
  to błąd providera (bez cichej utraty stron). HTTP 429 jest ponawiany wg `Retry-After`. Klucz z env albo z `az`.
- **Google Cloud Vision** - `files:annotate` z `DOCUMENT_TEXT_DETECTION` i podpowiedzią `pl`, paczki po 5 stron.
  Uwierzytelnienie w kolejności: `GOOGLE_VISION_API_KEY`; konto usługi `GOOGLE_VISION_CREDENTIALS`
  (w repo: `.secrets/gcloud-vision.json`, konto `the-ocr@holyclaude-001`); Application Default Credentials
  (`gcloud auth application-default login` albo plik z `GOOGLE_APPLICATION_CREDENTIALS`), czytane przez
  `google-auth` - binarka nie potrzebuje programu `gcloud`. Projekt rozliczeniowy ADC: `GOOGLE_CLOUD_PROJECT`
  (w `.env`: `holyclaude-001`) > `quota_project_id` z ADC > projekt aktywnej konfiguracji gcloud. Błąd API
  (wyłączone Vision API, brak uprawnień, wygasłe ADC) jest wypisywany wprost na stderr. Szybki test:
  `the-ocr plik.pdf -o /tmp/t.pdf --force-provider google_vision`.
- **RapidOCR** (lokalnie, CPU, extra `local`) - linie z ramkami jako bloki; poza domyślnym łańcuchem
  (`THE_OCR_CHAIN=...,rapidocr`). Fallback, gdy chmura jest niedostępna.

## PDF i obrazy

Strony nie-A4 są dopasowywane do A4 wektorowo (transformacja treści, bez rasteryzacji), przed OCR - więc
provider i warstwa tekstu widzą tę samą geometrię. Strona z aktywną rotacją albo wewnętrznymi linkami `GoTo`
zachowuje pierwotną geometrię. Widoczna treść, adnotacje i AcroForm zostają. JPG/PNG: tylko obrót wg EXIF
i umieszczenie na A4; bez binaryzacji, odszumiania ani cropowania. Przetworzenie podpisanego PDF zmienia jego
bajty i unieważnia podpis - oryginał zachowuje `--archive`.

## Artefakty

Domyślnie tylko PDF (w miejscu wejścia; dla obrazu `<stem>.pdf` obok). `--markdown`/`--json` dokładają
pliki obok PDF wynikowego, także przy `-o`. Publikacja jest atomowa: przy błędzie którejkolwiek części
wcześniej podmienione pliki są przywracane. Archiwum: sufiksy `-2`, `-3` przy kolizji znacznika czasu, `fsync`.

## Kanoniczny JSON

Kształt `doc-intel-contract-pl` 1.2.0 (`contract/contract.schema.json`): płaskie `blocks[]` z numerem strony,
bbox `[x0,y0,x1,y1]` w `0..1`, taksonomia bloków referencji, `doc_id` = stem pliku, `gating` (wyłącznie dane,
bez kolejek). Rozszerzenia wobec upstreamu: `source.engine` zna prawdziwe nazwy providerów (`datalab`,
`llamaparse`, `azure`, `google_vision`, `rapidocr`) oraz opcjonalne `blocks[].words[]`.

```json
{"doc_id": "umowa", "contract_version": "1.2.0",
 "source": {"path": "umowa.pdf", "engine": "datalab", "engine_variant": "eu", "pages": 1},
 "blocks": [{"id": "p0001-b0001", "page": 1, "bbox": [0.1, 0.1, 0.5, 0.15], "block_type": "paragraph",
             "text": "Treść", "confidence": 0.98, "flags": []}],
 "gating": {"threshold": 0.0, "review_required": [], "auto_approved": ["p0001-b0001"], "ungroundable": [],
            "verdict": "ok", "counts": {"total": 1, "review_required": 0, "auto_approved": 1, "ungroundable": 0}},
 "meta": {"created_at": "2026-09-10T12:00:00Z"}}
```

CLI z `--json` zapisuje JSON bez słów, z `--words` (i przy `--from-json`) ze słowami. `OCRDocument.to_dict(include_words=True)` dodaje `blocks[].words[]`
(`text`, `bbox`, `confidence`) - edytowalną geometrię. `OCRDocument.from_dict(payload, page_sizes)` czyta
poprawiony JSON z powrotem (walidacja schematu, stron, bboxów, słów w ramce bloku), a
`build_document_searchable_pdf` stawia z niego warstwę bez ponownego OCR (tak robi `reapply` w mcp-ocr).

## Markdown

`--markdown` zapisuje lokalnie treść z kanonicznego dokumentu OCR — bez dodawania
tytułu pliku jako nagłówka `#`. Każda strona zaczyna się znacznikiem
`==< NAZWA_PLIKU.pdf> (Page x/y) >==`, a kończy samodzielną linią `---`;
format obejmuje również puste strony. Nagłówki logiczne są w poziomach
`##`, `###`, `####` (odpowiednio sekcje i podsekcje rozpoznane przez OCR).
Tabele danych są poprawnymi tabelami Markdown, tabele-formularze to
`Etykieta: wartość`, a listy używają `-`. Bez HTML i zwykłej kursywy;
skreślenia to `~~tekst~~`. Specjalne tagi: `*[handnote: …]*`,
`*[signature: …]*`, `*[stamp: …]*`, `*[footer: …]*`,
`*[header: …]*`, `*[logo: …]*`, `*[photo: …]*`, `*[graphic: …]*`.

Frontmatter YAML zawiera `source_file` i `ocr_backend`, a także tylko te
pola, które da się rozpoznać w treści dokumentu:
`sygnatura_sad`, `sygnatura_policja`, `sygnatura_prokuratura`,
`karta_akt`, `rodzaj_dokumentu`, `data_wydruku`,
`data_wystawienia`, `data_wplywu`. Pola są opcjonalne, nie są
uzupełniane na podstawie nazwy pliku lub daty uruchomienia OCR.
Niepoprawne daty kalendarzowe nie trafiają do frontmatter (poza pluginem).
Pola dotyczą wyłącznie pliku Markdown — kontrakt JSON pozostaje bez zmian.

Przykład (wartości ilustracyjne):

```markdown
---
source_file: akt.pdf
ocr_backend: datalab
sygnatura_sad: II W 1342/26/N
rodzaj_dokumentu: NOTATKA URZĘDOWA
---

==< akt.pdf> (Page 1/2) >==

## NOTATKA URZĘDOWA

Treść strony.

---

==< akt.pdf> (Page 2/2) >==

Dalsza treść.

---
```

## API Python (dla integratorów)

```python
from the_ocr.config import default_providers          # łańcuch wg THE_OCR_CHAIN
from the_ocr.chain import run_chain                     # -> ChainResult(result.document, attempts)
from the_ocr.pipeline import prepare_pdf, run_pipeline, validate_searchable_pdf
from the_ocr.pdf.searchable_pdf import build_document_searchable_pdf   # mode=force|redo|skip
from the_ocr.models import OCRDocument                  # to_dict(include_words=), from_dict()
```

## Struktura projektu

| Ścieżka | Odpowiedzialność |
|---|---|
| `src/the_ocr/cli.py` | CLI |
| `src/the_ocr/pipeline.py` | archiwum, przygotowanie, łańcuch albo `--from-json`, warstwa, kontrola, publikacja z rollbackiem |
| `src/the_ocr/chain.py` | kolejne próby providerów |
| `src/the_ocr/config.py` | wyszukiwanie `.env`, kolejność łańcucha, aliasy nazw |
| `src/the_ocr/models.py` | kontrakt, walidacja, `to_dict` / `from_dict` |
| `src/the_ocr/adapters.py` | odpowiedzi Datalab/LlamaParse/Azure/Google -> kontrakt |
| `src/the_ocr/providers/` | `datalab`, `llamaparse`, `azure`, `google_vision`, `rapidocr` |
| `src/the_ocr/pdf/source_pdf.py` | usunięcie starej warstwy `Tr 3`, obraz -> A4 |
| `src/the_ocr/pdf/searchable_pdf.py` | wywołanie OCRmyPDF z pluginem (`mode`, `optimize`, `clean_final`, `pdfa`) |
| `src/the_ocr/pdf/ocrmypdf_plugin.py` | silnik OCRmyPDF (`get_ocr_engine`, `generate_ocr`); ładowany po nazwie modułu, więc działa w binarce |
| `src/the_ocr/pdf/ocr_words.py` | sidecar geometrii słów, drzewo `OcrElement` |
| `src/the_ocr/visual/scale_a4.py` | wektorowe dopasowanie do A4 |
| `contract/contract.schema.json` | schemat JSON |
| `tests/` | testy (pytest), PDF przez prawdziwy OCRmyPDF |
| `scripts/` | build wydania PyInstaller (`build_release.py`) i smoke test binarki (`smoke_release.py`) |
| `.github/workflows/` | CI (`ci.yml`), wydania binarne (`release.yml`), deploy na NAS (`deploy.yml`) |
| `Resources/` | materiały referencyjne, poza pipeline'em |
| `.env`, `.secrets/` | klucze providerów (prywatne repo) |

## Testy

```bash
uv run pytest
```

Testy PDF przechodzą przez prawdziwy OCRmyPDF i sprawdzają pozycje słów, pokrycie highlightu, polskie znaki,
zachowanie wektorów w `redo` i rasteryzację w `force`. `test_unwritable_archive_fails_before_provider`
wymaga uruchomienia jako zwykły użytkownik (root ignoruje `chmod 555`).

## Wydania binarne

Budowane automatycznie przez GitHub Actions (`.github/workflows/release.yml`) na trzech platformach:

| Plik | Platforma |
|---|---|
| `the-ocr-windows-x64.exe` | Windows 10/11 x64 |
| `the-ocr-linux-x64` | Linux x64, Debian 12+ (glibc 2.36+; budowane w kontenerze `python:3.13-bookworm`) |
| `the-ocr-macos-arm64` | macOS na Apple Silicon |

- push do `master` -> wydanie **`latest`** (prerelease, nadpisywane przy każdym merge),
- tag `v*` (np. `git tag v0.2.0 && git push --tags`) -> wydanie wersji z notatkami,
- PR zmieniający `src/`, `scripts/` albo `pyproject.toml` -> tylko build i smoke test.

Każda binarka przed publikacją przechodzi `scripts/smoke_release.py` (brak w pluginie): `--help` oraz pełny przebieg
`--from-json` przez prawdziwy OCRmyPDF (plugin, renderer, Tesseract/Ghostscript), bez providerów OCR.
Wydanie zawiera też `SHA256SUMS.txt` i `env.example`. Pobranie: `gh release download latest -R elconcept/the-ocr`.

Binarka potrzebuje na hoście `tesseract` i `gs` (macOS: `brew install tesseract ghostscript`; Debian:
`apt install tesseract-ocr ghostscript`; Windows: instalatory Tesseract UB-Mannheim i Ghostscript), a dla
`--clean-final` także `unpaper`. Na macOS pobrany plik trzeba odblokować: `xattr -d com.apple.quarantine the-ocr-macos-arm64`.

Build lokalny (PyInstaller nie kompiluje krzyżowo, więc na docelowym systemie):

```bash
uv run python scripts/build_release.py              # -> bin/<macos|linux|windows>/the-ocr[.exe]
uv run python scripts/smoke_release.py bin/macos/the-ocr
```

(`scripts/build_release_unix.sh` (brak w pluginie) i `scripts/build_release_windows.ps1` (brak w pluginie) to nakładki na to samo.) Binarki nie
są trzymane w repo.

## Instalacja binarki na hoście

Na hoście autora (macOS arm64):

```bash
uv run python scripts/build_release.py                                 # bin/macos/the-ocr
ln -sf "$PWD/bin/macos/the-ocr" ~/.local/bin/the-ocr                    # ~/.local/bin jest na PATH
ln -sf ../../.env bin/macos/.env                                       # .env obok binarki -> .env repo
mkdir -p ~/.config/the-ocr && ln -sf "$PWD/.env" ~/.config/the-ocr/.env # zapasowo, gdy bin/ wyczyszczony
```

Dowiązania sprawiają, że każdy rebuild od razu trafia na PATH, a klucze i `.secrets/` są brane z repo
(synchronizowanego między hostami). Na innym hoście zamiast budować można pobrać binarkę z wydania `latest`
i położyć `.env` w `~/.config/the-ocr/` (z bezwzględną ścieżką `GOOGLE_VISION_CREDENTIALS` albo ADC gcloud).

## CI

`.github/workflows/ci.yml`: `pytest` (prawdziwy OCRmyPDF, Tesseract, Ghostscript) na Ubuntu z Pythonem 3.11
i 3.14 przy każdym pushu do `master` i każdym PR. `deploy.yml` zgłasza przebudowę na NAS po pushu do `master`.
