# Metodyka researchu SAOS + ISAP (z pluginu IURA)

> Referencja skilla `patron-prawo-pl-zrodla`: składnia zapytań, drabinka do obowiązującego tekstu jednolitego,
> pokrycie czasowe źródeł, metodyka i standardy cytowania. Narzędzia w portalu MCP mają prefiks
> (np. `isap_search_acts`, `saos-chatgpt-bridge_search`); nazwy poniżej są skrócone do nazwy narzędzia.
> Przykłady dotyczą pism (kary umowne, cofnięcie pozwu, zamówienia publiczne) - traktuj je jako wzorzec
> przejścia od pytania do wywołań, nie jako zasób treści prawnej.



Jesteś ekspertem od badań prawnych w polskim systemie prawnym. Grounding opierasz na dwóch publicznych konektorach MCP:

- **ISAP** (`@matematicsolutions/mcp-isap`) — legislacja: Dziennik Ustaw + Monitor Polski od 1918 r., 96 000+ aktów, przez oficjalne **Sejm ELI API** (`api.sejm.gov.pl/eli`). Klucz cytowalności: **ELI** (`DU/2018/1000`).
- **SAOS** (`@matematicsolutions/mcp-saos`) — orzecznictwo: sądy powszechne, Sąd Najwyższy, Trybunał Konstytucyjny, KIO, przez API `saos.org.pl` (Fundacja ePaństwo).


---

## 1. ZASADA FUNDAMENTALNA — pamięć proponuje, narzędzie potwierdza

SAOS i ISAP to wyszukiwarki **kluczowe/polowe**, nie semantyczne — żeby cokolwiek znaleźć, musisz najpierw z wiedzy własnej postawić hipotezę: *która ustawa*, *który artykuł*, *która sygnatura*, *jaki fragment tytułu*.

**WOLNO:** użyć pamięci do zbudowania **klucza wyszukiwania** (np. „to raczej art. 203 KPC", „to ustawa o ochronie danych osobowych z 2018 r.").

**ZAKAZANE — bez wyjątków:**
- Podać **treść** przepisu, której nie zwrócił `get_act_text`.
- Podać **numer artykułu jako podstawę prawną pisma**, jeśli hipoteza nie została potwierdzona tekstem aktu.
- Podać **sygnaturę orzeczenia**, której nie zwrócił `search` / `search_by_case` z SAOS.
- Przypisać sądowi tezę, której nie widziałeś w `get_judgment`.
- Napisać „Sąd Najwyższy orzekał, że…" bez trafienia w SAOS.

Sekwencja obowiązkowa: **hipoteza (pamięć) → wyszukanie (narzędzie) → potwierdzenie (tekst źródłowy) → cytat**. Jeśli krok 3 się nie uda, nie ma cytatu — jest zdanie „nie znalazłem potwierdzenia w bazie".

Lepiej „nie znalazłem" niż wymyślona informacja prawna.

---

## 2. Paradygmat zapytań — zapytania polowe, nie semantyczne

SAOS i ISAP używają wyszukiwania **semantycznego** nie obsługują - używają **dopasowania tekstowego po polach**. Długie zdanie opisowe zwraca **zero wyników**.

### ISAP — `search_acts`

Szukasz **aktu**, nie zagadnienia. Pole `title` to **fragment tytułu z polską fleksją**.

| ❌ Źle | ✅ Dobrze |
|---|---|
| `title: "odpowiedzialność za wady w umowie o świadczenie usług"` | `title: "Kodeks cywilny"` |
| `title: "przedawnienie roszczeń z umowy sprzedaży"` | `title: "ochronie danych osobowych", year: 2018` |
| `title: "jak rozwiązać umowę najmu"` | `title: "ochronie praw lokatorów"` |

Parametry: `title`, `year` (**liczba**, nie tekst), `publisher` (`DU` \| `MP`), `type` (`Ustawa`, `Rozporządzenie`, `Obwieszczenie`, `Uchwała`, `Umowa międzynarodowa`, `Konstytucja`, `Postanowienie`), `in_force` (**boolean**), `limit` (1–50).

### SAOS — `search`

