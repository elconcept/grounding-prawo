# the-ocr

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
```

## Flagi CLI

| Flaga | Działanie |
|---|---|
| `INPUT` | PDF, JPG, JPEG lub PNG |
| `-o`, `--output PLIK` | PDF wynikowy w innym miejscu; wejście nietknięte |
| `--json` | dodatkowo `<wynik>.json` (kanoniczny JSON kontraktu) |
| `--archive` | kopia oryginału przed OCR do `$THE_OCR_ARCHIVE_DIR` albo `~/archive`; obraz wejściowy usuwany po sukcesie |
| `--archive-dir KATALOG` | jak `--archive`, do wskazanego katalogu |
| `--keep-geometry` | bez dopasowania stron do A4 |
| `--layer auto\|redo\|skip\|force` | tryb warstwy OCRmyPDF (niżej); domyślnie `auto` |
| `--force-provider NAZWA` | tylko ten provider: `datalab`, `llamaparse`, `azure`, `google_vision`, `rapidocr` (aliasy: `azure-di`, `google-vision`) |

Kody wyjścia: `0` sukces, `1` błąd wejścia/zapisu, `2` żaden provider nie dał wyniku (wejście nietknięte;
przy `--archive` kopia zostaje w archiwum). Kolejne próby providerów są wypisywane na stderr.

## Tryby warstwy tekstu (`--layer`)

| Tryb | OCRmyPDF | Skutek |
|---|---|---|
| `auto` | `redo`, a dla PDF z formularzem AcroForm `skip` | domyślnie: oryginalna treść stron bez rasteryzacji |
| `redo` | usuwa starą warstwę OCR, zachowuje wektory i widoczny tekst | wymiana wadliwego OCR |
| `skip` | strony z tekstem zostają bez zmian | PDF mieszane (natywne + skany) |
| `force` | **rasteryzuje** każdą stronę, potem warstwa | tylko świadomie: wektory i tekst natywny stają się obrazem |

## Konfiguracja

Zmienne procesu albo `.env` w katalogu uruchomienia (w wydaniu binarnym: obok pliku wykonywalnego);
zmienne procesu mają pierwszeństwo. Wzór: `env.example`. W tym prywatnym repo prawdziwe klucze są
świadomie w `.env` i `.secrets/` (synchronizacja między hostami autora; darmowe tiery).

| Zmienna | Znaczenie |
|---|---|
| `DATALAB_API_KEY` (albo `DATALAB_API_KEY_EU`/`_US`), `DATALAB_REGION_ORDER`, `DATALAB_API_URL[_EU/_US]` | Datalab |
| `LLAMA_CLOUD_API_KEY` (albo `_EU`/`_US`), `LLAMA_CLOUD_REGION_ORDER`, `LLAMA_CLOUD_REGION`, `LLAMA_CLOUD_BASE_URL[_EU/_US]` | LlamaParse |
| `AZURE_DOCUMENT_ENDPOINT` + `AZURE_DOCUMENT_KEY`, albo `AZURE_DOCUMENT_RESOURCE` [+ `AZURE_DOCUMENT_RESOURCE_GROUP`] z zalogowanym `az` | Azure DI |
| `AZURE_DOCUMENT_PAGES_PER_REQUEST` | stron na żądanie Azure (domyślnie 2 = limit F0) |
| `GOOGLE_VISION_API_KEY`, albo `GOOGLE_VISION_CREDENTIALS` (JSON konta usługi, ścieżka względem katalogu `.env`), albo ADC `gcloud` (+ `GOOGLE_CLOUD_PROJECT`) | Google Vision |
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
- **Google Cloud Vision** - `files:annotate` z `DOCUMENT_TEXT_DETECTION` i podpowiedzią `pl`, paczki po 5 stron;
  klucz API, konto usługi albo Application Default Credentials zalogowanego `gcloud`.
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

CLI zapisuje JSON bez słów. `OCRDocument.to_dict(include_words=True)` dodaje `blocks[].words[]`
(`text`, `bbox`, `confidence`) - edytowalną geometrię. `OCRDocument.from_dict(payload, page_sizes)` czyta
poprawiony JSON z powrotem (walidacja schematu, stron, bboxów, słów w ramce bloku), a
`build_document_searchable_pdf` stawia z niego warstwę bez ponownego OCR (tak robi `reapply` w mcp-ocr).

## Markdown

Budowany lokalnie z kanonicznego dokumentu, nie kopiowany z odpowiedzi modelu: `## Page N` na stronę,
nagłówki `###`, poprawne tabele Markdown (tabele-formularze jako `Etykieta: wartość`), listy `-`, stopki i
nagłówki typowane z etykiet providera oraz powtarzalności i położenia, bez HTML i zwykłej kursywy,
przekreślenia `~~tekst~~`. Frontmatter: `source_file`, `converted_at`, `ocr_backend`; pierwszy nagłówek
`# <stem>`. Tagi: `*[handnote: …]*`, `*[signature: …]*`, `*[stamp: …]*`, `*[footer: …]*`, `*[header: …]*`,
`*[logo: …]*`, `*[photo: …]*`, `*[graphic: …]*`.

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
| `src/the_ocr/pipeline.py` | archiwum, przygotowanie, łańcuch, warstwa, kontrola, publikacja z rollbackiem |
| `src/the_ocr/chain.py` | kolejne próby providerów |
| `src/the_ocr/config.py` | `.env`, kolejność łańcucha, aliasy nazw |
| `src/the_ocr/models.py` | kontrakt, walidacja, `to_dict` / `from_dict` |
| `src/the_ocr/adapters.py` | odpowiedzi Datalab/LlamaParse/Azure/Google -> kontrakt |
| `src/the_ocr/providers/` | `datalab`, `llamaparse`, `azure`, `google_vision`, `rapidocr` |
| `src/the_ocr/pdf/source_pdf.py` | usunięcie starej warstwy `Tr 3`, obraz -> A4 |
| `src/the_ocr/pdf/searchable_pdf.py` | wywołanie OCRmyPDF z pluginem (`mode`, `optimize`) |
| `src/the_ocr/pdf/ocrmypdf_plugin.py` | silnik OCRmyPDF (`get_ocr_engine`, `generate_ocr`) |
| `src/the_ocr/pdf/ocr_words.py` | sidecar geometrii słów, drzewo `OcrElement` |
| `src/the_ocr/visual/scale_a4.py` | wektorowe dopasowanie do A4 |
| `contract/contract.schema.json` | schemat JSON |
| `tests/` | testy (pytest), PDF przez prawdziwy OCRmyPDF |
| `scripts/` | buildy wydań PyInstaller (Windows, macOS) |
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

PyInstaller nie kompiluje krzyżowo; buduje się na docelowym systemie (z `tesseract` i `gs` na hoście):

```bash
sh scripts/build_release_macos.sh                                         # -> bin/macos/the-ocr
powershell -ExecutionPolicy Bypass -File scripts/build_release_windows.ps1 # -> bin/windows/the-ocr.exe
```

Binarki nie są trzymane w repo (stare z 09.2026 sprzed obecnego pipeline'u zostały usunięte). Wydanie
czyta `.env` z katalogu pliku wykonywalnego; skrypt kopiuje tam `env.example`.
