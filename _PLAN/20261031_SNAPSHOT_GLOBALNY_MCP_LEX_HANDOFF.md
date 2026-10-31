# GLOBALNY SNAPSHOT / HAND-OFF — pełen ekosystem MCP portalu LEX

**Data:** 31.10.2026 (Europe/Warsaw).  
**Cel:** niezależny model ma skontrolować całość prac w tym oknie kontekstowym, faktyczny stan 8 MCP w `lex`, dodatkowe REPERTORIUM, proponowaną architekturę, wykonane commity/PR-y, luki, testy i bezpieczną migrację.  
**Status:** dokument audytowy, nie wdrożenie. Dane źródłowe: odczyt `mcp__lex__portal_list_servers`, katalog `codemode.tools()`, Portainer Docker env=3, GitHub PRs/Actions, wcześniejsze read-only próby REPERTORIUM/USTAWY.

> **Nadrzędny zakaz:** REPERTORIUM działa; nie zmieniać jego kodu, kontenera, bazy, indeksu, obrazu, osobnego endpointu, routingu ani polityk w celu „naprawy”. Zmiany w innych usługach mogą tylko bezpiecznie SKORZYSTAĆ z istniejącego REPERTORIUM po odczytowym sprawdzeniu dostępu. Nie wdrażać niczego przed testem staging i planem rollbacku.

## AKTUALIZACJA — rzeczywista naprawa przypisania REPERTORIUM do Cloudflare lex (31.10.2026)

**Stan PO naprawie (nowszy niż historyczne pomiary 8/56 w dalszej części dokumentu):**

1. **Ustalona przyczyna:** zarejestrowany serwer `repertorium-oauth` w Cloudflare MCP Servers: `https://repertorium.xlap.pl/mcp`, OAuth `connected`, status `ready`, 1 tool. Nie był przypisany do portalu `lex-prawo` (`lex.xlap.pl`), w którym znajdowało się tylko 8 serwerów. Nie było awarii kontenera ani potrzeby tworzenia nowego serwera/tokena/polityki.
2. **Poprawka WYKONANA:** przez Cloudflare API w istniejącym `lex-prawo` dopisano serwer `{server_id: "repertorium-oauth", on_behalf: false, default_disabled: false}`. Zachowano wszystkie 8 upstreamów, ustawienia serwerów, overrides BASIC-MEMORY/UODO, nazwę/hostname, `code_mode=default_on` i polityki. Nie zmieniano REPERTORIUM, jego kontenera, URL, kodu, bazy ani sesji OAuth administratora.
3. **Weryfikacja administracyjna PASS:** odczyt ponowny portalu przez Cloudflare API: **9 serwerów, wszystkie `ready`**, REPERTORIUM OAuth `connected`, `on_behalf=false`, 1 narzędzie. Suma potencjalnych tools: **57**, nie zmniejszono ich jeszcze, ponieważ resolver nie jest gotowy.
4. **Aktualny konektor ChatGPT:** `portal_list_servers` w starej sesji nadal zwraca **8 serwerów i 56 tools**. Próba `portal_toggle_single_server` zwróciła sprzeczny błąd „ID not found” z listą zawierającą już nowe REPERTORIUM. Inicjowano `portal_toggle_servers`: jednorazowy link do selektora serwerów został przekazany użytkownikowi, ale **nie zakończono** interakcji. Nie publikować jednorazowego linku w repo. Użytkownik powinien włączyć REPERTORIUM w selektorze/odświeżyć grant i wtedy ponownie sprawdzić narzędzia z klienta.
5. **Status całego zadania:** naprawione przypisanie administracyjne; **NIE POTWIERDZONO** jeszcze skutecznego `tools/call` przez bieżące połączenie `lex`. To są dwa różne kryteria odbioru. Nie deklarować pełnego E2E przed próbą narzędzia. Nie rozwiązywać problemu restartem Repertorium ani tworzeniem nowego OAuth upstream.

**Nowy test odbioru:** po selektorze serwerów, `portal_list_servers` / `codemode.tools()` powinny wykazać `MCP REPERTORIUM` + narzędzie `szukaj_repertorium`, a jedno kontrolne zapytanie ma zwrócić identyfikatory. Potwierdzić osobny direct endpoint read-only i brak powtórnej upstream-autoryzacji użytkownika. Docelowe 2 tools dopiero po wdrożeniu resolvera.

## 1. Jednozdaniowy efekt docelowy

**W prawnym portalu `lex` model widzi tylko dwa narzędzia: istniejące `szukaj_repertorium` (bez zmian) i nowe `pobierz_dokument` (minimalny resolver), podczas gdy wszystkie dotychczasowe MCP pozostają niezależnymi, wewnętrznymi backendami, preferując lokalne korpusy i trwały cache przed zewnętrznymi API/Playwright.**

Nie scalać EU-SPARQL i EU-COMPLIANCE w monolit. Nie likwidować SAOS, NSA, KRS, UODO, USTAWY, EU, Basic Memory. Usunąć z *widocznego katalogu prawniczego*, nie z infrastruktury. Operacje specjalistyczne niewidoczne w dwóch narzędziach (np. cytator SAOS, analiza compliance, zapisy BASIC-MEMORY) zachować pod osobnym dostępem lub odpowiednią wąską drogą wewnętrzną — nie obiecywać bez dowodu pełnej parytetowości 56 obecnych funkcji.

## 2. Zmierzony stan obecny

### 2.1. Aktualny portal LEX i uruchomione kontenery

| Serwer | Widoczne narzędzia | Stan na `lex` | Stan NAS/Portainer | Działanie, które wymaga uwagi |
|---|---:|---|---|---|
| BASIC-MEMORY | **29** | enabled | `mcp-basic-memory` running, port 8401 | ingest, notatki, wiedza; duży narzut kontekstu, weryfikacja modelu e5-small/384D |
| EU-COMPLIANCE | **5** | enabled | `mcp-eu-compliance` running, 8409 | SQLite FTS5 14 regulacji UE, korpus EN; w portalu zdarza się utrata pola tekstu odpowiedzi |
| EU-SPARQL | **5** | enabled | `mcp-eu-sparql` running, 8408 | CELEX, ECLI, TSUE, GDPRhub; PL/deduplikacja wymagają poprawek |
| KRS | **3** | enabled | `mcp-krs` running, 8407 | odpis aktualny/pełny, status i historia wpisów |
| NSA | **3** | enabled | `mcp-nsa` running, 8405 | CBOSA, socket/TLS, paginacja pełnego orzeczenia |
| SAOS | **4** | enabled | `mcp-saos` running, 8402 | lokalny mirror, API fallback, `get_judgment`, `cite_check`; kontrola kompletności |
| UODO | **3** | enabled | `mcp-uodo` running, 8403 | decyzje UODO, dokładna sygnatura i bardzo długie uzasadnienia |
| USTAWY | **4** | enabled | `mcp-ustawy` running, 8412 | lokalne 37 aktów, artykuły + komentarze; nie pełne archiwum Dz.U. |
| **RAZEM** | **56** | **8 enabled** | **8 running** | „running” nie oznacza, że tekst i cytowania są poprawne |

