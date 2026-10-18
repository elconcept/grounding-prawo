# Indeks kanonicznych skilli grounding-prawo

Generowany przez [skrypt budowania](https://github.com/elconcept/grounding-prawo/blob/main/scripts/build.py) z selekcji pluginu.
Opis pochodzi z pola `why` selekcji lub frontmatter skilla.

**Skille:** 59. **Scalone moduły:** 10.

| Skill | Krótki opis | Źródło | Typ |
|---|---|---|---|
| [`wiki-basic-memory`](../wiki-basic-memory/SKILL.md) | pytania, syntezy i kontrola jakości wiki przez istniejące MCP | `own` | wywoływany |
| [`ingest-wiki`](../ingest-wiki/SKILL.md) | pełny ingest przez narzędzia MCP basic-memory, także w klientach przeglądarkowych | `own` | wywoływany |
| [`teczka-sprawy`](../teczka-sprawy/SKILL.md) | narzędzia teczki przeniesione z legal do pluginu | `own` | wywoływany |
| [`odczyt-dokumentow`](../odczyt-dokumentow/SKILL.md) | Jeden odczyt dokumentów do Markdown i kontraktu; the-ocr jako narzędzie, bez lokalnego OCR | `own` | wywoływany |
| [`prawny-router-v3`](../prawny-router-v3/SKILL.md) | jedyny router; patch: KROK 0A zamknięty na stałe bez anonimizacji, requires przycięte | `lex` | wywoływany |
| [`shared`](../shared/SKILL.md) | biblioteka hard-gate'ów, wymagana przez wszystkie skille silnika; nie jest agentem | `lex` | wewnętrzny |
| [`prawo-polskie-v2`](../prawo-polskie-v2/SKILL.md) | kwalifikacja postępowań, ROUTING-MAP do DR | `lex` | wywoływany |
| [`analiza-sadowa-v6`](../analiza-sadowa-v6/SKILL.md) | wieloprzebiegowy audyt sądowy | `lex` | wywoływany |
| [`analizator-dowodow-v3`](../analizator-dowodow-v3/SKILL.md) | sprzeczne zeznania, dokumentacja medyczna, nagrania, działania Policji | `lex` | wywoływany |
| [`analizator-przepisow-v2`](../analizator-przepisow-v2/SKILL.md) | przesłanki, wyjątki, brzmienie obowiązujące | `lex` | wywoływany |
| [`analizator-umow-v1`](../analizator-umow-v1/SKILL.md) | umowa najmu i kaucja; 13 odwołań z DR-02, więc odcięcie zepsułoby routing | `lex` | wywoływany |
| [`chronologia-sprawy-v1`](../chronologia-sprawy-v1/SKILL.md) | oś zdarzeń i niespójności między postępowaniami | `lex` | wywoływany |
| [`orzeczenia-sadowe-v2`](../orzeczenia-sadowe-v2/SKILL.md) | ocena tez orzeczeń | `lex` | wywoływany |
| [`pisma-procesowe-v3`](../pisma-procesowe-v3/SKILL.md) | główny generator pism | `lex` | wywoływany |
| [`pisma-proste-v2`](../pisma-proste-v2/SKILL.md) | 21 odwołań z shared; zostaje jako część silnika, ale profil MAX wymusza pełną kontrolę (patrz shared/ZASADY-PLUGINU.md) | `lex` | wywoływany |
| [`przesluchanie-swiadkow-v2-min90`](../przesluchanie-swiadkow-v2-min90/SKILL.md) | pytania do świadków, sprzeczności | `lex` | wywoływany |
| [`audyt-systemu-v4`](../audyt-systemu-v4/SKILL.md) | shared odwołuje się do niego 33x; zostaje jako biblioteka (9 MB, głównie references i mcp-servers) | `lex` | wewnętrzny |
| [`przewodnik-prawny-v2`](../przewodnik-prawny-v2/SKILL.md) | FALLBACK routera w 5 ścieżkach; odcięcie wymagałoby przepisania routera | `lex` | wewnętrzny |
| [`dr-01-ustroj-konstytucyjny-i-zrodla-prawa`](../dr-01-ustroj-konstytucyjny-i-zrodla-prawa/SKILL.md) | gwarancje konstytucyjne, kontrola działań państwa | `lex` | wewnętrzny |
| [`dr-02-prawo-cywilne-rodzinne-gospodarcze`](../dr-02-prawo-cywilne-rodzinne-gospodarcze/SKILL.md) | pozew przeciw szpitalowi, kaucja, odszkodowania | `lex` | wewnętrzny |
| [`dr-03-prawo-karne-wykroczenia-egzekucja`](../dr-03-prawo-karne-wykroczenia-egzekucja/SKILL.md) | sprawy karne i wykroczeniowe, zatrzymania, zażalenia | `lex` | wewnętrzny |
| [`dr-05-prawo-administracyjne-sadowoadministracyjne`](../dr-05-prawo-administracyjne-sadowoadministracyjne/SKILL.md) | skargi, UODO, WSA | `lex` | wewnętrzny |
| [`dr-10-zdrowie-farmacja-zywnosc-rolnictwo`](../dr-10-zdrowie-farmacja-zywnosc-rolnictwo/SKILL.md) | prawa pacjenta, dokumentacja medyczna, UoOZP | `lex` | wewnętrzny |
| [`dr-11-cyfrowe-cyber-ai-dane-ip`](../dr-11-cyfrowe-cyber-ai-dane-ip/SKILL.md) | RODO, monitoring, dowody cyfrowe | `lex` | wewnętrzny |
| [`dr-12-sadownictwo-prokuratura-zawody-prawnicze`](../dr-12-sadownictwo-prokuratura-zawody-prawnicze/SKILL.md) | postępowanie sądowe, prokuratura | `lex` | wewnętrzny |
| [`dr-13-sluzby-bezpieczenstwo-informacje-niejawne`](../dr-13-sluzby-bezpieczenstwo-informacje-niejawne/SKILL.md) | Policja, uprawnienia funkcjonariuszy | `lex` | wewnętrzny |
| [`dr-14-prawo-ue-miedzynarodowe-prawa-czlowieka`](../dr-14-prawo-ue-miedzynarodowe-prawa-czlowieka/SKILL.md) | EKPC, TSUE | `lex` | wewnętrzny |
| [`dr-16-pisma-strategia-dowody-orzecznictwo`](../dr-16-pisma-strategia-dowody-orzecznictwo/SKILL.md) | żądania, dowody, strategia | `lex` | wewnętrzny |
| [`citation-grounding-pl`](../citation-grounding-pl/SKILL.md) | kontrola treści cytatu (ISTNIENIE/TREŚĆ/FRAGMENT); LexMachina tego nie sprawdza | `awe:fundament-weryfikacyjny` | wywoływany |
| [`ekstraktor-cytatow-pl`](../ekstraktor-cytatow-pl/SKILL.md) | znajduje wszystkie powołania przed weryfikacją; sprawdzić, czy ma działający kod | `awe:fundament-weryfikacyjny` | wywoływany |
| [`adversarial-legal-review-pl`](../adversarial-legal-review-pl/SKILL.md) | debata czterech ról; bramka kosztu do wyłączenia patchem | `awe:fundament-weryfikacyjny` | wywoływany |
| [`atak-przeciwnika-pl`](../atak-przeciwnika-pl/SKILL.md) | osobny przebieg ataku | `awe:fundament-weryfikacyjny` | wywoływany |
| [`pierwsze-wrazenie-sedziego-pl`](../pierwsze-wrazenie-sedziego-pl/SKILL.md) | zimna lektura | `awe:fundament-weryfikacyjny` | wywoływany |
| [`subsumpcja-pl`](../subsumpcja-pl/SKILL.md) | pokrycie przesłanek faktami | `awe:fundament-weryfikacyjny` | wywoływany |
| [`deliverable-fidelity-pl`](../deliverable-fidelity-pl/SKILL.md) | czy ustalenia RED trafiły do pisma; check słowny traktować jako sito | `awe:fundament-weryfikacyjny` | wywoływany |
| [`struktura-wyroku-pl`](../struktura-wyroku-pl/SKILL.md) | rozdziela sentencję, ratio, votum separatum | `awe:orzecznictwo-zrodla` | wywoływany |
| [`uodo-grounding-pl`](../uodo-grounding-pl/SKILL.md) | decyzje UODO, sprawa RODO | `awe:orzecznictwo-zrodla` | wywoływany |
| [`webwright-legal-pl`](../webwright-legal-pl/SKILL.md) | orzeczenia z ms.gov.pl, sn.pl, TK bez MCP; wymaga Playwrighta | `awe:orzecznictwo-zrodla` | wywoływany |
| [`terminy-procesowe-pl`](../terminy-procesowe-pl/SKILL.md) | terminy; liczy wg KC, dla KPK/KPW wynik oznaczać do sprawdzenia | `awe:dokumenty` | wywoływany |
| [`kalkulatory-procesowe-pl`](../kalkulatory-procesowe-pl/SKILL.md) | opłata, WPS, odsetki, przedawnienie w pozwach cywilnych | `awe:dokumenty` | wywoływany |
| [`waliduj-podpis-pdf-pl`](../waliduj-podpis-pdf-pl/SKILL.md) | integralność podpisanych PDF od szpitali, sądów, prokuratury; tylko odczyt | `awe:dokumenty` | wywoływany |
| [`chronologia-stanowiska-pl`](../chronologia-stanowiska-pl/SKILL.md) | mechaniczna kontrola chronologii i stanowisk wobec cytatu i strony | `awe:dokumenty` | wywoływany |
| [`redline-docx-pl`](../redline-docx-pl/SKILL.md) | Track Changes; sanitize metadanych jest jawną komendą, nie domyślną operacją | `awe:dokumenty` | wywoływany |
| [`klauzule-kontraktowe-pl`](../klauzule-kontraktowe-pl/SKILL.md) | umowa zarządzania najmem | `awe:dokumenty` | wywoływany |
| [`rodo-dsar-pl`](../rodo-dsar-pl/SKILL.md) | żądania dostępu, sprostowania, usunięcia własnych danych | `awe:ochrona-danych` | wywoływany |
| [`marko-pl-content`](../marko-pl-content/SKILL.md) | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny | `awe:jakosc-tresci` | wewnętrzny |
| [`ocena-outputu-pl`](../ocena-outputu-pl/SKILL.md) | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny | `awe:fundament-weryfikacyjny` | wewnętrzny |
| [`patron-weryfikacja-cytatow`](../patron-weryfikacja-cytatow/SKILL.md) | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny | `own` | wewnętrzny |
| [`patron-przeglad-tabelaryczny`](../patron-przeglad-tabelaryczny/SKILL.md) | tabelaryczny przegląd dokumentów (z pipeline Patrona); do wzbogacenia o klauzule/kolumny pod Twoje sprawy | `own` | wywoływany |
| [`pisz-po-polsku`](../pisz-po-polsku/SKILL.md) | JEDEN skill redakcji: scala moduł poza pluginem + moduł poza pluginem + moduł poza pluginem (pliki skopiowane do own-skills, zmiany upstreamu trzeba przenosić ręcznie) | `own` | wywoływany |
| [`szturm-na-draft-pl`](../szturm-na-draft-pl/SKILL.md) | główny mechanizm wielokrotnej kontroli pisma; WYMAGA przebudowy (profil S/M/L i limit rund) - propozycja diffu, nie zastosowana | `own` | wywoływany |
| [`case-risk`](../case-risk/SKILL.md) | ryzyka dowodowe, medyczne, UoOZP, art. 192 kk; skrojony pod Twoje sprawy | `own` | wywoływany |
| [`medical-consent`](../medical-consent/SKILL.md) | zgoda na czynność medyczną, art. 192 kk | `own` | wywoływany |
| [`uoozp-compliance`](../uoozp-compliance/SKILL.md) | kontrola hospitalizacji psychiatrycznej | `own` | wywoływany |
| [`patron-analiza-akt-karnych`](../patron-analiza-akt-karnych/SKILL.md) | analiza akt karnych | `own` | wywoływany |
| [`patron-skan-dokumentu`](../patron-skan-dokumentu/SKILL.md) | deterministyczny skan przychodzących dokumentów pod kątem prompt injection | `own` | wywoływany |
| [`patron-identyfikatory-pl`](../patron-identyfikatory-pl/SKILL.md) | walidacja PESEL/NIP/KRS, ekstrakcja sygnatur | `own` | wywoływany |
| [`patron-prawo-pl-zrodla`](../patron-prawo-pl-zrodla/SKILL.md) | kolejność źródeł i konektorów MCP | `own` | wywoływany |
| [`zawiadomienie-o-przestepstwie`](../zawiadomienie-o-przestepstwie/SKILL.md) | pisane przez pokrzywdzonego obywatela | `own` | wywoływany |

## Moduły scalone z innymi skillami

| Moduł | Włączony do | Opis |
|---|---|---|
| `cofniecie-pozwu-ze-zrzeczeniem-roszczenia` | `pisma-procesowe-v3` | IURA: moduł typu pisma |
| `wniosek-o-rozprawe-zdalna` | `pisma-procesowe-v3` | IURA: moduł typu pisma (cywilne, karne) |
| `notatka-prawna` | `pisma-procesowe-v3` | IURA: struktura notatki; zastępuje osobny skill, wynik do analiza/_podsumowanie.md |
| `eu-legal-memo` | `pisma-procesowe-v3` | IURA-EU: memo prawa UE na eu-sparql i eu-compliance |
| `przeglad-umow` | `klauzule-kontraktowe-pl` | IURA: metodyka przeglądu umów; referencja zamiast osobnego skilla |
| `pozew-cywilny` | `pisma-procesowe-v3` | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
| `odpowiedz-na-pozew` | `pisma-procesowe-v3` | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
| `apelacja-karna` | `pisma-procesowe-v3` | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
| `zazalenie-na-postanowienie-prokuratora` | `pisma-procesowe-v3` | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
| `zarzuty-do-opinii-bieglego` | `pisma-procesowe-v3` | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
