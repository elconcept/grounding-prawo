# the-ocr

Prywatny pipeline OCR dla polskich dokumentów. Ten plik jest jedynym
aktualnym opisem architektury, decyzji i stanu repozytorium. Katalog
`Resources/` zawiera wyłącznie materiały referencyjne i historyczne projekty;
nie opisuje aktywnego pipeline'u.

## Stan

Aktywny pipeline obsługuje `.pdf`, `.jpg`, `.jpeg` i `.png`:

```text
archiwizacja wejścia
  -> bezstratne przygotowanie PDF A4
  -> Datalab API
  -> fallback LlamaParse przy błędzie lub niepełnym wyniku
  -> kanoniczny dokument OCR z bboxami
  -> <stem>.json + <stem>.md + <stem>.pdf
```

Azure Document Intelligence, Google Vision, Apple Vision, Tesseract,
consensus/scoring, wykrywanie PII, redaction candidates i human-review gating
zostały usunięte z kodu produkcyjnego. Ich historyczne implementacje pozostają
jedynie w `Resources/` i historii Git.

## Uruchomienie

```powershell
uv sync
uv run the-ocr dokument.pdf
uv run the-ocr skan.jpg
```

### Wydania binarne

PyInstaller nie obsługuje cross-compilacji, dlatego wydania są niezależne:

```text
bin/windows/the-ocr.exe
bin/macos/the-ocr
```