**Repertorium:** `mcp-repertorium` **running**, host port 8410, istniejący serwer MCP odpowiada na wcześniejsze zapytania; **brak** na liście aktualnych 8 upstreamów `lex` i brak jego toola w katalogu portalu. To **różnica dostępności portalu, nie dowód usterki Repertorium**. Nie naprawiać działającej usługi. Poza tym `mcp-ocr` running (8411), ale nie ma go w tych 56 tools.

**Nie widać nowych kontenerów** `mcp-prawo-resolver` ani `webwright-legal-pl`; nie doszło do staging/deploy. Nowy wrapper jest kodem na gałęziach. Portal `ai.xlap.pl/mcp` i niezależne serwery nie są tożsame z katalogiem `lex`. Istnieje oczekiwanie zachowania osobnego dostępu `repertorium.xlap.pl/mcp`; nie stwierdzono tu niezależnym testem, że działa z docelową polityką Access.

**Narzut schematów:** około **79 376 znaków** opisów/nazw/JSON inputSchema obecnych 56 tools w wcześniejszym pomiarze. To nie jest dokładna liczba tokenów każdego modelu. BASIC-MEMORY odpowiada za 29 z 56 tools; docelowo powinien być udostępniony poza minimalistycznym portalem prawnym, ale **bez wyłączania funkcji lub utraty dostępu do notatek**.

### 2.2. Co zwraca REPERTORIUM

Read-only zapytania wykonane do działającego MCP:
- `art. 23 ustawy o ochronie zdrowia psychicznego` → 8 wyników, m.in. `eli:DU/2024/917`, `saos:166511`, `nsa:389F2C5B67`, `sn:hFvgRJcBZvGrB8P_afyJ`.
- `RODO art. 33` (jurysdykcja eu) → 9 wyników, m.in. `celex:32016R0679:pl`, inne CELEX i EDPB.
- `Dz.U. 2024 poz. 917`, `II SA/Wa 1353/19` → prawidłowy numer/sygnatura występuje, lecz obok są niepowiązane trafienia.

Odpowiedzi zawierają ID, tytuł, datę, snippet, źródło/adres. **To wyszukiwarka semantyczna**, nie dowód, że każdy wynik rozstrzyga dokładnie wskazany artykuł. ID `sn:...` jest opaque ID Repertorium, nie zawsze ID z publicznego serwisu. URL wynikowy `celex:...:pl` może wskazywać EN: język trzeba kontrolować osobno. Nie modyfikować Repertorium ani nie opierać na nim pełnego tekstu.

## 3. Kontrakt docelowy i wewnętrzny routing

**Model-facing:** `szukaj_repertorium(q, jurysdykcja?)` do szukania zagadnień; `pobierz_dokument(identyfikator, artykul?, strona?, sygnatura?, na_dzien?)` do bezpośrednich ID. `jurysdykcja` oznacza PL/EU, **nie wybór języka**. Wszystkie odpowiedzi/opisy po polsku, bez `lang` w publicznych schematach. Nie wystawiać wewnętrznych tooli Webwright.

**Kolejność dla konkretnego ID:** (1) adekwatny lokalny korpus MCP, (2) lokalny zweryfikowany cache po pełnym kluczu: źródło + ID + wersja + język + data stanu, (3) fallback oficjalny API/Cellar/Playwright tylko przy braku, (4) kontrola tożsamości, wierności, kompletności, legalnej wersji, (5) trwały zapis oryginału/ekstraktu/metadanych/SHA, (6) ponowny odczyt z dysku bez internetu.

**Odpowiedź:** identyfikator i pochodzenie, dokładna wersja/stan na dzień, urzędowy adres, typ i organ, treść **określonego fragmentu**, długość, `next_offset`/`has_more`, oddzielne `source_fully_stored` i `response_partial`, `text_fidelity`, `legal_currency`, `official_status`, suma SHA PDF oraz SHA ekstraktu. Błąd usługi nie może wyglądać jak „nie znaleziono”. Snippet/strona logowania/potwierdzenie linku **nie są** kompletnym dokumentem.

