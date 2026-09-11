---
timestamp: 2026-09-11T10:43:49Z
sesja: Cowork / Claude (claude-opus-5)
zakres: import skilli, pluginów i narzędzi prawnych do GROUNDING-PRAWO + inicjalizacja repozytorium publicznego
autor_wpisu: asystent
---

# Import warstwy skilli prawnych do GROUNDING-PRAWO oraz inicjalizacja repozytorium

## 0. Zasada nadrzędna tej sesji

Katalog `GROUNDING-PRAWO` jest **współdzielony** — pracuje na nim więcej niż jedna
sesja/osoba. W związku z tym w całym przebiegu obowiązywała reguła: **wyłącznie
dokładanie własnych plików, zero usuwania, zero modyfikowania cudzych plików.**
Prośba o uprawnienie do usuwania plików została świadomie odrzucona przez
użytkownika i nie była ponawiana — wszystkie porządki wykonano przez `mv`
(przeniesienie własnych plików do własnego podkatalogu), nigdy przez `rm`.

Stan zastany przed tą sesją (nietknięty): `CACHE/`, `INDEX/`, `MAPY/`,
`ORZECZENIA/`, `USTAWY/`, `TEMP/Lex-Machina-main.zip`, `_log.md`,
`.claude/{.env,.log,.secrets,.skills,.src}`.

---

## 1. Co zostało dołożone i gdzie

### 1.1 `.claude/skills/` — silnik dostosowany (34 skille, 18 MB)

Kompletne drzewo Lex-Machina w wersji **stabilnej 21.08.2026**, w stanie
**po modyfikacjach wykonanych w tym projekcie**. To nie jest surowa kopia
dystrybucji — to wersja, w której naprawiono dwa problemy blokujące pracę
poza środowiskiem claude.ai:

**a) Usunięcie ścieżek absolutnych.** Skille adresowały moduły współdzielone
jako `/mnt/skills/user/shared/…` — ścieżkę montażu claude.ai. Po przeniesieniu
drzewa gdziekolwiek indziej **753 odwołania `view()` wskazywały na nieistniejące
pliki**. Zamieniono **913 wystąpień w 214 plikach** (`.md`, `.py`, `.sh`) na
ścieżki względne wobec korzenia katalogu skilli. Poprawiono również
`VIEW_PATTERN` oraz domyślne `--repo-root` w skryptach kontrolnych.

**b) Niezależność kontroli spójności od katalogu uruchomienia.**
`ci_check_shared.py` rozwiązywał odwołania `view()` względem CWD, nie względem
`--repo-root`. Oznaczało to, że wynik kontroli zależał od tego, z którego
katalogu uruchomiono skrypt. Funkcja `check_broken_links()` korzysta teraz
z `resolve_relative_ref(…, repo_root)`.

Wynik po obu naprawach: **753 zerwane odwołania → 0**, niezależnie od CWD.

```
python3 .claude/skills/audyt-systemu-v4/scripts/ci_check_shared.py --repo-root .claude/skills
→ WYNIK: OK — brak zerwanych odwołań.
```

**c) `audyt-systemu-v4` podbity 6.13 → 6.14.** Zarejestrowano dwie nowe
generacje mapy Dz.U. (`mapa_dzu_2026-09-07.md`, `mapa_dzu_2026-09-10.md`),
przełączono wskaźnik ⭐ AKTUALNA na 2026-09-10 i poprawiono wszystkie
odwołania w `SKILL.md` (frontmatter `references:`, instrukcja `view`,
FAZA 3, FAZA 7B, drzewo w sekcji struktury). Do `references/` wgrano też
zaległe wyniki trzech przebiegów zaplanowanych: trzy wpisy do
`AUDIT-JOURNAL.md`, flagi F-107/F-108/F-109 z aktualizacją licznika
w TABLICY STERUJĄCEJ (8→11 / 13→16) i przebudowaną tabelę MONITORING.

Lista skilli: `analiza-sadowa-v6`, `analizator-dowodow-v3`,
`analizator-przepisow-v2`, `analizator-umow-v1`, `audyt-systemu-v4`,
`chronologia-sprawy-v1`, `dr-01` … `dr-16` (16 modułów dziedzinowych +
`dr-09-out`), `orzeczenia-sadowe-v2`, `pisma-procesowe-v3`, `pisma-proste-v2`,
`prawny-router-v3`, `prawo-polskie-v2`, `przesluchanie-swiadkow-v2-min90`
(+ wariant `-v35`), `przewodnik-prawny-v2`, `raport-klienta-v1`,
`raport-sytuacyjny-v2`, `shared` (125 modułów kanonicznych).

