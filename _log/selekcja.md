# Selekcja skilli - grounding-prawo

Własna analiza (14.10.2026) z korektami właściciela. Analizy GPT i Sonnet były doradcami.

- w pluginie: **59** skilli: **42** widocznych dla modelu i **17** wewnętrznych (`disable-model-invocation`),
- **5** skilli scalonych jako moduły typów pism w `pisma-procesowe-v3`,
- poza pluginem: **73**, w tym 32 unikatów w `archive/` (płasko).

## Zasady

1. Jeden router (`prawny-router-v3`), bez bramek kosztu; pełna ścieżka kontroli zawsze.
2. Silnik LexMachina zostaje spójny (`shared` odwołuje się do `audyt-systemu-v4` 33 razy). Moduły dziedzinowe poza profilem (DR-04/06/07/08/09/15) usunięte, a martwe wiersze routingu wycinane przez `scripts/build.py`.
3. Brak anonimizacji, pseudonimizacji i zakazu chmury: KROK 0A zamknięty patchem, odwołania do `let-it-be` i `tajemnica-preflight` wycinane w buildzie.
4. Źródła prawa: jeden konektor, portal MCP `lex.xlap.pl/mcp`. Skille cache i wrappery SAOS usunięte.
5. Zmiany względem upstreamu to patche (`selection/patches/`) i reguły `build.py`; upstream zostaje przypięty w submodułach.

## Plugin

