# Selekcja skilli - grounding-prawo (14.10.2026)

Własna analiza. Analizy GPT i Sonnet były doradcami; tam, gdzie się rozchodzą z poniższym, powód jest w kolumnie uzasadnienia.

- w pluginie: **79** skilli, z czego **50** widocznych dla modelu i **29** wewnętrznych (`disable-model-invocation`),
- poza pluginem: **57**, w tym 29 unikatów przeniesionych płasko do `archive/`.

## Zasady, na których oparłem wybór

1. Jeden router (`prawny-router-v3`); bez `legal-request-router-pl` i bez bramek kosztu.
2. Silnik LexMachina zostaje cały: jest gęsto spleciony (`shared` odwołuje się do `audyt-systemu-v4` 33 razy, do DR-04…15 16 razy; router ma wiersze routingu do DR-04/08/09). Wycięcie modułów, jak proponował GPT, zostawiłoby martwe ścieżki. Zamiast tego moduły wewnętrzne są niewidoczne dla modelu.
3. Zostają skille, które Twój `szturm-na-draft-pl` faktycznie wykonuje (oznaczone `transitional`), dopóki szturm nie zostanie przebudowany.
4. Zostają unikaty pod Twoje sprawy, które żadna z analiz nie widziała: `case-risk`, `medical-consent`, `uoozp-compliance`.
5. Nic nie robi anonimizacji ani pseudonimizacji (`let-it-be` poza pluginem, KROK 0A routera zamknięty patchem).

## Plugin

