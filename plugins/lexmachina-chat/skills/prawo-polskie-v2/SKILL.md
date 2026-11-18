---
name: prawo-polskie-v2
description: "Fasada dziedzinowa LexMachina dla DR-01–DR-16. Uruchamiana z prawny-router-v3, nie samodzielny router spraw; mapuje temat na DR i moduł aktu."
metadata:
  version: '6.73'
  adapter_version: '0.5.0'
  type: domain-router
  status: chat-stage3-integrated
  compatibility: ChatGPT CHAT, available installed DR skills, actual file/web/MCP tools
  dependencies: '{"requires": ["shared", "prawny-router-v3"], "optional": ["dr-01-ustroj-konstytucyjny-i-zrodla-prawa", "dr-02-prawo-cywilne-rodzinne-gospodarcze", "dr-03-prawo-karne-wykroczenia-egzekucja", "dr-05-prawo-administracyjne-sadowoadministracyjne", "dr-10-zdrowie-farmacja-zywnosc-rolnictwo", "dr-11-cyfrowe-cyber-ai-dane-ip", "dr-12-sadownictwo-prokuratura-zawody-prawnicze", "dr-13-sluzby-bezpieczenstwo-informacje-niejawne", "dr-14-prawo-ue-miedzynarodowe-prawa-czlowieka", "dr-16-pisma-strategia-dowody-orzecznictwo"]}'
  source_skill_sha256: '83ca773d06c323a28369cd1f58d9a8be48f6e13534d3d1c6ee31ba991f756641'
  source_map_sha256: '0365ef3542204a2ba37f53e990530ee524048181af63335cefde25e40b7e4f23'
---


## Profil CHAT wydania 0.5.0 — tylko granice środowiska

**Jedyna selekcja dziedziny pochodzi z oryginalnego bloku `Routing błyskawiczny` i pełnego `ROUTING-MAP.md`; nie twórz drugiej macierzy i nie zmieniaj kolejności oryginalnego `prawny-router-v3` (PRIMARY → SECONDARY → FALLBACK).** Oryginalny `SKILL.md` 6.73 jest zachowany jako `SKILL.upstream.md`; pełna mapa 16 DR jest zachowana bajt w bajt. Zmiana dotyczy hosta, nie routingu materialnego.

1. **Wejście:** przy zwykłej sprawie prawnej najpierw rzeczywiście odczytaj `prawny-router-v3/SKILL.md` z tej samej wtyczki. Ta fasada jest wywoływana po jego kroku 1B lub tam, gdzie sam router wskazuje ją jako PRIMARY/SECONDARY. Nie uruchamiaj nowego, równoległego „chat routera” do selekcji dziedziny. W razie bezpośredniego wywołania skieruj przebieg do oryginalnego routera przed wyborem DR.
2. **Mapowanie:** odczytaj wyłącznie potrzebną sekcję DR z `ROUTING-MAP.md`, zachowaj wskazany DR i moduł. Historyczne wielkie litery i aliasy `dr-XX-...` z instrukcji szybkie routingu normalizuj wyłącznie do faktycznej nazwy katalogu skilla na podstawie `references/CHAT-DR-RESOLUTION.md` — to rozwiązywanie identyfikatora, a NIE zmiana przypisania dziedziny. Przy dwóch rzeczywiście występujących dziedzinach zaznacz PRIMARY i właściwy SECONDARY zgodnie z pierwotnym routerem.
3. **10/16 w kanonie:** zatwierdzony docelowy bundle obejmuje DR-01,02,03,05,10,11,12,13,14,16. Pozostałe DR-04,06,07,08,09,15 występują w źródłowej mapie i NIE WOLNO przekierować ich automatycznie do innej dziedziny. Wskaż zgodną trasę i `OUT_OF_BUNDLE`; korzystaj z odpowiedniego osobno zainstalowanego skilla tylko po rzeczywistym odczycie, inaczej `NOT_AVAILABLE`. W etapie 3 większość zatwierdzonych DR nadal jest w **odrębnych pluginach**; ich obecność w planie nie gwarantuje aktywacji w tej sesji.
4. **Canonical shared:** `shared/X` to kanoniczny `skills/shared/X` w **tej samej wtyczce**, nie jedna z historycznie skopiowanych bibliotek w starych skillach wykonawczych. Odczytuj tylko moduły potrzebne dla wybranej dziedziny; brak konkretnego pliku zgłoś, nie zastępuj jego treści pamięcią modelu. Reguły dowodowe z `shared/FACT-SOURCE-LOCK.md` i `shared/references/CHAT-EVIDENCE-MODEL.md` dotyczą spraw TK/NC i innych tam, gdzie właściwe.
5. **Pamięć i narzędzia:** nie wymagaj automatycznego `model-memory`, Basic Memory, MCP `repertorium_szukaj_repertorium`, SSH, Python, lokalnego `view`, pliku `_PRZEBIEGI.md` ani zapisu na `main` do udzielenia analizy. Korzystaj z narzędzi tylko gdy faktycznie są dostępne. Nie deklaruj odczytu ani zapisania notatki bez odpowiedzi narzędzia. Nie przenoś danych medycznych, osobowych ani danych spraw do publicznych wyszukiwarek bez wyraźnego uzasadnienia i uprawnienia.
6. **Prawo na datę:** `ROUTING-MAP.md` to historyczny indeks (ostatni zapis 2026-10-22) zawierający również Dz.U., statusy oraz liczniki; NIE jest dowodem aktualnego brzmienia przepisu ani kompletnego pokrycia aktu. Dla zastosowanego artykułu/rozstrzygnięcia sprawdź faktycznie tekst, wersję temporalną i źródło urzędowe. Jeśli nie sprawdzono: `NOT_CHECKED`, lecz wykonaj możliwą analizę faktów. Nie udawaj zapytania Repertorium lub odczytu ELI. `✅ OK` w mapie oznacza trasę, nie rozstrzygnięty stan prawny.
7. **Korekta potencjalnej asymetrii:** bezpośrednie relacje użytkownika są źródłem faktów wejściowych w jego sprawie; metadane dokumentu Policji/prokuratury/szpitala nie dowodzą prawdziwości jego twierdzeń. Najpierw zbadaj podstawy wersji obciążających, potem oceniaj dowody użytkownika łącznie. Nie dopisuj organom niewskazanych przez nich scenariuszy. Nie narzucaj standardu skazania zawiadomieniu o przestępstwie.
8. **Ślad:** wskaż wybrany DR, konkretny moduł (o ile znaleziony), rzeczywisty status `INSTALLED_READ`/`EXTERNAL_READ`/`OUT_OF_BUNDLE`/`NOT_AVAILABLE`, status prawa `VERIFIED` lub `NOT_CHECKED`, ewentualne luki. **Wybór trasy nie jest uruchomieniem skilla.** W przypadku brakującego DR nie udawaj jego pracy.

