# ugh-ocr

Mieszany pipeline OCR dla PDF-ow i obrazow, bez flagi `-o` -- tak samo jak
[markitdown-vision](../markitdown-vision/README.md) i
[llamaindex-ocr](../llamaindex_ocr/README.md), na ktorych bazuje.

```bash
ugh-ocr sciezka/do/pliku.pdf
# -> sciezka/do/pliku.md
```

## Dlaczego mieszany pipeline

Dla PDF-ow strony traktowane sa **osobno**:

- strona z prawdziwa, widoczna warstwa tekstu -> zwykly `markitdown`
  (szybko, tanio, bez OCR -- tekst juz tam jest).
- strona bez prawdziwej warstwy tekstu -> `llamaindex-ocr` (LlamaParse),
  a jesli ten zawiedzie (brak/zly klucz, brak srodkow, blad sieci) ->
  ostrzezenie na stdout i przelaczenie na `markitdown-vision` (Google Cloud
  Vision) dla tej i wszystkich pozostalych stron OCR w danym pliku.

**"Prawdziwa warstwa tekstu" != "PDF ma jakis tekst".** Skanowany dokument
przepuszczony wczesniej przez inny silnik OCR (np. ocrmypdf/Tesseract) czesto
ma niewidoczna warstwe tekstu nalozona na obraz strony ("sandwich PDF").
`page.get_text()` zwroci ten tekst tak samo jak prawdziwy -- **dlugosc
wyekstrahowanego tekstu nie odroznia jednego od drugiego** (zweryfikowano
eksperymentalnie: strona z jednym niewidocznym znakiem ma nizej wyzerowana
liczbe "widocznych" znakow, ale get_text() i tak go zwraca).

Rozroznienie idzie przez PDF text rendering mode (operator `Tr` w tresci
strony), odczytywany przez `page.get_texttrace()`: `type == 3` oznacza tekst
niewidoczny (tak dziala nalozona warstwa OCR), kazdy inny typ to normalny,
widoczny tekst. Strona liczy sie jako "ma prawdziwa warstwe" tylko gdy ma
jakikolwiek tekst z `type != 3`. Zobacz `src/ugh_ocr/_pdf_analysis.py`.

Efekt: nawet jesli PDF ma juz (byc moze slaba) niewidoczna warstwe OCR,
ugh-ocr ja ignoruje i **zawsze robi swiezy OCR** takiej strony -- zgodnie z
zasada "no matter the hidden ocr layer".

Dla samodzielnych obrazow (bez pojecia "warstwy tekstu"): ta sama kolejnosc
prob -- `llamaindex-ocr`, potem fallback `markitdown-vision`.

## Frontmatter

Superset schematu wspolnego z markitdown-vision/llamaindex-ocr
(`source_file`/`converted_at`/`converter`/`ocr_backend`/`ocr_used`), plus:

- `pages_count`, `pages_backend` -- lista per-strone (`"text"` /
  `"llamaparse"` / `"google-cloud-vision"`), `null`/pominiete dla obrazow
  (traktowanych jako jedna "strona").
- `fallback_used`, `fallback_reason` -- czy i dlaczego llamaindex-ocr zawiodl
  w trakcie przetwarzania tego pliku i przetwarzanie przeszlo na
  markitdown-vision.

W tresci wynikowej kazda strona ma znacznik
`<!-- ugh-ocr: strona N/M, zrodlo: <backend> -->` -- do sledzenia, ktora
strona skad pochodzi, bez zaburzania czytelnosci markdownu.

## Bledy

- Awaria pojedynczego backendu OCR (np. llamaindex-ocr bez waznego klucza)
  -> **ostrzezenie na stdout**, proba dalej z fallbackiem. Nie przerywa pracy.
- Awaria **obu** backendow OCR dla tej samej strony -> czytelny,
  sformatowany blad na stdout (ramka z tytulem/detalem/podpowiedzia) i
  **koniec dzialania** (kod wyjscia 1) -- bez pol-przetworzonego pliku
  wyjsciowego.
- Nieobslugiwany typ pliku (nie PDF, nie obraz) -> ten sam czytelny format
  bledu.

## Instalacja

Wymaga lokalnych checkoutow `markitdown-vision` i `llamaindex-ocr` obok tego
katalogu (patrz `[tool.uv.sources]` w `pyproject.toml`) -- albo dostosuj
sciezki, jesli uklad katalogow jest inny.

```bash
cd ugh-ocr
uv sync
uv tool install --editable .
```

`uv tool install` rejestruje `ugh-ocr` jako polecenie globalne (w
`~/.local/bin`, na PATH) -- dziala z dowolnego katalogu.

## Opcje

Te same co `llamaindex-ocr` (dotycza tylko etapu llamaindex-ocr, nie
markitdown ani markitdown-vision):

```
--plus                 tier agentic_plus (dokladniejszy, wolniejszy/drozszy)
--eco                   tier cost_effective
--polling-interval N    interwal odpytywania SDK (domyslnie 3s)
--timeout N             timeout SDK (domyslnie 1800s)
--custom-prompt-file P  wlasny prompt LlamaParse zamiast domyslnego
```