| Rodzaj źródła | Lokalna ścieżka | Fallback i zapis | Luka aktualnego prototypu |
|---|---|---|---|
| DU/M.P., artykuł/`, ELI | USTAWY SQLite/MCP + cache | ELI HTML lub **PDF-only**; import pełnego tekstu z walidacją | PDF-only dziś kończy się linkiem; USTAWY obejmuje 37 aktów/artykuły bez gwarancji załączników |
| SAOS ID / sygnatura | istniejący mirror SAOS + cache fragmentów | API przez obecny SAOS MCP | prawdziwa natywna paginacja, kompletność i identyczność offsetów |
| NSA ID 10-hex / sygnatura | lokalny cache + NSA MCP | CBOSA przez istniejący MCP | TLS/socket i nowy chunking tylko PR |
| KRS numer | KRS MCP odpis aktualny/pełny | istniejące oficjalne źródło KRS | **brak adaptera `krs:`** w nowym `slim_resolver.py` |
| UODO sygnatura / ID decyzji | UODO MCP / lokalny cache | istniejąca usługa UODO | **brak adaptera `uodo:`** w resolverze, długie uzasadnienia |
| CELEX/RODO/AI Act/inne akty UE | zweryfikowany lokalny **PL** corpus + wersjonowany cache | **CELLAR PL XHTML/XML** → ewent. Webwright EUR-Lex PDF | EN korpus EU-COMPLIANCE nie nadaje się do urzędowego cytatu PL; ETL PL niegotowe |
| ECLI, orzeczenia TSUE | lokalny cache pełnych PL orzeczeń | EU-SPARQL/CELLAR → pełny tekst | metadata ECLI ≠ pełny tekst wyroku |
| SN opaque-ID / sygnatura | cache ze zweryfikowanym mapowaniem | wewnętrzny Webwright SN, PDF | nie wolno promować PDF tylko na podstawie wystąpienia sygnatury |
| MS, TK | przyszły lokalny cache | przyszłe adaptery Webwright dla ms.gov.pl i trybunal.gov.pl | **nie ma adapterów** w skopiowanym skillu autora |
| EDPB / GDPRhub | cache oryginalnych decyzji | EDPB PDF / GDPRhub jako wtórny tekst | brak pełnego adaptera, trzeba wskazywać urzędowe pochodzenie |
| EUREKA / inne ID Repertorium | cache i istniejące zgodne serwisy | urzędowy dokument po mapowaniu | nie wymyślać URL na podstawie opaque ID |
| BASIC-MEMORY (notatki) | osobna ścieżka wiedzy, np. `ai` | istniejące 29 tools | NIE przepinać write/delete do publicznego resolvera |

Specjalistyczne funkcje nie są usuwane: `saos_cite_check`, `eu_compare/evidence`, historia KRS, zarządzanie Basic Memory mogą być dostępne wewnętrznie lub w innym kontekście. Decyzja o **dwóch** publicznych toolach wymaga świadomego zdefiniowania pokrycia, nie fikcyjnej pełnej parytetowości 56 narzędzi.

## 4. CO JUŻ ZROBIONO W TYM OKNIE KONTEKSTOWYM (tylko fakty)

Użyto konektorów GitHub, lex, Portainer/Synology. Zmiany zapisane na osobnych gałęziach/draft PR. **ŻADNEGO MERGE, żadnej zmiany produkcyjnego Cloudflare, żadnego restartu/zastąpienia produkcyjnych kontenerów, żadnej ingerencji w REPERTORIUM.**

### 4.1. Prace backendowe z pierwszego audytu

- W `elconcept/grounding-prawo` utworzono indeks indywidualnych planów: [`_PLAN/20261031_lex_indeks_planow_naprawczych.md`](https://github.com/elconcept/grounding-prawo/blob/main/_PLAN/20261031_lex_indeks_planow_naprawczych.md).
- **EU-SPARQL:** draft [PR #1](https://github.com/elconcept/mcp-eu-sparql/pull/1), gałąź `fix/lex-pl-mcp-20261031`, HEAD `c62d0abdd52537567da3d68c1d27ecb1fd339ce3`: stały PL, bez selektora języka, deduplikacja CELEX/ECLI, typy CJEU, testy offline. **CI success, CodeQL success** (runs 41143814976 i 41143814962), **bez deploy**.
- **KRS:** draft [PR #2](https://github.com/elconcept/mcp-krs/pull/2), HEAD `fef1ffeac8f28a21fe3c43a0326ab069323d00c8`: odpis aktualny jako źródło aktualnego statusu, pełna historia bezstratnie w chunkach. **CI success, CodeQL success** (41143821496, 41143821559), bez deploy.
- **NSA:** draft [PR #2](https://github.com/elconcept/mcp-nsa/pull/2), HEAD `7b1ea0e27e8989b9053b197c74e6244a8a65d6b2`: `get_judgment` offset/limit, metadane kontynuacji, testy. **CI success, CodeQL success** (41144040723, 41144040761), bez deploy; TLS bypass/socket hang up nadal wymagają osobnej bezpiecznej diagnozy.
- **BASIC-MEMORY:** historyczna poprawka `elconcept/basic-memory/docker-compose.nas.yml` commit `25eabcd371816fe332d65e5c940b87fc8477438d`: oznaczenie e5-small 384D zamiast e5-large; **brak potwierdzenia wdrożenia i reindeksacji**. Wymagany backup przed zmianami.
- **SAOS i UODO:** audyt, testy/plan problemów, bez wykazanego implementacyjnego PR w tej sesji. W REPERTORIUM wykonano wyłącznie read-only testy.

### 4.2. Projekt konsolidacji UE, później WYCOFANY architektonicznie

- **EU-COMPLIANCE** draft [PR #1](https://github.com/elconcept/mcp-eu-compliance/pull/1), HEAD `803bf8bb3abf3ef9e3a13f8ce411e704f3b1130a`, z 10 toolami (5 UE offline + 5 SPARQL live), fixturami, `structuredContent.text`, kontrolą 14 CELEX. **CI success** (run 41145843881). Jednak użytkownik później zdecydował **pozostawić oba serwery UE oddzielnie za resolverem**, więc **nie scalać tego PR**. Można selektywnie wykorzystać poprawki języka i testy, nie monolit.
- Stwierdzono przypadek `eu_compliance_eu_article`, w którym wywołanie przez portal Code Mode oddawało tylko `citations`, choć backend bezpośredni miał tekst. Trzeba zbadać surowe JSON-RPC na kolejnych warstwach; nie zakładać bez dowodu, że winny jest Cloudflare.

### 4.3. Analiza oryginalnego wrappera i PR #3

- Porównano Apache-2.0 [`matematicsolutions/prawo-pl-mcp`](https://github.com/matematicsolutions/prawo-pl-mcp) z `elconcept/mcp-prawo-wrapper`. Niektóre moduły (`server.py`, `pagination.py`, `audit.py`, `coverage.py`) identyczne; lokalny `pool.py` ma transport HTTP, `registry.py` dodatkowe źródło USTAWY. Mechaniczny cherry-pick całego repo odrzucony.
- **Wrapper draft [PR #3](https://github.com/elconcept/mcp-prawo-wrapper/pull/3)**, gałąź `fix/upstream-native-pagination-20261031`, HEAD `382d0aeb5a13be3f4bb5398c8f04c3d3a5a8273f`: `POOL.call_with_metadata` zachowuje `structured_content`; `pl_get_document` dla SAOS/NSA używa natywnego offset/limit i nie traktuje 2k znaków źródła jako kompletnego orzeczenia. Testy offline dopisane. **0 Actions runs** dla gałęzi, nie ogłaszać zielonego CI, bez deploy.

### 4.4. Minimalny resolver, USTAWY #81, Webwright i PDF — PR #4

- **Resolver draft [PR #4](https://github.com/elconcept/mcp-prawo-wrapper/pull/4)**, gałąź `feat/minimalny-resolver-repertorium-20261031`, HEAD ostatnio odczytany `a5fc343018257b7a203ce796226ec47bc9389755`. **PR #4 bazuje na gałęzi PR #3**, nie na `main`; 20 zmienionych plików przy ostatnim odczycie. **0 Actions runs**, brak Docker build/E2E/deploy.
- `src/prawo_pl_mcp/slim_resolver.py`: osobne FastMCP z **1 publicznym** `pobierz_dokument`, parser ELI/SAOS/NSA/CELEX/RODO/ECLI/SN/EDPB/MS/EUREKA, lokalne ścieżki plus fallback.
- `src/prawo_pl_mcp/local_corpus.py`: read-only lokalne USTAWY SQLite, trwały osobny cache `documents`/`fragments`/`candidates` i SHA-256; nie nadpisuje istniejących baz USTAWY/SAOS.
- `src/prawo_pl_mcp/browser_bridge.py` / `webwright_internal.py` / `webwright_asgi.py`: wewnętrzny MCP na fallback, bez tooli widocznych modelowi. Skopiowano z `matematicsolutions/awesome-matematic-skills-pl` rew. `e99b534` pliki `fetch_orzeczenie.py` (SN) i `fetch_eurlex.py` (CELEX) z licencją Apache-2.0; **oryginał nie ma MS/TK**.
- `src/prawo_pl_mcp/pdf_ingest.py`: heurystyczna kontrola URL/CELEX/sygnatury i `pypdf`, zapis oryginalnego PDF+ekstraktu+SHA. **To NIE dowodzi wiernego odczytu ani rzeczywistej zgodności ID wyroku.**
- `src/prawo_pl_mcp/slim_asgi.py`, `deploy/minimal-legal/compose.staging.yaml`, dwa Dockerfile, testy `tests/test_slim_resolver.py`, `test_local_corpus.py`, `test_pdf_ingest.py`. Przygotowana konfiguracja staging, lecz **nic nie uruchomiono**.
- **USTAWY draft [PR #81](https://github.com/elconcept/grounding-prawo/pull/81)**, gałąź `feat/eli-local-resolver-20261031`, HEAD `202de127458e1db75d7966f05b65cdaf9a557b79`. W `ustawy.py` i `ustawy_mcp.py` dodano `akt_po_eli(eli,offset,limit,art)`: lokalna SQLite po EXACT ELI, paginacja, `dokument_pelny=false` (artykuły bez gwarancji wszystkich załączników). **CI FAILED** [run 41149480617](https://github.com/elconcept/grounding-prawo/actions/runs/41149480617), job `build` step `plugins/ zgodny z buildem`: log wskazuje obowiązkowe `scripts/build.py` i commit wygenerowanego `plugins/`. Nie scalać przed zielonym CI.
- Testy faktycznie wykonane przez kontener pomocniczy: Python AST, parser 9 ID, mock SQLite exact ELI, SHA-256, fragmenty, testowy PDF; NIE były to pełne pytest ani live PDF/SN/EUR-Lex/ELI i nie są wdrożeniem.

### 4.5. Nowy zewnętrzny projekt: legal-cite-pl

- Audytowano Apache-2.0 [`apiotrowski-afk/legal-cite-pl`](https://github.com/apiotrowski-afk/legal-cite-pl) HEAD `2c4b7bf6e2af56b42b8b87a9bdbfe93d8078c988` (29.10.2026): `legal_cite/pdf_tj.py`, `core.py`, `na_dzien.py`, testy PDF i dat; zależność MIT `eli2md@v0.6.70` + Poppler `pdftotext`.
- Wartość do adaptacji: **wybór aktualnego tekstu jednolitego PRZED formatem**, obsługa ELI PDF-only, `eli2md` drzewo jednostek/odnośników, drugi niezależny czytnik `pdftotext`, test opuszczonych słów i porównanie ze starszym HTML; oddzielić wierność PDF od aktualności prawnej/nowelizacji; CELLAR PL XHTML + SPARQL wersji skonsolidowanych zamiast polegania na Playwright EUR-Lex.
- **Nie wykonano jeszcze cherry-pick legal-cite**, nie uruchomiono jego testów na NAS. `pdf_tj.py` ma powiązania z `core.py`, a `legal-cite` stosuje inne zależności MCP niż wrapper, więc rozważyć oddzielny wewnętrzny worker/adapter zamiast kopiowania wszystkiego.
- Szczegółowa analiza: [`mcp-prawo-wrapper/_PLAN/20261031_SNAPSHOT_AUDYT_legal_cite_pl_local_first.md`](https://github.com/elconcept/mcp-prawo-wrapper/blob/feat/minimalny-resolver-repertorium-20261031/_PLAN/20261031_SNAPSHOT_AUDYT_legal_cite_pl_local_first.md). Ten dokument jest **podrozdziałem** globalnego snapshotu, a nie jego zamiennikiem.

## 5. Krytyczne błędy / ryzyka jeszcze NIENAPRAWIONE

1. `lex` widzi **56 tools, nie 2**, a REPERTORIUM nie jest w jego katalogu. Nowy resolver nie jest zarejestrowany.
2. W PR #4 `_eli` gdy `textHTML=false` zwraca tylko PDF link. Nowe teksty jednolite PDF-only nie są rozwiązywane jako tekst.
3. `pdf_ingest` może podnieść flagę `dokument_pelny=true` po znalezieniu ID gdziekolwiek w PDF; może to być tylko cytowana sygnatura. Brak drugiego niezależnego czytnika i jakości wyciętych jednostek. Wymagana bramka przed `trusted_cache`.
4. `save_cache` przyjmuje pełny tekst ze słabą walidacją („źródło”, HTTPS, długość). Nie zapewnia semantycznej zgodności ID, aktualności, oficjalnej wersji ani kompletności załączników. Należy przechowywać wersje i odróżniać `full_source_stored` od `page_returned`.
5. `sn:opaque-id` Repertorium może zostać powiązane z PDF po podanej przez model sygnaturze, ale bez sprawdzenia relacji między tymi dwoma ID. **Nie promować** do zaufanej bazy bez mapowania.
6. `local_corpus.read_eu_pl(celex, artykul)` obecnie ignoruje argument artykułu i stronicuje cały akt; istniejący korpus EU-COMPLIANCE jest EN, nie PL. Wymaga osobnego polskiego ETL i drzew artykułów, wersji skonsolidowanych, dat.
7. `save_fragment` sprawdza długości z metadanych, ale nie dowodzi, że zserializowany tekst odpowiada surowemu chunkowi; źródłowe nagłówki/format mogą przesunąć offset.
8. Brak adapterów **KRS i UODO** w nowym resolverze pomimo obecności obu MCP w `lex`; brak pełnych ECLI, EDPB, EUREKA, MS, TK. Zachować zakres jako „niegotowe”, nie udawać pokrycia.
9. **CI:** USTAWY #81 RED; wrapper #3 i #4 NO RUNS. Zielone CI KRS/NSA/EU-SPARQL nie dowodzi E2E ani gotowości Cloudflare.
10. Basic Memory e5-small 384D: nie stosować migracji/reindex bez snapshotu, kontroli wektorów, testu przywracania.
11. Integrowanie 2 tools przez portal nie może zepsuć istniejących logowań, samodzielnego endpointu Repertorium ani pozostałych usług. Użytkownik nie chce nowych per-upstream Cloudflare policies ani dedykowanych service tokenów; istnieją polityki OAuth domeny laptopshop.pl i `ANY service token`, które należy zachować.
12. Zamiana problemów upstream/TLS/WAF na „brak danych” może prowadzić do fałszywych ustaleń prawnych. Brak tokenów/sterowania językiem w publicznych opisach nie zwalnia z poprawnej polskiej treści źródłowej.

## 6. Plan wdrożenia i kolejność (bez obietnicy gotowości produkcyjnej)

### FAZA 0 — snapshoty i read-only baseline
- Powtórz `portal_list_servers`/`tools/list`, mapę 8+REPERTORIUM, bezpośrednie testy MCP, sprawdź co wystawia Cloudflare i czy osobny endpoint Repertorium jest dostępny. Bez zmian tego serwera.
- Zabezpiecz backup aktualnego katalogu portalu/Access/routingu, obrazy po digestach, wolumeny SQLite i indeksy. Potwierdź możliwość rollbacku. Nie opieraj się tylko na tagu `latest`.
- Zbuduj fixtures odpowiedzi i zakresy: USTAWY `DU/2024/917 art.23`, `kpk/171`, SAOS `166511`, NSA `389F2C5B67`, KRS `0000028860`, UODO `DKE.561.5.2026`, RODO `32016R0679` art.33, ECLI, SN, MS, TK.

**Gate 0:** backup i odtwarzalne próbki; w prod zero zmian.

### FAZA 1 — source backend integrity i zielone CI
- USTAWY #81: uruchom `scripts/build.py`, dołącz wygenerowane `plugins/` i `.agents` zgodne z buildem, przetestuj `akt_po_eli`, dopiero po zielonym workflow rozważ merge i staging źródła.
- Wrapper #3: dodaj workflow/testy; przebiegnij 1,2,ostatni chunk SAOS/NSA; weryfikuj `content` i `structuredContent`; bez fałszywego `has_more=false`.
- NSA #2: zweryfikuj/napraw problem TLS/socket hang up na staging; nie wyłączać w ciemno walidacji certyfikatów. KRS #2 i EU-SPARQL #1: po istniejącym zielonym CI osobne E2E na staging.
- SAOS: zachowaj jego mirror i citator; UODO: uczyń długie decyzje stronicowalnymi lub udowodnij kompletność. Basic Memory: bez ingerencji w dane do czasu kopii.

**Gate 1:** stabilne źródła, pełne fragmenty, CI green i smoke oficjalnych źródeł.

### FAZA 2 — resolver 1-tool local-first
- Dokończ adaptery **KRS/UODO** i deterministyczne ID z Repertorium; dopracuj mapowanie sygnatura/opaque ID, ECLI, EDPB i pozostałe. Pytanie z dokładnym numerem ma iść do resolvera, nie do wyszukiwarki.
- Wymuś: local USTAWY/SAOS/NSA/EU PL → cache → oficjalny fallback tylko przy miss; write-through do osobnej trwałej bazy z pełnym provenance i wersją.
- Zabezpiecz parser i cache: link/snippet/strona wyszukiwania/wątpliwy PDF to `candidate`, nie trusted document. Wprowadź negatywny TTL, pojedyncze pobranie na identyczny ID, limity długości i budżet sieci.
- Testy niezależne od sieci: cache HIT = 0 fetch; MISS -> zapis -> restart -> HIT; niezgodny hash, brakujące słowa, obcy ID i fragment odrzucone.

**Gate 2:** jedno MCP `pobierz_dokument` działa na staging z rzeczywistymi lokalnymi bazami.

### FAZA 3 — PDF i polskie UE
- Adaptuj *selektywnie* `legal-cite-pl` + przypięty `eli2md@v0.6.70`, `pdftotext`: wersja tekstu jednolitego, strukturalny art./`, drugi czytnik, odnośniki, HTML comparison, aktualność po nowelizacjach. Nie wyświetlaj starej wersji jako aktualnej.
- Dla UE: lokalny urzędowy PL corpus, CELLAR PL XHTML/XML jako fallback **przed** Webwright; konsolidacja CELEX `0...-data` odróżniona od tekstu pierwotnego `3...`; ECLI wyroków to osobna ścieżka.
- Dla SN/MS/TK: niezależny parser orzeczeń, PDF+SHA, sygnatura **w nagłówku**, data/sąd/sentencja/uzasadnienie, dwuczytnikowa kontrola tekstu. Webwright ma na razie tylko SN i EUR-Lex, a MS/TK wymagają implementacji i realnych fixtures. Skan PDF -> `requires_ocr`, jawny status niezweryfikowanego OCR.
- Trzymaj raw PDF, ekstrakt, raport jakości i wersję konwertera lokalnie; oddziel autentyczne źródło od nieurzędowego odczytu.