| Skill | Źródło | Rola | Uzasadnienie |
|---|---|---|---|
| `prawny-router-v3` | lex | widoczny | jedyny router; patch: KROK 0A zamknięty na stałe bez anonimizacji, requires przycięte |
| `shared` | lex | wewnętrzny | biblioteka hard-gate'ów, wymagana przez wszystkie skille silnika; nie jest agentem |
| `prawo-polskie-v2` | lex | widoczny | kwalifikacja postępowań, ROUTING-MAP do DR |
| `analiza-sadowa-v6` | lex | widoczny | wieloprzebiegowy audyt sądowy |
| `analizator-dowodow-v3` | lex | widoczny | sprzeczne zeznania, dokumentacja medyczna, nagrania, działania Policji |
| `analizator-przepisow-v2` | lex | widoczny | przesłanki, wyjątki, brzmienie obowiązujące |
| `analizator-umow-v1` | lex | widoczny | umowa najmu i kaucja; 13 odwołań z DR-02, więc odcięcie zepsułoby routing |
| `chronologia-sprawy-v1` | lex | widoczny | oś zdarzeń i niespójności między postępowaniami |
| `orzeczenia-sadowe-v2` | lex | widoczny | ocena tez orzeczeń |
| `pisma-procesowe-v3` | lex | widoczny | główny generator pism |
| `pisma-proste-v2` | lex | widoczny | 21 odwołań z shared; zostaje jako część silnika, ale profil MAX wymusza pełną kontrolę (patrz profil-postepowan-wlasnych) |
| `przesluchanie-swiadkow-v2-min90` | lex | widoczny | pytania do świadków, sprzeczności |
| `audyt-systemu-v4` | lex | wewnętrzny | shared odwołuje się do niego 33x; zostaje jako biblioteka (9 MB, głównie references i mcp-servers) |
| `przewodnik-prawny-v2` | lex | wewnętrzny | FALLBACK routera w 5 ścieżkach; odcięcie wymagałoby przepisania routera |
| `dr-01-ustroj-konstytucyjny-i-zrodla-prawa` | lex | wewnętrzny | gwarancje konstytucyjne, kontrola działań państwa |
| `dr-02-prawo-cywilne-rodzinne-gospodarcze` | lex | wewnętrzny | pozew przeciw szpitalowi, kaucja, odszkodowania |
| `dr-03-prawo-karne-wykroczenia-egzekucja` | lex | wewnętrzny | sprawy karne i wykroczeniowe, zatrzymania, zażalenia |
| `dr-05-prawo-administracyjne-sadowoadministracyjne` | lex | wewnętrzny | skargi, UODO, WSA |
| `dr-10-zdrowie-farmacja-zywnosc-rolnictwo` | lex | wewnętrzny | prawa pacjenta, dokumentacja medyczna, UoOZP |
| `dr-11-cyfrowe-cyber-ai-dane-ip` | lex | wewnętrzny | RODO, monitoring, dowody cyfrowe |
| `dr-12-sadownictwo-prokuratura-zawody-prawnicze` | lex | wewnętrzny | postępowanie sądowe, prokuratura |
| `dr-13-sluzby-bezpieczenstwo-informacje-niejawne` | lex | wewnętrzny | Policja, uprawnienia funkcjonariuszy |
| `dr-14-prawo-ue-miedzynarodowe-prawa-czlowieka` | lex | wewnętrzny | EKPC, TSUE |
| `dr-16-pisma-strategia-dowody-orzecznictwo` | lex | wewnętrzny | żądania, dowody, strategia |
| `citation-grounding-pl` | awe:fundament-weryfikacyjny | widoczny | kontrola treści cytatu (ISTNIENIE/TREŚĆ/FRAGMENT); LexMachina tego nie sprawdza |
| `ekstraktor-cytatow-pl` | awe:fundament-weryfikacyjny | widoczny | znajduje wszystkie powołania przed weryfikacją; sprawdzić, czy ma działający kod |
| `adversarial-legal-review-pl` | awe:fundament-weryfikacyjny | widoczny | debata czterech ról; bramka kosztu do wyłączenia patchem |
| `atak-przeciwnika-pl` | awe:fundament-weryfikacyjny | widoczny | osobny przebieg ataku |
| `pierwsze-wrazenie-sedziego-pl` | awe:fundament-weryfikacyjny | widoczny | zimna lektura |
| `subsumpcja-pl` | awe:fundament-weryfikacyjny | widoczny | pokrycie przesłanek faktami |
| `deliverable-fidelity-pl` | awe:fundament-weryfikacyjny | widoczny | czy ustalenia RED trafiły do pisma; check słowny traktować jako sito |
| `struktura-wyroku-pl` | awe:orzecznictwo-zrodla | widoczny | rozdziela sentencję, ratio, votum separatum |
| `uodo-grounding-pl` | awe:orzecznictwo-zrodla | widoczny | decyzje UODO, sprawa RODO |
| `webwright-legal-pl` | awe:orzecznictwo-zrodla | widoczny | orzeczenia z ms.gov.pl, sn.pl, TK bez MCP; wymaga Playwrighta |
| `terminy-procesowe-pl` | awe:dokumenty | widoczny | terminy; liczy wg KC, dla KPK/KPW wynik oznaczać do sprawdzenia |
| `kalkulatory-procesowe-pl` | awe:dokumenty | widoczny | opłata, WPS, odsetki, przedawnienie w pozwach cywilnych |
| `waliduj-podpis-pdf-pl` | awe:dokumenty | widoczny | integralność podpisanych PDF od szpitali, sądów, prokuratury; tylko odczyt |
| `akta-przeszukiwalne-pl` | awe:dokumenty | widoczny | niezależny drugi odczyt akt, duplikaty, strony nieczytelne |
| `chronologia-stanowiska-pl` | awe:dokumenty | widoczny | mechaniczna kontrola chronologii i stanowisk wobec cytatu i strony |
| `redline-docx-pl` | awe:dokumenty | widoczny | Track Changes; sanitize metadanych jest jawną komendą, nie domyślną operacją |
| `klauzule-kontraktowe-pl` | awe:dokumenty | widoczny | umowa zarządzania najmem |
| `rodo-dsar-pl` | awe:ochrona-danych | widoczny | żądania dostępu, sprostowania, usunięcia własnych danych |
| `marko-pl-content` | awe:jakosc-tresci | wewnętrzny, przejściowy | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `ocena-outputu-pl` | awe:fundament-weryfikacyjny | wewnętrzny, przejściowy | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `patron-weryfikacja-cytatow` | own | wewnętrzny, przejściowy | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `doc-intel-contract-pl` | awe:dokumenty | wewnętrzny, przejściowy | jedyny dom tablicy prawdy normalizacji, którą testuje citation-grounding-pl (test-grounding.mjs 34/34). Ma mechanizmy maskowania - nieużywane, skill niewidoczny dla modelu |
| `patron-przeglad-tabelaryczny` | own | widoczny | tabelaryczny przegląd dokumentów (z pipeline Patrona); do wzbogacenia o klauzule/kolumny pod Twoje sprawy |
| `pisz-po-polsku` | own | widoczny | JEDEN skill redakcji: scala humanizer-pl + naturalne-pisanie + patron-pisz-po-ludzku (pliki skopiowane do own-skills, zmiany upstreamu trzeba przenosić ręcznie) |
| `the-ocr` | own | widoczny | własny OCR (Datalab/Azure DI/Google Vision); kopia skilla z aplikacją w środku, źródło: agents/skills/the-ocr |
| `szturm-na-draft-pl` | own | widoczny | główny mechanizm wielokrotnej kontroli pisma; WYMAGA przebudowy (profil S/M/L i limit rund) - propozycja diffu, nie zastosowana |
| `case-risk` | own | widoczny | ryzyka dowodowe, medyczne, UoOZP, art. 192 kk; skrojony pod Twoje sprawy |
| `medical-consent` | own | widoczny | zgoda na czynność medyczną, art. 192 kk |
| `uoozp-compliance` | own | widoczny | kontrola hospitalizacji psychiatrycznej |
| `patron-analiza-akt-karnych` | own | widoczny | analiza akt karnych |
| `patron-skan-dokumentu` | own | widoczny | deterministyczny skan przychodzących dokumentów pod kątem prompt injection |
| `patron-identyfikatory-pl` | own | widoczny | walidacja PESEL/NIP/KRS, ekstrakcja sygnatur |
| `patron-prawo-pl-zrodla` | own | widoczny | kolejność źródeł i konektorów MCP |
| `pozew-cywilny` | own | moduł w pisma-procesowe-v3 | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
| `odpowiedz-na-pozew` | own | moduł w pisma-procesowe-v3 | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
| `apelacja-karna` | own | moduł w pisma-procesowe-v3 | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
| `zazalenie-na-postanowienie-prokuratora` | own | moduł w pisma-procesowe-v3 | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
| `zawiadomienie-o-przestepstwie` | own | widoczny | pisane przez pokrzywdzonego obywatela |
| `zarzuty-do-opinii-bieglego` | own | moduł w pisma-procesowe-v3 | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
| `profil-postepowan-wlasnych` | own | widoczny | NOWY, mały skill nadrzędny (szkic do akceptacji): pełna ścieżka kontroli, brak anonimizacji, osobne przebiegi soczewek |

