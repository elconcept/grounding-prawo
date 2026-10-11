---
name: lexcache
description: "Jeden wrapper CLI na wszystkie źródła prawa używane przez LEX-MACHINA i MateMatic, spięty ze wspólnym repozytorium GROUNDING-PRAWO (OneDrive/SMB) — ISAP (Sejm ELI), SAOS, CBOSA (NSA/WSA), EUR-Lex/CELLAR, KRS, NBP, SUDOP, CEIDG oraz 9 krajowych rejestrów ELI UE przez uvx — z lokalnym cache w plikach .md z frontmatterem YAML (przeszukiwalnym), TTL per typ zapytania i ostrzeżeniem o danych wygasłych. Wyzwalaj gdy: powtarzalne odpytywanie tych samych aktów/orzeczeń, praca offline lub przy niedostępnym MCP, potrzeba przeszukania wcześniej pobranych źródeł, audyt czym się posłużono i kiedy, albo gdy trzeba sięgnąć do źródła, dla którego nie ma podłączonego konektora MCP."
---

# lexcache — wrapper na źródła prawa z lokalnym cache

Jedno narzędzie CLI zamiast dziewięciu osobnych ścieżek dostępu. Nie zastępuje konektorów MCP — **uzupełnia je**: daje cache, jednolity format wyniku, przeszukiwanie tego, co już pobrano, i dostęp do źródeł, dla których nie ma podłączonego serwera MCP.

Skrypt: `<skille>/lexcache/scripts/lexcache.py` (Python 3, tylko stdlib + `curl`; `mutool` opcjonalnie — potrzebny wyłącznie dla `isap pdf`).

```bash
python3 <skille>/lexcache/scripts/lexcache.py sources --health
```

---

## Kiedy lexcache, a kiedy MCP

| Sytuacja | Użyj |
|---|---|
| Pojedyncze pytanie prawne w rozmowie, konektor MCP podłączony | **MCP** (`saos`, `isap`, `eu-sparql`, `krs`) — skill `iura` opisuje jak |
| To samo zapytanie wraca wielokrotnie (research, przegląd portfela umów, batch) | **lexcache** — drugie wywołanie nie rusza sieci |
| Konektor MCP niepodłączony / środowisko bez MCP / praca wsadowa z Basha | **lexcache** |
| Źródło bez konektora: CBOSA, NBP, SUDOP, CEIDG, krajowe ELI UE | **lexcache** (jedyna ścieżka) |
| „Czego już szukałem w tej sprawie i kiedy" | **lexcache** `find` / `ls` |

Skille prawne (`iura`, `pozew-cywilny`, `odpowiedz-na-pozew`, `apelacja-karna` i pozostałe) kierują tu **jednym konkretnym przejściem**: gdy `get_act_text` zwróci `text_unavailable_use_pdf`. Poza tym przypadkiem rutynowy research zostaje na narzędziach MCP.

**Ten skill nie zmienia zasad cytowania.** Reguły merytoryczne — składnia zapytań polowych, drabinka „tekst ogłoszony → tekst jednolity", granice pokrycia SAOS, obowiązek `saos_cite_check` — są w skillu **`iura`** i obowiązują niezależnie od tego, czy dane przyszły z MCP, czy z cache.

---

## Baza GROUNDING-PRAWO: cache konektorów MCP i utrzymanie (2026-09-13)

`<skille>` w poleceniach to katalog ze skillami: w repozytorium `.claude/skills`, w pluginie
katalog `skills/` pluginu (nadrzędny wobec katalogu bazowego tego skilla).

- **Konektory MCP też zapisują do bazy.** `isap`, `saos`, `nsa`, `krs`, `eu-sparql`, `eu-compliance`
  i `eureka` działają za pośrednikiem `mcp/gp-cache.mjs`: wynik trafia do
  `CACHE/<źródło>/mcp-<narzędzie>-<klucz>.md` (ten sam frontmatter co wpisy lexcache, `origin: mcp-cache`),
  a powtórzone zapytanie przed upływem TTL wraca z bazy z linią `[GROUNDING-PRAWO cache] wynik pobrany …`.
  Gdy źródło nie odpowiada, wraca wpis wygasły - z ostrzeżeniem. `find` przeszukuje oba rodzaje wpisów.
- **`find`** korzysta z indeksu SQLite FTS5 trzymanego poza OneDrive (`~/.cache/lexcache/`),
  aktualizowanego przyrostowo; `--bez-fts` wymusza przeszukiwanie liniowe.