Windows buduje się na Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_release_windows.ps1
```

macOS buduje się na macOS:

```bash
sh scripts/build_release_macos.sh
```

Build macOS jest natywny dla architektury Pythona użytego podczas budowy.
Universal2 wymaga interpretera Python universal2; w przeciwnym razie należy
zbudować osobne pliki na Apple Silicon i Intel.

Repozytorium zawiera aktualnie zbudowany i sprawdzony wariant Windows.
Binarium macOS musi zostać wygenerowane na macOS, ponieważ PyInstaller nie
obsługuje cross-kompilacji z Windows.
Każdy skrypt budujący zapisuje obok executable plik `SHA256SUMS.txt`.

Do diagnostyki można wymusić jeden z dwóch aktywnych providerów:

```powershell
uv run the-ocr dokument.pdf --force-provider datalab
uv run the-ocr dokument.pdf --force-provider llamaparse
```

Wymagane sekrety:

```text
DATALAB_API_KEY=...
LLAMA_CLOUD_API_KEY=...
```

Można równolegle skonfigurować regiony EU i US. Domyślna kolejność prób to
EU, następnie US:

```text
DATALAB_API_KEY_EU=...
DATALAB_API_KEY_US=...
LLAMA_CLOUD_API_KEY_EU=...
LLAMA_CLOUD_API_KEY_US=...
DATALAB_REGION_ORDER=eu,us
LLAMA_CLOUD_REGION_ORDER=eu,us
```

W wersji źródłowej `.env` jest czytany z bieżącego katalogu. W wersji binarnej
`.env` jest czytany wyłącznie z katalogu zawierającego executable, czyli
`bin/windows/.env` albo `bin/macos/.env`. Zmienne procesu mają pierwszeństwo.
Szablon znajduje się w `bin/env.example` i jest kopiowany przy budowaniu.
Opcjonalne `LLAMA_CLOUD_REGION=eu|us`, `LLAMA_CLOUD_BASE_URL`,
`DATALAB_API_URL` zmienia konfigurację. Sekretów nie
wolno commitować.

## Artefakty

Dla `dokument.pdf` po sukcesie pozostają:

```text
dokument.pdf
dokument.md
dokument.json
archive/dokument_YYYYMMDD_HHMMSS.pdf
```

Dla `skan.jpg` lub `skan.png` źródłowy obraz jest najpierw trwale kopiowany
do `archive/`, a po opublikowaniu kompletu wyników usuwany z katalogu
roboczego. Pozostają `skan.pdf`, `skan.md`, `skan.json` oraz kopia obrazu w
`archive/`.

Archiwizacja jest krokiem 0 i zachodzi również wtedy, gdy OCR później zawiedzie.
Kopia jest zapisywana z `fsync` i kontrolą SHA-256. Kolizje sekundowego
timestampu otrzymują sufiks `-2`, `-3` itd.

## PDF i obrazy

PDF jest odczytywany z kopii archiwalnej. Pipeline usuwa poprzednią niewidzialną
warstwę OCR zapisaną trybem PDF `Tr 3`, również wewnątrz Form XObjectów, po czym
wektorowo dopasowuje strony nie-A4 do A4. Obrazy i grafika nie są
rasteryzowane ponownie. Widoczna treść, adnotacje i AcroForm są zachowywane.
Jeżeli strona ma aktywną rotację albo wewnętrzne linki `GoTo`, pipeline
zachowuje jej pierwotną geometrię zamiast ryzykować uszkodzenie odsyłaczy.

JPG/PNG jest obracany wyłącznie zgodnie z EXIF i umieszczany proporcjonalnie na
stronie A4. Nie ma binaryzacji, odszumiania, zmiany kolorów ani agresywnego
cropowania. JPG bez korekty orientacji jest osadzany bez ponownej kompresji.

Finalny PDF otrzymuje dokładnie jedną lokalnie wygenerowaną, niewidzialną
warstwę tekstową. Warstwa OCR nie osadza żadnego pliku fontu: używa standardowej
czcionki Base-14 `/Helvetica` i własnej mapy `/ToUnicode`, dzięki czemu polskie
znaki pozostają poprawnie ekstrahowalne. Słowa są scalane w linie, a cała
warstwa strony trafia do jednego strumienia. Zapis pikepdf włącza Object Streams,
kompresję i linearyzację. Fonty już obecne w dokumencie źródłowym pozostają
nietknięte, ponieważ ich usunięcie uszkodziłoby widoczną treść.

Przetwarzanie podpisanego cyfrowo PDF zmienia jego bajty i unieważnia podpis
kryptograficzny; oryginał pozostaje w `archive/`.

## Providerzy

### Datalab

Datalab jest pierwszym providerem. Żądanie `/api/v1/convert` używa:

```text
output_format=json
mode=accurate
word_bboxes=true
add_block_ids=true
extras=new_block_types
disable_image_extraction=true
```

Provider obsługuje asynchroniczny `request_check_url`, sprawdza jednocześnie
`status=complete` i `success=true`, pobiera podpisany `result_url` bez nagłówka
API oraz odrzuca wyniki z `metadata.failed_pages`. JSON Datalab zawiera strony,
typy bloków, Markdown, bboxy bloków oraz HTML ze spanami słów i ich bboxami.
Przy regionalnych kluczach próbuje kolejno konfiguracji wskazanych przez
`DATALAB_REGION_ORDER`; błąd EU uruchamia próbę US przed przejściem do
LlamaParse.

### LlamaParse

LlamaParse jest fallbackiem. Żądanie rozwija `items`, `markdown_full` i
`metadata`. `items.pages[]` dostarcza wymiar strony oraz bboxy elementów.
Nie używamy bboxów wymyślanych przez prompt. Wynik strony oznaczonej jako
nieudana albo dokument bez geometrii jest błędem providera.
Klucze `LLAMA_CLOUD_API_KEY_EU` i `LLAMA_CLOUD_API_KEY_US` są próbane według
`LLAMA_CLOUD_REGION_ORDER`. Każdy region używa własnego endpointu LlamaCloud.

Fallback zachodzi przy braku konfiguracji, błędzie sieci/API, pustym wyniku,
brakujących stron lub niepoprawnej geometrii. Nie ma głosowania ani wyboru
„zwycięzcy” spośród równoległych odpowiedzi.

## Kanoniczny JSON

`<stem>.json` jest źródłem dla chunkowania, embeddings, Markdown i warstwy
PDF. Najważniejszy kształt:

```json
{
  "schema_version": "1.0",
  "source": {"name": "dokument.pdf", "sha256": "..."},
  "ocr": {"provider": "datalab"},
  "pages": [
    {
      "number": 1,
      "width": 1596.0,
      "height": 2240.0,
      "blocks": [
        {
          "id": "p0001-b0001",
          "page": 1,
          "block_type": "paragraph",
          "text": "Treść",
          "markdown": "Treść",
          "bbox": [0.1, 0.1, 0.5, 0.2],
          "confidence": 0.99,
          "words": []
        }
      ]
    }
  ]
}
```

Bbox ma zawsze format `[x0, y0, x1, y1]`, zakres `0..1` i początek w lewym
górnym rogu. Nie ma pól PII, redakcji, gatingu ani ręcznej weryfikacji.

## Markdown

`<stem>.md` jest budowany lokalnie z kanonicznego JSON, a nie kopiowany wprost
z odpowiedzi modelu. Tekst i bboxy pochodzą od providera, natomiast struktura
jest deterministycznie normalizowana pod dalszą analizę LLM:

- każda strona ma nagłówek `## Page N`,
- nagłówki dokumentu używają poziomu `###`,
- tabele są zamieniane na listę rekordów `- Table row N: pole: wartość`,
- wszystkie listy są normalizowane do `-`,
- stopki i nagłówki są typowane z etykiety providera oraz z powtarzalności i
  położenia geometrycznego,