Szczegóły: `references/CHAT-RUNTIME.md`, `references/CHAT-DR-RESOLUTION.md`, oryginał w `SKILL.upstream.md`. Wszelkie aktualizacje treści mapy wymagają osobnego cyklu redakcji i weryfikacji, nie są skutkiem instalacji tego adaptera.

# prawo-polskie-v2 — Fasada Routera DR-01 do DR-16

## ⛔ STAŁE ZASADY WORKFLOW (odsyłacz — NIE duplikować)

> Sprawdzono 2026-07-06, zaktualizowano 2026-09-23: zasady zgłoszone przez
> użytkownika ("router→v3 pierwszy, przepisy przez ELI (nigdy z pamięci),
> HYBRID-VAL przed .docx, Karne: +kwalifikator") JUŻ są kanonicznie skodyfikowane w
> `prawny-router-v3/SKILL.md`, sekcja "PREFERENCJE UŻYTKOWNIKA (aktywne
> globalnie)" jako UP-1 do UP-5 — nie duplikuj ich treści tutaj.

Ten plik (`prawo-polskie-v2`) jest wywoływany DOPIERO z poziomu
`prawny-router-v3` (KROK 1B) — a więc UP-1..UP-5 są już aktywne, zanim
routing w tym pliku w ogóle się zacznie. Jedyne dodane tu wzmocnienie:
jeśli ten plik zostanie kiedykolwiek wywołany bezpośrednio, z pominięciem
routera (np. błąd w innym skillu) — potraktuj to jako naruszenie UP-1 i
najpierw wczytaj `prawny-router-v3/SKILL.md` zanim przejdziesz dalej.

## ⛔ DECYZJA ZAPISANA — ZAKRES `shared/PRAWO-HARDGATE.md` W TYM SKILLU

*(zapisana 2026-08-23g, flaga F-123 w `audyt-systemu-v4`. Powód zapisania, nie
tylko podjęcia: pomiar `grep -rl PRAWO-HARDGATE` wykazał tu ZERO odesłań i
zgłosił to jako lukę. Bez utrwalonej decyzji ten sam wynik wracałby jako nowe
zgłoszenie przy każdym kolejnym audycie — a każdy fałszywy alarm kosztuje tyle
co błąd przeoczony, patrz ZASADA 14 w `audyt-systemu-v4/SKILL.md`.)*

**Rozstrzygnięcie jest rozdzielne dla dwóch plików tego skilla:**

| Plik | Czy podlega PRAWO-HARDGATE | Uzasadnienie |
|---|---|---|
| `SKILL.md` (ten plik) | **NIE** | Czysta fasada routingu: kieruje do DR-skilla, nie twierdzi niczego o treści prawa — nie podaje przesłanek, terminów ani skutków. Bramka przed cytowaniem przepisu odpala się w DR-skillu, czyli w miejscu, w którym przepis faktycznie pada. Wpisanie jej także tutaj byłoby duplikacją bez zysku (CHECKLIST-DEDUP). |
| `ROUTING-MAP.md` | **TAK, w zakresie ograniczonym** | ⚠️ Ten plik **nie jest** czystą fasadą: nosi numery Dz.U., roczniki, pozycje i statusy tekstów jednolitych. To są weryfikowalne twierdzenia o stanie prawnym, a błędny numer propaguje się dalej w każdą sprawę, która przez ten routing przejdzie (klasa błędu F-82: numer należący do innego aktu o pokrewnym tytule). |