- **`refresh [--source S] [--all] [--limit N] [--mcp]`** - odświeża wygasłe wpisy, powtarzając
  zapisane zapytanie; `--mcp` obejmuje też wpisy konektorów (`mcp/gp-refresh.mjs`).
- **`harvest --z-map`** - metryki wszystkich aktów z `MAPA-AKTOW.md` modułów DR (ok. 230 pozycji);
  **`harvest --plik lista.txt`** - dowolna lista poleceń lexcache, np. `saos case "III CZP 11/13"`.
- **Citator w bazie:** `node mcp/gp-refresh.mjs --cite-check` wywołuje `saos_cite_check` dla orzeczeń
  z `ORZECZENIA/` i zapisuje werdykt w ich frontmatterze (`cite_check`, `cite_check_at`);
  potem `lexcache find --field cite_check=przelamanie_wykryte`.
- Zadanie cykliczne: `.claude/scheduled/odswiezanie-bazy/`.

## Mapa: narzędzie MCP → podkomenda lexcache

| MCP | lexcache |
|---|---|
| `isap.search_acts` | `isap search --title … [--publisher DU] [--type Obwieszczenie] [--year N] [--in-force]` |
| `isap.get_act` | `isap act DU/2018/1000` |
| `isap.get_act_text` | `isap text DU/2024/1568 --find "Art. 203."` |
| **brak odpowiednika w MCP** | `isap pdf DU/2026/795 --find "Art. 118."` — tekst z PDF obowiązującego tekstu jednolitego |
| `saos.search` | `saos search --all … --court COMMON --legalbase "art. 415 kc"` |
| `saos.search_by_case` | `saos case "I ACa 772/13"` |
| `saos.get_judgment` | `saos get 352475` |
| `saos.saos_cite_check` | **brak** — citator zostaje po stronie MCP |
| `eu-sparql.search_by_celex` | `eurlex celex 32016R0679 [--lang POL]` |
| `eu-sparql` (dowolne) | `eurlex sparql "SELECT …"` |
| `krs.get_entity` / `get_entity_full` | `krs act 0000028860` / `krs full 0000028860` |
| `nsa` (CBOSA) | `cbosa search "RODO"` |
| — | `nbp rate EUR [--date YYYY-MM-DD]` |
| — | `sudop nip 7740001454` |
| — | `ceidg nip … ` (wymaga `LEXCACHE_CEIDG_KEY`) |
| `de-eli` … `lu-eli` (uvx) | `eli de tools` / `eli de call de_search --args '{"query":{"searchTerm":"BGB"}}'` |
| — | `korpus normalize` / `korpus index` — ręcznie kurowany korpus GROUNDING-PRAWO |
| — | `migrate` — przeniesienie cache do wspólnego repozytorium |

Flagi globalne: `--refresh` (wymuś pobranie), `--no-cache` (nie czytaj i nie zapisuj), `--json` (surowa odpowiedź źródła), `--ttl N` (nadpisz TTL w dniach).

---

## Gdzie mieszkają dane: repozytorium GROUNDING-PRAWO

Wspólna baza dla wszystkich hostów, widoczna dwiema drogami do **tych samych danych**: przez OneDrive (sync lokalny) i przez SMB (`//10.0.10.200/GROUNDING-PRAWO`).

```
GROUNDING-PRAWO/
├── ORZECZENIA/  USTAWY/  OPRACOWANIA/  MAPY/   ← korpus ręcznie kurowany
├── CACHE/                                      ← to, co pobiera lexcache
└── INDEX/       INDEX.md + index.jsonl         ← generowany indeks całości
```

**Wrapper sam rozstrzyga, którą drogą iść** — testuje każdego kandydata realnym **zapisem i odczytem**, bo `stat`/`touch` potrafią się udać tam, gdzie `read` zwraca `Errno 5`. Tak właśnie zachowuje się obecnie udział SMB: 42 z 59 plików w `ORZECZENIA/` ma poprawny rozmiar w `stat` i zwraca 0 bajtów przy odczycie — te same pliki czytają się bez problemu przez OneDrive. Kolejność kandydatów:

1. `LEXCACHE_DIR` — wymuszenie katalogu cache
2. `GROUNDING_ROOT` — wymuszenie korzenia repozytorium
3. `~/OneDrive/GROUNDING-PRAWO`
4. `~/Library/CloudStorage/OneDrive-Osobisty/GROUNDING-PRAWO`
5. `/Volumes/GROUNDING-PRAWO`
6. `~/.claude/cache/lexcache` — fallback lokalny