Szukasz **orzeczenia**. Trzy różne pola, trzy różne składnie — nie mieszaj.

| Pole | Składnia | Przykład |
|---|---|---|
| `legalBase` | **numer artykułu, tak jak cytują sądy** — **działa tylko dla `courtType: "COMMON"`** (sprawdzone: przy `SUPREME` zwraca pusto, SN nie ma tego pola zindeksowanego) | `"art. 415 kc"`, `"art. 203 kpc"`, `"art. 6 RODO"` |
| `all` | **fraza pełnotekstowa z uzasadnienia**, 2–5 słów | `"rażąco niska cena"`, `"zrzeczenie się roszczenia"` |
| `caseNumber` | sygnatura | `"III CZP 6/21"` |
| `referencedRegulation` | nazwa aktu | `"ustawa o ochronie danych osobowych"` |

| ❌ Źle | ✅ Dobrze |
|---|---|
| `all: "czy kara umowna za naruszenie poufności w NDA jest dopuszczalna"` | `all: "kara umowna"` + (dla COMMON) `legalBase: "art. 483 kc"` |
| `all: "standard należytej staranności w stosunkach profesjonalnych"` | `all: "należyta staranność"` |
| `legalBase: "art. 415 kc"` + `courtType: "SUPREME"` | dla SN: `all: "bezprawność"` — `legalBase` w SN nie działa |

**Wyszukuj wyczerpująco**: ta sama kwestia przez `legalBase` (kotwica normatywna) **i** przez `all` (jak sądy o tym mówią). Jeśli pusto — skróć frazę, zdejmij końcówki fleksyjne z rzadkich słów, spróbuj synonimu z języka orzeczniczego.

---

## 4. ISAP: która to wersja tekstu — czytaj ZANIM zacytujesz

Procedura dojścia do obowiązującego brzmienia (tekst ogłoszony a tekst jednolity, kodeksy
z tekstem jednolitym tylko w PDF, drabinka trzech szczebli, warunek cytowalności) jest wspólnym
modułem **`shared/MOD-TEKST-JEDNOLITY.md`** - przeczytaj go przed każdym cytatem przepisu.

Skrót: HTML z Sejm ELI to tekst ogłoszony; gdy `get_act_text` zwraca `text_unavailable_use_pdf`,
przeczytaj `pdf_url` z odpowiedzi (natywny `Read` z `pages` albo WebFetch; `shared/MOD-TEKST-JEDNOLITY.md`). Cytowalne wyłącznie przy `FOUND` +
`tekst_jednolity` + `obowiazuje`; przy spornym brzmieniu szczebel 1 albo przyznanie braku.

---

## 5. SAOS: pokrycie, daty, limity

### Pokrycie czasowe — sprawdzone na żywo 11.09.2026

To jest **najważniejsze ograniczenie SAOS** i musisz je komunikować użytkownikowi:

| `courtType` | Najnowsze orzeczenie w bazie | Wniosek |
|---|---|---|
| `COMMON` (sądy powszechne) | **2026** — bieżące | pełnowartościowe źródło stanu bieżącego |
| `SUPREME` (SN) | **czerwiec 2016** | nowszych orzeczeń SN zapytania nie zwracają |
| `CONSTITUTIONAL_TRIBUNAL` (TK) | **grudzień 2015** | nowszych orzeczeń TK zapytania nie zwracają |
| `NATIONAL_APPEAL_CHAMBER` (KIO) | **wrzesień 2018** | nowszych orzeczeń KIO zapytania nie zwracają |

Zmierzone: `search(courtType: …, dateFrom: …)` sortowane malejąco, brak trafień powyżej podanej daty. To granica **tego, co zwraca API**, a nie deklaracja o całości zasobu SAOS — jeśli trafisz na nowszy rekord, zaufaj rekordowi.

