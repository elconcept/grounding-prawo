# 2026-11-02 — USTAWY: RODO, dyrektywa 2016/680 (LED) i DODO

**Status: kod na osobnej gałęzi, test GitHub Actions PASS, NIE wdrożono i NIE scalono.**
**Zależność:** gałąź z PR #81 `feat/eli-local-resolver-20261031`; osobny PR tej zmiany powinien mieć jako bazę tę gałąź, nie `main`.

## Cel i weryfikacja źródeł

Użytkownik potrzebuje polskich norm ochrony danych na potrzeby monitoringu i działania organów ścigania oraz wyszukiwarki wyroków TSUE; nie potrzebuje uniwersalnego MCP do compliance.

- **UODO** (ustawa 10.05.2018, `DU/2018/1000`) **już istnieje**: `.gitmodules` zawiera `vendor/law/o-ochronie-danych-osobowych`; katalog ma 132 jednostki według opisu źródła, bazuje na tekście jednolitym Dz.U. 2019 poz. 1781. Nie powielono. Stan po późniejszych nowelizacjach wymaga weryfikacji urzędowej.
- **RODO** `CELEX:32016R0679`: `legalize-dev/legalize-eu` jest autentycznym git-as-law (historia commitów), ale źródło angielskie. Wybrano polski dokument `eudirective/public-data`, przypięty do commita, 99 artykułów; osobny historyczny plik English `legalize-eu` służy do śledzenia pochodzenia, nie jest indeksowany.
- **LED / dyrektywa policyjna** `CELEX:32016L0680`: polski snapshot EUR-Lex/CELLAR z `eudirective/public-data` — 65 artykułów.
- **DODO** `DU/2019/125`: plik z `legalize-dev/legalize-pl`, **tekst pierwotny 2018, a nie aktualny tekst jednolity**, 108 artykułów. Aktualny tekst sprawdzaj przez ELI; znany tekst jednolity `DU/2023/1206` nie został tu zaimportowany.
- Źródła i wersje: `deploy/mcp-ustawy/fetch_data_protection.py` — konkretne commity Git, SHA blob, identyfikatory ELI/CELEX, polski język; przy zmianie bitów build kończy się błędem, nie domyślnym akceptowaniem.
- Weryfikacja źródeł zewnętrznych: https://github.com/legalize-dev/legalize-eu/blob/cf58758b3956abd728899a347837b19b49ea6945/eu/6e/32016R0679.md ; https://github.com/legalize-dev/legalize-pl/blob/663baba7eff0730cb169bca8df2de0fc1ef4b46d/pl/DU-2019-125.md ; https://github.com/eudirective/public-data/tree/6650d22a40379c8f2182b0086c24fded22262055/source-library/core/pl/eu

## Zmiany w kodzie

1. `fetch_data_protection.py` pobiera cztery **pojedyncze pliki** z przypiętych commitów, zamiast klonować gigabajtowe repozytoria. Weryfikuje Git blob SHA1, kontekst tekstu PL i zapisuje SHA256 do manifestu.
2. `data_protection_git.py` ekstrahuje `Artykuł 1–99`, `Artykuł 1–65`, `Art. 1–108`, wymaga ciągłej numeracji, i dodaje `rodo/led/dodo` do tej samej bazy SQLite + FTS.
3. `ustawy.py`: aliasy `rodo/gdpr`, `led/dyrektywa-policyjna`, `dodo`; rozszerzenie lookupu CELEX w `akt_po_eli`; DODO odmawia trybu po ELI (`OUT_OF_SCOPE`) **aby nie przedstawiać starego tekstu jako aktualnego**. `artykul('dodo','23')` zwraca historyczny tekst z wyraźnym ostrzeżeniem.
4. Dockerfile kompiluje bazę z dotychczasowych `vendor/law/*`, `vendor/law-git/*` i trzema nowymi źródłami.
5. Workflow `.github/workflows/ustawy-data-protection-git.yml` testuje prawdziwe pobranie ze zdalnego Git, integralność hash, SQLite, pełną numerację, artykuły, działanie CELEX i **brak regresji istniejącego UODO** (klonuje tylko jedną istniejącą ustawę). Bez sekretów produkcyjnych, bez deploy.

**Wynik:** GitHub Actions https://github.com/elconcept/grounding-prawo/actions/runs/41367781044 — SUCCESS. Import czterech aktów w izolowanym SQLite, 99+65+108 artykułów nowych, istniejąca UODO obecna. To nie jest test pełnego kontenera na NAS ani Cloudflare.

## Ograniczenia i następne etapy

- Słowo **git-as-law** nie oznacza automatycznej aktualności. Import reprezentuje wersje *pinned snapshot*, nie kompletną historię zmian prawnych; RODO/LED PL mają oznaczenie wydania 2016. DODO jest szczególnie stary. Brak walidacji z aktualnym tekstem skonsolidowanym w EUR-Lex/ELI. Nie wolno opierać aktualnych cytatów na starym źródle bez tego kroku.
- USTAWY w PR #81 jest wewnętrznym źródłem. Resolver `pobierz_dokument` w mcp-prawo-wrapper PR #4 może nadal wymagać osobnego routingu `CELEX` z USTAWY; nie udawać, że przetestowano pełne end-to-end klient→portal→resolver→USTAWY.
- Testy: powtórzyć na pełnej bazie wszystkich submodułów i z oficjalnym ELI/CELLAR, następnie staging Cloudflare. Brak merge/deploy do ukończenia.
- **Dalsze dyrektywy:** `2016/681` (PNR, dane pasażerów), `2023/977` (wymiana informacji organów ścigania) należy rozważyć jako *odrębne* rozszerzenia, po znalezieniu zweryfikowanej polskiej wersji i ustaleniu, że rzeczywiście są potrzebne. Wycofanej decyzji ramowej `2008/977/WSiSW` nie traktować jako obowiązującej.
- **Orzecznictwo:** utrzymać dostęp do TSUE (C‑212/13 `Ryneš`, ECLI:EU:C:2014:2428; C‑530/23 `Barało`, ECLI:EU:C:2025:322), a dla przymusowej hospitalizacji również *osobno* ETPC/HUDOC (np. `Winterwerp`). Nie mylić TSUE z ETPC. Żaden z powyższych wyroków nie został zaindeksowany w USTAWY — to repo przepisów, nie wyroków.

## Warunki bezpieczeństwa

Nie zmieniać istniejącego REPERTORIUM ani Cloudflare; brak merge do `main`, brak restartów, brak modyfikacji PR #3/#4 i #81. Każde źródło i przypadek dowodowy w języku polskim w interfejsie.
