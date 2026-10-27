# Indeks kanonicznych skilli grounding-prawo

Generowany przez [skrypt budowania](https://github.com/elconcept/grounding-prawo/blob/main/scripts/build.py) z selekcji pluginu.
Opis pochodzi z pola `why` selekcji lub frontmatter skilla.

**Skille:** 38. **Scalone moduły:** 32.

| Skill | Krótki opis | Źródło | Typ |
|---|---|---|---|
| [`wiki-basic-memory`](../wiki-basic-memory/SKILL.md) | pytania, syntezy i kontrola jakości wiki przez istniejące MCP | `own` | wywoływany |
| [`teczka-sprawy`](../teczka-sprawy/SKILL.md) | narzędzia teczki przeniesione z legal do pluginu | `own` | wywoływany |
| [`odczyt-dokumentow`](../odczyt-dokumentow/SKILL.md) | Jeden odczyt dokumentów do Markdown i kontraktu; the-ocr jako narzędzie, bez lokalnego OCR | `own` | wywoływany |
| [`prawny-router-v3`](../prawny-router-v3/SKILL.md) | jedyny router; patche: konfiguracja pluginu, wyjątek zawiadomienia, requires przycięte | `lex` | wywoływany |
| [`shared`](../shared/SKILL.md) | biblioteka hard-gate'ów, wymagana przez wszystkie skille silnika; nie jest agentem | `lex` | wewnętrzny |
| [`prawo-polskie-v2`](../prawo-polskie-v2/SKILL.md) | kwalifikacja postępowań, ROUTING-MAP do DR | `lex` | wywoływany |
| [`analiza-sadowa-v6`](../analiza-sadowa-v6/SKILL.md) | wieloprzebiegowy audyt sądowy | `lex` | wywoływany |
| [`analizator-dowodow-v3`](../analizator-dowodow-v3/SKILL.md) | sprzeczne zeznania, dokumentacja medyczna, nagrania, działania Policji | `lex` | wywoływany |
| [`analizator-przepisow-v2`](../analizator-przepisow-v2/SKILL.md) | przesłanki, wyjątki, brzmienie obowiązujące | `lex` | wywoływany |
| [`analizator-umow-v1`](../analizator-umow-v1/SKILL.md) | umowa najmu i kaucja; 13 odwołań z DR-02, więc odcięcie zepsułoby routing | `lex` | wywoływany |
| [`chronologia-sprawy-v1`](../chronologia-sprawy-v1/SKILL.md) | oś zdarzeń i niespójności między postępowaniami | `lex` | wywoływany |
| [`orzeczenia-sadowe-v2`](../orzeczenia-sadowe-v2/SKILL.md) | ocena tez orzeczeń | `lex` | wywoływany |
| [`pisma-procesowe-v3`](../pisma-procesowe-v3/SKILL.md) | główny generator pism | `lex` | wywoływany |
| [`pisma-proste-v2`](../pisma-proste-v2/SKILL.md) | 21 odwołań z shared; zostaje jako część silnika, a pełna kontrola jest wymagana zawsze (patrz shared/ZASADY-PLUGINU.md) | `lex` | wywoływany |
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
| [`kalkulatory-procesowe-pl`](../kalkulatory-procesowe-pl/SKILL.md) | opłata, WPS, odsetki, przedawnienie w pozwach cywilnych | `awe:dokumenty` | wywoływany |
| [`redline-docx-pl`](../redline-docx-pl/SKILL.md) | Track Changes; sanitize metadanych jest jawną komendą, nie domyślną operacją | `awe:dokumenty` | wywoływany |
| [`rodo-dsar-pl`](../rodo-dsar-pl/SKILL.md) | żądania dostępu, sprostowania, usunięcia własnych danych | `awe:ochrona-danych` | wywoływany |
| [`humanizer-pl`](../humanizer-pl/SKILL.md) | drugi, obowiązkowy etap redakcji po pisz-po-polsku; mechanika upstream 1.5.1, opis dostrojony do pism i analiz (22.10.2026) | `own` | wywoływany |
| [`patron-przeglad-tabelaryczny`](../patron-przeglad-tabelaryczny/SKILL.md) | tabelaryczny przegląd dokumentów (z pipeline Patrona); do wzbogacenia o klauzule/kolumny pod Twoje sprawy | `own` | wywoływany |
| [`pisz-po-polsku`](../pisz-po-polsku/SKILL.md) | autorski skill redakcji: pierwszy obowiązkowy etap przed humanizer-pl; scala moduł poza pluginem + moduł poza pluginem (22.10.2026) | `own` | wywoływany |
| [`szturm-na-draft-pl`](../szturm-na-draft-pl/SKILL.md) | główny mechanizm wielokrotnej kontroli pisma w pętli do GOTOWE; bez bramki kosztu i bez limitu rund | `own` | wywoływany |
| [`case-risk`](../case-risk/SKILL.md) | ryzyka dowodowe, medyczne, UoOZP, art. 192 kk; skrojony pod Twoje sprawy | `own` | wywoływany |
| [`patron-prawo-pl-zrodla`](../patron-prawo-pl-zrodla/SKILL.md) | kolejność źródeł i konektorów MCP | `own` | wywoływany |
| [`zawiadomienie-o-przestepstwie`](../zawiadomienie-o-przestepstwie/SKILL.md) | pisane przez pokrzywdzonego obywatela | `own` | wywoływany |

## Moduły scalone z innymi skillami

| Moduł | Włączony do | Opis |
|---|---|---|
| `ingest-wiki` | `wiki-basic-memory` | pełny ingest przez narzędzia MCP basic-memory, także w klientach przeglądarkowych |
| `ekstraktor-cytatow-pl` | `citation-grounding-pl` | znajduje wszystkie powołania przed weryfikacją; sprawdzić, czy ma działający kod |
| `adversarial-legal-review-pl` | `szturm-na-draft-pl` | debata czterech ról; pełny cykl zawsze, bez bramki kosztu |
| `atak-przeciwnika-pl` | `szturm-na-draft-pl` | osobny przebieg ataku |
| `pierwsze-wrazenie-sedziego-pl` | `szturm-na-draft-pl` | zimna lektura |
| `subsumpcja-pl` | `szturm-na-draft-pl` | pokrycie przesłanek faktami |
| `deliverable-fidelity-pl` | `szturm-na-draft-pl` | czy ustalenia RED trafiły do pisma; check słowny traktować jako sito |
| `struktura-wyroku-pl` | `orzeczenia-sadowe-v2` | rozdziela sentencję, ratio, votum separatum |
| `uodo-grounding-pl` | `patron-prawo-pl-zrodla` | decyzje UODO, sprawa RODO |
| `webwright-legal-pl` | `patron-prawo-pl-zrodla` | orzeczenia z ms.gov.pl, sn.pl, TK bez MCP; wymaga Playwrighta |
| `terminy-procesowe-pl` | `kalkulatory-procesowe-pl` | terminy; liczy wg KC, dla KPK/KPW wynik oznaczać do sprawdzenia |
| `waliduj-podpis-pdf-pl` | `odczyt-dokumentow` | integralność podpisanych PDF od szpitali, sądów, prokuratury; tylko odczyt |
| `chronologia-stanowiska-pl` | `chronologia-sprawy-v1` | mechaniczna kontrola chronologii i stanowisk wobec cytatu i strony |
| `klauzule-kontraktowe-pl` | `analizator-umow-v1` | umowa zarządzania najmem |
| `marko-pl-content` | `szturm-na-draft-pl` | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `ocena-outputu-pl` | `szturm-na-draft-pl` | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `patron-weryfikacja-cytatow` | `citation-grounding-pl` | używany przez szturm-na-draft-pl jako soczewka/skrypt; zostaje do czasu przebudowy szturmu, potem do ponownej oceny |
| `cofniecie-pozwu-ze-zrzeczeniem-roszczenia` | `pisma-procesowe-v3` | IURA: moduł typu pisma |
| `wniosek-o-rozprawe-zdalna` | `pisma-procesowe-v3` | IURA: moduł typu pisma (cywilne, karne) |
| `notatka-prawna` | `pisma-procesowe-v3` | IURA: struktura notatki; zastępuje osobny skill, wynik do analiza/_podsumowanie.md |
| `eu-legal-memo` | `pisma-procesowe-v3` | IURA-EU: memo prawa UE na eu-sparql i eu-compliance |
| `przeglad-umow` | `klauzule-kontraktowe-pl` | IURA: metodyka przeglądu umów; referencja zamiast osobnego skilla |
| `medical-consent` | `case-risk` | zgoda na czynność medyczną, art. 192 kk |
| `uoozp-compliance` | `case-risk` | kontrola hospitalizacji psychiatrycznej |
| `patron-analiza-akt-karnych` | `analiza-sadowa-v6` | analiza akt karnych |
| `patron-skan-dokumentu` | `odczyt-dokumentow` | deterministyczny skan przychodzących dokumentów pod kątem prompt injection |
| `patron-identyfikatory-pl` | `citation-grounding-pl` | walidacja PESEL/NIP/KRS, ekstrakcja sygnatur |
| `pozew-cywilny` | `pisma-procesowe-v3` | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
| `odpowiedz-na-pozew` | `pisma-procesowe-v3` | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
| `apelacja-karna` | `pisma-procesowe-v3` | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
| `zazalenie-na-postanowienie-prokuratora` | `pisma-procesowe-v3` | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
| `zarzuty-do-opinii-bieglego` | `pisma-procesowe-v3` | moduł typu pisma w pisma-procesowe-v3 (modules/typy/) |