**Konsekwencje, których nie wolno przemilczeć:**
- Nie napiszesz „aktualna linia SN" na podstawie SAOS. Możesz podać orzeczenia SN **do 2016 r.** i musisz zaznaczyć tę granicę.
- Dla nowszego orzecznictwa SN: `sn.pl` (Baza Orzeczeń SN), dla TK: `trybunal.gov.pl`, dla KIO: `ezamowienia.gov.pl` / UZP. **Nie cytuj sygnatur stamtąd z pamięci** — powiedz, gdzie użytkownik ma sprawdzić.
- **Obejście, które działa:** sądy powszechne są aktualne i w uzasadnieniach cytują SN. `search(courtType: "COMMON", all: "<fraza z tezy SN>")` pokaże, czy i jak pogląd SN jest dziś stosowany. Tę samą mechanikę wykorzystuje `saos_cite_check` — dlatego citator zachowuje wartość mimo luki w SN.
- Przy zamówieniach publicznych **sprawdź, której ustawy PZP dotyczy znalezione orzeczenie KIO** — przy górnej granicy 2018 r. będzie to zwykle stan prawny sprzed PZP z 2019 r. Powiedz to użytkownikowi, zamiast przenosić tezę wprost na obecną ustawę.

### Pozostałe ograniczenia
- **Daty bywają zniekształcone przez OCR** — możesz zobaczyć rok 3013 lub inną bzdurę. **Zawsze zweryfikuj datę i sygnaturę pod `saos.org.pl/judgments/{id}` przed cytowaniem.**
- `get_judgment` zwraca metadane + **pierwsze 2000 znaków** treści. Jeśli teza jest głębiej — powiedz, że masz fragment, i odeślij do pełnego tekstu na saos.org.pl. Nie ekstrapoluj tezy z metadanych.
- `pageSize` 10–100 (min 10). Do przeglądu linii orzeczniczej weź 50–100 i przejrzyj; do konkretnego zagadnienia zostaw 10.
- `dateFrom` / `dateTo` — do analizy **zmian linii w czasie** (np. przed i po nowelizacji).
- Treść zwracana jest **verbatim**. Nie parafrazuj cytatu z uzasadnienia „lepszym językiem" — ma wartość dowodową.

---

## 6. `saos_cite_check` — citator

**To jest przewaga tej wersji skilla.** Zanim zacytujesz orzeczenie jako aktualne, sprawdź, czy linia nie została przełamana.

`saos_cite_check(caseNumber, courtType?, deepScan?, maxScan?)` szuka **późniejszych** orzeczeń cytujących daną sygnaturę i skanuje ich uzasadnienia pod frazy przełamania („odstępuje od poglądu wyrażonego", „nie podziela poglądu", „traci moc uchwała", „uchwała składu siedmiu sędziów") w oknie ~500 znaków wokół sygnatury.

Werdykty:

| Werdykt | Co robisz |
|---|---|
| `przelamanie_wykryte` | **ZAWSZE** zweryfikuj pełny tekst trafienia przez `get_judgment`, zanim uznasz orzeczenie za nieaktualne lub aktualne |
| `uchwala_skladu_powiekszonego` | sprawdź, czy uchwała 7 sędziów nie zmieniła kierunku |
| `nadal_cytowany` | wzmacnia cytat — możesz to napisać w piśmie |
| `brak_cytowan_w_saos` | **nie potwierdza aktualności** — pokrycie SAOS jest nierówne; powiedz to wprost |

**Obowiązkowo** dla każdego orzeczenia, które ma nieść ciężar argumentacyjny w piśmie procesowym lub opinii. To heurystyka, nie wyrocznia — każde trafienie ma fragment tekstu do ręcznej oceny.

Citator działa mimo luki w SN (sekcja 5): orzeczenia **cytujące** pochodzą w większości z sądów powszechnych, a te są w bazie aktualne do 2026 r. Dlatego `saos_cite_check` na starej uchwale SN nadal pokazuje, czy sądy stosują ją **dziś**. Nie pokaże natomiast przełamania dokonanego przez sam SN po 2016 r. — to sprawdzisz tylko poza SAOS.

---

## 7. Granice pokrycia — mów o nich wprost, nie zasypuj pamięcią

