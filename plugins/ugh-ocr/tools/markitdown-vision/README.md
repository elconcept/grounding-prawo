# markitdown-vision

MarkItDown + Google Cloud Vision OCR w jednym poleceniu, bez flagi `-o`.

## Co to robi

Konwertuje dowolny plik (PDF, obraz, DOCX, PPTX, XLSX, ...) do pliku `.md`
o tej samej nazwie, w tej samej lokalizacji co plik wejściowy. Automatycznie
używa Google Cloud Vision (`document_text_detection`) do OCR:

- dla samodzielnych obrazów (jpg/png/tiff/bmp/webp/gif),
- dla PDF-ów bez warstwy tekstowej (skan bez OCR),
- dla obrazów osadzonych w DOCX/PPTX/XLSX.

Detekcję "PDF bez warstwy tekstowej" i renderowanie stron zapewnia pakiet
[`markitdown-ocr`](../markitdown/packages/markitdown-ocr) (lokalna zależność
ścieżkowa) — ten projekt tylko podmienia jego silnik OCR (domyślnie
LLM Vision) na Google Cloud Vision.

Wyjściowy `.md` ma dopisany frontmatter YAML: `source_file`, `converted_at`,
`converter`, `ocr_backend`, `ocr_used`.

## Wymagania

- Google Cloud: projekt z włączonym Vision API, uwierzytelnienie przez
  `GOOGLE_APPLICATION_CREDENTIALS` (plik klucza service account) albo
  `gcloud auth application-default login`.

## Instalacja

```bash
cd markitdown-vision
uv sync
```

## Użycie — CLI

```bash
uv run markitdown-vision sciezka/do/pliku.pdf
# -> sciezka/do/pliku.md
```

## Użycie — MCP (Claude i inni klienci)

Zarejestrowany już globalnie w Claude Code (`claude mcp list` pokaże
`markitdown-vision`), dostępny w każdej sesji/projekcie od razu. Wystawia
jedno narzędzie: `convert_to_markdown(path)`.

Rejestracja (jednorazowo, już wykonana):

```bash
claude mcp add -s user markitdown-vision -- "D:\projects\markitdown-vision\.venv\Scripts\python.exe" "-m" "markitdown_vision.mcp_server"
```

Dla innego klienta MCP (nie Claude Code) uruchom serwer ręcznie (STDIO):

```bash
uv run markitdown-vision-mcp
```

## Użycie — jako biblioteka

```python
from markitdown_vision import convert_file

output_path = convert_file("sciezka/do/pliku.pdf")
```
