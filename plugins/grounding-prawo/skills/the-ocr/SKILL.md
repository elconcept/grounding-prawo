---
name: the-ocr
description: OCR polskich dokumentów (PDF, JPG, PNG) przez Datalab (Chandra) z zapasowymi LlamaParse, Azure Document Intelligence i Google Cloud Vision - wynik to Markdown ze stronami `## Page N`, JSON z bboxami i przeszukiwalny PDF. Użyj, gdy dokument jest skanem albo PDF-em bez warstwy tekstu, gdy użytkownik prosi o OCR albo o przygotowanie akt do analizy i cytowania ze stronami.
---

# the-ocr

## Wybór silnika odczytu dokumentu

| Dokument | Silnik |
|---|---|
| skan, zdjęcie, PDF bez warstwy tekstowej | `the-ocr` (niżej) |
| wynik wątpliwy | drugi, niezależny odczyt drugim silnikiem; rozbieżności zgłoś, nie wygładzaj |

Każdy silnik tworzy nową reprezentację tekstową. Plik źródłowy pozostaje nietknięty; przy sporze rozstrzyga warstwa wizualna (PDF/obraz).

Rdzeń projektu `the-ocr` (repozytorium `elconcept/the-ocr`; providery `azure-di` i `google-vision` dodane 10.10.2026 - upstream usunął je w commicie „remodel”).
Tu jest sam kod `src/the_ocr` z `pyproject.toml` i `uv.lock` - bez binariów, materiałów
referencyjnych i próbek.

## Uruchomienie
Wymaga Pythona 3.11+ oraz kluczy `DATALAB_API_KEY` i `LLAMA_CLOUD_API_KEY` (dla pierwszych dwóch providerów; fallbacki - niżej) - w zmiennych
środowiska albo w pliku `.env` w katalogu, z którego uruchamiasz (szablon: `env.example`,
regiony EU/US opisane w `README.md`). Kluczy nie zapisuj w repozytorium ani w pluginie.

```bash
# z uv (zalecane)
uv run --project <katalog tego skilla> the-ocr akta/pismo.pdf

# bez uv
pip install httpx pillow pymupdf pikepdf pyyaml python-dotenv llama-cloud
PYTHONPATH=<katalog tego skilla>/src python -m the_ocr akta/pismo.pdf
```

Diagnostyka jednego providera: `--force-provider datalab|llamaparse|azure-di|google-vision`.

## Łańcuch providerów i darmowe limity
Domyślnie: `datalab` → `llamaparse` → `azure-di` → `google-vision` (pierwszy sukces wygrywa).
Kolejność zmienia `THE_OCR_CHAIN`, np. `THE_OCR_CHAIN=azure-di,google-vision` - najpierw darmowe pule:
- **Azure Document Intelligence** (`azure-di`, model `prebuilt-read`, REST bez SDK): zasób F0 = 500 stron/mies.
  F0 analizuje tylko 2 pierwsze strony dokumentu, dlatego PDF idzie paczkami po
  `AZURE_DOCUMENT_PAGES_PER_CALL` stron (domyślnie 2) i jest scalany. Poświadczenia: `AZURE_DOCUMENT_ENDPOINT` +
  `AZURE_DOCUMENT_KEY` albo `AZURE_DOCUMENT_RESOURCE` (+ `AZURE_DOCUMENT_RESOURCE_GROUP`) - klucz pobierany w locie
  przez zalogowane `az` (subskrypcja pay-as-you-go).
- **Google Cloud Vision** (`google-vision`, `DOCUMENT_TEXT_DETECTION`): 1000 jednostek/mies. (1 strona = 1 jednostka),
  strony renderowane w `GOOGLE_VISION_DPI` (domyślnie 200). Poświadczenia: `GOOGLE_VISION_API_KEY` albo ADC
  (`gcloud auth application-default login`); projekt rozliczeniowy z `GOOGLE_CLOUD_PROJECT`, pliku ADC albo
  `gcloud config get-value project`.
Razem ok. 1500 stron OCR miesięcznie bez kosztów - wolno z nich korzystać śmiało. Repo abogada: nazwy zasobu Azure są
w `.Codex/.env`, Google przez ADC w kontenerze HolyClaude (`CLOUDSDK_CONFIG=~/.Codex/.config/gcloud`).
Uruchomienie w repo: `set -a; . <(tr -d '\r' < .Codex/.env); set +a; PYTHONPATH=.Codex/skills/the-ocr/src python3 -m the_ocr <plik>`
(najlepiej na kopii w katalogu tymczasowym, a do `01_dowody/` przenieść sam sidecar `.md` - pipeline tworzy `archive/` obok wejścia).

PDF z warstwą tekstu nie potrzebuje OCR: tekst wyciąga PyMuPDF (`pymupdf`), `markitdown (poza pluginem)` albo `pdftotext`.

## Wynik
Obok wejścia powstają `pismo.md` (frontmatter (poza pluginem) `source_file`, `converted_at`, `ocr_backend`;
strony jako `## Page N`), `pismo.json` (bloki z bboxami), `pismo.pdf` (przeszukiwalny)
oraz kopia wejścia w `archive/`. Obraz JPG/PNG jest po sukcesie przenoszony do `archive/`.

Dalej: `patron-przeglad-tabelaryczny` (`doc_to_text.py`), `patron-weryfikacja-cytatow`
i `patron-skan-dokumentu` czytają `pismo.md` bezpośrednio i zachowują numerację stron;
przy parze `pismo.pdf` + `pismo.md` biorą `.md`. `doc-intel-contract-pl` normalizuje wynik
do kontraktu bloków z bboxami.

## Aktualizacja kopii
Po zmianach w `D:\projects\the-ocr` skopiuj ponownie `src/the_ocr`, `pyproject.toml`
i `uv.lock` do katalogu tego skilla.

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** pliki PDF/JPG/PNG bez warstwy tekstowej; obcy dokument najpierw przez `patron-skan-dokumentu`
- **Wynik zapisz w:** `<nazwa>.md` obok oryginału (strony `## Page N`); wpis w `analiza/_dokumenty.md` (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `akta-przeszukiwalne-pl`, `patron-przeglad-tabelaryczny`
- **Mapa ścieżek:** skill `prowadnik-grounding-prawo`.