## Poza pluginem

| Skill | Gdzie | Powód |
|---|---|---|
| `iura` | archive/ | zastąpiona przez MCP lex.xlap.pl (SAOS lokalny dump, ISAP) |
| `opendataloader-pdf` | upstream | scalony w the-ocr (references/opendataloader-pdf.md) |
| `humanizer-pl` | upstream | scalony w pisz-po-polsku |
| `naturalne-pisanie` | upstream | scalony w pisz-po-polsku (vendor/naturalne-pisanie zostaje jako źródło) |
| `patron-pisz-po-ludzku` | archive/ | scalony w pisz-po-polsku |
| `dr-04-prawo-pracy-zus-swiadczenia` | upstream | poza profilem spraw (decyzja właściciela) |
| `dr-06-podatki-finanse-publiczne-aml` | upstream | poza profilem spraw (decyzja właściciela) |
| `dr-07-zamowienia-publiczne-fundusze-ue` | upstream | poza profilem spraw (decyzja właściciela) |
| `dr-08-samorzad-terytorialny-prawo-lokalne` | upstream | poza profilem spraw (decyzja właściciela) |
| `dr-09-budownictwo-srodowisko-energia-transport` | upstream | poza profilem spraw (decyzja właściciela) |
| `dr-15-compliance-iso-governance-audyt` | upstream | poza profilem spraw (decyzja właściciela) |
| `raport-klienta-v1` | upstream | raportowanie dla klientów, niepotrzebne |
| `raport-sytuacyjny-v2` | upstream | niepotrzebny |
| `legal-ai-audit-bundle` | upstream | to nie USA: nikt w PL nie oczekuje sha256 pliku poza sprawami o zbrodnie; rejestr kontroli w Basic Memory |
| `lexcache` | archive/ | cache zastąpiony przez MCP z lokalnym dumpem SAOS (lex.xlap.pl/mcp) |
| `wniosek-o-rozprawe-zdalna` | archive/ | decyzja właściciela |
| `saos-orzecznictwo` | upstream | zastąpiony przez mcp-saos z lokalnym dumpem |
| `let-it-be` | upstream | anonimizacja/pseudonimizacja, sprzeczne z polityką właściciela |
| `legal-request-router-pl` | upstream | drugi router, bramka kosztu, ścieżka bez kontroli |
| `intake-sufficiency-pl` | upstream | pokrywa shared/INTAKE-GAP i CLAIM-VALIDATION |
| `eu-sparql-search` | upstream | zastąpiony przez MCP mcp-eu-sparql |
| `legal-data-hunter-pl` | upstream | hurtowy korpus, nie praca nad sprawą |
| `hierarchia-zrodel-pl` | upstream | duplikat shared/HIERARCHIA-ZRODEL.md |
| `markitdown` | upstream | jednoplikowy adapter, host czyta pliki sam |
| `doc-intel-llm-tier-pl` | upstream | wymaga contextgem i modelu lokalnego |
| `rodo-dpia-pl` | upstream | strona administratora; pokrywa DR-11 + mcp-eu-compliance |
| `rodo-naruszenie-72h-pl` | upstream | strona administratora |
| `rodo-ropa-dpa-pl` | upstream | strona administratora |
| `nis2-ksc-pl` | upstream | governance |
| `ai-act-triage-pl` | upstream | governance |
| `kyc-kancelaria-pl` | upstream | kancelaria |
| `matematic-expert-panel` | upstream | governance |
| `matematic-konstytucja-ai` | upstream | governance |
| `matematic-workspace-backup` | upstream | governance |
| `tajemnica-preflight-pl` | upstream | redagowanie promptów, sprzeczne z pracą na oryginałach |
| `matematic-marketplace-installer` | upstream | narzędzie developerskie |
| `matematic-mcp-fastmcp-instructions-pl` | upstream | narzędzie developerskie |
| `matematic-patron-pr-review-pl` | upstream | narzędzie developerskie |
| `matematic-spec-driven` | upstream | narzędzie developerskie |
| `gemini-agent` | upstream | narzędzie developerskie |
| `generate-goal` | upstream | narzędzie developerskie |
| `git-worktree-prune` | upstream | narzędzie developerskie |
| `root-cause-tracing` | upstream | narzędzie developerskie |
| `skill-creator` | upstream | narzędzie developerskie |
| `decyzja-procesowa-prokuratora` | archive/ | pisanie decyzji prokuratora |
| `cofniecie-pozwu-ze-zrzeczeniem-roszczenia` | archive/ | poza profilem, drugi generator pism |
| `patron-obrona-pisma` | archive/ | duplikat szturm-na-draft-pl |
| `patron-pismo-procesowe-pl` | archive/ | duplikat pisma-procesowe-v3 |
| `patron-streszczenia-umow` | archive/ | kancelaria |
| `patron-streszczenie-dla-klienta` | archive/ | kancelaria |
| `przeglad-tabelaryczny` | archive/ | kancelaria |
| `przeglad-umow` | archive/ | kancelaria |
| `contract-review-pl` | archive/ | kancelaria, pseudonimizacja |
| `notatka-prawna` | archive/ | pokrywa analiza-sadowa-v6 |
| `eu-legal-memo` | archive/ | pokrywa analiza-sadowa-v6 + dr-14 |
| `pomoc-prawna-konfiguracja` | archive/ | NGO/kliniki prawa |
| `pomoc-prawna-kwalifikacja` | archive/ | NGO/kliniki prawa |
| `pomoc-prawna-memo` | archive/ | NGO/kliniki prawa |
| `pomoc-prawna-projekt-pisma` | archive/ | NGO/kliniki prawa |
| `pomoc-prawna-wywiad` | archive/ | NGO/kliniki prawa |
| `risk-and-issues-manager-pl` | archive/ | zarządzanie kancelarią |
| `status-report-drafter-pl` | archive/ | zarządzanie kancelarią |
| `scope-change-controller-pl` | archive/ | zarządzanie kancelarią |
| `ugh-ocr` | archive/ | stary pipeline OCR, zastąpiony the-ocr |
| `mac-ocr` | archive/ | macOS-only |
| `przesluchanie-swiadkow-v2-min90-v35` | archive/ | starsza linia tego samego skilla |
| `dr-09-out` | archive/ | artefakt wyjścia |
| `document-analysis-classification` | archive/ | brak opisu, nieznane przeznaczenie |
| `find-skills` | archive/ | narzędzie developerskie |
| `frontmatter` | archive/ | legenda do pdf-generation |
| `pdf-generation` | archive/ | host ma własny skill pdf |
| `szukaj-orzeczen-v2` | archive/ | zastąpiony przez MCP |
| `commercial-legal-pl` | upstream | umowy B2B/IT, poza profilem (submoduł vendor zostaje jako źródło) |

