# Ingest wiki i zależność Basic Memory

`vendor/mcp/basic-memory` to submoduł kanonicznego repo `elconcept/basic-memory`.
Przypięta rewizja zawiera `wiki_ingest` i `wiki_plan`; nie używaj dawnej nazwy repo
`mcp-basic-memory` jako odrębnego źródła. Zmianę zależności weryfikuj przez git i gh.

Submoduł dostarcza kod serwera i dokumentację wdrożenia. Nie jest kopiowany do paczki
skilli i sam nie uruchamia MCP. Hosty claude.ai oraz chatgpt.com korzystają z wdrożonego
serwera przez skonfigurowany konektor. Lokalny shell klienta nie jest wymagany do ingestu.

1. Wdróż przypiętą wersję Basic Memory według `vendor/mcp/basic-memory/docs/wiki-ingest-migration.md`.
2. Przypisz katalog źródeł do UUID projektu oraz skonfiguruj montowania i połączenie the-ocr.
3. Sprawdź `tools/list`, podręczniki `wiki-ingest` i `wiki-plan` oraz pełny przepływ na źródle testowym.
4. Zainstaluj grounding-prawo 0.4.0; użyj `ingest-wiki`. Do składu lokalnej teczki służy `teczka-sprawy`.
5. Przełącz workspace legal na konfigurację `.agents` dopiero po sprawdzeniu narzędzi serwera.

Aktualizacja checkoutu: `git submodule update --init vendor/mcp/basic-memory`.
Przy zmianie przypięcia uruchom testy ingestu w Basic Memory i walidatory pluginu.
Nie kopiuj do tego repo dokumentów ani danych konkretnych spraw.
