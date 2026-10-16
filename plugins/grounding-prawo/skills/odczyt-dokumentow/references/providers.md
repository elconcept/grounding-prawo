# Providery

Narzędzie the-ocr jest dołączone w `tools/the-ocr/`. Konwerter używa jego adapterów i providerów, bez zmieniania
źródłowego PDF i bez generowania drugiego OCR. Wszystkie ścieżki kończą się tym samym kontraktem.

- Datalab: `DATALAB_API_KEY`; obsługiwany przez istniejący provider Datalab.
- Azure Document Intelligence: `AZURE_DOCUMENT_ENDPOINT` i `AZURE_DOCUMENT_KEY`, albo
  `AZURE_DOCUMENT_RESOURCE` i zalogowane `az`. Dzielenie PDF na żądania obsługuje provider.
- Google Cloud Vision: `GOOGLE_VISION_API_KEY` albo `gcloud` z Application Default Credentials.
- LlamaParse pozostaje opcjonalnym fallbackiem istniejącego the-ocr; wymaga pakietu `llama-cloud`.

Bez `--provider` działa `THE_OCR_CHAIN`, domyślnie datalab,llamaparse,azure-di,google-vision.
Wybór `--provider azure-di` lub `--provider google-vision` jest zwykłym trybem pracy, nie diagnostyką.
Limity i rozliczenia ustala konto providera; narzędzie nie zna pozostałej puli miesięcznej.

Nieznana confidence pozostaje null. Brak bbox pozostaje null. Kontrakt nie podwyższa jakości odczytu;
jedynie zachowuje wynik, pochodzenie i ograniczenia. Wyniki OCR porównuj z oryginałem przy cytowaniu.
