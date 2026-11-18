# CHAT-DR-RESOLUTION — przepisanie **identyfikatorów** bez zmiany routingu

Oryginalne wiersze `Routing błyskawiczny` w `SKILL.upstream.md` i aktywnym `SKILL.md` są identyczne; historyczny zapis `dr-XX` z wielkimi literami jest aliasem. Ta tabela tylko rozwiązuje alias na aktualny folder skilla, nigdy nie wybiera innej dziedziny.

| DR | Historyczny alias z oryginału | Docelowa nazwa skilla | W kanonie 26? | Obsługa przy braku w tej instalacji |
|---|---|---|---|---|
| DR-01 | `dr-01-Ustroj-Konstytucyjny-i-Zrodla-Prawa` | `dr-01-ustroj-konstytucyjny-i-zrodla-prawa` | TAK | `PLANNED` w wydaniu przejściowym lub `EXTERNAL_READ` po odczycie skilla |
| DR-02 | `dr-02-Prawo-Cywilne-Rodzinne-Gospodarcze` | `dr-02-prawo-cywilne-rodzinne-gospodarcze` | TAK | `PLANNED` w wydaniu przejściowym lub `EXTERNAL_READ` po odczycie skilla |
| DR-03 | `dr-03-Prawo-Karne-Wykroczenia-Egzekucja` | `dr-03-prawo-karne-wykroczenia-egzekucja` | TAK | `PLANNED` w wydaniu przejściowym lub `EXTERNAL_READ` po odczycie skilla |
| DR-04 | `dr-04-Prawo-Pracy-ZUS-Swiadczenia` | — | NIE | `OUT_OF_BUNDLE`, ewentualny osobny skill tylko po faktycznym odczycie |
| DR-05 | `dr-05-Prawo-Administracyjne-Sadowoadministracyjne` | `dr-05-prawo-administracyjne-sadowoadministracyjne` | TAK | `PLANNED` w wydaniu przejściowym lub `EXTERNAL_READ` po odczycie skilla |
| DR-06 | `dr-06-Podatki-Finanse-Publiczne-AML` | — | NIE | `OUT_OF_BUNDLE`, ewentualny osobny skill tylko po faktycznym odczycie |
| DR-07 | `dr-07-Zamowienia-Publiczne-Fundusze-UE` | — | NIE | `OUT_OF_BUNDLE`, ewentualny osobny skill tylko po faktycznym odczycie |
| DR-08 | `dr-08-Samorzad-Terytorialny-Prawo-Lokalne` | — | NIE | `OUT_OF_BUNDLE`, ewentualny osobny skill tylko po faktycznym odczycie |
| DR-09 | `dr-09-Budownictwo-Srodowisko-Energia-Transport` | — | NIE | `OUT_OF_BUNDLE`, ewentualny osobny skill tylko po faktycznym odczycie |
| DR-10 | `dr-10-Zdrowie-Farmacja-Zywnosc-Rolnictwo` | `dr-10-zdrowie-farmacja-zywnosc-rolnictwo` | TAK | `PLANNED` w wydaniu przejściowym lub `EXTERNAL_READ` po odczycie skilla |
| DR-11 | `dr-11-Cyfrowe-Cyber-AI-Dane-IP` | `dr-11-cyfrowe-cyber-ai-dane-ip` | TAK | `PLANNED` w wydaniu przejściowym lub `EXTERNAL_READ` po odczycie skilla |
| DR-12 | `dr-12-Sadownictwo-Prokuratura-Zawody-Prawnicze` | `dr-12-sadownictwo-prokuratura-zawody-prawnicze` | TAK | `PLANNED` w wydaniu przejściowym lub `EXTERNAL_READ` po odczycie skilla |
| DR-13 | `dr-13-Sluzby-Bezpieczenstwo-Informacje-Niejawne` | `dr-13-sluzby-bezpieczenstwo-informacje-niejawne` | TAK | `PLANNED` w wydaniu przejściowym lub `EXTERNAL_READ` po odczycie skilla |
| DR-14 | `dr-14-Prawo-UE-Miedzynarodowe-Prawa-Czlowieka` | `dr-14-prawo-ue-miedzynarodowe-prawa-czlowieka` | TAK | `PLANNED` w wydaniu przejściowym lub `EXTERNAL_READ` po odczycie skilla |
| DR-15 | `dr-15-Compliance-ISO-Governance-Audyt` | — | NIE | `OUT_OF_BUNDLE`, ewentualny osobny skill tylko po faktycznym odczycie |
| DR-16 | `dr-16-Pisma-Strategia-Dowody-Orzecznictwo` | `dr-16-pisma-strategia-dowody-orzecznictwo` | TAK | `PLANNED` w wydaniu przejściowym lub `EXTERNAL_READ` po odczycie skilla |

Historyczne aliasy dla wyłączonych DR pozostają **bez zmian** w `SKILL.upstream.md`/`ROUTING-MAP.md`. Znak `—` oznacza, że w tym bundlu nie utworzono ani nie zainstalowano skilla, a nie nowy adres routingu.

### Testy przypadków, wyłącznie jako kontrola semantyczna
- „skarga na policjanta” → oryginalny DR-13, jeżeli kontekst służbowy; równoległe KPK może uruchomić DR-03 w oryginalnym routerze, nie według nowej reguły adaptera.
- „egzekucja komornicza” → oryginalny DR-02 (KPC); „komornik jako zawód” → oryginalny DR-12.
- „przemoc domowa” → DR-03; dokumentacja psychiatryczna → DR-10; służbowe uprawnienia Policji → DR-13, zależnie od pytania.
- „umowa najmu na czas określony” → DR-02, a nie DR-04.
- „podatek VAT” → DR-06, mimo że poza bundlem; **nie** kieruj do DR-02.
- „prawa człowieka i ETPC” → DR-14, z rozróżnieniem EKPC od prawa UE.
- Wyszukanie dopasowania nie zastępuje realnego odczytu skilla ani aktu.