**Gate 3:** testy ELI PDF-only, CELEX/RODO PL, SN pełny PDF i wymaganych orzeczeń; brak fałszywych „verified”.

### FAZA 3A — INTEGRACJA legal-cite-pl: kod, zależności, kontrakt i bramki (NIE TYLKO REKOMENDACJA)

**Cel implementacyjny:** zdolność pobrania, odczytania, zweryfikowania wierności i utrwalenia **pełnego PDF ELI** (także gdy API nie ma HTML) oraz poprawnego odczytu odpowiednich artykułów i wersji obowiązujących na zadany dzień. Projekt `apiotrowski-afk/legal-cite-pl` SHA `2c4b7bf6e2af56b42b8b87a9bdbfe93d8078c988` należy *zaadaptować modułowo*, a NIE dodawać jego publicznych `verify_article`/`list_acts` do portalu (limit 2 tools).

**Moduły i dokładny zakres adaptacji:**

| Źródło legal-cite | Co przenieść i gdzie | Weryfikacja |
|---|---|---|
| `legal_cite/pdf_tj.py::odczyt` oraz `_konwertuj` | worker `pdf-legal-ingest` (biblioteka/proces wewnętrzny). Przyjmuje **już pobrane bajty/ścieżkę do PDF** z resolvera/Webwright; rezygnuje z dodatkowego HTTP GET. `eli2md@v0.6.70`, hash oryginału, wersja konwertera | SHA + reprodukowalny Markdown + liczba stron i granice art./` |
| `pdf_tj.py::_warstwa`, `_tokeny_pdftotext`, `wiernosc_pdftotext`, `wyjasnienia_warstwy` | drugi niezależny czytnik `poppler-utils/pdftotext`; kontrola słów i ich kolejności względem `eli2md`, raport różnic | missing/swap/duplicate token => FAIL lub REVIEW, nie VERIFIED |
| `pdf_tj.py::jednostki_md`, `przypisy_md` | strukturalny indeks `akt, wersja, artykul, paragraf, przypis, tekst`; rozróżnienie bieżących/przyszłych wariantów jednostek | poprawne numery `117^1`, `479^61`, `23`, `33` i brak zlepienia dwóch brzmień |
| `core.py::_teksty_jednolite`, `_nowelizacje_po`, `_aktualnosc_pl` | osobny moduł **wersjonowania i aktualności**; wybór publikacji vs t.j. wg żądanej daty **przed** wyborem HTML/PDF; zmiany skuteczne i przyszłe | najnowszy t.j. PDF-only, starszy HTML, data wejścia zmian, brak fikcyjnej aktualności |
| `core.py::_wersja_eu`, `_fetch_eu`, `extract_eu_article` | adapter CELLAR dla polskiego CELEX/RODO/AI Act, konsolidacji `0...-YYYYMMDD` i XHTML; preferowany przed przeglądarką | tekst `RODO art. 33` po polsku z właściwej wersji; EN → FAIL |
| `testy/pdf_wiernosc.py`, `testy/wiernosc_warstwy.py`, `testy/krzyzowa.py`, `testy/awaria_html_pdf.py` | adaptacja danych testowych i negatywnych przypadków do własnego pytest/CI; nie kopiować bezrefleksyjnie wyników autorów | testy offline + real ELI w staging PASS |

**Izolacja zależności:** legal-cite jest Apache-2.0, eli2md MIT (tag `v0.6.70`, pin również SHA), Poppler w dedykowanym obrazie/warstwie; źródło ma zależności od `core.py` i starszego MCP niż FastMCP 3.x wrappera. Nie kopiować całego `core.py` jako niezależnej nowej publicznej usługi bez audytu. Minimalny worker z wewnętrznym API (lub moduł uruchamiany poza procesem MCP) jest preferowany, jeśli wynik testów wykaże konflikt zależności. Nie dodaje nowych publicznych tools.

**Kontrakt lokalnego magazynu:** pełny klucz `source_id + document_id + version_id + language + valid_on`, raw PDF i SHA-256, wyciąg `eli2md`, odczyt `pdftotext`, parser_version, raport różnic, kompletność oryginału, official_status, currentness_status, wersja tekstu; `pobrano_at` nigdy nie jest stanem prawnym. Nie nadpisywać wcześniejszych wersji. Ograniczyć CPU/bajty, single-flight konwersji według hasha, czas i retry. Cache **zweryfikowanych** dokumentów oddzielić od cache **kandydatów**.

**Krytyczna zmiana PR #4 do wykonania PRZED jakimkolwiek E2E:** `pdf_ingest.py` obecnie uznaje za zweryfikowany PDF, gdy tekst zawiera numer CELEX lub sygnaturę — numer może pochodzić tylko z cytowanego wyroku, a tekst może być niekompletny. `save_cache` jest zbyt liberalny i pozwala oznaczyć treść jako full/verified. Na tym etapie wprowadzić stany `DOWNLOADED`, `EXTRACTED_UNVERIFIED`, `VERIFIED_FIDELITY`, `REQUIRES_OCR`, `MISMATCH`; automatycznie promować dopiero przy niezależnej kontroli ID w nagłówku/URL metadanych, pełności i wierności. Osobno rozdzielić `full_document_stored` i `current_response_is_partial`.

**Rozróżnienie żądań:** `Dz.U. 2024 poz. 917` = konkretna publikacja, nie automatycznie najnowszy tekst; `artykuł na_dzien` = osobny wybór wersji i nowelizacji. Ten sam akt może mieć różne teksty jednolite, załączniki i daty wejścia poszczególnych zmian. Test spójności: HTML ELI 500, PDF 200 => pełen tekst z właściwego PDF, wierność weryfikowana; awaria ELI ≠ brak przepisu.

**Przejście fazy 3A:** parser ELI PDF-only działa local-first, oryginał i raport są zapisane, błędne słowa/strony są odrzucane, a CI i integracyjny test prawdziwego ELI są zielone. NIE mylić wyniku testu autora z naszym testem.

### FAZA 3B — INTEGRACJA Webwright-legal-pl z legal-cite i lokalnym resolverem

**Stan faktyczny:** PR #4 zawiera już oryginalne skrypty Webwright Apache-2.0 z `matematicsolutions/awesome-matematic-skills-pl` rew. `e99b534` dla **SN** i **EUR-Lex** oraz prototyp prywatnego `webwright_internal.py` z 2 backend toolami. Nie ma rzeczywistych adapterów `orzeczenia.ms.gov.pl` ani `trybunal.gov.pl`. Skrypty źródłowe zapisują metadane, URL PDF, markdown strony i screenshot; znalezienie linku ≠ pobranie pełnego orzeczenia. PR #4 ma `pdf_ingest.py` (pypdf, heurystyka), który trzeba zastąpić/bramkować warstwą jakości.

**Docelowy przepływ (odpowiedzialności bez dodatkowych tools w lex):**

1. Publiczny `pobierz_dokument` otrzymuje `document_id` Repertorium lub ścisły numer/sygnaturę. Lokalne źródło (USTAWY, SAOS mirror, NSA cache, PL UE, KRS, UODO) i zweryfikowany cache są **ZAWSZE pierwsze**. Test: HIT ⇒ **zero** żądań HTTP/Playwright.
2. MISS kieruje do konkretnego upstream, nigdy do wszystkich równocześnie: Dz.U./M.P. → oficjalny ELI HTML/PDF; CELEX/RODO → **CELLAR XHTML/XML PL** (wersja pierwotna/skonsolidowana) → ewentualnie Webwright EUR-Lex PDF; SN/MS/TK → Webwright do odkrycia i pobrania oficjalnego dokumentu; ECLI → pełne TSUE/CELLAR, nie parser aktu UE.
3. Webwright działa jako **prywatny MCP** w Docker network, z precyzyjnymi adapterami serwisów, allowlistą domen i redirectów, limitami timeout/CPU/konkurencji, bez obchodzenia CAPTCHA/WAF. Zapisuje raw HTML/PDF, screenshot, URL finalny, sygnaturę, sąd, datę, checksum i ścieżkę artefaktów.
4. **Te same bajty PDF** dostarcza do workera legal-cite (bez ponownego pobrania) w bezpiecznym lokalnym wolumenie. Worker rozpoznaje typ: akty ELI → strukturalne `eli2md + pdftotext`; CELEX PL → strukturalny XHTML preferowany, PDF fallback → kontrola wierności i języka; orzeczenia SN/MS/TK → **osobny parser orzeczniczy**, kontrola sygnatury **w nagłówku**, sądu, daty, sentencji i uzasadnienia, dwa niezależne odczyty tekstu; algorytm art./` nie nadaje się do wyroków.
5. Skan bez tekstu → `REQUIRES_OCR`, oryginał pozostaje; opcjonalnie istniejący `mcp-ocr` i jawne `OCR_UNVERIFIED`, nie „urzędowy zweryfikowany tekst”. Wynik metadata/link-only → `CANDIDATE`.
6. Przy pozytywnej kontroli `source-ID + document-ID + version + fidelity + completeness` resolver zapisuje wersjonowany dokument/fragment, SHA raw i extract, wyniki QC, strony i daty w trwałym cache, a kolejny odczyt idzie lokalnie. **SN opaque-ID nie wolno dopasować do PDF na podstawie arbitralnie podanej przez model sygnatury**; wymagane wiarygodne mapowanie ID Repertorium→dokument urzędowy.
7. Model dostaje wyłącznie tekst z cytatami/provenance, jasne statusy, `has_more` i `next_offset`. Wszystkie istniejące serwery źródłowe nadal działają samodzielnie, a Webwright/worker nie są publicznymi narzędziami w `lex`.