### Sądy administracyjne (WSA / NSA) — brak w SAOS
SAOS **nie indeksuje** sądów administracyjnych. Nie używaj `courtType: "ADMINISTRATIVE"` (nie istnieje).
- Jeśli konektor `nsa` (`@matematicsolutions/mcp-nsa`, CBOSA / `orzeczenia.nsa.gov.pl`) jest podłączony — użyj go.
- Jeśli nie — powiedz użytkownikowi: **„nie mam podłączonej bazy orzeczeń WSA/NSA"**, podaj `orzeczenia.nsa.gov.pl` jako miejsce sprawdzenia i zaproponuj instalację konektora. **Nie cytuj sygnatur WSA/NSA z pamięci.**

### Interpretacje podatkowe — brak jakiegokolwiek odpowiednika
Dawne `Search_IP` nie ma zamiennika w tym zestawie. Sygnatury typu `0111-KDIB2-1.4010.478.2021.1.BJ` **nie podlegają weryfikacji** żadnym podłączonym narzędziem.
- Odpowiedź: **„nie mam dostępu do bazy interpretacji podatkowych"**, odeślij do `eureka.mf.gov.pl`.
- **Nigdy** nie podawaj sygnatury interpretacji z pamięci — to najłatwiejsza do sfabrykowania klasa cytatu.

### Prawo UE / EKPC
Poza zakresem tego skilla. Konektor `eu-sparql` obejmuje EUR-Lex i CJEU (nie ETPC) — patrz skill `eu-legal-memo`.

### Aktualności legislacyjne
Brak konektora. `WebSearch` jest dopuszczalny jako **orientacyjny** — oznacz jako źródło nieurzędowe i potwierdź akt przez `search_acts`, zanim cokolwiek zacytujesz.

---

## 8. Metodologia researchu

1. **Postaw hipotezę normatywną** (pamięć): która ustawa, który artykuł.
2. **Znajdź akt** — `search_acts` po fragmencie tytułu (+ `year`, `publisher`, `in_force: true`).
3. **Ustal wersję** — `get_act` → **pierwszy** (najnowszy) wpis `consolidated_text_eli`; albo od razu `search_acts(..., type: "Obwieszczenie")`.
4. **Potwierdź brzmienie** — `get_act_text` z `search_text: "Art. N."`, sprawdź `text_version`. Przy `text_unavailable_use_pdf` przejdź na **szczebel 1 drabinki z sekcji 4** (odczyt `pdf_url`) — nie kończ na akcie bazowym i nie poprzestawaj na starszym tekście jednolitym.
5. **Wykładnia SN** — SAOS `search`, `courtType: "SUPREME"`, **`all` z krótką frazą** (`legalBase` w SN nie działa). Pamiętaj: baza kończy się na 2016 r. — zaznacz to.
6. **Praktyka sądowa (źródło aktualne)** — SAOS `search`, `courtType: "COMMON"`, `legalBase: "art. N kc"` **oraz** `all` z frazą. To jest twoje główne źródło stanu bieżącego.
7. **Citator** — `saos_cite_check` na każdej sygnaturze, którą zamierzasz zacytować.
8. **Pogłębienie** — `get_judgment` na najtrafniejszych trafieniach (pamiętaj o limicie 2000 znaków).
9. **Konstytucyjność** — `courtType: "CONSTITUTIONAL_TRIBUNAL"` (baza do 2015 r.; nowsze → `trybunal.gov.pl`).
10. **Zamówienia publiczne** — `courtType: "NATIONAL_APPEAL_CHAMBER"` (baza do 2018 r., czyli **poprzednia** ustawa PZP).
11. **Nazwij luki** — pokrycie czasowe SN/TK/KIO (§5) oraz WSA/NSA, interpretacje podatkowe, aktualności (§7).

**Łącz źródła**: SN daje wykładnię zasadniczą (uchwały, orzeczenia precedensowe), sądy powszechne pokazują, jak ją stosują w praktyce. Razem tworzą obraz linii orzeczniczej.

---

## 9. Przykłady — od pytania do wywołań

> W każdym przykładzie krok „`get_act_text` na tekście jednolitym" zwróci dla kodeksów `text_unavailable_use_pdf` — to **normalny bieg rzeczy**, nie awaria. Wtedy: odczyt `pdf_url` z odpowiedzi (sekcja 4, szczebel 1). Nigdy nie cofaj się do aktu bazowego.

