# Źródła objęte wrapperem — stan zweryfikowany 11.09.2026

Każdy wiersz sprawdzony realnym wywołaniem, nie z dokumentacji.

| # | Źródło | Endpoint | Transport | Klucz | Zweryfikowano | Normatyw? |
|---|---|---|---|---|---|---|
| 1 | **Sejm ELI** — Dz.U. + M.P. | `api.sejm.gov.pl/eli` | REST JSON | nie | ✅ search / act / text.html | tak |
| 2 | **SAOS** — sądy powszechne, SN, TK, KIO | `www.saos.org.pl/api` | REST JSON | nie | ✅ search/judgments, judgments/{id} | tak |
| 3 | **CBOSA** — NSA + 16 WSA | `orzeczenia.nsa.gov.pl/cbo/find` | **HTML scrape** | nie | ✅ http 200, 10 linków `/doc/…` | tak |
| 4 | **EUR-Lex / CELLAR** | `publications.europa.eu/webapi/rdf/sparql` | SPARQL | nie | ✅ CELEX 32016R0679 → tytuł PL | tak |
| 5 | **KRS** | `api-krs.ms.gov.pl/api/krs` | REST JSON | nie | ✅ OdpisAktualny 0000028860 | nie (rejestr) |
| 6 | **NBP** | `api.nbp.pl/api/exchangerates` | REST JSON | nie | ✅ kurs EUR | nie (fakt) |
| 7 | **SUDOP / UOKiK** | `api-sudop.uokik.gov.pl/sudop-api` | REST JSON | nie | ✅ param `nip-beneficjenta` | nie (rejestr) |
| 8 | **CEIDG** | `dane.biznes.gov.pl/api/ceidg/v2` | REST JSON | **TAK** | ⚠️ ścieżka bez klucza niesprawdzona | nie (rejestr) |
| 9 | **Krajowe ELI UE** ×9 | `uvx <cc>-eli-mcp` | MCP stdio | nie* | ✅ `de-eli-mcp` 3.4.7, `de_search` 271 trafień | tak |

\* `fr-eli` wymaga darmowych danych dostępowych PISTE.

Wszystkie 9 pakietów ELI istnieje na PyPI (HTTP 200): `de- at- es- fi- ie- nl- se- fr- lu- eli-mcp`. `uv`/`uvx` obecne w `~/.local/bin`.

## Skąd te źródła — rodowód

**LEX-MACHINA** (`<skille>/shared/`): `KONEKTORY-REKOMENDOWANE.md` nazywa **7 serwerów referencyjnych** — `isap-eli-example`, `saos-example`, `krs-example`, `nbp-example`, `sudop-example`, `ceidg-example`, `eurlex-example` (katalog `shared/tools/mcp-servers/`). To jest te „siedem źródeł". Cztery z nich (KRS, NBP, SUDOP, CEIDG) to rejestry faktyczne, nie źródła prawa — wrapper obejmuje je mimo to, bo warstwa cache jest niezależna od rodzaju źródła.

**MateMatic** (`~/.claude/plugins/marketplaces/matematic-skills-pl/`): `.mcp.json` pluginu `orzecznictwo-zrodla` deklaruje `saos`, `krs`, `eu-sparql`; na npm dochodzą `@matematicsolutions/mcp-isap` i `mcp-nsa`; `.mcp.json` pluginu `multi-jurysdykcja-ue` deklaruje **9 serwerów ELI wołanych przez `uvx`**. Skille `saos-orzecznictwo` i `szukaj-orzeczen-v2` mają dodatkowo własne skrypty Pythona (`saos.py`, `saos_fetch.py`) sięgające do tego samego API SAOS — czyli **cztery ścieżki dostępu do jednego źródła**.

Wrapper deduplikuje to po **źródle danych**, nie po pakiecie.

## Źródła bez API — świadomie poza wrapperem

Potwierdzone w `KONEKTORY-REKOMENDOWANE.md` jako pozbawione publicznego API; jedyna droga to `WebFetch`/`WebSearch` na stronie HTML:

- **Interpretacje podatkowe / EUREKA** (`eureka.mf.gov.pl`) — brak udokumentowanego REST API. Sygnatur interpretacji **nie da się zweryfikować** żadnym narzędziem w tym zestawie.
- **KIO / UZP** (`orzeczenia.uzp.gov.pl`) — wyszukiwarka HTML + archiwalny FTP z PDF-ami. Częściowe pokrycie przez SAOS, ale tylko do 2018 r.
- **KNF** — rejestry jako HTML/XLS.
- **ZUS** — wyłącznie uwierzytelnione interfejsy dla płatników (PUE), nieprzydatne jako konektor weryfikacyjny.

CBOSA również nie ma API — objęty wrapperem jako scrape, z pełnym ostrzeżeniem o captchy.

### Domknięta luka: obowiązujący tekst jednolity kodeksów