**Prace do wykonania w repo:**

| Zakres | Lokalizacja/nowa odpowiedzialność | Stan |
|---|---|---|
| Interfejs 1-tool/wybór lokalnego źródła | `mcp-prawo-wrapper/src/prawo_pl_mcp/slim_resolver.py` | draft, nie E2E |
| Cache, provenance i SHA | `local_corpus.py` | prototyp; naprawić brak wersji/QC |
| Wewnętrzny Webwright | `webwright_internal.py` + `vendor/webwright_legal_pl` | dwa adaptery SN/EUR-Lex, bez realnych testów browser |
| Worker legal-cite | nowy moduł/worker PDF, import z `legal_cite/pdf_tj.py`/`core.py` | **NIE ZAIMPLEMENTOWANY** |
| Elastyczny ingest PDF | zastąpić/zaostrzyć `pdf_ingest.py`, integracja worker | prototyp nie jest bezpieczny do trusted cache |
| MS/TK | nowe skrypty Playwright + parsery orzecznicze | **NIE ZAIMPLEMENTOWANE** |
| CELEX PL + ECLI | ETL CELLAR po polsku + wersjonowane teksty, osobne drogi dla aktów i wyroków | **NIE ZAIMPLEMENTOWANE** |
| Prawdziwe testy PDF/UI/CI | pytest z fixtures i staging rzeczywistych źródeł | **NOT RUN** |