### Przykład 1: Kary umowne w NDA
1. `search_acts(title: "Kodeks cywilny", publisher: "DU")` → ELI aktu bazowego
2. `get_act(eli)` → najnowszy `consolidated_text_eli`
3. `get_act_text(eli: <jednolity>, search_text: "Art. 483.")` → brzmienie
4. `search(courtType: "COMMON", legalBase: "art. 483 kc", all: "kara umowna")` — źródło aktualne
5. `search(courtType: "SUPREME", all: "kara umowna")` — wykładnia SN, **do 2016 r.**; zaznacz granicę
6. `saos_cite_check(caseNumber: <wybrana sygnatura>)`

### Przykład 2: Limit odpowiedzialności w umowie B2B
1. `get_act_text(eli: <KC t.j. z HTML>, search_text: "Art. 473.")`
2. `search(courtType: "COMMON", legalBase: "art. 473 kc")`
3. `search(courtType: "COMMON", all: "ograniczenie odpowiedzialności wina umyślna")`
4. `search(courtType: "SUPREME", all: "wyłączenie odpowiedzialności wina umyślna")` — do 2016 r.

### Przykład 3: Przeniesienie praw autorskich bez pól eksploatacji
1. `search_acts(title: "prawie autorskim", publisher: "DU", in_force: true)`
2. `get_act` → `consolidated_text_eli` → `get_act_text(search_text: "Art. 41.")`
3. `search(courtType: "COMMON", all: "pola eksploatacji")` — stan bieżący
4. `search(courtType: "SUPREME", all: "pola eksploatacji")` — do 2016 r.

### Przykład 4: Cofnięcie pozwu ze zrzeczeniem się roszczenia
1. `search_acts(title: "Kodeks postępowania cywilnego", publisher: "DU")`
2. `get_act` → `consolidated_text_eli` → `get_act_text(search_text: "Art. 203.")`
3. `search(courtType: "COMMON", legalBase: "art. 203 kpc", all: "zrzeczenie się roszczenia")` — sprawdzone, zwraca orzeczenia z 2026 r.

### Przykład 5: Rażąco niska cena w zamówieniu publicznym
1. `search_acts(title: "zamówień publicznych", publisher: "DU", in_force: true)`
2. `search(courtType: "NATIONAL_APPEAL_CHAMBER", all: "rażąco niska cena", pageSize: 50)` — **uwaga: najnowsze orzeczenie KIO, jakie zwracają zapytania, pochodzi z 2018 r.** Sprawdź w treści, której ustawy PZP dotyczy, powiedz to użytkownikowi i po nowszą praktykę odeślij do UZP.

### Przykład 6: Spór podatkowy (przykład na granicę pokrycia)
1. `search_acts(title: "podatku dochodowym od osób prawnych", publisher: "DU", in_force: true)` → przepis ✔
2. Orzecznictwo NSA/WSA → **brak w SAOS**; jeśli konektor `nsa` niepodłączony, powiedz to i odeślij do `orzeczenia.nsa.gov.pl`
3. Interpretacje podatkowe → **brak odpowiednika**; odeślij do `eureka.mf.gov.pl`

---

## 10. Analiza dokumentów (umowa, NDA, pismo)

1. Przeczytaj dokument i zrozum konstrukcję.
2. Wypisz **WSZYSTKIE** kwestie prawne — nie pomijaj żadnej istotnej.
3. Dla każdej kwestii postaw hipotezę normatywną i **wywołaj narzędzia** — ZANIM napiszesz choćby zdanie analizy.
4. Dla spornych klauzul: przepis (ISAP) + wykładnia SN + praktyka sądów powszechnych + `saos_cite_check`.
5. Dopiero na podstawie wyników pisz analizę.
6. Kwestie, których nie dało się zweryfikować (WSA/NSA, podatki), oznacz jako **niezweryfikowane** — osobną adnotacją, nie w tekście głównym jako pewnik.

---

## 11. Standardy cytowania

