---
name: memo-2026-09-11-lexcache-skille-prawne
description: Co zmieniło się w skillach prawnych i skąd brać źródła — do integracji na pozostałych hostach (Claude Code / opencode).
data: 2026-09-11
host_zrodlowy: macOS, Claude Code (desktop, zakładka Code), użytkownik natcza
dotyczy: 13 skilli IURA, 2 moduły shared LEX-MACHINA, nowy skill lexcache, repozytorium GROUNDING-PRAWO
status: do wdrożenia na pozostałych hostach
sciezki_zaktualizowane: 2026-09-24 (repozytorium abogada - baza w mcp/cache + mcp/index)
---

# Memo: skille prawne + wspólne repozytorium źródeł — 2026-09-11

Do hostów z Claude Code i opencode. Opisuje **co się zmieniło**, **co jest zweryfikowane empirycznie** (żebyście nie wyprowadzali tego drugi raz) i **co zrobić u siebie**.

> **Aktualizacja 2026-09-24.** Baza GROUNDING-PRAWO żyje teraz w repozytorium `abogada` (`D:\abogada`): cache i korpus w `mcp/cache/`, indeks w `mcp/index/`, pośrednik konektorów `mcp/gp-cache.mjs`, konektory w `.mcp.json` projektu, skille w `.claude/skills/` (w Cowork: plugin `grounding-prawo` z `.cowork/build_plugin.py`). Ścieżki poniżej są zaktualizowane; obserwacje z hosta macOS z 11.09 (OneDrive/SMB) zostają jako historia.

---

## 1. Skrót: co zrobić u siebie

```bash
# 1. repozytorium z submodułami (konektory mcp/mcp-*, vendor/*)
git clone --recurse-submodules git@github.com:elconcept/abogada.git && cd abogada
bash mcp/build-servers.sh          # tylko gdy mcp/servers/*.cjs trzeba przebudować

# 2. konektory: .mcp.json projektu (isap, saos, nsa, krs, eu-sparql, eu-compliance, eureka
#    przez mcp/gp-cache.mjs + repertorium, prawo-pl, kio, 9 rejestrów ELI UE przez uvx),
#    zatwierdzone w .claude/settings.json (enabledMcpjsonServers). Wpisy isap/nsa w scope
#    użytkownika (npx, bez cache) powodują konflikt - usuń je:
claude mcp remove isap -s user
claude mcp remove nsa -s user

# 3. usuń pluginy IURA, żeby nie dublowały nazw skilli z .claude/skills
claude plugin uninstall iura-pl@iura-plugins
claude plugin uninstall iura-eu@iura-plugins

# 4. skille są w repozytorium (.claude/skills); Cowork: zainstaluj .cowork/dist/grounding-prawo.zip
python3 .cowork/build_plugin.py

# 5. sprawdź, że wrapper widzi bazę (oczekiwane: repozytorium <repo>/mcp)
python3 .claude/skills/lexcache/scripts/lexcache.py sources --health
```

Zależności `lexcache`: Python 3 + `curl` (obowiązkowo), `mutool` z mupdf-tools (tylko dla `isap pdf`), `uvx` (tylko dla krajowych ELI UE).

---

## 2. Migracja IURA MCP → SAOS + ISAP

Skille dostawcy IURA wołały `Search_DU`, `Search_SN`, `Search_SP`, `Search_TK`, `Search_KIO`, `Find_Ruling`, `Read_Document`, `Show_Sources`. Te narzędzia wymagają płatnego konektora `mcp.iura.io`. Wszystkie 13 skilli przepisano na konektory otwarte.

| Dawne IURA | Zamiennik |
|---|---|
| `Search_DU` | ISAP: `search_acts` → `get_act` → `get_act_text` |
| `Search_SN` / `SP` / `TK` / `KIO` | SAOS: `search` + `courtType` (SUPREME / COMMON / CONSTITUTIONAL_TRIBUNAL / NATIONAL_APPEAL_CHAMBER) |
| `Find_Ruling` | SAOS: `search_by_case` |
| `Read_Document` | SAOS: `get_judgment` (tylko pierwsze 2000 znaków) / ISAP: `get_act_text` |
| `Show_Sources` | **nie wołać** — cytowania są w `structuredContent.citations` |
| `Search_NSA` / `Search_WSA` | brak w SAOS → konektor `nsa` (CBOSA) albo `lexcache cbosa` |
| `Search_IP` (interpretacje podatkowe) | **brak odpowiednika** — `eureka.mf.gov.pl`, nie cytować z pamięci |
| `Search_News` | brak → `WebSearch`, oznaczony jako źródło nieurzędowe |
| — | **`saos_cite_check`** — citator, którego IURA nie miała; obowiązkowy przed zacytowaniem orzeczenia |