| Akt | Obowiązujący t.j. | HTML | `isap pdf` | Sprawdzony artykuł |
|---|---|---|---|---|
| Kodeks cywilny | `DU/2026/795` | ❌ | ✅ | art. 118 — „termin przedawnienia wynosi sześć lat" |
| Kodeks postępowania cywilnego | `DU/2026/468` | ❌ | ✅ | art. 203 § 1 — cofnięcie pozwu |
| Kodeks postępowania karnego | `DU/2026/490` | ❌ | ✅ | art. 306 § 1 — zażalenie na odmowę wszczęcia |
| Kodeks pracy | `DU/2025/277` | ❌ | ✅ | art. 30 § 1 — rozwiązanie umowy o pracę |

PDF-y ISAP mają **prawdziwą warstwę tekstu** (`/Font` obecny, KC: 119 stron, 1,2 MB) — OCR jest zbędny, wystarczy `mutool draw -F txt`. Potwierdza to, że brzmienie na dziś jest osiągalne bez schodzenia do nieaktualnych tekstów jednolitych.

### Baza orzeczeń SN (`sn.pl`) — luka znana, świadomie niewciągnięta

Plugin `orzecznictwo-zrodla` ma skrypt `webwright-legal-pl/scripts/fetch_orzeczenie.py`, który pobiera orzeczenia SN po sygnaturze **bezpośrednio z `sn.pl`** — dokładnie to, czego brakuje SAOS-owi po czerwcu 2016 r. To realny fetcher, nie sam URL w dokumentacji, ale działa przez **Playwright** (automatyzacja przeglądarki), a nie przez HTTP.

Nie został wciągnięty do wrappera, bo złamałby jego jedyną zasadę instalacyjną: stdlib + `curl`, zero ciężkich zależności. Jeśli Playwright jest zainstalowany, skrypt można wołać osobno; domknięcie luki SN w `lexcache` (podkomenda `sn`, delegująca do tego skryptu) jest możliwe, ale wymaga świadomej zgody na tę zależność.

## Zweryfikowane zachowania filtrów

Parametry filtrujące sprawdzone porównaniem z zapytaniem bez filtra (błędna nazwa parametru na tych API **nie daje błędu**, tylko ciche zwrócenie niefiltrowanych wyników):

| Filtr | Bez filtra | Z filtrem | Działa? |
|---|---|---|---|
| `saos search --date-from 2026-06-01` | daty od 2012 | daty od 2026-06 | ✅ |
| `isap search --in-force` | 61 trafień | 49 trafień | ✅ |
| `isap search --year 2026` | 61 trafień | 2 trafienia | ✅ |

## Zweryfikowane pułapki, które wrapper obsługuje

1. **`urllib` vs `curl`** — przy inspekcji TLS `urllib` rzuca `CERTIFICATE_VERIFY_FAILED: self-signed certificate in certificate chain`, `curl` przechodzi. Wrapper używa wyłącznie `curl`.
2. **EUR-Lex i nagłówek `Accept`** — `Accept: application/json` daje `406 Not Acceptable`; poprawny jest `application/sparql-results+json`.
3. **FastMCP i zamknięte stdin** — wysłanie wszystkich wiadomości naraz i zamknięcie potoku kończy serwer przed obsłużeniem `tools/list`. Wrapper pisze po jednej wiadomości i czeka na odpowiedź o tym samym `id`.
4. **Tekst jednolity tylko w PDF** — obowiązujące obwieszczenia dla KC, KPC, KPK i KP nie mają wersji HTML. `isap text` zwraca `ERROR`/`text_unavailable_use_pdf`; **`isap pdf` domyka lukę** — pobiera PDF i wyciąga z niego warstwę tekstu.
5. **Urwane pobranie PDF zatruwa cache** — pierwsza wersja zapisywała plik bezpośrednio pod docelową nazwą; częściowy plik dawał potem ekstrakcję bez szukanej frazy na 90 dni. Pobieranie idzie teraz do `.part`, waliduje nagłówek `%PDF` i rozmiar, i dopiero wtedy robi `os.replace`.
6. **PDF aktu bazowego ≠ tekst jednolity** — pierwsza wersja `isap pdf` stemplowała `text_version: tekst_jednolity` bezwarunkowo, więc `isap pdf DU/1964/93` zwróciłby brzmienie KC z 1964 r. („lat dziesięć", „jednostki gospodarki uspołecznionej") oznaczone jako obowiązujące — gorzej niż błąd, bo pewnie. Rozróżnienie idzie teraz po `references` aktu: klucz `Tekst jednolity dla aktu` → to jest t.j.; klucz `Inf. o tekście jednolitym` → to akt bazowy, więc `status: AMBIGUOUS`, `status_obowiazywania: tekst_jednolity_nieaktualny` i przekierowanie w `uzyj_zamiast`.
7. **Ekstrakcja z PDF gubi spacje** — zaobserwowane `niepóźniej` zamiast `nie później` w KPC; indeksy górne wychodzą jako `Art. 205[1]`. Frontmatter niesie ostrzeżenie, a `SKILL.md` wymaga weryfikacji wzrokowej przed cytatem dosłownym.
5. **Puste ciało odpowiedzi ≠ trafienie** — SUDOP na NIP bez pomocy publicznej zwraca `"\n"` z HTTP 200. Klasyfikowane jako `NOT_FOUND`, nie `FOUND`.