**Reżim dla `ROUTING-MAP.md`** — nie pełna bramka cytowania, lecz reżim mapy:
`audyt-systemu-v4` FAZA 3 (A–D) + ZASADA 8 (weryfikuj NUMER niezależnie od
zgodności NAZWY) + REGUŁA 3 HARDGATE-AUDYT (synchronizacja z lokalnymi
`MAPA-AKTOW.md` i mapą centralną Dz.U.). Numer wpisany do tego pliku bez
weryfikacji w Rzędzie 1/2 jest naruszeniem tego reżimu.

⛔ **Wyzwalacz zmiany decyzji.** Jeżeli do któregokolwiek pliku tego skilla
trafi kiedykolwiek twierdzenie o TREŚCI prawa — przesłanka, termin, właściwość
sądu, skutek procesowy, cokolwiek poza nazwą aktu, jego numerem i wskazaniem
modułu — decyzja wygasa z automatu i `view shared/PRAWO-HARDGATE.md`
staje się obowiązkowe. Zakres „tylko routing" jest warunkiem tej decyzji, nie
jej trwałą cechą.

---

## Zasada

```
prawny-router-v3
    ↓ KROK 1B (identyfikacja dziedziny)
prawo-polskie-v2 (ten plik — routing)
    ↓
DR-skill właściwy (np. dr-04-Prawo-Pracy-ZUS-Swiadczenia)
    ↓
moduł aktu prawnego (np. modules/mod-KP-prawo-pracy.md)
```

Nie ładuj wszystkich DR-skills naraz. Wczytaj JEDEN pasujący.

## Centralna mapa routingu

```
view prawo-polskie-v2/ROUTING-MAP.md
```

## Routing błyskawiczny