| Skill | Źródło | Wewn. | Uzasadnienie |
|---|---|---|---|
| `prawny-router-v3` | lex |  | jedyny router; patch: KROK 0A zamknięty na stałe bez anonimizacji, requires przycięte |
| `shared` | lex | tak | biblioteka hard-gate'ów, wymagana przez wszystkie skille silnika; nie jest agentem |
| `prawo-polskie-v2` | lex |  | kwalifikacja postępowań, ROUTING-MAP do DR |
| `analiza-sadowa-v6` | lex |  | wieloprzebiegowy audyt sądowy |
| `analizator-dowodow-v3` | lex |  | sprzeczne zeznania, dokumentacja medyczna, nagrania, działania Policji |
| `analizator-przepisow-v2` | lex |  | przesłanki, wyjątki, brzmienie obowiązujące |
| `analizator-umow-v1` | lex |  | umowa najmu i kaucja; 13 odwołań z DR-02, więc odcięcie zepsułoby routing |
| `chronologia-sprawy-v1` | lex |  | oś zdarzeń i niespójności między postępowaniami |
| `orzeczenia-sadowe-v2` | lex |  | ocena tez orzeczeń |
| `pisma-procesowe-v3` | lex |  | główny generator pism |
| `pisma-proste-v2` | lex |  | 21 odwołań z shared; zostaje jako część silnika, ale profil MAX wymusza pełną kontrolę (patrz profil-postepowan-wlasnych) |
| `przesluchanie-swiadkow-v2-min90` | lex |  | pytania do świadków, sprzeczności |
| `raport-sytuacyjny-v2` | lex |  | status wielu spraw |
| `audyt-systemu-v4` | lex | tak | shared odwołuje się do niego 33x; zostaje jako biblioteka (9 MB, głównie references i mcp-servers) |
| `przewodnik-prawny-v2` | lex | tak | FALLBACK routera w 5 ścieżkach; odcięcie wymagałoby przepisania routera |
| `dr-01-ustroj-konstytucyjny-i-zrodla-prawa` | lex | tak | gwarancje konstytucyjne, kontrola działań państwa |
| `dr-02-prawo-cywilne-rodzinne-gospodarcze` | lex | tak | pozew przeciw szpitalowi, kaucja, odszkodowania |
| `dr-03-prawo-karne-wykroczenia-egzekucja` | lex | tak | sprawy karne i wykroczeniowe, zatrzymania, zażalenia |
| `dr-05-prawo-administracyjne-sadowoadministracyjne` | lex | tak | skargi, UODO, WSA |
| `dr-10-zdrowie-farmacja-zywnosc-rolnictwo` | lex | tak | prawa pacjenta, dokumentacja medyczna, UoOZP |
| `dr-11-cyfrowe-cyber-ai-dane-ip` | lex | tak | RODO, monitoring, dowody cyfrowe |
| `dr-12-sadownictwo-prokuratura-zawody-prawnicze` | lex | tak | postępowanie sądowe, prokuratura |
| `dr-13-sluzby-bezpieczenstwo-informacje-niejawne` | lex | tak | Policja, uprawnienia funkcjonariuszy |
| `dr-14-prawo-ue-miedzynarodowe-prawa-czlowieka` | lex | tak | EKPC, TSUE |
| `dr-16-pisma-strategia-dowody-orzecznictwo` | lex | tak | żądania, dowody, strategia |
| `dr-04-prawo-pracy-zus-swiadczenia` | lex | tak | poza profilem spraw, ale router ma do niego dziesiątki wierszy routingu; zostaje jako moduł wewnętrzny |
| `dr-06-podatki-finanse-publiczne-aml` | lex | tak | poza profilem spraw, ale router ma do niego dziesiątki wierszy routingu; zostaje jako moduł wewnętrzny |
| `dr-07-zamowienia-publiczne-fundusze-ue` | lex | tak | poza profilem spraw, ale router ma do niego dziesiątki wierszy routingu; zostaje jako moduł wewnętrzny |
| `dr-08-samorzad-terytorialny-prawo-lokalne` | lex | tak | poza profilem spraw, ale router ma do niego dziesiątki wierszy routingu; zostaje jako moduł wewnętrzny |
| `dr-09-budownictwo-srodowisko-energia-transport` | lex | tak | poza profilem spraw, ale router ma do niego dziesiątki wierszy routingu; zostaje jako moduł wewnętrzny |
| `dr-15-compliance-iso-governance-audyt` | lex | tak | poza profilem spraw, ale router ma do niego dziesiątki wierszy routingu; zostaje jako moduł wewnętrzny |
| `raport-klienta-v1` | lex | tak | poza profilem spraw, ale router ma do niego dziesiątki wierszy routingu; zostaje jako moduł wewnętrzny |
| `citation-grounding-pl` | awe:fundament-weryfikacyjny |  | kontrola treści cytatu (ISTNIENIE/TREŚĆ/FRAGMENT); LexMachina tego nie sprawdza |
| `ekstraktor-cytatow-pl` | awe:fundament-weryfikacyjny |  | znajduje wszystkie powołania przed weryfikacją; sprawdzić, czy ma działający kod |
| `adversarial-legal-review-pl` | awe:fundament-weryfikacyjny |  | debata czterech ról; bramka kosztu do wyłączenia patchem |
| `atak-przeciwnika-pl` | awe:fundament-weryfikacyjny |  | osobny przebieg ataku |
| `pierwsze-wrazenie-sedziego-pl` | awe:fundament-weryfikacyjny |  | zimna lektura |
| `subsumpcja-pl` | awe:fundament-weryfikacyjny |  | pokrycie przesłanek faktami |
| `deliverable-fidelity-pl` | awe:fundament-weryfikacyjny |  | czy ustalenia RED trafiły do pisma; check słowny traktować jako sito |
| `struktura-wyroku-pl` | awe:orzecznictwo-zrodla |  | rozdziela sentencję, ratio, votum separatum |
| `uodo-grounding-pl` | awe:orzecznictwo-zrodla |  | decyzje UODO, sprawa RODO |
| `webwright-legal-pl` | awe:orzecznictwo-zrodla |  | orzeczenia z ms.gov.pl, sn.pl, TK bez MCP; wymaga Playwrighta |
| `terminy-procesowe-pl` | awe:dokumenty |  | terminy; liczy wg KC, dla KPK/KPW wynik oznaczać do sprawdzenia |
| `kalkulatory-procesowe-pl` | awe:dokumenty |  | opłata, WPS, odsetki, przedawnienie w pozwach cywilnych |
| `waliduj-podpis-pdf-pl` | awe:dokumenty |  | integralność podpisanych PDF od szpitali, sądów, prokuratury; tylko odczyt |
| `akta-przeszukiwalne-pl` | awe:dokumenty |  | niezależny drugi odczyt akt, duplikaty, strony nieczytelne |
| `chronologia-stanowiska-pl` | awe:dokumenty |  | mechaniczna kontrola chronologii i stanowisk wobec cytatu i strony |
| `opendataloader-pdf` | awe:dokumenty |  | tabele i układ w dokumentacji szpitalnej |
| `redline-docx-pl` | awe:dokumenty |  | Track Changes; sanitize metadanych jest jawną komendą, nie domyślną operacją |
| `klauzule-kontraktowe-pl` | awe:dokumenty |  | umowa zarządzania najmem |
| `rodo-dsar-pl` | awe:ochrona-danych |  | żądania dostępu, sprostowania, usunięcia własnych danych |
| `humanizer-pl` | awe:jakosc-tresci | tak (przejściowy) | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `marko-pl-content` | awe:jakosc-tresci | tak (przejściowy) | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `ocena-outputu-pl` | awe:fundament-weryfikacyjny | tak (przejściowy) | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `legal-ai-audit-bundle` | awe:fundament-weryfikacyjny | tak (przejściowy) | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `saos-orzecznictwo` | awe:orzecznictwo-zrodla | tak (przejściowy) | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `iura` | own | tak (przejściowy) | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `patron-weryfikacja-cytatow` | own | tak (przejściowy) | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `patron-pisz-po-ludzku` | own | tak (przejściowy) | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `doc-intel-contract-pl` | awe:dokumenty | tak (przejściowy) | jedyny dom tablicy prawdy normalizacji, którą testuje citation-grounding-pl (test-grounding.mjs 34/34). Ma mechanizmy maskowania - nieużywane, skill niewidoczny dla modelu |
| `naturalne-pisanie` | vendor:naturalne-pisanie |  | jedyny edytor stylu (ma warstwę prawniczą); zastępuje humanizer-pl i patron-pisz-po-ludzku |
| `the-ocr` | own |  | własny OCR (Datalab/Azure DI/Google Vision); kopia skilla z aplikacją w środku, źródło: agents/skills/the-ocr |
| `szturm-na-draft-pl` | own |  | główny mechanizm wielokrotnej kontroli pisma; WYMAGA przebudowy (profil S/M/L i limit rund) - propozycja diffu, nie zastosowana |
| `case-risk` | own |  | ryzyka dowodowe, medyczne, UoOZP, art. 192 kk; skrojony pod Twoje sprawy |
| `medical-consent` | own |  | zgoda na czynność medyczną, art. 192 kk |
| `uoozp-compliance` | own |  | kontrola hospitalizacji psychiatrycznej |
| `patron-analiza-akt-karnych` | own |  | analiza akt karnych |
| `patron-skan-dokumentu` | own |  | deterministyczny skan przychodzących dokumentów pod kątem prompt injection |
| `patron-identyfikatory-pl` | own |  | walidacja PESEL/NIP/KRS, ekstrakcja sygnatur |
| `patron-prawo-pl-zrodla` | own |  | kolejność źródeł i konektorów MCP |
| `lexcache` | own |  | cache źródeł; DO WERYFIKACJI: zakłada bazę GROUNDING-PRAWO na OneDrive/SMB, może być artefaktem starego systemu |
| `pozew-cywilny` | own |  | pozew cywilny |
| `odpowiedz-na-pozew` | own |  | odpowiedź na pozew |
| `apelacja-karna` | own |  | apelacja karna |
| `zazalenie-na-postanowienie-prokuratora` | own |  | zażalenia na postanowienia prokuratora |
| `zawiadomienie-o-przestepstwie` | own |  | pisane przez pokrzywdzonego obywatela |
| `wniosek-o-rozprawe-zdalna` | own |  | wniosek o rozprawę zdalną |
| `zarzuty-do-opinii-bieglego` | own |  | zarzuty do opinii biegłych (psychiatria) |
| `profil-postepowan-wlasnych` | own |  | NOWY, mały skill nadrzędny (szkic do akceptacji): pełna ścieżka kontroli, brak anonimizacji, osobne przebiegi soczewek |

