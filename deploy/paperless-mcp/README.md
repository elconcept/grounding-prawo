# Paperless MCP przez Lex

Gotowy serwer [OrellBuehler/paperless-mcp](https://github.com/OrellBuehler/paperless-mcp), wersja 1.4.1.
Konto Paperless `mcp-reader` ma wyłącznie uprawnienia `view_*`. Nie uruchamiamy drugiego indeksu embeddingów.

```sh
sudo docker compose --env-file /workspace/docker/mcp-paperless/.env \
  -f deploy/paperless-mcp/compose.yaml -p mcp-paperless up -d
```

Plik `.env` poza repo zawiera `PAPERLESS_TOKEN` konta `mcp-reader` (tryb 0600).
Serwer nie publikuje portu hosta; używa sieci `cf_paperless`, istniejącej usługi `10.0.10.201:8010` (host dozwolony przez Paperless) i tunelu `ds1821`.
`mcp-paperless.xlap.pl/mcp` chroni Cloudflare Access: aplikacja `Paperless MCP — Lex only`,
polityka Service Auth z tokenem `lex-paperless-mcp` (ważny do 18.10.2027; odnowić przed wygaśnięciem).
Portal `lex-prawo` przekazuje token Access i token Paperless w statycznych nagłówkach serwera `paperless`.
Sekrety przechowuje Cloudflare; nie umieszczaj ich w repo ani logach.
Portal udostępnia wyłącznie wybrane narzędzia odczytu. Uprawnienia konta Paperless są drugą granicą dostępu.

Test wdrożenia: inicjalizacja MCP, tools/list, wyszukanie i odczyt dokumentu kontem `mcp-reader`,
oraz odmowa połączenia bez nagłówków Access. Po zmianie konfiguracji odśwież połączenie `lex` w kliencie.
Rollback: odłącz `paperless` od `lex-prawo`, zatrzymaj ten stos (`compose down`),
usuń wyłącznie jego wpis tunelu, DNS, aplikację i token Access. Dokumenty Paperless pozostają nietknięte.