| Fraza / temat sprawy | DR-skill |
|---|---|
| Konstytucja, TK, Trybunał Konstytucyjny, ustrój, skarga konstytucyjna, referendum, Rzecznik Praw Obywatelskich, mandat posła, mandat senatora, stan wyjątkowy, stan wojenny, stan klęski żywiołowej, partia polityczna, ustawa o Sądzie Najwyższym, Izba Kontroli Nadzwyczajnej, KRS, Sejm, Senat, Prezydent RP, weto, podpisanie ustawy, immunitet, wotum nieufności, inicjatywa ustawodawcza, źródła prawa, hierarchia aktów prawnych, umowa międzynarodowa a ustawa, przepisy przejściowe, specustawa, niedziałanie prawa wstecz, Rada Ministrów, uchwała Sejmu, wybory do Sejmu, wybory parlamentarne, wybory prezydenckie, protest wyborczy, ustrój sądów, sędzia Sądu Najwyższego, kadencja Sejmu, kadencja, kontrasygnata, ratyfikacja, ustawa zasadnicza, zmiana konstytucji, wolności obywatelskie, prawa obywatelskie, rozporządzenie ministra, delegacja ustawowa, Trybunał Stanu, Marszałek Sejmu, Krajowa Rada Sądownictwa, proces legislacyjny, projekt ustawy, Dziennik Ustaw, vacatio legis, obywatelski projekt ustawy, komitet inicjatywy ustawodawczej, poseł, senator, wybory samorządowe a konstytucja, zgodność ustawy z Konstytucją, działa wstecz, wsteczne działanie ustawy, przegłosowali ustawę, uchwalenie ustawy, komisja sejmowa, posłowie, posłanka, rozporządzenie wykraczające poza ustawę | `dr-01-Ustroj-Konstytucyjny-i-Zrodla-Prawa` |
| Umowa, odszkodowanie, zadośćuczynienie, KC, spadek, zachowek, testament, dziedziczenie, alimenty, ojcostwo, ustalenie ojcostwa, zaprzeczenie ojcostwa, rozwód, separacja, władza rodzicielska, kontakty z dzieckiem, najem, czynsz, eksmisja, lokator, rękojmia, reklamacja, konsument, kredyt, frankowy, deweloper, wspólnota mieszkaniowa, nieruchomość, służebność, zasiedzenie, dobra osobiste, spółka, upadłość, upadłość konsumencka, windykacja, windykator, dług, zapłata, fundacja rodzinna, księga wieczysta, chwilówka, parabank, kaucja, wyprowadzka, przedawnienie roszczenia, faktura, pies, pogryzienie, zwierzę, spółka cywilna, spółka jawna, uchwała wspólników, zgromadzenie wspólników, walne zgromadzenie, uchwała zarządu, hipoteka, ubezpieczyciel, sąsiad, dział spadku, podział majątku, majątek wspólny, rozdzielność majątkowa, odwołanie darowizny, wada prawna, wada fizyczna, kontakty z wnukiem, ubezwłasnowolnienie, wspólnik, sprzeciw od nakazu zapłaty, pozew o zapłatę, umowa deweloperska, umowa najmu, umowa najmu na czas określony, umowa najmu na czas nieokreślony, użytkowanie wieczyste, współwłasność, zniesienie współwłasności, odpowiedzialność deliktowa, zwrot pożyczki, pożyczka, poręczenie, weksel, gwarancja, przewoźnik bagaż, kontakty z wnukami, zepsuł się, sklep odsyła, naprawa gwarancyjna, wadliwy towar, usługi remontowe, reklamować towar, reklamować wadliwy, wspólnota, zarząd wspólnoty, egzekucja komornicza, zajęcie rachunku, zajęcie wynagrodzenia, egzekucja z wynagrodzenia, kwota wolna od zajęcia, skarga na czynność komornika, skarga na komornika, uprowadzenie dziecka, wywiózł dziecko, wywiozła dziecko, zabrał dziecko za granicę, powództwo przeciwegzekucyjne, zwolnienie spod egzekucji | `dr-02-Prawo-Cywilne-Rodzinne-Gospodarcze` |
| Przestępstwo, KK, KPK, wykroczenie, mandat, stalking, przemoc, cyberprzestępstwo, pobicie, kradzież, oszustwo, nietrzeźwy, po alkoholu, prokurator, śledztwo, akt oskarżenia, pokrzywdzony, areszt, niebieska karta, groźby karalne, zniesławienie, znieważenie, punkty karne, prawo jazdy, oszukany, przywłaszczenie, sprzeniewierzenie, fałszerstwo, podrobienie podpisu, zatarcie skazania, Krajowy Rejestr Karny, wypadek drogowy, narkotyki, marihuana, podrobić podpis, sfałszować, pijany kierowca, KKS, karny skarbowy, groźby, grozi śmiercią, nękanie, warunkowe przedterminowe zwolnienie, odroczenie wykonania kary, dozór elektroniczny, kara pozbawienia wolności, przesłuchanie w charakterze podejrzanego, podejrzany, oskarżony, wyłudzenie, metoda na wnuczka, metoda na policjanta, przemoc domowa, znęcanie, jazda bez uprawnień, bez prawa jazdy, niealimentacja, prywatny akt oskarżenia, zawiadomienie o przestępstwie, nadużycie zaufania, korupcja, łapówka, porwanie rodzicielskie | `dr-03-Prawo-Karne-Wykroczenia-Egzekucja` |
| Wypowiedzenie, KP, umowa o pracę, stosunek pracy, pracodawca, zwolnienie dyscyplinarne, mobbing, nadgodziny, urlop, sąd pracy, wypadek przy pracy, zakaz konkurencji, umowa zlecenie, ZUS, zasiłek, L4, zwolnienie lekarskie, macierzyński, emerytura, renta, KRUS, PFRON, pomoc społeczna, dyskryminacja płacowa, choroba zawodowa, świadectwo pracy, czas pracy, 800 plus, świadczenie wychowawcze, PIP, inspekcja pracy, odprawa, bezrobotny, wynagrodzenie, pensja, staż pracy, świadczenie rehabilitacyjne, renta rodzinna, emerytura rolnicza, urlop macierzyński, urlop rodzicielski, praca w niedziele, kodeks pracy, pracownik, zwolnienie grupowe, obniżenie wynagrodzenia, wypowiedzenie zmieniające, regulamin pracy, orzecznik ZUS, niezdolność do pracy, świadczenie przedemerytalne, praca w szczególnych warunkach, umowa na czas nieokreślony, umowa na czas określony, przełożony, kierownik, rencie, decyzja o rencie, szefowa, szef w pracy | `dr-04-Prawo-Pracy-ZUS-Swiadczenia` |
| KPA, decyzja urzędu, decyzja administracyjna, SKO, WSA, NSA, bezczynność, przewlekłość, informacja publiczna, cudzoziemcy, karta pobytu, egzekucja admin., stwierdzenie nieważności decyzji, petycja, skarga kasacyjna do NSA, Samorządowe kolegium odwoławcze, postępowanie administracyjne, interes prawny, zaświadczenie, Rzecznik Praw Dziecka, zezwolenie na pracę, cudzoziemiec, ponaglenie, organ administracji, sąd administracyjny, wojewódzki sąd administracyjny, skarga kasacyjna, decyzja wojewody, wojewoda odmówił, zezwolenie na pobyt, zażalenie na postanowienie organu, wyłączenie pracownika organu, wznowienie postępowania administracyjnego, odwołanie od decyzji, kara administracyjna, administracyjna kara pieniężna, grzywna w celu przymuszenia, egzekucja administracyjna, decyzja ostateczna, organ pierwszej instancji, organ drugiej instancji, urzędnik, urząd nie odpowiada, dostęp do informacji publicznej, udostępnienie informacji publicznej, uchylenie decyzji, przywrócenie terminu do wniesienia odwołania, nie rozpatruje wniosku, rozpatrzenie wniosku, zwrot świadczenia, decyzja o zwrocie, oględziny, skarga do sądu administracyjnego, odrzucenie skargi, udostępnienie umów, udostępnienie dokumentów, starostwo, Karta Polaka, kurator oświaty, braki wniosku, uzupełnienie braków wniosku, wszczęcie postępowania administracyjnego, zawiadomienie o wszczęciu postępowania, legalizacja pobytu, skarga na bezczynność | `dr-05-Prawo-Administracyjne-Sadowoadministracyjne` |
| PIT, VAT, CIT, podatki, podatek, urząd skarbowy, kontrola podatkowa, interpretacja podatkowa, ryczałt, KAS, akcyza, cło, finanse publiczne, podatek od nieruchomości, koszty uzyskania przychodu, opłata skarbowa, PCC, KSeF, biała lista, zeznanie roczne, podatek od wygranej, zeznanie podatkowe, korekta deklaracji, deklaracja VAT, odliczenie VAT, ulga na dziecko, ulga podatkowa, podatek od spadków i darowizn, podatek od darowizny, zgłoszenie darowizny, kantor, zaległość podatkowa, zaległość w podatku, zwolnienie z podatku, PIT-38, sprzedaż mieszkania a podatek, przychód, Ordynacja podatkowa, decyzja podatkowa, ryczałt od najmu, kontrola celno-skarbowa, rozliczenie najmu, wynajem krótkoterminowy, koszty w działalności, darowizna od rodziny, otrzymałem darowiznę, darowizna od rodziców, biuro rachunkowe | `dr-06-Podatki-Finanse-Publiczne-AML` |
| Przetarg, KIO, PZP, zamówienie, fundusze UE, notariat, zamówienie publiczne, partnerstwo publiczno-prywatne, PPP, akt notarialny, zamawiający, wykonawca w przetargu, najkorzystniejsza oferta, wadium, tryb podstawowy, koncesja na roboty, NIK, Najwyższa Izba Kontroli, RIO, regionalna izba obrachunkowa, dyscyplina finansów publicznych, dotacja unijna, dofinansowanie z funduszy europejskich, oferta przetargowa, SWZ, specyfikacja warunków zamówienia, odwołanie do KIO, zamówienie z wolnej ręki, podwykonawca, korekta finansowa, instytucja zarządzająca, beneficjent, wniosek o płatność, waloryzacja wynagrodzenia, konsorcjum, JEDZ, samooczyszczenie, rażąco niska cena, próg bagatelności, próg unijny, unieważnienie postępowania o udzielenie zamówienia, wykluczenie wykonawcy, odrzucenie oferty, termin realizacji umowy, realizacja zamówienia | `dr-07-Zamowienia-Publiczne-Fundusze-UE` |
| Gmina, powiat, JST, MPZP, miejscowy plan, warunki zabudowy, uchwała, radny, wójt, burmistrz, prawo lokalne, samorząd, referendum lokalne, odwołanie burmistrza, odwołanie wójta, strefa płatnego parkowania, rada gminy, renta planistyczna, odszkodowanie planistyczne, plan miejscowy, sołectwo, sołtys, budżet obywatelski, mienie komunalne, akt prawa miejscowego, dziennik urzędowy województwa, prezydent miasta, starosta, sejmik, uchwała krajobrazowa, skarga na wójta, skarga na działalność wójta, droga powiatowa, droga gminna, obywatelska inicjatywa uchwałodawcza, dodatek mieszkaniowy, regulamin utrzymania czystości, opłata za śmieci, opłata za odpady, nadzór wojewody, rozstrzygnięcie nadzorcze, nieważność uchwały, skarga na uchwałę, odśnieżanie chodnika, rada miasta, mieszkańcy gminy, odwołać burmistrza, odwołać wójta | `dr-08-Samorzad-Terytorialny-Prawo-Lokalne` |
| Budowa, pozwolenie na budowę, samowola, PINB, nadzór budowlany, środowisko, odpady, energia, fotowoltaika, transport, szkody łowieckie, łowiectwo, obwód łowiecki, wywłaszczenie, ZRID, wycinka drzew, farma wiatrowa, decyzja środowiskowa, charakterystyka energetyczna, system kaucyjny, pozwolenie na użytkowanie, odbiór budynku, usunięcie drzewa, URE, taryfa za prąd, polowanie, myśliwy, koło łowieckie, droga publiczna, pozwolenie wodnoprawne, studnia, prawo geologiczne, kopalina, konserwator zabytków, zabytek, geodeta, rozgraniczenie, Natura 2000, BDO, nadzór budowlany, prawo budowlane, zgłoszenie budowy, wiata, altana, zmiana sposobu użytkowania, odległość od granicy działki, zrzut ścieków, zanieczyszczenie rzeki, emisja, pompa ciepła, przyłączenie do sieci, operator sieci, sieć gazowa, OZE, elektrownia słoneczna, mikroinstalacja, przewóz osób, licencja na przewóz, taksówka, transport drogowy, las, wycinka lasu, linia energetyczna, służebność przesyłu, ferma, uciążliwość zapachowa, budowa domu letniskowego, inspektor nadzoru budowlanego, wstrzymanie budowy, legalizacja samowoli, nakaz rozbiórki, warunki techniczne, przewoźnik towar, list przewozowy, prawo przewozowe, przerwa w dostawie prądu, farma fotowoltaiczna, kamieniołom, wibracje, biogazownia, wyciął drzewa, drzewa na granicy, zakład przemysłowy, zanieczyszcza, linia wysokiego napięcia, koncesja geologiczna, wydobywanie piasku, panele fotowoltaiczne, wycięcie drzewa, wyciąłem drzewo, wyciąłem dąb | `dr-09-Budownictwo-Srodowisko-Energia-Transport` |
| Lekarz, szpital, pacjent, błąd medyczny, NFZ, apteka, farmacja, żywność, rolnictwo, rolnik, szkoła, uczeń, sport, impreza masowa, sanepid, szpital psychiatryczny, suplement diety, GIS, matura, egzamin maturalny, uczelnia, student, hodowla, weterynarz, wyroby medyczne, pielęgniarka, położna, telemedycyna, e-recepta, recepta, dokumentacja medyczna, lekarz rodzinny, przyjęcie do szpitala, skierowanie do szpitala, refundacja leczenia, produkt leczniczy, działanie niepożądane leku, rolniczy handel detaliczny, inspekcja weterynaryjna, eksperyment medyczny, badanie kliniczne, druga opinia lekarska, zakażenie szpitalne, Rzecznik Praw Pacjenta, prawa pacjenta, zdarzenie medyczne, ARiMR, dopłaty bezpośrednie, susza, gospodarstwo rolne, praktyka lekarska, działalność lecznicza, leczenie, przychodnia, zapisać do lekarza, agencja rolna, dopłaty do hektara, dopłaty rolnicze, Karta Nauczyciela, awans nauczyciela, nauczyciel w szkole, suplementy, nauczyciel ucznia, pielęgniarka środowiskowa | `dr-10-Zdrowie-Farmacja-Zywnosc-Rolnictwo` |
| RODO, dane osobowe, ochrona danych, przetwarzanie danych, UODO, IOD, inspektor ochrony danych, wyciek danych, naruszenie ochrony danych, rejestr czynności przetwarzania, powierzenie przetwarzania, klauzula informacyjna, monitoring wizyjny, nagrywanie rozmów, wizerunek, cookies, spam, newsletter, profilowanie, KSC, NIS2, AI Act, cyberbezpieczeństwo, IP, prawo autorskie, znak towarowy, patent, wizerunek dziecka, publikacja wizerunku, ujawnienie danych, udostępnienie danych, lista dłużników z nazwiskami, podpis kwalifikowany, podpis zaufany, Digital Services Act, DSA, platforma internetowa, dostęp do danych, usunięcie danych, monitoruje, kamera, nagrywa, telemarketing, plagiat, skopiowany artykuł, autor utworu, CSIRT, incydent, atak hakerski, kryptowaluty, MiCA, dane klientów, baza klientów, hakerzy, ransomware, zaszyfrowali dane, włamanie do systemu, wzór przemysłowy, nazwa domeny, prawa do utworu, utwór muzyczny, nagranie w internecie, zdjęcie w internecie, prywatne maile, sklep internetowy dane, strona internetowa skopiowana, ochrona danych osobowych, zdjęcia uczniów, publikuje zdjęcia, nazwa marki, nazwy marki, akt o sztucznej inteligencji, AI Act, licencja na oprogramowanie, prawa do programu komputerowego, zablokowane konto w serwisie, usunięty post, skopiował kurs online, oprogramowanie sztuczna inteligencja, opublikował nagranie, przejęcie konta, przejął konto, konto na Facebooku, fałszywy profil, podszywa się, chatbot musi informować, zbiera lokalizację, przekazał moje dane, wysłał moje dane, udostępnił moje dane, sprostowanie danych, zdjęcie bez zgody, zdjęcie użyte bez zgody | `dr-11-Cyfrowe-Cyber-AI-Dane-IP` |
| Sąd, prokuratura, adwokat, radca, notariusz, koszty sądowe, opłata sądowa, biegły sądowy, mediacja, taksa notarialna, izba adwokacka, pełnomocnik z urzędu, opłata od pozwu, sąd polubowny, arbitraż, zapis na sąd polubowny, opłata egzekucyjna, komornik, komornik sądowy, wybór komornika, kurator sądowy, referendarz, asesor sądowy, rzecznik patentowy, doradca restrukturyzacyjny, odpowiedzialność dyscyplinarna, sędzia, koszty zastępstwa procesowego, radca prawny, ławnik, aplikacja adwokacka, aplikacja radcowska, skarga na sędziego, prezes sądu, wyłączenie sędziego, opłata od apelacji, zwolnienie od kosztów sądowych, tajemnica adwokacka, tajemnica zawodowa, postępowanie dyscyplinarne, adwokat z urzędu, nie wyznaczył rozprawy, wyznaczenie rozprawy, pełnomocnik nie informuje, mediator, biegły nie stawił się, zaginęły akta, aplikant adwokacki, aplikant radcowski, aplikacja adwokacka, aplikacja radcowska, ochrona adwokata, ochrona radcy prawnego, adwokat funkcjonariusz publiczny, radca prawny funkcjonariusz publiczny, adwokaci funkcjonariusze publiczni, nowelizacja prawa o adwokaturze, kancelaria adwokacka, tytuł adwokata, koszty pozwu | `dr-12-Sadownictwo-Prokuratura-Zawody-Prawnicze` |
| Policja, ABW, służby specjalne, informacje niejawne, wojsko, obrona, Straż Graniczna, pozwolenie na broń, poświadczenie bezpieczeństwa, retencja danych, CBA, Centralne Biuro Antykorupcyjne, straż pożarna, OSP, strażak, legitymowanie, przeszukanie, paralizator, Żandarmeria, ćwiczenia wojskowe, kwalifikacja wojskowa, karta mobilizacyjna, mobilizacja, rezerwa, żołnierz, żołnierz zawodowy, Wojska Obrony Terytorialnej, WOT, służba wojskowa, koncesja MSWiA, ochrona osób i mienia, agencja ochrony, pracownik ochrony, cofnięcie poświadczenia bezpieczeństwa, podsłuch, kontrola operacyjna, IPN, funkcjonariusz, interwencja policji, skarga na policjanta, postępowanie dyscyplinarne funkcjonariusza, dostęp służb do danych, billingi, dane telekomunikacyjne | `dr-13-Sluzby-Bezpieczenstwo-Informacje-Niejawne` |
| Prawo UE, TSUE, EKPC, ETPC, prawo międzynarodowe, prawo prywatne międzynarodowe, prawo właściwe, europejski tytuł egzekucyjny, egzekucja za granicą, konwencja genewska, uchodźca, Karta praw podstawowych, pytanie prejudycjalne, Europejski Trybunał Praw Człowieka, rzetelny proces, Konwencja, jurysdykcja, różnych narodowości, zagraniczny wyrok, europejski nakaz zapłaty, konwencja wiedeńska, immunitet dyplomatyczny, dyplomata, mały ruch graniczny, swoboda przepływu, dyrektywa, TFUE, ONZ, Pakt Praw, arbitraż inwestycyjny, BIT, NATO, za granicą, Unia Europejska, Komisja Europejska, skarga do Komisji Europejskiej, europejski nakaz aresztowania, ENA, ekstradycja, rozporządzenie spadkowe, spadek za granicą, emerytura z zagranicy, koordynacja zabezpieczenia społecznego, formularz A1, uprowadzenie dziecka za granicę, konwencja haska, uznanie orzeczenia zagranicznego, wykonanie wyroku zagranicznego, status uchodźcy, azyl, ochrona czasowa, opóźniony lot, odwołany lot, pasażer linii lotniczej, procedura OSS, sąd zagraniczny, sankcje UE, sankcje unijne, obejście sankcji, towary podwójnego zastosowania, uznanie orzeczenia, uznać orzeczenie, rozwód za granicą | `dr-14-Prawo-UE-Miedzynarodowe-Prawa-Czlowieka` |
| Compliance, ISO, AML instytucjonalny, zamówienia obronne, sygnaliści, sygnalista, ISO 27001, ISO 37001, ISO 37301, ISO 42001, ustawa antykorupcyjna, DORA, ryzyko ICT, kodeks etyki, konflikt interesów, audyt wewnętrzny, whistleblowing, ład korporacyjny, dobre praktyki, nadużycia, szkolenia compliance, lista sankcyjna, sankcje, prezenty od dostawców, kodeks postępowania etycznego, system zarządzania zgodnością, system zarządzania bezpieczeństwem informacji, kontrola wewnętrzna, system kontroli wewnętrznej, zarządzanie ryzykiem, komitet audytu, due diligence, łańcuch dostaw, ESG, CSRD, raport zrównoważonego rozwoju, kanał zgłoszeń, zgłoszenia wewnętrzne, procedura zgłoszeń, polityka antykorupcyjna, rejestr konfliktów interesów, certyfikacja ISO, audyt zgodności, dochodzenie wewnętrzne, polityka bezpieczeństwa informacji, liście sankcyjnej, polityce antykorupcyjnej, audytor, audyt, mapa ryzyk, ryzyko braku zgodności | `dr-15-Compliance-ISO-Governance-Audyt` |
| Pismo procesowe, strategia, narzędzia, kalkulatory, e-doręczenia, portal informacyjny, odtworzenie akt, kalkulator, odsetki ustawowe, sprostowanie prasowe, prawo prasowe, wzór pisma, paszport, prasa, redakcja, kompletność pozwu, zameldowanie, meldunek, obywatelstwo, arbitraż sportowy, prawo do sądu, strategia procesowa, archiwizacja dokumentacji, plan dowodowy, wnioski dowodowe, siła dowodów, orzeczenia Sądu Najwyższego, weryfikacja sygnatury, sygnatura wyroku, podważyć opinię biegłego, argumenty na rozprawę, autoryzacja wywiadu, dziennikarz, sprostowanie artykułu, opublikować sprostowanie, nieprawdziwy artykuł, gazeta, wymeldowanie, przegląd orzecznictwa, zestawienie orzecznictwa, orzecznictwo SN, orzecznictwo Sądu Najwyższego, plan przesłuchania | `dr-16-Pisma-Strategia-Dowody-Orzecznictwo` |