**Testy i kryteria odbioru:**

- **ELI:** lokalne `DU/2024/917 art.23` bez API; brak → PDF-only → dwie niezależne ekstrakcje + jakościowy raport → zapisz → restart → lokalny HIT; odrębne wersje i nowelizacje.
- **CELEX/RODO:** `RODO art.33` urzędowe PL (nigdy angielski tekst z obecnego EU-COMPLIANCE); CELLAR pierwszy fallback, EUR-Lex Webwright drugi; oznacz nieurzędowe konsolidacje; ECLI wyroku TSUE nie jest tekstem rozporządzenia.
- **SN:** sygnatura musi być zgodna w nagłówku i metadanych, a nie tylko cytowana; pełny PDF, sentencja/uzasadnienie, strony, raw SHA i cache hit bez przeglądarki. Konflikt między `sn:opaque` i sygnaturą → bez promocji.
- **MS/TK:** nowe adaptery, fixtures oficjalnego HTML/PDF, realne smoke kilku typów dokumentów, udokumentowane braki. Przy braku adaptera wynik `NOT_IMPLEMENTED`.
- **Negatywne:** brak strony lub słowa, zmieniona kolejność słów, dwie kolumny, błąd PDF/redirect, WAF/CAPTCHA, skan, obca sygnatura, błędny SHA, dwie wersje artykułu, zły offset, timeout, duplikaty równoległe. Żaden nie awansuje do `VERIFIED_FIDELITY` bez dowodu.
- **Test operacyjny:** cache hit rate, zewnętrzne wywołania na dokument, czas/CPU worker, liczba stron, odtwarzalność SHA i brak utraty `content`/`structuredContent` w łańcuchu MCP→portal→klient.