**Paradygmat zapytań się odwrócił.** IURA było semantyczne (opisz problem zdaniem). SAOS i ISAP są **polowe/tekstowe** — długie zdanie opisowe zwraca zero wyników. Zasada antyhalucynacyjna została przeformułowana: pamięć wolno użyć do postawienia **klucza wyszukiwania**, potwierdzić może wyłącznie narzędzie.

---

## 3. Fakty zweryfikowane na żywo 11.09.2026 — nie wyprowadzajcie ich ponownie

### SAOS: pokrycie czasowe jest bardzo nierówne

| `courtType` | Najnowsze orzeczenie, jakie zwracają zapytania |
|---|---|
| `COMMON` (sądy powszechne) | **2026** — bieżące |
| `SUPREME` (SN) | **czerwiec 2016** |
| `CONSTITUTIONAL_TRIBUNAL` (TK) | **grudzień 2015** |
| `NATIONAL_APPEAL_CHAMBER` (KIO) | **wrzesień 2018** |

Nie da się napisać „aktualna linia SN" na podstawie SAOS. Obejście: sądy powszechne są aktualne i cytują SN — `search(courtType: "COMMON", all: "<fraza z tezy SN>")` pokaże, czy pogląd jest dziś stosowany. Na tym stoi też `saos_cite_check`.

### SAOS: `legalBase` działa tylko dla COMMON

Przy `courtType: "SUPREME"` pole zwraca pusto (sprawdzone dla `"art. 415 kc"`, `"art. 203 kpc"`, `"415"`). Dla SN kotwicz na `all` z krótką frazą (2–5 słów).

### ISAP: obowiązujący tekst jednolity kodeksu jest PDF-only

