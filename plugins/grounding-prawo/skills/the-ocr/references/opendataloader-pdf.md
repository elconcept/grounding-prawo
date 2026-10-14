# OpenDataLoader PDF (silnik dla PDF z warstwą tekstową i tabelami)

Część skilla `the-ocr`; wcześniej osobny skill `opendataloader-pdf` (Apache-2.0).

# OpenDataLoader PDF - PDF→JSON/MD (PL)

Java-based (Python wrapper) parser PDF najwyższej jakości dla AI. Benchmarki: NID (reading order), TEDS (tabele), MHS (headings). Używany w pipeline `Konwerter/` w vault.

## Instalacja (zrobione 2026-04-21)

```bash
python -m pip install --user opendataloader-pdf
```

Python 3.14, `opendataloader-pdf 2.2.1`. Wymaga **Java 17+** (mamy Eclipse Adoptium JDK 17). CLI: `python -m opendataloader_pdf` albo `opendataloader-pdf.exe` ze Scripts/.

## Wspierane outputy

- **JSON** (pełna struktura - reading order, bounding boxes, tabele jako 2D arrays) - default
- **Markdown** (flattened output, gotowy pod LLM)
- **HTML** (opcjonalnie)

## Użycie

### CLI - pojedynczy PDF
```bash
python -m opendataloader_pdf --input plik.pdf --output output/ --format md
```

### Zaawansowane flagi
- `--enrich-formula` - wyciąga formuły LaTeX
- `--enrich-picture-description` - opis obrazów (wymaga `--hybrid-mode full`)
- `--filter-hidden-text` - wykrywa ukryty tekst (off by default, per-page rendering)

### Python API
```python
import opendataloader_pdf
result = opendataloader_pdf.load("plik.pdf", output_format="markdown")
print(result.markdown)
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

<!-- shared-rules:begin (wygenerowane z ../../SHARED-RULES.md przez scripts/shared-rules-sync.py - nie edytuj tutaj) -->
## Wspólne reguły wtyczki dokumenty (Dokumenty)

Te reguły obowiązują w każdym skillu tej wtyczki, także gdy sam skill milczy. Są skopiowane do każdego skilla, więc działają zarówno po instalacji całej wtyczki, jak i pojedynczego skilla.

Plugin obsługuje dokumenty: konwersję do Markdown, redlining .docx i anonimizację danych osobowych. Część operacji dotyka danych wrażliwych, więc reguła ochrony danych jest tu pierwsza.

### Ochrona danych

- **Metadane przy wysyłce** - redlining .docx czyści też metadane autora; sprawdź je przed przekazaniem pliku na zewnątrz.
- **Próg poufności** - materiał objęty tajemnicą lub szczególnie wrażliwy oceniaj osobno, czy w ogóle wnosić do narzędzia. Przy wątpliwości nie przekazuj.

### Operacje nieodwracalne


### Bramka człowieka

Wynik to projekt. Nic nie zostaje wysłane ani złożone, zanim sprawdzi to uprawniony człowiek. Plugin przygotowuje plik, nie wykonuje aktu wysyłki.

### Zakres pluginu

Plugin daje narzędzia na dokumentach (konwersja, redline, anonimizacja, akta i chronologia). Nie ocenia treści prawnej. Weryfikację cytatu wobec źródła prawa daje plugin „fundament weryfikacyjny”; `chronologia-stanowiska-pl` sprawdza tylko, czy cytat stoi na wskazanej stronie akt.
<!-- shared-rules:end -->
