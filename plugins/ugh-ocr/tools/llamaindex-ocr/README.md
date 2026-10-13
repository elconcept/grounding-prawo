# llamaindex-ocr

Parsuje pojedynczy plik przez LlamaCloud/LlamaParse do Markdown, bez flagi
`-o` — tak samo jak [markitdown-vision](../markitdown-vision/README.md).

## Co to robi

```bash
llamaindex-ocr sciezka/do/pliku.pdf
# -> sciezka/do/pliku.md
```

Wynikowy `.md` ma frontmatter zgodny z bazowym schematem markitdown-vision
(`source_file`, `converted_at`, `converter`, `ocr_backend`, `ocr_used`),
rozszerzony o dane, które daje tylko LlamaParse: `tier` (agentic/plus/eco),
`pages_count`, `page_numbers`, `confidence`, `notes` (per-strone metadane z
odpowiedzi API — `null` gdy niedostępne). Frontmatter jest budowany
deterministycznie w Pythonie, nie przez model — prompt ma wprost zakaz
generowania własnego frontmatteru (patrz `src/llamaindex_ocr/_prompt.py`).

Domyślny prompt zachowuje instrukcje wiernej transkrypcji polskich
dokumentów prawno-medycznych (rozróżnianie druku/odręcznego, pieczęci,
podpisów, stanu checkboxów, niepewności OCR) — nadpisz go przez
`--custom-prompt-file <plik>` gdy potrzeba innego typu dokumentu.

**Konwencja nawiasów kwadratowych**: każdy opis elementu wizualnego
autorstwa modelu (logo, pieczęć, podpis, checkbox, nieczytelny fragment...)
musi być w `[nawiasach]` — nigdy jako goła linia `etykieta: opis`, bo to
wygląda jak prawdziwa treść dokumentu. Reguła jest wymuszona na początku
i na końcu promptu (v3, 2026-09-06) po tym jak wersja z regułą tylko w
środku promptu nie była konsekwentnie przestrzegana na realnym dokumencie
(`logo: laptopshop.pl...` zamiast `[logo: laptopshop.pl...]`).

## Klucz API

Nigdy nie hardcoduj klucza w kodzie (poprzednia wersja to robiła — patrz
`legacy_batch_script.py.bak`, zachowany tylko jako referencja starego trybu
wsadowego z kanonicznym nazewnictwem `(ID).md`, tu nieużywanego).

Kolejność wczytywania klucza:
1. zmienna środowiskowa `LLAMA_CLOUD_API_KEY`,
2. plik `C:\Users\tom\.claude\secrets\llamacloud_api_key.txt`.

## Instalacja

```bash
cd llamaindex_ocr
uv sync
uv tool install --editable .
```

`uv tool install` rejestruje `llamaindex-ocr` jako polecenie globalne (w
`~/.local/bin`, już na PATH na tej maszynie) — działa z dowolnego katalogu
bez `uv run` ani `cd` do projektu.

## Opcje

```
--plus                 tier agentic_plus (dokładniejszy, wolniejszy/droższy)
--eco                   tier cost_effective
--polling-interval N    interwał odpytywania SDK (domyślnie 3s)
--timeout N             timeout SDK (domyślnie 1800s)
--custom-prompt-file P  własny prompt zamiast domyślnego
```
