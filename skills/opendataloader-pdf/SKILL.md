---
name: opendataloader-pdf
description: Wysokiej jakości konwerter PDF→JSON/Markdown dla AI - zachowuje reading order, strukturę tabel, headings. Użyj gdy użytkownik mówi "wysoka jakość PDF", "papers naukowe PDF", "tabele z PDF", "opendataloader", "PDF z skomplikowaną strukturą", albo gdy MarkItDown daje słaby output. Główny konwerter PDF→MD w pipeline Konwerter/ w Obsidian Vault.
license: Apache-2.0
allowed-tools: [Bash, Read, Write]
data-residency: local
requires-human-approval: false
pii-egress: none
---

# OpenDataLoader PDF - PDF→JSON/MD (PL)

Java-based (Python wrapper) parser PDF najwyższej jakości dla AI. Benchmarki: NID (reading order), TEDS (tabele), MHS (headings). Używany w pipeline `Konwerter/` w vault.

## Instalacja (zrobione 2026-04-21)

```bash
python -m pip install --user opendataloader-pdf
```

`opendataloader-pdf 2.4.x` (w `D:\abogada\.venv`, sprawdzone 2026-09-24). Wymaga **Java 11+** (jest OpenJDK 21). CLI: `python -m opendataloader_pdf` albo `opendataloader-pdf.exe` ze Scripts/.
Od 2.4 wejście jest argumentem pozycyjnym (`--input` nie istnieje), format to `markdown`, nie `md`.

## Wspierane outputy

- **JSON** (pełna struktura - reading order, bounding boxes, tabele jako 2D arrays) - default
- **Markdown** (flattened output, gotowy pod LLM)
- **HTML** (opcjonalnie)

## Użycie

### CLI - pojedynczy PDF
```bash
python -m opendataloader_pdf plik.pdf -o output/ -f markdown -q
```

### Batch (Obsidian Vault, pipeline Konwerter)
```bash
python -m opendataloader_pdf \
  "%USERPROFILE%/Documents/Obsidian Vault/wszystko co wpada szybko/" \
  -o "%USERPROFILE%/Documents/Obsidian Vault/Konwerter/" \
  -f markdown
```

### Zaawansowane flagi
- `--pages 1,3,5-7` - wybrane strony
- `--table-method`, `--reading-order`, `--use-struct-tree` - tabele i kolejność czytania
- `--hybrid-mode full` - tryb hybrydowy (opis obrazów, OCR); pełna lista: `python -m opendataloader_pdf -h`

### Python API
```python
import opendataloader_pdf
opendataloader_pdf.convert(input_path=["plik.pdf"], output_dir="output/", format="markdown")
# wynik: output/plik.md
```

## Kiedy użyć vs MarkItDown

| PDF | Narzędzie |
|---|---|
| Prosty, tekst liniowy (blog, artykuł prasowy) | MarkItDown (szybsze) |
| Papers naukowe, raporty z tabelami | **OpenDataLoader** (jakość) |
| Dokumenty z 2-kolumnowym layoutem | **OpenDataLoader** (reading order) |
| Multi-page tabele | **OpenDataLoader** (TEDS) |
| Batch Konwerter/ (domyślnie) | **OpenDataLoader** |

## Integracja z vault

Pipeline Konwerter (istnieje Python script w `_vault-management/scripts/`):
1. PDF wrzucone do `wszystko co wpada szybko/` lub dropowane bezpośrednio
2. `opendataloader-pdf <path> -f markdown -o Konwerter/`
3. Frontmatter: `type: source-pdf, tags: [pdf, zrodlo]` - zgodnie z `vault-rules.json` → `clippings.classification_rules.pdf_source`
4. Powiązane oryginały PDF w folderze `Konwerter/` lub Attachments

## Gotcha

- **Java 17 wymagana** - Adoptium JDK zainstalowana (`/c/Program Files/Eclipse Adoptium/jdk-17.0.10.7-hotspot/`)
- **Wolniejsze** niż MarkItDown - nie używaj dla prostych PDFów
- **ForkJoinPool parallelism** - per-page przetwarzanie równoległe, `--filter-hidden-text` wyłącza parallel
- Przy zmianach CLI opcji w Java: `npm run sync` (dla kontrybutorów - nas nie dotyczy)

## Zasady

- Zawsze output do `Konwerter/`, nie nadpisuj oryginalnych PDF
- Batch > 10 PDF → zapytaj Wiesława przed startem
- Idempotencja: jeśli `.md` już istnieje w output i checksumma PDF nie zmieniona → skip
