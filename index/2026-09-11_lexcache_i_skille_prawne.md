---
name: memo-2026-09-11-lexcache-skille-prawne
description: Co zmieniło się w skillach prawnych i skąd brać źródła — do integracji na pozostałych hostach (Claude Code / opencode).
data: 2026-09-11
host_zrodlowy: macOS, Claude Code (desktop, zakładka Code), użytkownik natcza
dotyczy: 13 skilli IURA, 2 moduły shared LEX-MACHINA, nowy skill lexcache, repozytorium GROUNDING-PRAWO
status: do wdrożenia na pozostałych hostach
---

# Memo: skille prawne + wspólne repozytorium źródeł — 2026-09-11

Do hostów z Claude Code i opencode. Opisuje **co się zmieniło**, **co jest zweryfikowane empirycznie** (żebyście nie wyprowadzali tego drugi raz) i **co zrobić u siebie**.

---

## 1. Skrót: co zrobić u siebie

```bash
# 1. konektor legislacyjny (wymagany przez wszystkie skille prawne)
claude mcp add isap -s user -- npx -y @matematicsolutions/mcp-isap
# opcjonalnie: sądy administracyjne (SAOS ich NIE indeksuje)
claude mcp add nsa  -s user -- npx -y @matematicsolutions/mcp-nsa

# 2. usuń pluginy IURA, żeby nie dublowały nazw skilli z ~/.claude/skills
claude plugin uninstall iura-pl@iura-plugins
claude plugin uninstall iura-eu@iura-plugins

# 3. skopiuj skille (14 katalogów) do ~/.claude/skills/
#    iura, lexcache, apelacja-karna, cofniecie-pozwu-ze-zrzeczeniem-roszczenia,
#    decyzja-procesowa-prokuratora, eu-legal-memo, notatka-prawna, odpowiedz-na-pozew,
#    pozew-cywilny, przeglad-tabelaryczny, przeglad-umow, wniosek-o-rozprawe-zdalna,
#    zarzuty-do-opinii-bieglego, zazalenie-na-postanowienie-prokuratora
#    + zaktualizowane shared/ISAP-METRYKI-AKTOW.md i shared/AKTY-PRAWNE-MASTER.md

# 4. sprawdź, że wrapper widzi wspólne repozytorium
python3 ~/.claude/skills/lexcache/scripts/lexcache.py sources --health
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
L=~/.claude/skills/lexcache/scripts/lexcache.py
python3 $L sources --health
python3 $L isap pdf DU/2026/795 --find "Art. 118."     # brzmienie obowiązujące z PDF
python3 $L saos search --all "kara umowna" --court COMMON --legalbase "art. 483 kc"
python3 $L find "przedawnienie" --field source=echr    # szuka w cache I w korpusie
python3 $L korpus normalize && python3 $L korpus index
```

TTL per typ zapytania (od 1 dnia dla KRS/NBP do 180 dni dla `saos get`), każdy wpis ma `expires_at`, odczyt wygasłego wypisuje ostrzeżenie i kończy się kodem 3. `purge` nigdy nie rusza korpusu.

**Relacja do MCP:** `lexcache` jest **dodatkiem, nie zamiennikiem**. Skille prawne kierują do niego **jednym konkretnym przejściem** — gdy `get_act_text` zwróci `text_unavailable_use_pdf`. Rutynowy research zostaje na konektorach MCP, bo mają citator.

---

## 5. Wspólne repozytorium GROUNDING-PRAWO

Jedna baza źródeł dla wszystkich hostów. Dwie drogi dostępu do **tych samych danych** (potwierdzone identycznymi sumami md5):

| Droga | Ścieżka | Stan na tym hoście |
|---|---|---|
| OneDrive (sync lokalny) | `~/OneDrive/GROUNDING-PRAWO` | ✅ działa |
| SMB | `/Volumes/GROUNDING-PRAWO` (`//10.0.10.200/GROUNDING-PRAWO`) | ⚠️ **odczyt niesprawny** |

### ⚠️ Udział SMB nie nadaje się tu na ścieżkę odczytu

Na tym hoście **42 z 59 plików w `ORZECZENIA/` zwraca `Errno 5 Input/output error`** przy próbie odczytu, mimo że `stat` podaje poprawny rozmiar, a `dd` czyta z nich 0 bajtów. Zimny odczyt pojedynczego pliku też pada, więc to nie jest wyczerpanie uchwytów ani limit prędkości. Te same pliki czytają się bez problemu przez OneDrive. **Udział wymaga uwagi po stronie NAS-a** — nie diagnozowałem dalej, bo to osobne zadanie.

Wnioski dla Was: **nie zakładajcie z góry, która ścieżka działa.** `lexcache` rozstrzyga to sam, testując każdego kandydata realnym **zapisem i odczytem** (`touch`/`stat` nie wystarcza — na uszkodzonym udziale oba przechodzą). Kolejność:

1. `LEXCACHE_DIR` (wymuszenie)
2. `GROUNDING_ROOT` (wymuszenie korzenia repozytorium)
3. `~/OneDrive/GROUNDING-PRAWO`
4. `~/Library/CloudStorage/OneDrive-Osobisty/GROUNDING-PRAWO`
5. `/Volumes/GROUNDING-PRAWO`
6. `~/.claude/cache/lexcache` (fallback lokalny)

