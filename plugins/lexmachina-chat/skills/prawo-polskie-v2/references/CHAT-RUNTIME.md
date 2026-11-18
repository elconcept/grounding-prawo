# CHAT-RUNTIME — prawo-polskie-v2 v6.73, nakładka 0.5.0

Status: **wydanie przejściowe etapu 3/8**; nie jest to potwierdzenie, że wszystkie DR zostały już scalone ani że aktywna sesja ChatGPT odświeżyła skill. Źródło: `../SKILL.upstream.md`, mapa bajt w bajt: `../ROUTING-MAP.md`.

## Niezmienna architektura LexMachina

`prawny-router-v3` → **ta fasada** → konkretny DR i jego moduł → wykonawca/raport. Zachowuj wybór PRIMARY/SECONDARY/FALLBACK dokonany przez router [1]–[11]. Przypisanie DR wybiera wyłącznie źródłowy `Routing błyskawiczny` oraz `ROUTING-MAP.md`. Nie ładować pełnej mapy 154 KB przy każdym zapytaniu, lecz odpowiedni fragment wskazany przez przypadek.

## Bramka dostępności

- `IN_BUNDLE`: rozpoznany DR jest faktycznie dołączony do tego samego wydania (na etapie 3 brak większości docelowych DR).
- `EXTERNAL_READ`: właściwy DR jest w osobnej zainstalowanej wtyczce i **został rzeczywiście odczytany**.
- `PLANNED`: DR ma trafić do docelowego 26-skillowego bundla, ale nie został jeszcze załadowany w tej wersji.
- `OUT_OF_BUNDLE`: historyczna mapa wskazała DR-04/06/07/08/09/15; **nie zmieniaj** decyzji na inny DR tylko dla uniknięcia komunikatu.
- `NOT_AVAILABLE`: potrzebnego DR/źródła nie odczytano lub brak go w hostowanej sesji. Nie deklaruj wykonanego raportu jego metodą.
- Do wyniku dołącz dane `selected_dr`, `original_alias`, `resolved_slug`, `module`, `availability`, `source_version`, `law_verification`.

## Reżim źródeł i czasu

Wybór domeny nie wymaga odpytania Repertorium. Powołanie konkretnego artykułu, numeru Dz.U., statusu wejścia w życie lub wyroku wymaga osobnego świeżego odczytu miarodajnego tekstu, z datą; inaczej `NOT_CHECKED`. Mapa zawiera historyczne metadane i oznaczenia `✅ OK`/`MONITORING`, które **nie są** pomiarem dzisiejszego stanu prawa. Weryfikuj wersję na datę zdarzenia i datę czynności, także przepisy przejściowe.

## Synergia ze shared i routerem

Zasób `shared/HIERARCHIA-ZRODEL.md`, `shared/PRAWO-HARDGATE.md`, `shared/FACT-SOURCE-LOCK.md`, `shared/LEGAL-STATUS-LOCK.md`, odczytuj selektywnie. Nie preferuj relacji Policji lub szpitala na podstawie formy urzędowej. W tekście odróżnij relację strony, twierdzenie dokumentu, dane obiektywne, wniosek i zamiar. Zapis do Basic Memory/Git, test CLI, automatyczny podgląd plików i zapytania MCP są opcjonalne, gdy istnieje realne narzędzie i użytkownik powierzył zadanie.

Bezpośrednie wywołanie fasady poza routerem ma skierować do `prawny-router-v3`, nie udawać, że pierwotny router już działał.