`lexcache sources` pokazuje, który korzeń wygrał i dlaczego; odrzuceni kandydaci lądują na stderr.

**Obsługa OneDrive nie wymaga MCP.** macOS montuje go przez File Provider jako zwykły katalog — zwykłe `open()`, bez tokenów i limitów API. Konektor do Graph API byłby kosztem bez korzyści.

### RODO — świadoma decyzja

`CACHE/` gromadzi orzeczenia z SAOS (anonimizacja bywa niepełna) i odpisy KRS/CEIDG — **dane osobowe** — a repozytorium jest synchronizowane przez konsumencką chmurę. Każdy host podłączony do tej bazy staje się kolejnym miejscem przetwarzania. Jeśli obowiązuje Cię inny reżim: ustaw `LEXCACHE_DIR` na katalog lokalny i korzystaj z repozytorium tylko do odczytu korpusu. Frontmatter niesie `pii_risk: low|high`; wpisy `high` traktuj jak akta.

## TTL: jak długo trzymamy wpis

Zasada z `shared/KONEKTORY-REKOMENDOWANE.md` (reguła 2) jest wbudowana: **każdy wpis ma TTL i żaden przeterminowany nie jest serwowany po cichu** — odczyt wygasłego wpisu wypisuje `[UWAGA] wpis w cache WYGASL` i kończy się kodem wyjścia 3.

| Zapytanie | TTL | Dlaczego |
|---|---|---|
| `isap text` / `isap pdf` | 90 dni | tekst jednolity jest stabilny do następnego obwieszczenia |
| `isap act` | 30 dni | metadane i lista tekstów jednolitych zmieniają się rzadko |
| `isap search` | 7 dni | nowe pozycje Dz.U. dochodzą na bieżąco |
| `saos get` | 180 dni | opublikowane orzeczenie się nie zmienia |
| `saos case` | 30 dni | |
| `saos search` | 3 dni | baza sądów powszechnych rośnie codziennie |
| `cbosa search` | 7 dni | scrape HTML, oszczędzaj zapytania (captcha) |
| `eurlex celex` / `sparql` | 30 / 14 dni | |
| `krs`, `nbp`, `ceidg` | 1 dzień | dane rejestrowe i kursy zmieniają się z dnia na dzień |
| `sudop` | 7 dni | |
| `eli` (UE) | 30 / 14 dni | |
| dowolny wynik `status: ERROR` | **1 dzień** | błąd źródła nie ma być utrwalany |

---

## Frontmatter — po czym szukasz

Zgodny ze `shared/SCHEMAT-ODPOWIEDZI-MCP.md` plus kontrakt `structuredContent.citations` konektorów MateMatic i księgowość cache:

```yaml
---
status: FOUND                  # FOUND | NOT_FOUND | AMBIGUOUS | ERROR
query_type: akt_prawny         # akt_prawny | orzeczenie | podmiot | kurs | pomoc_publiczna
source: isap
tool: isap.act
query: "{\"eli\": \"DU/1964/93\"}"
identyfikator: DU/1964/93
tytul: "Ustawa z dnia 23 kwietnia 1964 r. - Kodeks cywilny."
status_obowiazywania: obowiazuje   # obowiazuje | uchylony | tekst_jednolity_nieaktualny | nieznany
data: "1964-05-18"
url: "https://isap.sejm.gov.pl/..."
retrieved_at: "2026-09-11T08:12:00Z"
expires_at: "2026-10-11T08:12:00Z"
ttl_days: 30
confidence: deterministic
pii_risk: low
cache_key: dd9c8fec75d7e155
eli: DU/1964/93
in_force: IN_FORCE
teksty_jednolite: [DU/2026/795, DU/2025/1071, ...]
---
```

Pola dodatkowe per źródło: `eli`, `typ_aktu`, `ma_html`, `ma_pdf`, `teksty_jednolite`, `error_code`, `pdf_url`, `zrodlo_tekstu`, `text_version`, `pdf_lokalnie`, `uzyj_zamiast` (ISAP); `sygnatura`, `sygnatury`, `saos_id`, `court_type`, `judgment_type`, `uwaga_ocr` (SAOS); `celex` (EUR-Lex); `krs`, `rejestr` (KRS); `jurysdykcja`, `pakiet` (ELI UE).

Przeszukiwanie:

```bash
lexcache find "kara umowna"
lexcache find "znaczne pogorszenie"                       # pełny tekst orzeczeń z korpusu
lexcache find "" --field source=echr --meta-only          # tylko orzeczenia ETPC
lexcache find "" --source isap --field status_obowiazywania=obowiazuje
lexcache find "kara umowna" --bez-korpusu                 # wyłącznie cache
lexcache ls --stale
lexcache purge --stale        # purge NIGDY nie rusza korpusu
lexcache purge --errors
```