### 1.2 `.claude/scheduled/` — instrukcje zadań cyklicznych (3)

`monitoring-nowych-dzu--tj` (codziennie 04:00), `peny-audyt-systemu`
(sobota 09:30), `zamykanie-otwartych-flag` (niedziela 09:30).

Prompty są **kanoniczne i samodzielne** — każde uruchomienie startuje bez
pamięci poprzednich rozmów, więc instrukcja zawiera komplet: które pliki
wczytać, które fazy wykonać, gdzie zapisać wynik, jaką kontrolę uruchomić
po zapisie. Zawierają bramki jakości („nigdy z pamięci", „nie zgaduj numeru
Dz.U.", „zgodność numeru nie dowodzi tożsamości aktu").

### 1.3 `TEMP/_pluginy-cowork/` — 15 pluginów Cowork (622 pliki, ~3,5 MB)

Pluginy wyjęte z synchronizowanego katalogu Cowork i przeniesione w całości
(skille + `commands/` + `.mcp.json` + assety + skrypty pomocnicze), razem
z plikami `*.meta.json` i zbiorczym `manifest.json`:

| Plugin | Zawartość istotna dla praktyki prawniczej |
|---|---|
| `orzecznictwo-zrodla` | **rdzeń darmowych źródeł**: SAOS (REST API, Fundacja ePaństwo), EUR-Lex/Cellar (SPARQL), `legal-data-hunter-pl` (bulk-harvest UODO/UOKiK/KNF/UKE/URE/KIO/NSA/TK/SN/Sejm ELI), `webwright-legal-pl` (Playwright do orzeczenia.ms.gov.pl / sn.pl / trybunal.gov.pl), `hierarchia-zrodel-pl`, `struktura-wyroku-pl`, `uodo-grounding-pl` |
| `fundament-weryfikacyjny` | warstwa anty-halucynacyjna: `citation-grounding-pl` (gradient ISTNIENIE/TREŚĆ/FRAGMENT), `ekstraktor-cytatow-pl`, `deliverable-fidelity-pl`, `adversarial-legal-review-pl`, `atak-przeciwnika-pl`, `pierwsze-wrazenie-sedziego-pl`, `subsumpcja-pl`, `legal-request-router-pl`, `ocena-outputu-pl`, `intake-sufficiency-pl`, `legal-ai-audit-bundle` |
| `dokumenty` | `doc-intel-contract-pl` (kontrakt OCR: block_type/bbox/text/confidence + flagi PII), `doc-intel-llm-tier-pl`, `terminy-procesowe-pl`, `kalkulatory-procesowe-pl`, `klauzule-kontraktowe-pl`, `redline-docx-pl`, `waliduj-podpis-pdf-pl` (pyHanko, eIDAS/PAdES), `let-it-be` (anonimizacja offline), `markitdown`, `opendataloader-pdf` |
| `iura-pl`, `iura-eu` | szablony pism: pozew, odpowiedź na pozew, apelacja karna, zażalenie na postanowienie prokuratora, zarzuty do opinii biegłego, wniosek o rozprawę zdalną, notatka prawna, memo EU |
| `ochrona-danych` | RODO: DPIA, DSAR, naruszenie 72h, RoPA/DPA, NIS2/KSC |
| `governance-kancelarii` | AI Act triage, Konstytucja AI kancelarii, expert panel, `tajemnica-preflight-pl` (bramka tajemnicy zawodowej przed wysłaniem promptu do chmury) |
| `jakosc-tresci` | `humanizer-pl`, `marko-pl-content` |
| `dev-mcp` | budowa własnych MCP (FastMCP), installer marketplace, spec-driven |
| `legal~g2` | plugin Anthropic knowledge-work (triage NDA, review kontraktu, vendor check) |
| `pdf-generation`, `pdf-viewer`, `tufte-report` | generowanie i przegląd PDF, raporty |
| `desktop-commander~g2`, `exa~g2` | narzędzia ogólne — `exa` jest **płatne**, więc stoi w sprzeczności z założeniem „wyłącznie darmowe źródła"; dołożone do triage'u, nie do kanonu |