## Poza pluginem

| Skill | Archiwum | Powód |
|---|---|---|
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
| `patron-przeglad-tabelaryczny` | archive/ | kancelaria, bulk-review umów |
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

- `szturm-na-draft-pl` nadal ma profil S/M/L, limit rund 1-3 i bramkę kosztu. Przebudowa na pełny profil to propozycja do Twojej akceptacji (diff), nie została zastosowana.
- `profil-postepowan-wlasnych` to szkic do akceptacji.
- `raport-klienta-v1` zawiera regułę „cytaty z akt bez anonimizacji świadków” jako błąd stylu; nie jest to dyrektywa routera, ale koliduje z zasadą bez anonimizacji. Do decyzji, czy zostawić.
- Patch routera zmienia pliki objęte `CHECKSUMS.sha256`; sumy kontrolne w skillu nie zgadzają się po patchu.
- `lexcache` zakłada bazę GROUNDING-PRAWO na OneDrive/SMB; ustalić, czy to artefakt starego systemu.
- Upstream LexMachina jest na licencji GPL v3; publiczny marketplace z przerobionymi skillami oznacza dystrybucję na GPL. Repo jest prywatne.
- Nie sprawdzano: czy claude.ai / chatgpt.com przyjmują ten marketplace w tym układzie. Claude Code: instalacja przetestowana w izolowanym HOME.
- `ekstraktor-cytatow-pl` ma tylko SKILL.md, bez skryptów (potwierdzone w katalogu): ekstrakcja cytatów jest wykonywana promptem, nie kodem. Do napisania ekstraktor z testami lub wykorzystanie `patron-identyfikatory-pl` (ma `pl_entities.py`).