**Zależności:** 1) naprawa fałszywych stanów verified, 2) źródłowe PR #81/NSA/wrapper #3 z zielonym CI, 3) wewnętrzny worker legal-cite + testy, 4) Webwright→worker→cache dla SN/UE/ELI, 5) MS/TK i CELLAR PL, 6) pokrycie KRS/UODO/ECLI w resolverze, 7) pełny staging 2-tool, 8) cutover portalu z rollbackiem. Zachować licencje i pin zależności. NIE scalać monolitu UE.

### FAZA 4 — dwa kontenery staging + testy portalu
- Zbuduj obrazy resolver i wewnętrzny Webwright bez podmieniania produkcyjnych `latest`, z prywatną siecią, readonly mountami upstreamów oraz trwałym cache.
- Zweryfikuj bezpośrednie MCP: resolver wystawia **1 tool**, Repertorium 1 wyszukiwawcze tool; dodatkowe serwery nie muszą być zarejestrowane jako publiczne tools.
- Na *odrębnej bezpiecznej konfiguracji staging* portalu sprawdź, czy można wskazać istniejący serwer Repertorium bez jego zmian. Jeśli wymagana ingerencja w kod/usługę/polityki Repertorium — STOP i przegląd.
- Testuj end-to-end przez Cloudflare Access, ChatGPT/Claude: dotychczasowa polityka OAuth kont laptopshop.pl i `ANY service token` bez osobnych promptów autoryzacyjnych upstream. Nie twórz osobnych policies każdego MCP; nie narusz osobnego direct endpointu Repertorium. Kontrola surowego `content`/`structuredContent`, PL, pełnych wersji, kolejnych stron, linków.
- Brak zgody na ukrycie 54 innych tools dopóki `szukaj_repertorium` i `pobierz_dokument` nie działają prawidłowo.

**Gate 4:** 2 publiczne narzędzia działają na staging, nie ma regresji, przygotowany rollback.

### FAZA 5 — cutover `lex`, monitorowanie i rollback
- Dopiero po gate 0–4 przełącz **wyłącznie widoczność/rejestrację** upstreamów w prawnym `lex` na REPERTORIUM + resolver. Nie kasuj kontenerów, nie usuwaj danych, nie restartuj REPERTORIUM.
- Sprawdź z rzeczywistego klienta `tools/list` = `szukaj_repertorium` + `pobierz_dokument` (dokładnie 2), brak dodatkowego upstream OAuth, zachowany osobny endpoint Repertorium, polskie odpowiedzi i wersjonowane cytaty.
- Obserwuj health, procent local cache HIT, ilość zewnętrznych fetch / dokument, timeouty, PDF fidelity, fragmenty, provenance i wielkości odpowiedzi.
- **Rollback:** odtwórz uprzednio zapisaną listę 8 upstreamów/56 tools i konfigurację portalu bez modyfikowania Repertorium; odłącz nowy resolver/Webwright jeśli wadliwy. Zachowaj artefakty i logi do audytu.