## Jak wywołać DR-skill

```
view dr-[XX]-[Nazwa]/SKILL.md
# następnie:
view dr-[XX]-[Nazwa]/modules/mod-[akt].md
```

## Weryfikacja
- Teksty aktów: kanon E-1…E-5 (`shared/HIERARCHIA-ZRODEL.md`) — E-1 api.sejm.gov.pl/eli | eli.gov.pl; E-2 isap.sejm.gov.pl jako adres dla człowieka; E-3 LEX/Legalis; E-4 ArsLege
- Prawo UE: eur-lex.europa.eu
- Orzeczenia: orzeczenia.ms.gov.pl | sn.pl | nsa.gov.pl

---

## Protokół integracji DR → prawo-polskie → audyt

### Przepływ danych (pull)

```
DR-XX/MAPA-AKTOW.md         ← źródło prawdy dla danej dziedziny
        ↓  pull przy audycie DZU
ROUTING-MAP.md               ← centralna mapa wszystkich 16 DR
        ↓  porównanie (FAZA 3 audytu)
audyt-systemu-v4/references/mapa_dzu_*.md  ← rejestr Dz.U.
```

### Jak zaktualizować po zmianie w DR-skill

1. Wczytaj zmieniony `dr-XX/MAPA-AKTOW.md`
2. Porównaj z odpowiednią sekcją `ROUTING-MAP.md`
3. Uzupełnij rozbieżności — nowe akty, zmienione t.j., nowe statusy
4. Zaktualizuj liczniki w tabeli TABELA STATUSU
5. Wpis z vacatio legis → dodaj do sekcji MONITORING na końcu ROUTING-MAP.md
6. Wywołaj `audyt-systemu-v4` TRYB DZU — zweryfikuje `mapa_dzu_*.md`