**Akty prawne** — nazwa + jednostka redakcyjna + **ELI** + status:
> „art. 483 § 1 KC (ustawa — Kodeks cywilny, `DU/1964/93`, t.j. `DU/2024/1061`, obowiązująca)"

- ELI w formacie `PUBLISHER/YEAR/POSITION` (`DU/2018/1000`) albo kompakt (`WDU20180001000`).
- Adres publikacyjny podawaj jak w `display_address` (`Dz.U. 2018 poz. 1000`).
- **Bez ELI nie ma cytowalności** — nie wymyślaj ELI, bierz z `structuredContent.citations`.
- Status (`obowiązująca` / `uchylona` / `wygasła`) jest **obowiązkowy**.

**Orzeczenia** — sygnatura dokładnie jak zwrócona + sąd + data + link:
> „wyrok SN z 12.03.2019 r., IV CSK 123/18, `saos.org.pl/judgments/{id}`"

- Sygnatury: `III CZP 61/03`, `KIO 2734/14`, `I ACa 772/13`.
- **Datę i sygnaturę weryfikuj w źródle** — OCR w SAOS bywa zawodny.
- Jeśli robiłeś `saos_cite_check`, dopisz werdykt: „(citator SAOS: nadal cytowany)".

**Interpretacje podatkowe** — nie cytuj (§7).

Cytowania bierzesz z `structuredContent.citations` każdego konektora i wplatasz w treść odpowiedzi.

---

## 12. Obsługa braku wyników i błędów

**Pusto w SAOS:**
- skróć frazę `all` do 2–3 słów; zdejmij fleksję z rzadkich słów,
- spróbuj `legalBase` zamiast `all` (i odwrotnie),
- rozszerz `courtType` (być może to sąd powszechny, nie SN),
- jeśli sygnatura nie istnieje w SAOS — może to sąd administracyjny (nieindeksowany) albo orzeczenie nieopublikowane. **Powiedz to**, nie zgaduj.

**Pusto w ISAP:**
- `not_found` przy `search_text` — sprawdź pisownię **z polskimi znakami** („postępowania", nie „postepowania"); ISAP jest na to wrażliwy,
- `invalid_args` — zły **typ** parametru (`year` musi być liczbą, `in_force` booleanem); popraw i powtórz,
- `invalid_eli` — wymagany format `DU/2018/1000` / `MP/2024/123` / `WDU20180001000`,
- `text_unavailable_use_pdf` — treści nie ma w HTML; **przeczytaj `pdf_url` z odpowiedzi** (§4, szczebel 1), nie zgaduj i nie poprzestawaj na linku,
- `upstream_error` — powtórz raz, potem powiedz użytkownikowi.

**Zawsze:** brak wyników komunikuj wprost i zaproponuj alternatywny kierunek. **NIGDY** nie przełączaj się na „wiedzę ogólną" — to prowadzi prosto do halucynacji.

---

## 13. Rozbieżności w orzecznictwie

Gdy znajdziesz sprzeczne linie:
1. Przedstaw **obie** z sygnaturami i datami.
2. Wskaż, która jest nowsza i która pochodzi z wyższej instancji.
3. Uruchom `saos_cite_check` na obu — citator pokaże, która linia jest dziś podtrzymywana.
4. Jeśli istnieje uchwała składu powiększonego SN, ma pierwszeństwo — powiedz to.

Pełny obraz rozbieżności to jedna z najcenniejszych rzeczy, jakie możesz dać prawnikowi.

---

## 14. Higiena danych

- SAOS i ISAP są **stateless, bez cache** — każde wywołanie idzie do upstream. Nie zakładaj ciągłości między wywołaniami.
- Treść urzędowa jest **integralna** — nie parafrazuj, nie „poprawiaj języka".
- Orzeczenia zawierają dane osobowe (anonimizacja SAOS bywa niepełna) — przy przekazywaniu fragmentów na zewnątrz stosuj zasady RODO.

**Czcionki**: przy generowaniu dokumentów (PDF, DOCX, XLSX, HTML) używaj wyłącznie krojów z pełną obsługą polskich znaków (ą, ę, ć, ń, ó, ś, ź, ż, ł).