## 7. STATUSY DO SPRAWDZENIA PRZEZ KOLEJNY MODEL

| Sprawdzian | Stan ustalony na 31.10 | Dowód / jak powtórzyć |
|---|---|---|
| 8 serwerów i 56 tools w `lex` | **PASS read-only** | `portal_list_servers` + `codemode.tools()` |
| 8/8 kontenerów źródłowych `running` | **PASS procesu** (nie treści) | Portainer `/containers/json` env=3 |
| REPERTORIUM odpowiada na zapytania | **PASS wcześniejszego read-only** | `mcp-repertorium /mcp`, źródłowe IDs |
| REPERTORIUM widoczne w `lex` | **FAIL** | brak w katalogu 8 serwerów |
| EU-SPARQL PR #1 | **PASS CI i CodeQL**, bez staging | runs 41143814976, 41143814962 |
| KRS PR #2 | **PASS CI i CodeQL**, bez staging | runs 41143821496, 41143821559 |
| NSA PR #2 | **PASS CI i CodeQL**, bez staging | runs 41144040723, 41144040761 |
| EU-COMPLIANCE united PR #1 | **PASS CI, architektura nieaktualna** | run 41145843881; nie merge |
| USTAWY PR #81 | **FAIL CI** | run 41149480617, generated `plugins/` drift |
| Wrapper PR #3 / resolver PR #4 | **NOT RUN CI (0 workflows)** | GitHub Actions branch runs |
| USTAWY exact ELI / cache SHA / PDF | **PASS tylko mock/AST** | odtworzyć na fixtures i live |
| Nowy resolver i Webwright w produkcji | **NO / NOT DEPLOYED** | brak na liście kontenerów |
| Polski urzędowy CELEX ETL / pełne ECLI | **NOT IMPLEMENTED** | brak zweryfikowanego PL corpus |
| Adaptery KRS/UODO/MS/TK w resolverze | **NOT IMPLEMENTED** | przegląd `slim_resolver.py` |
| Nowy ELI PDF-only parser legal-cite | **NOT IMPLEMENTED** | tylko link dla `textHTML=false` |
| Redukcja do 2 tools w portalu i test OAuth | **NOT RUN** | staging, dopiero potem prod |

**Interpretacja:** zielone CI backendu ≠ zielone E2E. Testy mockowe ≠ test oficjalnego PDF. Działający kontener ≠ treść kompletna. Brak uruchomionego testu ≠ PASS.

## 8. ŹRÓDŁA i indeks kontroli

- Indeks planów wszystkich dotychczasowych MCP: https://github.com/elconcept/grounding-prawo/blob/main/_PLAN/20261031_lex_indeks_planow_naprawczych.md
- Repertorium, stary plan nieupoważniający do zmian: https://github.com/elconcept/mcp-repertorium/blob/main/_PLAN/20261031_plan_naprawczy_mcp_lex.md
- USTAWY PR #81 + czerwony build: https://github.com/elconcept/grounding-prawo/pull/81 oraz https://github.com/elconcept/grounding-prawo/actions/runs/41149480617
- Wrapper PR #3: https://github.com/elconcept/mcp-prawo-wrapper/pull/3
- Resolver + Webwright PR #4: https://github.com/elconcept/mcp-prawo-wrapper/pull/4
- Snapshot szczegółowy wyłącznie PDF/resolver: https://github.com/elconcept/mcp-prawo-wrapper/blob/feat/minimalny-resolver-repertorium-20261031/_PLAN/20261031_SNAPSHOT_AUDYT_legal_cite_pl_local_first.md
- EU-SPARQL PR #1: https://github.com/elconcept/mcp-eu-sparql/pull/1
- KRS PR #2: https://github.com/elconcept/mcp-krs/pull/2
- NSA PR #2: https://github.com/elconcept/mcp-nsa/pull/2
- EU-COMPLIANCE draft monolitu, **nie scalać**: https://github.com/elconcept/mcp-eu-compliance/pull/1
- Apache-2.0 Webwright: https://github.com/matematicsolutions/awesome-matematic-skills-pl/tree/e99b534/orzecznictwo-zrodla/skills/webwright-legal-pl
- Apache-2.0 legal-cite (SHA audytu 2c4b7bf6e2af56b42b8b87a9bdbfe93d8078c988): https://github.com/apiotrowski-afk/legal-cite-pl
- MIT eli2md v0.6.70: https://github.com/PolskiAgentW/eli2md/tree/v0.6.70

## 9. PROMPT KONTROLNY DLA KOLEJNEGO MODELU

> Otwórz w całości `_PLAN/20261031_SNAPSHOT_GLOBALNY_MCP_LEX_HANDOFF.md` w repo `elconcept/grounding-prawo`, gałąź `docs/20261031-lex-global-handoff`. To jest nadrzędny snapshot WSZYSTKICH MCP portalu `lex`, a nie tylko PDF. Nie ufaj poprzedniej narracji bez sprawdzenia: ponownie odczytaj 8 enabled upstreamów i 56 tooli, Portainer env=3, działające REPERTORIUM poza katalogiem, dokładne SHA i statusy wszystkich PR-ów i GitHub Actions. Porównaj oryginały z kodem zmienionym i planami. Cel produktu: model w `lex` ma widzieć tylko `szukaj_repertorium` i `pobierz_dokument`, pozostałe serwery pracują wewnętrznie local-first; REPERTORIUM jest nietykalne. Katalog legalny ma być polskojęzyczny bez selektora języka. Skontroluj USTAWY #81 (czerwone CI), wrapper #3/#4 (brak CI), NSA/KRS/EU-SPARQL (zielone CI, bez staging), SAOS, UODO, BASIC-MEMORY, europejskie polskie teksty i CELEX/ECLI, jakość PDF legal-cite, Webwright SN/MS/TK, wersjonowanie oraz zawartość `content`/`structuredContent`. Najpierw sporządź macierz PASS/FAIL/NOT RUN z odnośnikami do kodu/CI. Dopiero potem wykonuj małe, testowalne poprawki na gałęziach i przygotuj staging/rollback. Nie scalaj ani nie wdrażaj przed bramkami faz 0–4. Żadnych zmian w REPERTORIUM, żadnych nowych osobnych policies/tokenów dla każdego backendu.

**Stan dokumentu: snapshot gotowy; żadna z planowanych zmian portalu nie została wdrożona.**