### Akty oczekujące (MONITORING) — reguły

| Sytuacja | Akcja |
|---|---|
| Nowy Dz.U. z vacatio legis znaleziony podczas weryfikacji w ELI (RZĄD 1) | Dodaj `⏳ OCZEKUJE` do tabeli DR i do sekcji MONITORING |
| Data wejścia w życie minęła | Zmień `⏳→✅ OK`, usuń z MONITORING, zaktualizuj mapa_dzu |
| Akt uchylony przed wejściem | Status `❌`, usuń z MONITORING, odnotuj w AUDIT-JOURNAL |
| Wejście w ciągu 90 dni od daty audytu | Zmień na `⚡ WCHODZI` — priorytetowa aktualizacja modułu |

*Numer wersji: wyłącznie pole `version:` we frontmatterze — decyzja generalna
F-102(C), dwa źródła prawdy o wersji zawsze się rozjeżdżają (ta stopka niosła
„5.2" przy `version: 6.1`, rozjazd o dziewięć wersji, usunięty 2026-08-23g).*

*Ostatnia zmiana treści: 2026-08-23g — zapisana decyzja o zakresie
`shared/PRAWO-HARDGATE.md` w tym skillu (F-123). Wcześniej: 2026-07-02,
WARN-28 zamknięty — ABW/AW to nowy t.j. tej samej ustawy z 2002 r., nie
reforma; sync ROUTING-MAP.*

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** `prawny-router-v3` (krok kwalifikacji)
- **Wynik zapisz w:** wskazanie modułu DR (w `analiza/_brief.md`) (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `dr-02-prawo-cywilne-rodzinne-gospodarcze`, `dr-03-prawo-karne-wykroczenia-egzekucja`, `dr-05-prawo-administracyjne-sadowoadministracyjne`
- **Basic Memory (`legal`):** czytaj teczkę sprawy (`build_context`) i notatki wiki po sygnaturze i nazwiskach; zapisz stan sprawy i terminy w teczce, nowe fakty z akt zgłoś do ingestu (protokół: `shared/BASIC-MEMORY.md`)
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
