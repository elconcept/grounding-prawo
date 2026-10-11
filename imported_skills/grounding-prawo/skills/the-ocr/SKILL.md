---
name: the-ocr
description: OCR polskich dokumentów (PDF, JPG, PNG) przez Datalab (Chandra) z zapasowym LlamaParse - wynik to Markdown ze stronami `## Page N`, JSON z bboxami i przeszukiwalny PDF. Użyj, gdy dokument jest skanem albo PDF-em bez warstwy tekstu, gdy użytkownik prosi o OCR albo o przygotowanie akt do analizy i cytowania ze stronami.
---

# the-ocr

Rdzeń projektu `the-ocr` (źródło prawdy: `D:\projects\the-ocr`, praca w toku właściciela).
Tu jest sam kod `src/the_ocr` z `pyproject.toml` i `uv.lock` - bez binariów, materiałów
referencyjnych i próbek.

## Uruchomienie
Wymaga Pythona 3.11+ oraz kluczy `DATALAB_API_KEY` i `LLAMA_CLOUD_API_KEY` - w zmiennych
środowiska albo w pliku `.env` w katalogu, z którego uruchamiasz (szablon: `env.example`,
regiony EU/US opisane w `README.md`). Kluczy nie zapisuj w repozytorium ani w pluginie.

```bash
# z uv (zalecane)
uv run --project <katalog tego skilla> the-ocr akta/pismo.pdf

# bez uv
pip install httpx pillow pymupdf pikepdf pyyaml python-dotenv llama-cloud
PYTHONPATH=<katalog tego skilla>/src python -m the_ocr akta/pismo.pdf
```

Diagnostyka jednego providera: `--force-provider datalab` albo `--force-provider llamaparse`.

## Wynik
Obok wejścia powstają `pismo.md` (frontmatter `source_file`, `converted_at`, `ocr_backend`;
strony jako `## Page N`), `pismo.json` (bloki z bboxami), `pismo.pdf` (przeszukiwalny)
oraz kopia wejścia w `archive/`. Obraz JPG/PNG jest po sukcesie przenoszony do `archive/`.

Dalej: `patron-przeglad-tabelaryczny` (`doc_to_text.py`), `patron-weryfikacja-cytatow`
i `patron-skan-dokumentu` czytają `pismo.md` bezpośrednio i zachowują numerację stron;
przy parze `pismo.pdf` + `pismo.md` biorą `.md`. `doc-intel-contract-pl` normalizuje wynik
do kontraktu bloków z bboxami.

## Aktualizacja kopii
Po zmianach w `D:\projects\the-ocr` skopiuj ponownie `src/the_ocr`, `pyproject.toml`
i `uv.lock` do katalogu tego skilla.
