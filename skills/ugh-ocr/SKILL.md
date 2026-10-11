---
name: ugh-ocr
description: Konwertuje PDF lub obraz do Markdown przez mieszany pipeline OCR — markitdown dla stron z prawdziwą warstwą tekstu, llamaindex-ocr (LlamaParse) dla reszty, z automatycznym fallbackiem na markitdown-vision (Google Cloud Vision) gdy llamaindex-ocr zawiedzie. Użyj gdy trzeba wyciągnąć tekst z PDF-a mieszanego (część stron zeskanowana, część natywna) albo z pojedynczego obrazu, i chcesz jednego polecenia zamiast ręcznego wyboru narzędzia per plik.
---

# ugh-ocr — mieszany pipeline OCR

Narzędzie CLI: `ugh-ocr <plik>`. Wszystko w tym katalogu
(`<skille>/ugh-ocr/`) jest globalne.

## Kiedy używać

- PDF, w którym **nie wiadomo z góry**, które strony mają prawdziwą warstwę
  tekstu, a które są zeskanowane (albo mieszanka obu w jednym pliku).
- Pojedynczy obraz (zdjęcie/skan dokumentu) do przepisania na tekst.
- Sytuacje, gdzie osobne narzędzia (`markitdown-vision`, `llamaindex-ocr`)
  wymagałyby ręcznej decyzji, które z nich odpalić na którym pliku/stronie.

Gdy **z góry wiadomo**, że cały plik ma prawdziwą warstwę tekstu i nie trzeba
OCR-u wcale, zwykły `markitdown <plik>` (bez `ugh-ocr`) jest szybszy. Gdy z
góry wiadomo, że cały plik trzeba OCR-ować konkretnym backendem (np. zawsze
LlamaParse), można użyć bezpośrednio `llamaindex-ocr <plik>` albo
`markitdown-vision <plik>` — `ugh-ocr` ma sens tam, gdzie ta decyzja
per-strona nie jest z góry znana.

## Jak to działa

Dla PDF, każda strona jest klasyfikowana osobno:

- **Prawdziwa (widoczna) warstwa tekstu** → zwykły `markitdown`, bez OCR.
- **Brak prawdziwej warstwy tekstu** (w tym strona z niewidoczną warstwą OCR
  nałożoną wcześniej przez inne narzędzie, np. ocrmypdf/Tesseract — ta warstwa
  jest **celowo ignorowana**, bo mogła być niskiej jakości) → `llamaindex-ocr`
  (LlamaParse). Jeśli to zawiedzie (brak/zły klucz, brak środków, błąd sieci)
  → ostrzeżenie na stdout i przełączenie na `markitdown-vision` (Google Cloud
  Vision) dla tej i wszystkich pozostałych stron OCR w danym pliku.
- Jeśli **oba** backendy OCR zawiodą dla tej samej strony → czytelny,
  sformatowany błąd na stdout i **koniec działania** (bez pliku wyjściowego
  częściowo przetworzonego).

Rozróżnienie "prawdziwa warstwa" vs "OCR-sandwich" nie polega na długości
wyekstrahowanego tekstu (to zawodne — niewidoczna warstwa OCR też ma
niezerową długość tekstu), tylko na PDF text rendering mode (`page.get_texttrace()`,
`type == 3` = niewidoczny). Szczegóły: `tools/ugh-ocr/README.md` i
`tools/ugh-ocr/src/ugh_ocr/_pdf_analysis.py`.

Dla samodzielnych obrazów: ta sama kolejność prób (`llamaindex-ocr` →
fallback `markitdown-vision`), bez etapu klasyfikacji stron.

## Użycie

```bash
ugh-ocr sciezka/do/pliku.pdf
# -> sciezka/do/pliku.md

ugh-ocr sciezka/do/skanu.jpg
# -> sciezka/do/skanu.md
```

Bez flagi `-o` — wyjście zawsze obok wejścia, ta sama nazwa bazowa. Opcje
`--plus`/`--eco`/`--polling-interval`/`--timeout`/`--custom-prompt-file`
dotyczą wyłącznie etapu `llamaindex-ocr` (patrz `tools/llamaindex-ocr/README.md`).

## Frontmatter

Zobacz skill [frontmatter](../frontmatter/SKILL.md) dla ogólnej konwencji
kluczy w tym repozytorium narzędzi. `ugh-ocr` dokłada do wspólnego schematu
(`source_file`/`converted_at`/`converter`/`ocr_backend`/`ocr_used`):
`pages_count`, `pages_backend` (lista per-strone: `text`/`llamaparse`/
`google-cloud-vision`), `fallback_used`, `fallback_reason`. Treść ma
znaczniki `<!-- ugh-ocr: strona N/M, zrodlo: <backend> -->` przed każdą
stroną — do śledzenia pochodzenia bez zaburzania czytelności.

## Wymagania i sekrety

- Klucz LlamaCloud: zmienna `LLAMA_CLOUD_API_KEY` albo plik
  `~/.claude/secrets/llamacloud_api_key.txt`.
- Google Cloud Vision: Application Default Credentials (`gcloud auth
  application-default login`) albo `GOOGLE_APPLICATION_CREDENTIALS`.
- Brak jednego z dwóch nie blokuje działania — `ugh-ocr` po prostu przełącza
  się na drugi backend z ostrzeżeniem. Brak **obu** = błąd dla stron/plików,
  które faktycznie wymagają OCR (strony z prawdziwym tekstem nadal działają).

## Instalacja / reinstalacja narzędzi CLI

Źródła narzędzi (`ugh-ocr`, `llamaindex-ocr`, `markitdown-vision`,
`markitdown-ocr`) są w `tools/` obok tego pliku, jako samodzielne projekty
`uv` (bez zależności od `D:\projects\...` — te ścieżki istnieją tylko na
maszynie, na której skill powstał). Jeśli polecenie `ugh-ocr` nie jest
rozpoznawane:

```bash
bash <skille>/ugh-ocr/tools/install.sh
```

(Windows: `pwsh <skille>/ugh-ocr/tools/install.ps1`). Wymaga `uv`
(https://docs.astral.sh/uv/) i Pythona 3.12 (`uv python install 3.12` jeśli
brak).