`purge` przechodzi także przez `<cache>/isap/_pdf/` — PDF-y to pliki binarne, nie wpisy `.md`, więc bez tego zostawałyby na dysku bez końca (i to one stanowią praktycznie cały rozmiar cache). Ponowne użycie pobranego PDF-a jest ważne przez TTL `isap.pdf` (90 dni); po tym czasie plik pobiera się od nowa, a `--refresh` wymusza to od razu.

### Korpus: normalizacja i indeks

```bash
lexcache korpus normalize --dry-run    # pokaż, co zostanie dopisane
lexcache korpus normalize              # dopisz frontmatter (idempotentne)
lexcache korpus index                  # przebuduj INDEX/INDEX.md + index.jsonl
lexcache migrate --dry-run             # przeniesienie starego cache lokalnego
```

`normalize` dopisuje frontmatter **wyłącznie na początku pliku i nigdy nie dotyka treści** — orzeczenia mają wartość dowodową. Ponowne uruchomienie jest bezczynne. Pliki będące kopiami 1:1 innych (to samo ciało po odjęciu frontmatteru) są pomijane i wypisywane do decyzji właściciela.

Wpisy korpusu dostają `origin: korpus` i **nie mają `expires_at`** — nie wymyślamy TTL dla ręcznie kurowanego pliku. Klasyfikacja `source` odróżnia `saos` / `echr` / `cbosa`: numery typu `34806/04` to **numery skarg do ETPC**, nie sygnatury polskie, więc dostają pusty `court_type`, żeby nie trafiły do zapytań SAOS.

**Teksty w `USTAWY/` to snapshoty**, nie źródło aktualności: mają pole `Wersja od:` i cicho dezaktualizują się przy kolejnym obwieszczeniu. Są wygodne (czysty tekst, tytuły artykułów w nawiasach), ale **nie zastępują szczebla 1 drabinki z `iura` §4**.

`find` przeszukuje frontmatter **i** treść; `--meta-only` ogranicza do frontmatteru. Wpisy wygasłe są oznaczane `[WYGASLY]`. Ponieważ to zwykłe pliki .md, działa też `grep -r` i każde narzędzie do notatek.

---

## Zachowania, które musisz znać przed użyciem wyniku

**ISAP, `isap text` → `isap pdf`** — na obowiązującym tekście jednolitym kodeksu `isap text` zwróci `status: ERROR`, `error_code: text_unavailable_use_pdf`: świeże obwieszczenia są publikowane wyłącznie w PDF. **Nie schodź wtedy do starszego tekstu jednolitego — użyj `isap pdf`:**

```bash
lexcache isap pdf DU/2026/795 --find "Art. 118."
```

Pobiera PDF obowiązującego tekstu jednolitego do cache, wyciąga warstwę tekstu (`mutool`), skleja wyrazy złamane myślnikiem na końcu wiersza i zwraca fragment wokół szukanego artykułu. Frontmatter dostaje wtedy `zrodlo_tekstu: pdf`, `text_version: tekst_jednolity`, `status_obowiazywania: obowiazuje`, `in_force: IN_FORCE` — czyli **dowód brzmienia na dziś**, którego drabinka „zejdź do starszego t.j." nigdy nie dawała. Sam PDF zostaje w `<cache>/isap/_pdf/` i jest w `pdf_lokalnie`.

**Warunek cytowalności — sprawdź, zanim użyjesz wyniku:**

| Co zobaczysz | Co to znaczy | Wolno cytować jako obowiązujące? |
|---|---|---|
| `status: FOUND` + `text_version: tekst_jednolity` | ELI wskazywał obwieszczenie z tekstem jednolitym | **TAK** |
| `status: AMBIGUOUS` + `text_version: tekst_ogloszony_istnieje_nowszy_jednolity` | podałeś ELI **aktu bazowego** — dostałeś brzmienie **pierwotne** | **NIE** — powtórz z ELI z pola `uzyj_zamiast` |

To rozróżnienie jest wymuszone kodem, nie zaufaniem. `isap pdf DU/1964/93 --find "Art. 118."` (akt bazowy KC) zwraca `AMBIGUOUS` i brzmienie z 1964 r. — „w stosunkach między jednostkami gospodarki uspołecznionej… termin przedawnienia wynosi lat dziesięć" — ze `status_obowiazywania: tekst_jednolity_nieaktualny`, które blokuje bramkę MCP-VERIFIED. Ten sam artykuł z obowiązującego tekstu jednolitego (`DU/2026/795`) brzmi „**sześć lat**".