Jeśli u Was SMB działa, a OneDrive nie — ustawcie `GROUNDING_ROOT=/Volumes/GROUNDING-PRAWO`.

### Obsługa OneDrive: nie trzeba żadnego MCP ani skilla

macOS montuje OneDrive przez File Provider jako zwykły katalog (`~/OneDrive`, `~/Library/CloudStorage/OneDrive-Osobisty`). To jest najtańsza możliwa obsługa — zwykłe `open()`, bez tokenów, bez API, bez limitów. Konektor do Graph API byłby tu kosztem bez korzyści. Na Linuksie/Windows: `rclone` z backendem `onedrive` albo natywny klient — ważne tylko, żeby katalog był widoczny w systemie plików.

### Stary cache lokalny — źródłem prawdy jest repozytorium

`migrate` **kopiuje, nie przenosi** (przenosi dopiero z `--usun-zrodlo`). Na tym hoście uruchomiłem go bez tej flagi, więc pod `~/.claude/cache/lexcache` leży nadal komplet 43 MB. Jest nieaktywny — rozstrzyganie ścieżki wybiera repozytorium — ale **od teraz będzie się cicho rozjeżdżał**. Autorytatywne jest `GROUNDING-PRAWO/CACHE`; stary katalog możecie skasować albo zostawić jako zapasową kopię, byle świadomie.

### Czyszczenie cache obejmuje też PDF-y

PDF-y ISAP (`CACHE/isap/_pdf/`, tu ~43 MB, czyli praktycznie cały rozmiar cache) to pliki binarne, nie wpisy `.md`. Do 11.09.2026 `purge` ich nie widział i serwowały się w nieskończoność jako świeże — nawet po skasowaniu towarzyszącego wpisu. Naprawione: ponowne użycie PDF-a sprawdza teraz jego wiek względem TTL 90 dni (`--refresh` wymusza pobranie), a `purge --stale` / `purge --all` przechodzi też przez `_pdf/`. Jeśli kopiowaliście `lexcache.py` wcześniej — weźcie nowszą wersję.

### Układ repozytorium

```
GROUNDING-PRAWO/
├── ORZECZENIA/     59 plików (54 unikalne + 5 kopii 1:1) — SN, SA, NSA, ETPC
├── USTAWY/         11 tekstów ujednoliconych (.md.docx, format LEX)
├── OPRACOWANIA/     7 PDF-ów
├── MAPY/            2 mapy artykułów
├── CACHE/          ← lexcache (isap/ saos/ eurlex/ krs/ nbp/ ... + isap/_pdf/)
└── INDEX/          ← INDEX.md (czytelny) + index.jsonl (maszynowy)
```

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

1. **5 plików bez rozszerzenia to kopie 1:1** plików `.md`: `III_OSK_5079-21`, `I_CKN_908-98`, `SD_ 9-13`, `V_KK_75-20`, `WA_39-08`. Zostawione nietknięte i wyłączone z indeksu — usunięcie to decyzja właściciela, nie narzędzia.
2. **`USTAWY/Ustawa_o_srodkach_przymusu_bezposredniego_i_broni_palnej.md.docx` ma 0 bajtów** — plik pusty, nie artefakt SMB. Oznaczony w indeksie jako ⚠️.
3. **Teksty w `USTAWY/` to snapshoty** z polem `Wersja od:`. Są wygodne i czyste (mają nawet tytuły artykułów w nawiasach), ale **nie zastępują ścieżki ISAP** — przy kolejnym obwieszczeniu cicho się dezaktualizują. Traktować jako pomoc, nie jako dowód brzmienia na dziś.

---

## 8. RODO — jedna rzecz do świadomej decyzji

`CACHE/` gromadzi orzeczenia z SAOS (anonimizacja bywa niepełna) i odpisy KRS — **dane osobowe**. Repozytorium jest synchronizowane przez OneDrive, czyli konsumencką chmurę. To świadoma decyzja właściciela, ale każdy host, który podłączy się do tej bazy, staje się kolejnym miejscem przetwarzania. Jeśli u Was obowiązuje inny reżim — ustawcie `LEXCACHE_DIR` na katalog lokalny i korzystajcie z repozytorium tylko do odczytu korpusu.

Frontmatter niesie `pii_risk: low|high` — wpisy `high` traktować jak akta.

---

## 9. Czego świadomie nie zrobiłem

- **Skille `iura-nl`** (7, prawo niderlandzkie) — nieprzeniesione: nie są zainstalowane, a konektory polskie nie obsłużą prawa holenderskiego.
- **Baza orzeczeń SN `sn.pl`** — to zamknęłoby lukę SAOS po 2016 r. Skrypt istnieje (`webwright-legal-pl/scripts/fetch_orzeczenie.py`), ale działa przez Playwright, nie HTTP — złamałoby to zasadę „stdlib + curl" w `lexcache`. Do rozważenia jako osobna, opt-in ścieżka.
- **Diagnostyka udziału SMB** — poza zakresem; zgłoszone w punkcie 5.

---

*Memo wygenerowane przez Claude Code na hoście macOS użytkownika natcza, 2026-09-11. Wszystkie liczby i zachowania API sprawdzone wywołaniem tego dnia — jeśli czytacie to znacznie później, zweryfikujcie punkt 3 ponownie.*