Archiwum źródłowe przebiegu: `TEMP/_pluginy-cowork/cowork-plugins-prawne.tar.gz`
(zostawione, bo w tej sesji nie było uprawnienia do usuwania; można je skasować
ręcznie — jest identyczne z rozpakowaną zawartością).

---

## 2. Kontrola danych wrażliwych przed upublicznieniem

Repozytorium jest **publiczne**, więc przed inicjalizacją wykonano skan
**całego drzewa** (nie tylko plików dołożonych w tej sesji): 1517 plików
tekstowych, 10 klas wzorców.

| Klasa | Trafień surowych | Ocena po weryfikacji kontekstu |
|---|---|---|
| Klucze API / tokeny (`sk-`, `ghp_`, `AKIA`, `xox*`) | **0** | czysto |
| Sekret w przypisaniu (`api_key=`, `password=` …) | **0** | czysto |
| Sygnatury spraw użytkownika | **0** | czysto |
| PESEL (11 cyfr) | 608 | **fałszywe** — identyfikatory ISAP (`20260000199` = WDU20260000199) |
| NIP/REGON | 91 | **fałszywe/publiczne** — REGON `524731175` i KRS `0000796445` (HP sp. z o.o.) jako przykłady formatu; reszta to stałe liczbowe w kodzie vendora |
| IBAN PL | 1 | **fałszywy** — kanoniczny IBAN testowy w `test_pii.py` anonimizatora |
| E-mail | 29 | **publiczne/przykładowe** — `example.com`, `admin@kancelaria.pl`, `handelludzmibsk@policja.gov.pl` (adres instytucjonalny KGP) |
| Telefon PL | 16 | **fałszywe/publiczne** — zakresy liczbowe („187 500-937") oraz infolinia KGP `664-974-934` |
| Nazwiska stron postępowań | 2 | **fałszywe** — domena `gasiorowska.eu` cytowana jako źródło |
| Ścieżka `/Users/tom` | 14 | 1 wystąpienie w `AUDIT-JOURNAL.md` — **zgeneralizowane** w tej sesji; 13 w `_log.md` — **plik cudzy, nietknięty** |

Nie skanowano treściowo: 9 plików PDF (Dziennik Ustaw z ISAP — źródła publiczne)
oraz `TEMP/Lex-Machina-main.zip` (archiwum silnika, własność użytkownika).
Osobny skan sekretów objął `.ts/.mjs/.jsx/.js/.sh/.yaml` — zero trafień.

**Wniosek: brak danych wrażliwych w materiale dołożonym w tej sesji.**

⚠️ **Do decyzji użytkownika (nie moja):** plik `_log.md` w korzeniu repozytorium
zawiera 13 odwołań do lokalnych ścieżek `/Users/tom/…`. To nie jest dana
wrażliwa w rozumieniu RODO, ale ujawnia nazwę użytkownika i układ dysku.
Plik nie jest mój — nie ruszałem go.

---

## 3. Repozytorium

- `git init`, gałąź `main`.
- `.gitignore` obejmuje — zgodnie z poleceniem — `.claude/.secrets`, `.env`,
  `.claude/.src`, a dodatkowo `.claude/.env`, `.tmp/`, `.DS_Store`,
  `__pycache__/` i archiwum przebiegu.
- Origin: publiczne repozytorium GitHub.

---

## 4. Dług otwarty

1. `exa~g2` w `TEMP/_pluginy-cowork/` to narzędzie **płatne** — sprzeczne
   z założeniem „wyłącznie darmowe źródła". Do decyzji: zostaje jako opcja
   komercyjna czy wypada z kanonu.
2. Pluginy w `TEMP/` czekają na triage — które trafiają do `.claude/skills/`
   jako kanon repozytorium, a które zostają materiałem referencyjnym.
3. `.claude/.skills` (z kropką, pusty) i `.claude/skills` (bez kropki, dołożony
   w tej sesji) współistnieją. Nie wiem, która konwencja jest zamierzona —
   pustego katalogu nie ruszałem.
4. Brak `README.md` w korzeniu opisującego przeznaczenie repozytorium
   dla osób z zewnątrz — a to repo ma być publiczne.
5. Dla warstwy cache/indeks nie ma jeszcze opisu kontraktu `index.jsonl`
   ani dokumentacji `lexcache.py` — bez tego repo jest trudne do przejęcia
   przez kogoś spoza projektu.
