# Ingest wiki i zależność Basic Memory

`vendor/general/basic-memory` to submoduł kanonicznego repo `elconcept/basic-memory`.
Przypięta rewizja zawiera `wiki_ingest` i `wiki_plan`; nie używaj dawnej nazwy repo
`mcp-basic-memory` jako odrębnego źródła. Zmianę zależności weryfikuj przez git i gh.

Submoduł dostarcza kod serwera i dokumentację wdrożenia. Nie jest kopiowany do paczki
skilli i sam nie uruchamia MCP. Hosty claude.ai oraz chatgpt.com korzystają z wdrożonego
serwera przez skonfigurowany konektor. Lokalny shell klienta nie jest wymagany do ingestu.

1. Wdróż przypiętą wersję Basic Memory według `vendor/general/basic-memory/docs/wiki-ingest-migration.md`.
2. Przypisz katalog źródeł do UUID projektu oraz skonfiguruj montowania i połączenie the-ocr.
3. Potwierdź akcje `inspect_page` i `verify_page` oraz obrazy stron PDF. Sprawdź `tools/list`, podręczniki `wiki-ingest` i `wiki-plan` oraz pełny przepływ na źródle testowym.
4. Zainstaluj grounding-prawo 0.4.1; użyj `ingest-wiki`. Do składu lokalnej teczki służy `teczka-sprawy`.
5. Przełącz workspace legal na konfigurację `.agents` dopiero po sprawdzeniu narzędzi serwera.

Aktualizacja checkoutu: `git submodule update --init vendor/general/basic-memory`.
Przy zmianie przypięcia uruchom testy ingestu w Basic Memory i walidatory pluginu.
Nie kopiuj do tego repo dokumentów ani danych konkretnych spraw.

## Wdrożenie kontroli PDF — 2026-10-18

Basic Memory PR #2 scalony jako `15c7f157f1fdbfabbfcae5c0515f85a7d47093a2`.
Aktywny kontener NAS: `mcp-basic-memory:pdf-review-15c7f157`, status healthy.
Obraz zbudowano z dotychczasowego obrazu wdrożeniowego oraz źródeł i lockfile tej
rewizji; `uv sync --locked --python 3.13` doinstalował PyMuPDF. Poprzedni obraz
`mcp-basic-memory:wiki-ingest-f834fbbe` i kopia konfiguracji compose
`docker-compose.yml.before-pdf-review-20261018` pozostały do wycofania zmiany.

Przez działające MCP, w osobnym projekcie `wiki-ingest-smoke`, sprawdzono syntetyczny
PDF bez warstwy tekstowej: oryginał zawierał 123 PLN, sidecar błędne 999 PLN i komentarz.
`start` zatrzymał publikację; `inspect_page` dostarczył obraz; `verify_page` przyjął
poprawioną transkrypcję. Kolejne start/read/finish/index potwierdziły zapis 123 PLN
bez komentarza. To test techniczny ze znaną treścią, nie kontrola rzeczywistych akt.

Nowa rozmowa klienta musi odświeżyć plugin i schemat narzędzi. Synchronizacji konta
claude.ai/chatgpt.com nie potwierdza test bezpośredniego endpointu MCP.
