# CHAT-CANON — zatwierdzony bundle LexMachina

**Istniejące routery prowadzą selekcję:** `prawny-router-v3` → `prawo-polskie-v2` → właściwe DR / wykonawca; `przewodnik-prawny-v2` jest fallbackiem. Nie twórz konkurencyjnej macierzy.

**Routery:** `prawny-router-v3`, `prawo-polskie-v2`, `przewodnik-prawny-v2`.

**Egzekutory i analityka:** `analiza-sadowa-v6`, `analizator-dowodow-v3`, `chronologia-sprawy-v1`, `analizator-przepisow-v2`, `przesluchanie-swiadkow-v2-min90`, `pisma-procesowe-v3`, `pisma-proste-v2`, `analizator-umow-v1`, `orzeczenia-sadowe-v2`, `raport-sytuacyjny-v2`, `raport-klienta-v1`.

**Wiedza wybrana do spraw TK/NC:** `dr-01-ustroj-konstytucyjny-i-zrodla-prawa`, `dr-02-prawo-cywilne-rodzinne-gospodarcze`, `dr-03-prawo-karne-wykroczenia-egzekucja`, `dr-05-prawo-administracyjne-sadowoadministracyjne`, `dr-10-zdrowie-farmacja-zywnosc-rolnictwo`, `dr-11-cyfrowe-cyber-ai-dane-ip`, `dr-12-sadownictwo-prokuratura-zawody-prawnicze`, `dr-13-sluzby-bezpieczenstwo-informacje-niejawne`, `dr-14-prawo-ue-miedzynarodowe-prawa-czlowieka`, `dr-16-pisma-strategia-dowody-orzecznictwo`.

**Biblioteka:** `shared`. **Oddzielne utrzymanie systemu (wywołanie jawne):** `audyt-systemu-v4`.

W sumie **26 skilli**. `chronologia-stanowiska-pl` nie należy do tego bundla. Dwa raportery są oczekiwane z LexMachina, ale przed integracją należy odczytać ich rzeczywisty kod i zasoby. Nazwa `prawne` nie została przypisana do istniejącego pliku SKILL; nie dopisuj jej jako fikcyjnego skilla.

`INDEKS-SKILLI.md` i `ACTIVATION-MATRIX.md` przechowują szerszą **historyczną** strukturę LexMachina. Każde odwołanie do skilla spoza zatwierdzonego kanonu ma status `EXTERNAL_NOT_BUNDLED`, chyba że jest rzeczywiście połączone niezależnie. Oryginalne zasoby `shared/` są czytane selektywnie i zachowują historyczne nazwy.
