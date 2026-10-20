# grounding-prawo

Prywatny marketplace z jednym pluginem do prowadzenia własnych spraw według prawa polskiego (Claude Desktop, Cowork,
Code; ChatGPT/Codex). Łączy silnik Lex Machina, skille weryfikacji MateMatic i skille własne. Zasada: **źródłem tezy
o przepisie lub orzeczeniu jest narzędzie MCP albo dokument, nigdy pamięć modelu.**

To repo służy do rozwijania pluginu. Praca nad sprawami odbywa się w repo `elconcept/legal` (`legal/AGENTS.md`,
`legal/PRZEWODNIK.md`). Wejście do pracy prawnej: skill `prawny-router-v3`. Reguły, które model dostaje razem z
pluginem: `plugins/grounding-prawo/skills/shared/ZASADY-PLUGINU.md`, `SCIEZKI-PRACY.md`, `ARTEFAKTY-SPRAWY.md`,
`FORMAT-PISMA.md`, `BASIC-MEMORY.md`.

Plugin jest **generowany** - nie edytuj `plugins/grounding-prawo/` ręcznie (sekcja [Utrzymanie](#utrzymanie));
zasady pracy nad repo: `AGENTS.md`.

## 1. Instalacja

Wersja semver (tylko manifest Codex): `selection/selection.yaml`.

| Klient | Jak |
|---|---|
| **Claude Code** | `claude plugin marketplace add elconcept/grounding-prawo`, potem `claude plugin install grounding-prawo@grounding-prawo` |
| **Claude Desktop / Cowork** | Ustawienia organizacji → Plugins → dodaj marketplace z GitHub (repo `elconcept/grounding-prawo`; repo prywatne, więc wymaga autoryzacji GitHub). Po synchronizacji plugin pojawia się w katalogu konta. |
| **ChatGPT / Codex** | `codex plugin marketplace add elconcept/grounding-prawo --ref main --sparse .agents/plugins --sparse plugins/grounding-prawo`, potem `codex plugin add grounding-prawo@grounding-prawo`. |

Po instalacji sprawdź w **nowej rozmowie**: „Użyj prawny-router-v3 i powiedz, co potrafi plugin”. Skille z błędem
ładowania nie pojawią się na liście.

Konektory ładuje `.mcp.json` pluginu: jeden serwer `lex` → `https://lex.xlap.pl/mcp` (portal Cloudflare z logowaniem
OAuth). Bez autoryzacji skille działają, ale nie mogą podawać przepisów ani sygnatur. Pełna lista kontroli instalacji:
`_log/marketplace-validation.md`.

### Aktualizacje

- Manifest pluginu nie ma pola `version`, więc każda zmiana na `main` to nowa wersja (SHA commita).
- Claude Desktop / Cowork: aktualizacja automatyczna; nowa wersja działa w nowej rozmowie.
- Claude Code: auto-update dla marketplace spoza Anthropic jest domyślnie wyłączony. Włącz: `/plugin` → Marketplaces →
  grounding-prawo → Enable auto-update, albo ręcznie `claude plugin update grounding-prawo@grounding-prawo`.
- Codex: jeśli aktualizacja zgłasza `plugin source path is not a directory`, sparse checkout musi obejmować
  `.agents/plugins` i `plugins/grounding-prawo` (usuń marketplace i dodaj go ponownie poleceniem z tabeli).

## 2. Co jest w pluginie

**23 skille do wywołania** i 14 modułów wewnętrznych (`shared`, `prawo-polskie-v2`, `przewodnik-prawny-v2`,
`audyt-systemu-v4`, DR-01…16 bez DR-04, 06-09, 15). Katalog generuje build: `skills/shared/INDEKS-SKILLI.md`.

Skille robiące to samo są scalone: dawny osobny skill jest modułem skilla nadrzędnego (`<skill>/modules/<moduł>/MODULE.md`),
więc nie zajmuje miejsca na liście skilli modelu, a jego treść i skrypty zostają.

| Skill | Moduły scalone |
|---|---|
| `szturm-na-draft-pl` (kontrola pisma w pętli) | `atak-przeciwnika-pl`, `adversarial-legal-review-pl`, `pierwsze-wrazenie-sedziego-pl`, `subsumpcja-pl`, `deliverable-fidelity-pl`, `ocena-outputu-pl`, `marko-pl-content` |
| `citation-grounding-pl` (weryfikacja cytatów) | `ekstraktor-cytatow-pl`, `patron-weryfikacja-cytatow`, `patron-identyfikatory-pl` |
| `odczyt-dokumentow` (przyjęcie dokumentu) | `patron-skan-dokumentu`, `waliduj-podpis-pdf-pl` |
| `wiki-basic-memory` (wiki spraw) | `ingest-wiki` |
| `patron-prawo-pl-zrodla` (źródła prawa) | `webwright-legal-pl`, `uodo-grounding-pl` |
| `kalkulatory-procesowe-pl` (terminy i obliczenia) | `terminy-procesowe-pl` |
| `analizator-umow-v1` | `klauzule-kontraktowe-pl` |
| `chronologia-sprawy-v1` | `chronologia-stanowiska-pl` |
| `orzeczenia-sadowe-v2` | `struktura-wyroku-pl` |
| `analiza-sadowa-v6` | `patron-analiza-akt-karnych` |
| `case-risk` | `medical-consent`, `uoozp-compliance` |

Pozostałe: `prawny-router-v3`, `analizator-dowodow-v3`, `analizator-przepisow-v2`, `pisma-procesowe-v3` (typy pism jako
moduły `modules/typy/`), `pisma-proste-v2`, `przesluchanie-swiadkow-v2-min90`, `zawiadomienie-o-przestepstwie`,
`teczka-sprawy`, `rodo-dsar-pl`, `redline-docx-pl`, `pisz-po-polsku`, `patron-przeglad-tabelaryczny`.

Komendy: tylko `/transkrypcja` (zapis sesji do doskonalenia skilli). Dawne komendy `/sprawa`, `/pismo`, `/kontrola`,
`/zamknij` są sekcjami `shared/SCIEZKI-PRACY.md` routera i skilla `szturm-na-draft-pl`; `/orzeczenie`, `/szukaj`,
`/eurlex` to moduł `webwright-legal-pl`; `/teczka` to skill `teczka-sprawy`. W Claude Code każdy skill wywołasz też
bezpośrednio (`/grounding-prawo:<skill>`).

Profil spraw (decyzje właściciela, `shared/ZASADY-PLUGINU.md`): praca na oryginałach danych, pisma wnoszone osobiście
(podpis autora, bez tytułu zawodowego i numeru wpisu), pełna kontrola każdego pisma bez bramek kosztu, zawiadomienie
o przestępstwie poza torem procesowym routera.

## 3. Dokumenty, wiki i pamięć

- **Odczyt:** `odczyt-dokumentow` - skan bezpieczeństwa, podpis PDF, the-ocr (Markdown ze stronami `## Page N`),
  PyMuPDF i MarkItDown, kontrakt JSON do cytowania. the-ocr pochodzi z prywatnego repo `elconcept/the-ocr`
  (submoduł `vendor/docs/the-ocr`, kopiowany przez build do `tools/the-ocr`, bez `.env`).
- **Ingest do wiki:** wyłącznie przez model, PDF strona po stronie (`the-ocr-ingest-page`, kontrola obrazu, ewentualnie
  ponowny odczyt strony innym silnikiem). Markdown trafia do Basic Memory (projekt `legal`, `dokumenty/`), niezmieniony PDF
  wyłącznie do prywatnego bucketu Cloudflare R2 (`the-ocr-archive`). Bez kolejek, skanów folderów i `wiki_ingest`.
  Procedura: `wiki-basic-memory` (moduł `ingest-wiki`) i `shared/BASIC-MEMORY.md`.
- **Pamięć:** projekty Basic Memory `legal` (sprawy, źródła, ustalenia), `main` (recap każdej sesji w `sesje/`),
  `model-memory` (wyłącznie kuratorowane trwałe ustalenia). Hooki pluginu `SessionStart` i `PreCompact` przypominają
  o odczycie i zapisie; zapis zawsze potwierdza `read_note`.

## 4. Źródła prawa

Kolejność (`shared/ZASADY-PLUGINU.md`): semantycznie Repertorium, potem pełne brzmienie i weryfikacja właściwym MCP
portalu `lex`. Mapa konektorów: skill `patron-prawo-pl-zrodla`.

**Baza ustaw z komentarzem** (`own-skills/patron-prawo-pl-zrodla/scripts/ustawy.py`, SQLite FTS5, bez zależności):

- 37 ustaw z komentarzem do każdego artykułu (`vendor/law/<ustawa>`, forki `elconcept`): kodeksy, Konstytucja,
  ustawy ustrojowe (sądy, SN, prokuratura, adwokatura, radcowie), PPSA, koszty sądowe, prawo medyczne, konsumenckie,
  ochrona lokatorów, Policja, RODO i inne; lista to submoduły w `.gitmodules`;
- przy każdym artykule dosłowne brzmienie z tekstu jednolitego wskazanego w repo (pola `tekst_jednolity`, `eli`)
  i komentarz; nowelizacje późniejsze niż ten tekst jednolity trzeba sprawdzić w ELI.

```bash
python3 own-skills/patron-prawo-pl-zrodla/scripts/ustawy.py buduj            # indeks ustawy.sqlite
python3 own-skills/patron-prawo-pl-zrodla/scripts/ustawy.py art uopl 11 --komentarz
python3 own-skills/patron-prawo-pl-zrodla/scripts/ustawy.py szukaj "obrona konieczna" --akt kk
python3 own-skills/patron-prawo-pl-zrodla/scripts/ustawy.py cytat kk 148 "Kto zabija człowieka"
```

Serwer MCP tej bazy (`ustawy_mcp.py`, narzędzia `akty`, `szukaj`, `artykul`, `cytat`) ma zastąpić konektory `cite` i
`isap`; wdrożenie: `deploy/mcp-ustawy/` (obraz klonuje ustawy według `.gitmodules`). Orzeczenia
SAOS i NSA ma obsługiwać jeden wrapper `elconcept/mcp-prawo-wrapper`. Do przełączenia portalu `lex` reguły pluginu
korzystają z `cite`, `isap`, `saos` i `nsa`. Akty spoza korpusu: ELI (`api.sejm.gov.pl`).

## Utrzymanie

```bash
python3 -I scripts/build.py              # generuje plugins/grounding-prawo z selekcji
python3 -I scripts/validate_marketplace.py
python3 -I scripts/lint_refs.py          # martwe odwołania do skilli i plików
node plugins/grounding-prawo/skills/citation-grounding-pl/scripts/test-grounding.mjs
python3 -m unittest discover -s tests
```

| Co zmienić | Gdzie |
|---|---|
| lista skilli, opisy, scalenia (`merge_into`), typy pism (`fold_into`) | `selection/selection.yaml` |
| przepływ i mosty między skillami | `selection/bridges.yaml` |
| skill własny, typ pisma | `own-skills/<nazwa>/` |
| plik dopisany do pluginu (np. `shared/ZASADY-PLUGINU.md`) | `selection/overlay/` |
| komendy i hooki pluginu | `selection/claude/` |
| zmiana skilla z upstreamu | `selection/patches/NN-*.patch` (nigdy w `vendor/`) |
| reguła generująca (scalanie, czyszczenie, oznaczanie odwołań) | `scripts/build.py` |

Build: kopiuje skille z `vendor/` i `own-skills/`, nakłada overlay i patche, scala moduły (`merge_into`, `fold_into`),
usuwa bloki wspólnych reguł pakietów MateMatic i odwołania do konektora EUREKA, czyści dawne instrukcje anonimizacji,
oznacza odwołania poza pluginem, dopisuje mosty (`MOST`) i protokół pamięci, generuje indeks skilli, komendy i hooki.

CI (`.github/workflows/build-plugin.yml`): build, walidacja, lint, test groundingu, commit wyniku na `main`, synchronizacja
reguł `shared/` do `elconcept/legal` (`scripts/sync_legal.py`, klucz `LEGAL_SYNC_KEY`; `legal-autosync` pobiera je na NAS
co 900 s). Co tydzień job `upstream-bump` buduje plugin na nowych wersjach LexMachina i awesome-matematic-skills i
wypycha gałąź `upstream-bump-RRRRMMDD` i próbuje otworzyć PR; jeśli ustawienia repo nie pozwalają Actions
tworzyć PR, job kończy się błędem po wypchnięciu gałęzi i PR otwiera człowiek.

Historia selekcji: `_log/selekcja.md`, `_log/skill-triage.md`, `_log/source-map.md`.

## Skille do rozwijania tego repo

W `.agents/skills/` (te same źródła w `.claude/skills/` i `.opencode/skills/`): `skill-creator`, `plugin-creator`,
`plugin-structure`, `skill-development`, `mcp-integration`, `feature-factory`, `whitepaper-audit`, `release`,
`interview-me` (wzorzec wywiadu dla `zawiadomienie-o-przestepstwie`). `peer-agent-collaboration` jest globalny w HolyClaude
(`~/.agents/skills`). Pochodzenie i przypięte commity: `.agents/skills/SOURCES.json`. To narzędzia pracy nad
repo, nie składniki pluginu.
