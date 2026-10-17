# Providery

Narzędzie the-ocr jest dołączone w `tools/the-ocr/` (kopia kodu z repozytorium `elconcept/the-ocr`, budowana
przez `scripts/build.py` z submodułu `vendor/docs/the-ocr`; opis: `tools/the-ocr/README.md`). Konwerter używa jego
łańcucha providerów i adapterów, bez zmieniania źródłowego PDF i bez generowania drugiego OCR. Wszystkie
ścieżki kończą się tym samym kontraktem.

- Datalab: `DATALAB_API_KEY` (albo regionalne `DATALAB_API_KEY_EU`/`_US`).
- LlamaParse: `LLAMA_CLOUD_API_KEY`; wymaga pakietu `llama-cloud`.
- Azure Document Intelligence: `AZURE_DOCUMENT_ENDPOINT` i `AZURE_DOCUMENT_KEY`, albo `AZURE_DOCUMENT_RESOURCE`
  i zalogowane `az`. PDF idzie paczkami po 2 strony (limit F0), składanymi w jeden wynik.
- Google Cloud Vision: `GOOGLE_VISION_API_KEY`, plik konta usługi `GOOGLE_VISION_CREDENTIALS` albo `gcloud`
  z Application Default Credentials.

Bez `--provider` działa `THE_OCR_CHAIN`, domyślnie `datalab,llamaparse,azure,google_vision`.
`--provider azure` (alias `azure-di`) lub `--provider google_vision` (alias `google-vision`) to zwykły tryb pracy,
nie diagnostyka. Limity i rozliczenia ustala konto providera; narzędzie nie zna pozostałej puli miesięcznej.

Bez lokalnego środowiska ten sam łańcuch jest dostępny jako konektor `ocr` portalu `lex` (serwer mcp-ocr,
zob. `SKILL.md`).

Nieznana confidence pozostaje null. Brak bbox pozostaje null. Kontrakt nie podwyższa jakości odczytu;
jedynie zachowuje wynik, pochodzenie i ograniczenia. Wyniki OCR porównuj z oryginałem przy cytowaniu.