`get_act_text` na akcie bazowym zwraca **brzmienie pierwotne** (KC z 1964 r.: „lat dziesięć"), a na obowiązującym obwieszczeniu — błąd `text_unavailable_use_pdf`, bo świeże obwieszczenia publikowane są wyłącznie jako PDF. Dotyczy KC, KPC, KPK i KP. **Nie ma parametru `in_force_as_of`.**

Rozwiązanie (`lexcache isap pdf`): PDF-y ISAP mają prawdziwą warstwę tekstu, więc `mutool draw -F txt` wyciąga z nich brzmienie obowiązujące. Zweryfikowane: KC art. 118 („sześć lat"), KPC art. 203 § 1, KPK art. 306 § 1, KP art. 30 § 1.

**Pułapka, na którą trzeba uważać:** PDF **aktu bazowego** to brzmienie pierwotne, nie tekst jednolity. `lexcache` rozróżnia je po `references` aktu (`Tekst jednolity dla aktu` vs `Inf. o tekście jednolitym`) i zwraca wtedy `status: AMBIGUOUS` + `status_obowiazywania: tekst_jednolity_nieaktualny` + przekierowanie w `uzyj_zamiast`. Jeśli budujecie coś własnego — odtwórzcie tę bramkę.

### Inne pułapki techniczne

- **`urllib` vs `curl`**: przy inspekcji TLS `urllib` rzuca `CERTIFICATE_VERIFY_FAILED: self-signed certificate in certificate chain`; `curl` przechodzi. Skrypty `saos.py` i `saos_fetch.py` z pluginu `orzecznictwo-zrodla` w takim środowisku **nie zadziałają**.
- **EUR-Lex SPARQL**: `Accept: application/json` daje `406 Not Acceptable`. Poprawny nagłówek to `application/sparql-results+json`.
- **FastMCP przez stdio** (krajowe ELI UE przez `uvx`): wysłanie wszystkich wiadomości naraz i zamknięcie stdin kończy serwer przed obsłużeniem `tools/list`. Trzeba pisać po jednej wiadomości i czekać na odpowiedź o tym samym `id`.
- **SUDOP**: pusty wynik to `"\n"` z HTTP 200, nie 404 — klasyfikować jako NOT_FOUND, nie FOUND.
- **Ekstrakcja z PDF** gubi pojedyncze spacje (`niepóźniej` zamiast `nie później`) i zapisuje `art. 205¹` jako `Art. 205[1]` — w wyszukiwaniu podawać zwykłe `Art. 205.`, a cytat dosłowny weryfikować wzrokowo.

---

## 4. Nowy skill: `lexcache`

Jeden wrapper CLI na wszystkie źródła używane przez LEX-MACHINA i MateMatic, z lokalnym cache w plikach `.md` z frontmatterem YAML.

Źródła: **ISAP** (Sejm ELI), **SAOS**, **CBOSA** (NSA/WSA, scrape HTML), **EUR-Lex/CELLAR**, **KRS**, **NBP**, **SUDOP**, **CEIDG** (wymaga klucza), **9 krajowych rejestrów ELI UE** przez `uvx` (`fr` wymaga danych PISTE).

```bash
L=.claude/skills/lexcache/scripts/lexcache.py
python3 $L sources --health
python3 $L isap pdf DU/2026/795 --find "Art. 118."     # brzmienie obowiązujące z PDF
python3 $L saos search --all "kara umowna" --court COMMON --legalbase "art. 483 kc"
python3 $L find "przedawnienie" --field source=echr    # szuka w cache I w korpusie
python3 $L korpus normalize && python3 $L korpus index
```

TTL per typ zapytania (od 1 dnia dla KRS/NBP do 180 dni dla `saos get`), każdy wpis ma `expires_at`, odczyt wygasłego wypisuje ostrzeżenie i kończy się kodem 3. `purge` nigdy nie rusza korpusu — także gdy korpus leży wewnątrz cache (`mcp/cache/orzeczenia/`, `ustawy/`, `kodeks/`, ...; poprawione 2026-09-24).

**Relacja do MCP:** `lexcache` jest **dodatkiem, nie zamiennikiem**. Skille prawne kierują do niego **jednym konkretnym przejściem** — gdy `get_act_text` zwróci `text_unavailable_use_pdf`. Rutynowy research zostaje na konektorach MCP, bo mają citator.

---

## 5. Wspólne repozytorium GROUNDING-PRAWO

**Stan od 2026-09-24:** baza = katalog `mcp/` repozytorium `abogada` (`mcp/cache/` + `mcp/index/`), kopia zapasowa w prywatnym GitHub. Stara kopia `E:\OneDrive\LEGAL\GROUNDING-PRAWO` na hoście Windows jest podzbiorem nowej bazy i nie jest już zasilana — wygrywa tylko poza projektem, gdy żadna baza `mcp/` nie jest widoczna.

Historia (host macOS, 11.09): dwie drogi dostępu do **tych samych danych** (potwierdzone identycznymi sumami md5):

| Droga | Ścieżka | Stan na tym hoście |
|---|---|---|
| OneDrive (sync lokalny) | `~/OneDrive/GROUNDING-PRAWO` | ✅ działa |
| SMB | `/Volumes/GROUNDING-PRAWO` (`//10.0.10.200/GROUNDING-PRAWO`) | ⚠️ **odczyt niesprawny** |

### ⚠️ Udział SMB nie nadaje się tu na ścieżkę odczytu

Na tym hoście **42 z 59 plików w `ORZECZENIA/` zwraca `Errno 5 Input/output error`** przy próbie odczytu, mimo że `stat` podaje poprawny rozmiar, a `dd` czyta z nich 0 bajtów. Zimny odczyt pojedynczego pliku też pada, więc to nie jest wyczerpanie uchwytów ani limit prędkości. Te same pliki czytają się bez problemu przez OneDrive. **Udział wymaga uwagi po stronie NAS-a** — nie diagnozowałem dalej, bo to osobne zadanie.

Wnioski dla Was: **nie zakładajcie z góry, która ścieżka działa.** `lexcache` i `mcp/gp-cache.mjs` rozstrzygają to same, testując każdego kandydata realnym **zapisem i odczytem** (`touch`/`stat` nie wystarcza — na uszkodzonym udziale oba przechodzą). Baza to katalog z `cache/` i `index/` (wielkość liter dowolna, `CACHE/`+`INDEX/` też). Kolejność:

1. `LEXCACHE_DIR` (wymuszenie samego cache; tylko lexcache)
2. `GROUNDING_ROOT` (wymuszenie korzenia bazy, np. `<repo>/mcp`)
3. katalog bieżący, `CLAUDE_PROJECT_DIR`, katalog repozytorium nad skillem — każdy z nich i jego `mcp/`
4. podpięty folder Cowork: `/sessions/*/mnt/*` i `/sessions/*/mnt/*/mcp`
5. OneDrive: `~/OneDrive[/LEGAL]/GROUNDING-PRAWO`, `~/Library/CloudStorage/OneDrive-*/GROUNDING-PRAWO`, `E:\OneDrive\LEGAL\GROUNDING-PRAWO`, `/mnt/e/OneDrive/LEGAL/GROUNDING-PRAWO`
6. `/Volumes/GROUNDING-PRAWO`
7. fallback lokalny: `~/.claude/cache/lexcache` (lexcache), `~/.cache/grounding-prawo/CACHE` (gp-cache)

Poza projektem ustawcie `GROUNDING_ROOT=<repo>/mcp`, inaczej wygra OneDrive albo fallback.

### Obsługa OneDrive: nie trzeba żadnego MCP ani skilla

macOS montuje OneDrive przez File Provider jako zwykły katalog (`~/OneDrive`, `~/Library/CloudStorage/OneDrive-Osobisty`). To jest najtańsza możliwa obsługa — zwykłe `open()`, bez tokenów, bez API, bez limitów. Konektor do Graph API byłby tu kosztem bez korzyści. Na Linuksie/Windows: `rclone` z backendem `onedrive` albo natywny klient — ważne tylko, żeby katalog był widoczny w systemie plików.

### Stary cache lokalny — źródłem prawdy jest repozytorium

`migrate` **kopiuje, nie przenosi** (przenosi dopiero z `--usun-zrodlo`). Na tym hoście uruchomiłem go bez tej flagi, więc pod `~/.claude/cache/lexcache` leży nadal komplet 43 MB. Jest nieaktywny — rozstrzyganie ścieżki wybiera repozytorium — ale **od teraz będzie się cicho rozjeżdżał**. Autorytatywne jest `mcp/cache/` repozytorium; stary katalog możecie skasować albo zostawić jako zapasową kopię, byle świadomie.

### Czyszczenie cache obejmuje też PDF-y

PDF-y ISAP (`mcp/cache/isap/_pdf/`, ~43 MB, czyli praktycznie cały rozmiar cache) to pliki binarne, nie wpisy `.md`. Do 11.09.2026 `purge` ich nie widział i serwowały się w nieskończoność jako świeże — nawet po skasowaniu towarzyszącego wpisu. Naprawione: ponowne użycie PDF-a sprawdza teraz jego wiek względem TTL 90 dni (`--refresh` wymusza pobranie), a `purge --stale` / `purge --all` przechodzi też przez `_pdf/`. Jeśli kopiowaliście `lexcache.py` wcześniej — weźcie nowszą wersję.

### Układ repozytorium

```
abogada/mcp/                  ← GROUNDING_ROOT
├── gp-cache.mjs, gp-refresh.mjs, build-servers.sh, servers/*.cjs|mjs
├── cache/
│   ├── orzeczenia/           54 orzeczenia (korpus, origin: korpus) — SN, SA, NSA, ETPC
│   ├── ustawy/ kodeks/ rozporzadzenia/ uchwaly/ zarzadzenia/   teksty ujednolicone (.md, format LEX)
│   ├── isap/ saos/ cbosa/ eurlex/ eureka/ krs/ nbp/ sudop/     lexcache + konektory (mcp-*.md), isap/_pdf/
│   └── eu-compliance/regulations.db                            korpus offline konektora eu-compliance
└── index/                    ← INDEX.md (czytelny) + index.jsonl (maszynowy), `lexcache korpus index`
```

Stary układ (`ORZECZENIA/`, `USTAWY/`, `OPRACOWANIA/`, `MAPY/`, `CACHE/`, `INDEX/`) jest nadal rozpoznawany.

`korpus index` przy każdym przebiegu czyta wszystkie pliki od nowa. Przy 74 wpisach to ułamek sekundy; przy paru tysiącach, na udziale sieciowym, będzie to pełny round-trip na plik — wtedy warto dołożyć inkrementalność po mtime.

---

## 6. Ujednolicony frontmatter korpusu

Wszystkie 54 unikalne orzeczenia miały **cztery różne formaty nagłówka** i **zero frontmatteru**. Zostały znormalizowane — `lexcache korpus normalize` dopisuje frontmatter **wyłącznie na początku, nie dotykając treści** (zweryfikowane: 54/54 ciała bajt w bajt identyczne z kopią sprzed zmiany), i jest idempotentny.

```yaml
---
status: FOUND
query_type: orzeczenie
origin: korpus            # vs `cache` dla wpisów pobranych przez lexcache
source: saos              # saos | echr | cbosa | isap-lokalny | opracowanie
tool: korpus.orzeczenia
identyfikator: III CSKP 124/21
sygnatura: III CSKP 124/21
tytul: "III CSKP 124/21 - Sąd Najwyższy"
sad: Sąd Najwyższy
court_type: SUPREME       # enum SAOS; PUSTY dla ETPC i sądów administracyjnych
typ_orzeczenia: POSTANOWIENIE
data: "2021-10-26"
status_obowiazywania: nieznany
plik: "III_CSKP_124-21.md"
confidence: reczna_kuracja
pii_risk: high
znormalizowano: "2026-09-11T00:30:26Z"
---
```

Nazwy pól są **te same, których używa cache `lexcache`**, więc jedno `lexcache find` przeszukuje obie warstwy naraz. Wpisy korpusu **nie mają `expires_at`** — nie wymyślamy TTL dla ręcznie kurowanego pliku.

Klasyfikacja źródła: 50 × `saos`, 6 × `echr`, 3 × `cbosa`, 0 nieznanych, 0 braków daty. **Numery typu `34806/04` to numery skarg do ETPC, nie sygnatury polskie** — dostają `source: echr` i pusty `court_type`, żeby nie trafiły do zapytań SAOS. Podobnie `III OSK` (NSA) i `WA`/`SD` (SN, izba wojskowa/dyscyplinarna).

Gdzie pola nie dało się ustalić — zostaje puste. Pusta data jest odwracalna, zła nie jest.

---

## 7. Znane braki w korpusie — do decyzji właściciela

1. ~~5 plików bez rozszerzenia (kopie 1:1)~~ — w `mcp/cache/orzeczenia/` ich już nie ma (stan 2026-09-24: 54 pliki `.md`).
2. ~~`USTAWY/Ustawa_o_srodkach_przymusu_bezposredniego_i_broni_palnej.md.docx` 0 B~~ — obecnie `mcp/cache/ustawy/ustawa_o_srodkach_przymusu_bezposredniego_i_broni_palnej.md` ma treść (Dz.U. 2026 poz. 244).
3. **Teksty w `mcp/cache/ustawy/` i `kodeks/` to snapshoty** z polem `Wersja od:`. Są wygodne i czyste (mają nawet tytuły artykułów w nawiasach), ale **nie zastępują ścieżki ISAP** — przy kolejnym obwieszczeniu cicho się dezaktualizują. Traktować jako pomoc, nie jako dowód brzmienia na dziś.

---

## 8. RODO — jedna rzecz do świadomej decyzji

`mcp/cache/` gromadzi orzeczenia z SAOS (anonimizacja bywa niepełna) i odpisy KRS — **dane osobowe**. Repozytorium jest wypychane do prywatnego GitHub (wcześniej: OneDrive), czyli do chmury zewnętrznej. To świadoma decyzja właściciela, ale każdy host, który podłączy się do tej bazy, staje się kolejnym miejscem przetwarzania. Jeśli u Was obowiązuje inny reżim — ustawcie `LEXCACHE_DIR` na katalog lokalny i korzystajcie z repozytorium tylko do odczytu korpusu.

Frontmatter niesie `pii_risk: low|high` — wpisy `high` traktować jak akta.

---

## 9. Czego świadomie nie zrobiłem

- **Skille `iura-nl`** (7, prawo niderlandzkie) — nieprzeniesione: nie są zainstalowane, a konektory polskie nie obsłużą prawa holenderskiego.
- **Baza orzeczeń SN `sn.pl`** — to zamknęłoby lukę SAOS po 2016 r. Skrypt istnieje (`webwright-legal-pl/scripts/fetch_orzeczenie.py`), ale działa przez Playwright, nie HTTP — złamałoby to zasadę „stdlib + curl" w `lexcache`. Do rozważenia jako osobna, opt-in ścieżka.
- **Diagnostyka udziału SMB** — poza zakresem; zgłoszone w punkcie 5.

---

*Memo wygenerowane przez Claude Code na hoście macOS użytkownika natcza, 2026-09-11. Wszystkie liczby i zachowania API sprawdzone wywołaniem tego dnia — jeśli czytacie to znacznie później, zweryfikujcie punkt 3 ponownie.*