PDF-y starych aktów bazowych to zresztą skany o kiepskiej warstwie tekstu (`uwzg lęd­ nić`), co jest dodatkowym powodem, żeby ich nie używać jako źródła cytatu.

> **Zweryfikuj fragment wzrokowo przed wklejeniem do pisma.** Ekstrakcja z PDF potrafi zgubić spację (zaobserwowane: `niepóźniej` zamiast `nie później`) i zapisuje oznaczenia typu `art. 205¹` jako `Art. 205[1]` — dlatego w `--find` podawaj **zwykłą formę** `Art. 205.`, inaczej dostaniesz `not_found`. Treść normatywna jest prawidłowa, zniekształcone bywa formatowanie — do cytatu dosłownego otwórz `pdf_lokalnie` skillem **`view-pdf`** albo natywnym `Read`.

Jeśli `mutool` nie jest zainstalowany albo PDF nie ma warstwy tekstu, wrapper zwróci `brak_mutool` / `brak_warstwy_tekstu` wraz ze ścieżką pobranego pliku — wtedy przeczytaj go natywnym `Read`, skillem `mac-ocr` (OCR on-device) lub `ugh-ocr`.

`text_version` jest obecne w każdej odpowiedzi `isap pdf` — również przy `status: ERROR` (np. gdy `--find` nie trafi). Dzięki temu nietrafiony `--find` na akcie bazowym da się odróżnić od nietrafionego na tekście jednolitym bez ponownego pobierania.

Starsza droga — `alternatywy` w odpowiedzi `isap text`, czyli lista tekstów jednolitych od najnowszego — zostaje jako plan B (np. gdy PDF jest niedostępny). Pełna drabinka: skill `iura`, sekcja 4.

**SAOS** — pokrycie czasowe jest bardzo nierówne: sądy powszechne do 2026 r., SN tylko do czerwca 2016, TK do grudnia 2015, KIO do 2018. `legalBase` działa wyłącznie przy `--court COMMON`. Daty bywają zniekształcone przez OCR — weryfikuj w `saos.org.pl/judgments/{id}`.

**CBOSA** — to **nie jest API**, tylko scrape formularza HTML. Zwraca listę linków `/doc/<ID>` i fragment tekstu strony, nie ustrukturyzowane orzeczenia. Po serii zapytań pojawia się captcha — stąd TTL 7 dni i zasada „nie odpytuj w pętli". CBOSA jest źródłem orzeczeń **których nie ma w SAOS** (NSA + 16 WSA); w ISAP nie ma żadnych orzeczeń, bo to rejestr aktów prawnych.

**EUR-Lex** — `--lang` domyślnie `POL`; bez polskiej wersji językowej tytuł może nie wrócić, wtedy `--lang ENG`.

**CEIDG** — jedyne źródło z kluczem API. Bezpłatny wniosek na `dane.biznes.gov.pl`, potem `export LEXCACHE_CEIDG_KEY=…`.

**Baza orzeczeń SN (`sn.pl`)** — poza wrapperem. Luka SAOS po czerwcu 2016 r. jest domykalna skryptem `webwright-legal-pl/scripts/fetch_orzeczenie.py` z pluginu `orzecznictwo-zrodla`, ale ten działa przez Playwright, a nie HTTP — szczegóły w `references/ZRODLA.md`.

**Krajowe ELI UE** — `eli fr` wymaga darmowych danych dostępowych **PISTE**; bez nich serwer wystartuje, ale zapytania nie zwrócą treści. Pierwsze uruchomienie każdego kraju pobiera pakiet przez `uvx` i trwa dłużej.

---

## Dlaczego CLI, a nie kolejny serwer MCP

Działa od razu z Basha — bez wpisu w konfiguracji, bez restartu sesji, bez OAuth. Transport to `curl`, nie `urllib`: w środowiskach z inspekcją TLS `urllib` przerywa się na `CERTIFICATE_VERIFY_FAILED`, `curl` przechodzi. Z tego samego powodu istniejące skrypty `saos.py` i `saos_fetch.py` z pluginu `orzecznictwo-zrodla` mogą w takim środowisku nie działać, a `lexcache saos …` zadziała.

Wrapper jest **addytywny** — nie modyfikuje ani nie zastępuje skilli, które wołają narzędzia MCP po nazwie.