## Znane problemy i rzeczy niezrobione

- Po usunięciu skilli zostają odwołania w prozie (ok. 150 miejsc, głównie w `shared`, `analizator-umow-v1`, `citation-grounding-pl`); nie są to ścieżki wczytywane przez router, ale wymagają stopniowego sprzątania.
- `profil-postepowan-wlasnych` to szkic do akceptacji właściciela.
- Patche routera zmieniają pliki objęte `CHECKSUMS.sha256`; sumy w skillu się nie zgadzają.
- `ekstraktor-cytatow-pl` ma tylko SKILL.md, bez kodu: ekstrakcja idzie promptem.
- `doc-intel-contract-pl` jest wewnętrzny wyłącznie dla testu `citation-grounding-pl` (tablica prawdy normalizacji); ma nieużywane mechanizmy maskowania.
- Komentarze w `iura`-pochodnych skillach nadal wspominają `text_unavailable_use_pdf` (ISAP zwracał to dla kodeksów); sprawdzić po naprawie paginacji w mcp-isap.
- `pisz-po-polsku`: pliki skopiowane z upstreamu, zmiany `humanizer-pl` i `naturalne-pisanie` trzeba przenosić ręcznie.
- Upstream LexMachina jest na GPL v3; publiczny marketplace z przerobionymi skillami oznacza dystrybucję na GPL. Repo jest prywatne.
- Nie sprawdzono, czy claude.ai i chatgpt.com przyjmują ten układ marketplace.
