# MCP lex — indeks planów naprawczych z audytu 31.10.2026

## Cel i wymaganie nienegocjowalne
Wyszukiwanie naturalnojęzykowe i **wszystkie widoczne użytkownikowi odpowiedzi wyłącznie w języku polskim**, bez selektora języka. Jedynymi nieprzetłumaczonymi elementami pozostają identyfikatory techniczne i źródłowe nazwy własne. Tekst urzędowy musi pochodzić z prawidłowego źródła i być odróżniony od komentarza lub tłumaczenia roboczego.

## Plany w repozytoriach

| Projekt / kontener | Plan MD | Główne zagadnienie |
|---|---|---|
| BASIC-MEMORY | [basic-memory/_PLAN/20261031_plan_naprawczy_mcp_lex.md](https://github.com/elconcept/basic-memory/blob/main/_PLAN/20261031_plan_naprawczy_mcp_lex.md) | dryf e5-large→e5-small, spójność manifestu i indeksu |
| EU-COMPLIANCE | [mcp-eu-compliance/_PLAN/20261031_plan_naprawczy_mcp_lex.md](https://github.com/elconcept/mcp-eu-compliance/blob/main/_PLAN/20261031_plan_naprawczy_mcp_lex.md) | brak pełnej treści przez portal, polski korpus FTS, kanon obecny |
| EU-SPARQL | [mcp-eu-sparql/_PLAN/20261031_plan_naprawczy_mcp_lex.md](https://github.com/elconcept/mcp-eu-sparql/blob/main/_PLAN/20261031_plan_naprawczy_mcp_lex.md) | usunąć lang, adresy PL, deduplikacja i filtrowanie typów |
| KRS | [mcp-krs/_PLAN/20261031_plan_naprawczy_mcp_lex.md](https://github.com/elconcept/mcp-krs/blob/main/_PLAN/20261031_plan_naprawczy_mcp_lex.md) | odpis pełny: tablice historyczne, fałszywy status, reprezentacja |
| NSA | [mcp-nsa/_PLAN/20261031_plan_naprawczy_mcp_lex.md](https://github.com/elconcept/mcp-nsa/blob/main/_PLAN/20261031_plan_naprawczy_mcp_lex.md) | SSL/socket hang up, pełna treść i paginacja |
| REPERTORIUM | [mcp-repertorium/_PLAN/20261031_plan_naprawczy_mcp_lex.md](https://github.com/elconcept/mcp-repertorium/blob/main/_PLAN/20261031_plan_naprawczy_mcp_lex.md) | 100 retry, proxy, trafienia dokładne vs semantyczne |
| SAOS | [mcp-saos/_PLAN/20261031_plan_naprawczy_mcp_lex.md](https://github.com/elconcept/mcp-saos/blob/main/_PLAN/20261031_plan_naprawczy_mcp_lex.md) | content chunków, ostrożny werdykt cytatora, walidacja pageSize |
| UODO | [mcp-uodo/_PLAN/20261031_plan_naprawczy_mcp_lex.md](https://github.com/elconcept/mcp-uodo/blob/main/_PLAN/20261031_plan_naprawczy_mcp_lex.md) | działające wyszukiwanie, regresja i kompletność długich decyzji |
| USTAWY | [grounding-prawo/_PLAN/20261031_plan_naprawczy_mcp_lex.md](https://github.com/elconcept/grounding-prawo/blob/main/_PLAN/20261031_plan_naprawczy_mcp_lex.md) | 37 aktów, niepowtórzony OUT_OF_SCOPE, integralność indeksu i komentarzy |
| INTEGRACJA LEX / WRAPPER | [mcp-prawo-wrapper/_PLAN/20261031_plan_naprawczy_mcp_lex.md](https://github.com/elconcept/mcp-prawo-wrapper/blob/main/_PLAN/20261031_plan_naprawczy_mcp_lex.md) | śledzenie pól content/structuredContent w całym łańcuchu |

## Kolejność wdrażania (zależności)

1. **P0, warstwa wspólna:** ustalić, na którym etapie portal `lex`/adapter lub klient gubi `content`. Zachowanie treści `eu_article`, `krs_get_board`, `saos_get_judgment` jest warunkiem odbioru pozostałych zmian. Nie przypisywać automatycznie winy Cloudflare Tunnel — sam test HTTP zewnętrzny dla EU-COMPLIANCE zwrócił pełny `content`.
2. **P0, integralność:** KRS `get_entity_full` fałszywy status i `[object Object]`; NSA wyłączona walidacja certyfikatów TLS i niespójna dostępność; Repertorium nadmierne retry. Należy zapobiec fałszywym ustaleniom prawnym i lawinowym żądaniom.
3. **P1, polski end-to-end:** EU-COMPLIANCE urzędowy polski korpus i polska indeksacja; EU-SPARQL jeden język stały `POL` i polskie adresy; we wszystkich serwerach usunąć niepotrzebny parametr `lang` ze schematu. Brak urzędowego PL nie może być maskowany angielskim tekstem.
4. **P1, kompletność dokumentów:** NSA chunking z kontrolą całkowitej długości, SAOS odtwarzalne offsety i pewność zakresu cytatora, UODO kontrola braku obcięcia obszernej decyzji, USTAWY trwałość indeksu i komentarza.
5. **P2, utrzymanie:** Basic Memory zgodność 384D i modelu wektorowego po wdrożeniu historycznie poprawionego compose; dopracowanie walidacji i raportowania pokrycia; ujednolicone fixtures i obserwowalność.

## Minimalny test odbiorczy na każdym etapie
- Sprawdzenie opublikowanego `tools/list` i schematu: brak selektora `lang`, polskie opisy i komunikaty.
- Ten sam fixture przez bezpośredni MCP, HTTP/Tunnel i portal `lex`: tekst, metadane i sumy kontrolne w polach `content` / `structuredContent` zgodne, z jawnym stronicowaniem, jeśli występuje.
- Przykłady sprawdzające: GDPR art. 33 (treść PL), `KRS 0000028860`, NSA `389F2C5B67`, SAOS `166511`, UODO `DKE.561.5.2026`, USTAWY `uozp/23` i `kpk/171`, Repertorium dokładna sygnatura i art. 23.
- Błędy/upstream brak dostępności są **błędami**, a nie komunikatem „brak wyników”; wszystkie wyniki prawne zawierają źródło, datę i granice pokrycia.

## Ograniczenia audytu
Nie wszystkie symptomy są błędami: `pageSize=1` w SAOS nie spełnia minimalnego wymagania 10. USTAWY po wcześniejszym `OUT_OF_SCOPE` przeszły następny test pozytywnie. Wrapper `mcp-prawo` nie został potwierdzony jako osobny aktywny kontener w ostatnim odczycie Portainera — plan dotyczy repo integracyjnego i możliwego wykorzystania, nie zakłada aktualnego routingu.

## Status realizacji
Zapisano **plany**, a nie poprawki implementacyjne. Wyjątek historyczny sprzed tego audytu: `basic-memory/docker-compose.nas.yml` został już poprawiony w commicie `25eabcd371816fe332d65e5c940b87fc8477438d`; w tym audycie nie wdrażano kontenerów, nie uruchamiano migracji i nie edytowano DNS/polityk Access.