- HTML, bold i zwykłe italic są usuwane,
- surowy `block.markdown` providera nie steruje finalną strukturą poza lokalnym
  odczytem komórek tabel i elementów list.

Frontmatter zawiera wyłącznie:

```yaml
source_file: dokument.pdf
converted_at: 2026-09-10T12:00:00Z
ocr_backend: datalab
```

Pierwszy nagłówek to zawsze `# dokument`, bez rozszerzenia. Renderer usuwa HTML,
bold i zwykłe italic, normalizuje listy nieuporządkowane do `-` i zachowuje
przekreślenia jako `~~tekst~~`.

Dozwolone specjalne tagi:

```text
*[handnote: treść]*
*[signature: imię i nazwisko lub illegible]*
*[stamp: treść]*
*[footer: treść]*
*[header: treść]*
*[logo: opis]*
*[photo: opis]*
*[graphic: opis]*
```

## Układ kodu

| Plik | Odpowiedzialność |
| --- | --- |
| `src/the_ocr/cli.py` | minimalne CLI |
| `src/the_ocr/pipeline.py` | archiwizacja, orkiestracja i publikacja z rollbackiem |
| `src/the_ocr/models.py` | kanoniczny dokument OCR i walidacja bbox |
| `src/the_ocr/adapters.py` | normalizacja odpowiedzi Datalab/LlamaParse |
| `src/the_ocr/providers/datalab_provider.py` | Convert API i polling |
| `src/the_ocr/providers/llamaparse_provider.py` | fallback LlamaParse z `items` |
| `src/the_ocr/pdf/source_pdf.py` | stripping starego OCR i obraz do PDF |
| `src/the_ocr/pdf/text_layer.py` | nieosadzana, liniowa warstwa OCR i optymalizacja PDF |
| `src/the_ocr/visual/scale_a4.py` | wektorowe dopasowanie do A4 |
| `src/the_ocr/frontmatter.py` | minimalny frontmatter i dokument Markdown |
| `scripts/build_release_windows.ps1` | natywny build Windows |
| `scripts/build_release_macos.sh` | natywny build macOS |
| `.opencode/skills/the-ocr/SKILL.md` | instrukcja obsługi dla LLM |

## Testy i development

```powershell
uv run pytest
npx --yes markdownlint-cli2 README.md CLAUDE.md SampleData/<timestamp>/*.md
```

Testy jednostkowe używają `tmp_path`. Każdy ręczny smoke test lub próbne
wywołanie providera musi pozostawić trwały ślad w
`SampleData/<YYYYMMDD_HHMMSS>/`; `SampleData/` jest ignorowany przez Git i
może zawierać dokumenty prywatne.

Aktualna zweryfikowana baza: 38 testów jednostkowych oraz live E2E z
2026-09-10: Datalab w `SampleData/20260910_100054/`, LlamaParse w
`SampleData/20260910_100136/` i wejście PNG w
`SampleData/20260910_095406/`. Materiały z wcześniejszych architektur
pozostają w `Resources/`, ale nie są częścią runtime ani źródłem aktualnych
decyzji.

Test `sample8.pdf`: `SampleData/20260912_191824/`. Wynik ma 4 jawne sekcje
stron, zero tabel Markdown, jedną dodatkową warstwę OCR na stronę, 59 obiektów
PDF, linearyzację i rozmiar około 61% pliku wejściowego. OCR nie dodał żadnego
osadzonego fontu; fonty Calibri widoczne w inspekcji pochodzą z dokumentu
źródłowego.
