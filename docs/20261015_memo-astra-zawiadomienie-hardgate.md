# Memo dla Astry: refaktor `zawiadomienie-o-przestepstwie`

## Cel

Wzmocnić skill tak, aby żaden korpus ani skill od pism procesowych nie degradował relacji pokrzywdzonego przez wymaganie uprzedniego dowodu dla każdego twierdzenia. W tym rodzaju pisma materiałem wejściowym i podstawą narracji jest możliwie pełny, dokładny, wierny opis przeżyć, spostrzeżeń, skutków i kontekstu podany w dobrej wierze. Dowody, świadkowie i ślady mają pomagać organowi zaplanować czynności, lecz ich brak nie usuwa epizodu ani krzywdy z zawiadomienia.

To jest dziennik inkrementalny. Każda pozycja niżej została dopisana po przeczytaniu wskazanego źródła; wnioski końcowe należy wyprowadzić dopiero po zamknięciu całej listy.

## Stan wejściowy skilla (przeczytany przed researchem)

Źródło: `plugins/grounding-prawo/skills/zawiadomienie-o-przestepstwie/SKILL.md` (wersja 0.3) oraz jego `references/wywiad.md` i `references/hardgate-spojnosc.md`.

- Skill trafnie ustanawia K1–K4: relacja użytkownika jest przyjmowana jako prawdziwa na potrzeby redakcji; brak dowodu nie usuwa krzywdy; zawiadomienie nie jest aktem oskarżenia; model nie dopisuje faktów.
- Istniejący wyjątek od `CLAIM-VALIDATION` jest opisowy, ale nie ma jeszcze nadrzędnej, łatwo testowalnej bramki kolizyjnej, która zatrzyma każdy później uruchomiony moduł dowodowy.
- Obecny K5 czyni spójność z wcześniejszymi relacjami warunkiem wersji do złożenia. To ryzyko: pamięć po traumie może być fragmentaryczna, nowe szczegóły są naturalne, a nierozstrzygnięta rozbieżność nie powinna automatycznie blokować zawiadomienia. Potrzebna jest bramka integralności i jawnego oznaczenia perspektywy, nie bramka „zgodności za wszelką cenę”.
- F1–F3 mają właściwy kierunek, lecz trzeba wyżej postawić obowiązek wielorundowego wywiadu rozszerzającego: pytania mają wydobywać sensorykę, słowa, gesty, sekwencję, relację sił, powtarzalność, kontrolę, skutki i zachowania po zdarzeniu oraz fakty mogące otworzyć alternatywne lub kumulatywne kwalifikacje.
- Należy rozdzielić dwa hardgate’y: (1) nadrzędny `NARRATIVE-INTEGRITY / COMPLETENESS`, blokujący redakcję finalną, jeśli istotne luki nie zostały dopytane albo świadomie oznaczone; (2) pomocniczy audyt spójności, który ujawnia rozbieżności i prosi o wyjaśnienie, ale nie kasuje relacji i co do zasady nie blokuje złożenia.

## Nauki z `skill-creator`

- Hardgate ma chronić konkretny, wykazany invariant, a nie mnożyć ogólne reguły. Najważniejszy invariant: „brak zewnętrznego dowodu nigdy nie jest kryterium usunięcia relacjonowanego epizodu lub skutku”.
- Regułę kolizyjną trzeba umieścić w `SKILL.md`, bo jest zawsze potrzebna; rozbudowane drzewa pytań, katalogi okoliczności i przykłady powinny pozostać w `references/` (progressive disclosure).
- Opis skilla powinien pozostać dyskryminujący i jasno odróżnić zawiadomienie od późniejszych pism w toczącym się postępowaniu.
- Walidacja powinna badać zachowanie i invarianty na realistycznych scenariuszach, nie tylko obecność fraz. Evale muszą obejmować konflikt ze skillem dowodowym i przypadek braku dokumentów.

## Nauki z `plugin-creator`

- Refaktor dotyczy istniejącego skilla wewnątrz istniejącego pluginu; nie należy scaffoldować nowego pluginu ani ręcznie zmieniać marketplace.
- Po zmianie trzeba zwalidować zarówno folder skilla (`quick_validate.py`), jak i cały plugin (`validate_plugin.py`), a ewentualne odświeżenie instalacji wykonać mechanizmem cachebuster/update, nie ręczną edycją konfiguracji marketplace.
- Należy zachować istniejącą strukturę i manifest pluginu; memo nie rekomenduje zmian manifestu bez realnej potrzeby.

## Dziennik źródeł i nauk

### Wzorce wywiadowe dostępne lokalnie

Przeczytano `references/wywiad.md` obecnego skilla i sprawdzono lokalne kandydaty `interview-me` / `about-me`. Repo zawiera puste katalogi `cold-start-interview`, lecz nie zawiera treści skilla `interview-me` ani `about-me`, z której dałoby się rzetelnie wyprowadzić dalsze reguły.

- Zachować dobry wzorzec: najpierw swobodna relacja, potem krótkie serie 3–6 pytań wokół jednego epizodu, na końcu pytanie otwarte o pominięte szczegóły.
- Wzmocnić pytania rozszerzające przez pętlę zależną od odpowiedzi: każda nowa osoba, miejsce, wypowiedź, czynność, skutek, wcześniejszy podobny epizod lub źródło wiedzy otwiera własną gałąź pytań „kto/co dokładnie/kiedy/gdzie/jak długo/co było przed/co potem/jaki skutek/skąd to wiesz”.
- Nie ustalać sztywnego maksimum rund. Kryterium zakończenia powinno być treściowe: użytkownik potwierdził, że dla każdego znanego epizodu omówiono przebieg, kontekst, skutki, wzorzec, relację sił i potencjalne kategorie krzywd; luki są jawne, a nie przemilczane.
- Technika zmiany perspektywy nie może nakłaniać do zgadywania cudzych doznań. Wolno pytać wyłącznie o to, co użytkownik sam widział lub co dana osoba mu przekazała, z oznaczeniem źródła.
- Pytania o ślady i świadków należy zachować, ale przenieść semantycznie z „walidacji tezy” do „wskazówek dla organu i ochrony szybko zanikających źródeł”. Brak odpowiedzi nie obniża statusu relacji.

### 1. Wielkopolski Urząd Wojewódzki — wzór zawiadomienia (PDF)

Źródło: https://www.poznan.uw.gov.pl/system/files/zalaczniki/zawiadomienie_przestepstwo_0.pdf (3 strony, odczyt 2026-10-15).

- Instytucjonalny wzór wprost każe podać **dokładny opis sytuacji osoby/rodziny**, osoby doznającej przemocy i osoby ją stosującej, sytuacje oraz czasookres. Wspiera to hardgate kompletności narracji, nie hardgate dowodowy.
- Katalog pytań powinien aktywnie obejmować odrębne postacie krzywdy: obrażenia ciała, cierpienia psychiczne, niezaspokajanie podstawowych potrzeb, zastraszanie oraz przymuszanie seksualne. To nie mogą być tylko przykłady schowane w mapie — model powinien dopytać o każdą kategorię adekwatną do relacji.
- Wzór uwidacznia czynniki kontekstowe ważne dla kwalifikacji i obrazu czynu: długotrwałość/powtarzalność, trwanie zachowania nadal, relacja rodzinna, małoletnie dzieci i ich obecność, zależność ekonomiczna, uzależnienie sprawcy, wcześniejsze próby zawiadomienia oraz groźby powstrzymujące zgłoszenie.
- Sekcja „Dowód” pojawia się dopiero po opisie i zawiera przykładowych świadków oraz zaświadczenie lekarskie. Dla refaktoru: dowody mają być osobną warstwą po relacji; brak pozycji w tej warstwie nigdy nie powoduje usunięcia opisu.
- Wzór używa kwalifikacji już w formule otwierającej, ale jest to przykład dla znęcania. Skill nie powinien mechanicznie wymuszać pewnej kwalifikacji od użytkownika; powinien wydobyć fakty i po weryfikacji prawa przedstawić możliwe przepisy bez zawężania relacji do jednego artykułu.

### 2. Kancelaria Słupińska — „Zawiadomienie o możliwości popełnienia przestępstwa”

Źródło: https://slupinska.eu/blog/zawiadomienie-o-mozliwosci-popelnienia-przestepstwa/ (publ. 2021, aktualizacja oznaczona 2023; odczyt 2026-10-15).

- Brak ustawowo szczególnej formy pisma wzmacnia zasadę, by nie podporządkowywać relacji formalistycznemu pipeline’owi pism procesowych. Rdzeń ma jasno odpowiadać: kto, co, kiedy, gdzie i w jakich okolicznościach zrobił.
- Wywiad powinien wydobywać rodzaj i rozmiar szkody/krzywdy oraz obrażenia, a nie tylko sam czyn. Dla szkody majątkowej trzeba pytać o przedmiot, wartość, sposób wyliczenia i dalsze koszty; dla zdrowia — lokalizację, charakter, czas trwania i następstwa.
- Świadkowie, dokumentacja i inne dowody są informacjami pomocniczymi, szczególnie gdy grozi ich utrata lub zniekształcenie. Refaktor powinien dodać triage pilności (monitoring nadpisywany, wiadomości znikające, świeże obrażenia), ale nigdy nie uzależniać ujęcia czynu od zabezpieczenia śladu.
- Artykuł potwierdza rozdział ról: po zawiadomieniu organ może prowadzić czynności sprawdzające, uzupełniać dane, przesłuchiwać i dopiero dalej gromadzić materiał dowodowy. Model ma przygotować „mapę tropów dla organu”, nie przeprowadzać prywatne postępowanie dowodowe jako warunek pisma.
- Pytania o miejsce powinny obejmować nie tylko miejsce działania sprawcy, ale też miejsce zaniechania oraz miejsce, gdzie nastąpił albo miał nastąpić skutek — może to ujawnić właściwość i dodatkowe epizody.
- Artykuł ostrzega o art. 234 i 238 k.k.; użyteczna nauka to precyzyjne oddzielanie obserwacji, informacji cudzej i wniosku oraz zakaz dopisywania. Nie należy jednak przenosić odstraszającego tonu ani reguły „nie składaj pod wpływem emocji”: emocje i doświadczenie krzywdy są pełnoprawną treścią, a odpowiedzialność wymaga świadomego fałszu, nie samego braku dowodu.
- Dane adresowe i kontaktowe wymagają uważnego potraktowania z uwagi na bezpieczeństwo. Wywiad powinien zapytać o aktualny bezpieczny adres do korespondencji i ryzyko ujawnienia danych, zamiast automatycznie kopiować adres zamieszkania do narracji.

### 3. Sprawy-karne.biz.pl — kompletny wzór i instrukcja (2024)

Źródło: https://sprawy-karne.biz.pl/zawiadomienie-o-mozliwosci-popelnienia-przestepstwa-wzor/ (odczyt 2026-10-15).

- Źródło trafnie stwierdza, że zawiadamiający nie musi znać kwalifikacji prawnej; kluczowy jest dokładny opis. Skill powinien sam wykonywać „issue spotting” po zebraniu relacji i wracać z pytaniami o brakujące cechy czynów, zamiast oczekiwać nazwania przestępstwa przez użytkownika.
- Warto przejąć metaforę operacyjną „instrukcja obsługi sprawy”: czytelnik nie zna historii, więc z pisma musi dać się odtworzyć sekwencję, uczestników, lokalizacje, wypowiedzi, działania, następstwa i tropy do pilnego zabezpieczenia.
- Przykład rozboju pokazuje wagę mikro-sekwencji: żądanie pieniędzy → odmowa → uderzenie i upadek → kopnięcia → zabranie portfela → kierunek ucieczki. Pytania powinny rozbijać etykietę użytkownika („napadł mnie”) na kolejność zachowań, bo relacje między przemocą, celem i zaborem mogą zmieniać kwalifikację.
- Trzeba pytać o osoby obecne nie tylko jako „świadków czynu”, lecz także o osoby, które widziały stan bezpośrednio po nim albo udzieliły pomocy. Podobnie skutki zawodowe (np. niemożność pracy przez okres leczenia) są częścią krzywdy.
- Szczególnie użyteczny jest sygnał czasu zaniku: monitoring bywa nadpisywany po kilku tygodniach, świadkowie zapominają. Dodać do wywiadu osobną flagę `[PILNE ZABEZPIECZENIE]` uruchamiającą krótką informację praktyczną, bez blokowania narracji.
- Źródło miejscami przeciwstawia „emocje” faktom. Tego nie przejmować literalnie: emocje, strach i cierpienie psychiczne mogą być skutkiem czynu i elementem znamion. Odfiltrować należy obraźliwe etykiety oraz ogólne oceny charakteru sprawcy, ale zachować opis doznań, reakcji i wpływu na życie.
- Lista rozbudowanych wniosków dowodowych jest użyteczna opcjonalnie w sprawach pilnych, lecz nie powinna przekształcić skilla w tor pisma procesowego ani uczynić ich obligatoryjnymi.

### 4. Adwokat Murdza — „Zawiadomienie o popełnieniu przestępstwa”

Źródło: https://www.adwokatmurdza.pl/zawiadomienie-o-popelnieniu-przestepstwa/ (odczyt 2026-10-15).

- Najbardziej wartościowa formuła intake’u: **kto, co, kiedy, gdzie, jak i skąd to wiadomo**. „Skąd wiadomo” służy oznaczeniu perspektywy (własne spostrzeżenie / cudza wypowiedź / wniosek), nie warunkowi dopuszczenia twierdzenia.
- Źródło wprost odpowiada, że twarde dowody nie są wymagane, a zebranie i weryfikacja dowodów procesowych należy do organów ścigania. To powinno zostać zacytowane sensowo w nadrzędnym hardgate kolizyjnym skilla.
- Rozróżnienie informacji pewnej i przypuszczenia chroni wierność relacji. Model nie powinien jednak automatycznie przepisywać bezpośredniej obserwacji jako „podejrzenia” tylko dlatego, że brak dokumentu; stopień pewności wynika z pamięci i źródła wiedzy użytkownika.
- W sprawach cyfrowych, gospodarczych, oszustwach i przywłaszczeniach ważne jest szybkie pytanie o dane kont, profile, rachunki, historię transakcji i miejsca przechowywania logów. Są to tropy o ograniczonej retencji.
- Źródło potwierdza dobrą wiarę: art. 238 k.k. dotyczy świadomego fałszu, nie pomyłki ani błędnej oceny prawnej. Hardgate ma blokować dopisywanie i świadome przedstawianie fikcji, a nie szczere twierdzenia bez zewnętrznego potwierdzenia.
- Teza autora o stylu „pozbawionym zbędnych emocji” wymaga korekty w skillu: usuwać retoryczne obelgi, ale zachowywać przeżycia i skutki emocjonalne, jeżeli opisują krzywdę, uzasadnioną obawę, długotrwałość albo wpływ czynu.

### 5. Sprawy-karne.biz.pl — kompensata dla pokrzywdzonego

Źródło: https://sprawy-karne.biz.pl/kompensata/ (odczyt 2026-10-15).

- Wywiad o skutkach powinien być przyszłościowo użyteczny: pytać o czas naruszenia czynności narządu/rozstroju zdrowia, leczenie i rehabilitację, utracone zarobki lub środki utrzymania, wydatki, dojazdy oraz — przy śmierci — koszty pogrzebu i osoby najbliższe.
- Nie wolno redukować „krzywdy” do kosztów kwalifikowanych do państwowej kompensaty. Ból, trauma i cierpienie niematerialne pozostają ważnym opisem skutków, choć dane świadczenie ich nie pokrywa.
- Pytanie o to, kiedy ujawnił się skutek, może mieć znaczenie niezależnie od daty samego czynu; model powinien zbierać obie osie czasu.
- Stopień i czas obrażeń mogą wpływać na kwalifikację oraz dalsze środki. Model ma dokładnie wypytać o objawy i przebieg, ale nie diagnozować ani samodzielnie przesądzać progu medyczno-prawnego.
- Materiał pokazuje dalszą ścieżkę pomocy jako powód zbierania szczegółów, nie jako wymóg wiarygodności zawiadomienia.

### 6. Sprawy-karne.biz.pl — jak udowodnić przywłaszczenie mienia

Źródło: https://sprawy-karne.biz.pl/jak-udowodnic-przywlaszczenie-mienia/ (odczyt 2026-10-15).

- To dobry przykład pytań rozszerzających kwalifikację: jak rzecz znalazła się u sprawcy (zabór czy legalne przekazanie), na jakiej podstawie i do kiedy, kiedy zażądano zwrotu, co odpowiedział, co zrobił z rzeczą, czy ją sprzedał/zastawił/przerobił, czy zerwał kontakt. Etykieta użytkownika „ukradł” nie może zamknąć dalszego wywiadu.
- Dla rozróżnienia oszustwa i przywłaszczenia ważna jest oś zamiaru: jakie zachowania lub wypowiedzi wystąpiły **przed przekazaniem**, a jakie dopiero **po nim**. Model pyta o obserwowalne fakty, nie o pewność co do „tego, co siedziało w głowie”.
- Trzeba pytać o charakter rzeczy powierzonej, numery seryjne, wartość, własność, warunki przekazania i termin zwrotu oraz o czynności rozporządzające jak właściciel. Każda odpowiedź może otworzyć wątki rzeczy powierzonej, paserstwa lub oszustwa.
- Artykuł mocno dowodocentryczny („musisz udowodnić”) jest dokładnie tym, czego hardgate ma nie przenosić do kryterium redakcji. Nawet bez umowy, wezwania czy korespondencji opis przekazania i odmowy pozostaje w zawiadomieniu; braki tworzą listę tropów/luk, nie cenzurę narracji.
- Dodać pytanie o ryzyko zbycia/ukrycia rzeczy i zanikające oferty internetowe; jeśli występuje, oznaczyć pilność zabezpieczenia.

### 7. Sprawy-karne.biz.pl — Niebieska Karta

Źródło: https://sprawy-karne.biz.pl/niebieska-karta/ (odczyt 2026-10-15).

- Przemoc domowa wymaga lejka co najmniej czterech kategorii: fizycznej, psychicznej (wyzwiska, poniżanie, izolowanie), ekonomicznej (wydzielanie pieniędzy, zakaz pracy) i seksualnej. Nie wolno zawężać rozmowy do uderzeń.
- Pytania muszą wydobyć systemowość: powtarzalność, eskalację, groźby, uzależnienia, obecność dzieci, interwencje, widoczne ślady, ocenę ryzyka, nakazy/zakazy, osobne rozmowy z instytucjami i aktualne bezpieczeństwo.
- Istotne źródła informacji to nie tylko Policja: MOPS/GOPS, zespół interdyscyplinarny, komisja rozwiązywania problemów alkoholowych, szkoła/oświata i ochrona zdrowia. Model powinien pytać, kto z tych podmiotów widział skutki lub sporządzał notatki.
- Procedura NK i postępowanie karne są odrębne; zamknięcie lub brak NK nie przeczy relacji i nie blokuje zawiadomienia. Akta NK są możliwym źródłem szczegółów, nie arbitrem prawdy.
- Przy aktualnym zagrożeniu model powinien przerwać zwykły rytm redakcyjny krótkim triage bezpieczeństwa i wskazać pilny kontakt z numerem alarmowym/instytucją pomocową; następnie wrócić do pracy nad relacją, jeśli użytkownik może bezpiecznie kontynuować.

### 8. Sprawy-karne.biz.pl — organy postępowania przygotowawczego

Źródło: https://sprawy-karne.biz.pl/postepowanie-przygotowawcze-organy/ (odczyt 2026-10-15).

- Przekazanie sprawy z prokuratury Policji nie oznacza degradacji ani podważenia relacji. Informacja praktyczna skilla powinna uprzedzać ten typ niepokoju.
- Organ po zawiadomieniu sam weryfikuje podejrzenie, przesłuchuje świadków i zabezpiecza monitoring, dokumenty oraz dane telekomunikacyjne. To kolejny argument za oddzieleniem narracji od dowodowego progu dopuszczenia.
- Osobny bank pytań jest potrzebny, gdy sprawcą może być funkcjonariusz publiczny (policjant, prokurator, sędzia) albo gdy czyn dotyczy służb; może to wpływać na tryb i organ prowadzący.
- Pierwsze wypowiedzi do protokołu są później porównywane. Model powinien pomagać użytkownikowi przeczytać protokół przed podpisem i od razu zgłaszać skróty/błędy, lecz nie może uznawać później przypomnianego szczegółu za niewiarygodny tylko dlatego, że brak go w pierwszym protokole.
- Po redakcji warto podać, że Policja może prowadzić dochodzenie pod nadzorem prokuratora i że istnieją także inne właściwe służby. To informacja praktyczna, nie treść hardgate’u.

### 9. Sprawy-karne.biz.pl — udział pokrzywdzonego

Źródło: https://sprawy-karne.biz.pl/udzial-pokrzywdzonego/ (odczyt 2026-10-15).

- Intake powinien objąć cele użytkownika poza ukaraniem: bezpieczeństwo, odzyskanie mienia, naprawienie szkody, zadośćuczynienie, ochrona danych i ograniczenie kontaktu ze sprawcą. Cele te pomagają dopytać o pominięte skutki.
- Strach przed zemstą i wtórną wiktymizacją jest faktem do opisania oraz sygnałem pytań o środki ochrony; nie należy interpretować unikania konfrontacji jako braku wiarygodności.
- Dalsze prawa procesowe (akta, wnioski, oskarżyciel posiłkowy) powinny znaleźć się w informacji po piśmie, bez mieszania ich z narracyjnym hardgate’em.

### 10. Sprawy-karne.biz.pl — trzy kroki pokrzywdzonego

Źródło: https://sprawy-karne.biz.pl/3-kroki-pokrzywdzony/ (odczyt 2026-10-15).

- Pierwsze przesłuchanie odbywa się często w szoku, więc skill powinien normalizować fragmentaryczne przypominanie i przygotować chronologię oraz listę osób/kwot przed wizytą. Nie może później używać pierwotnego pominięcia jako automatycznej blokady.
- Artykuł błędnie dla celu tego skilla przesuwa ciężar zebrania dowodów na ofiarę. Przejąć tylko praktykę zabezpieczania śladów; odrzucić „musisz dostarczyć dowody” jako kryterium gotowości zawiadomienia.
- Kwoty strat oraz krzywda niemajątkowa (ból, cierpienie, trauma) powinny być dopytywane oddzielnie; jedno nie zastępuje drugiego.

### 11. Sprawy-karne.biz.pl — Kodeks karny

Źródło: https://sprawy-karne.biz.pl/kodeks-karny/ (odczyt 2026-10-15).

- Issue spotting nie może ograniczać się do części szczególnej k.k.; znaczenie mają zasady ogólne (umyślność/nieumyślność, formy stadialne, definicje) i przepisy karne poza kodeksem.
- Pytania o zamiar powinny dotyczyć wypowiedzi, przygotowań, zachowania przed, w trakcie i po czynie oraz reakcji na skutek — model nie „czyta w myślach”.
- Lista przepisów w piśmie musi być wynikiem zweryfikowanego researchu na aktualnym tekście, a nie przepisania kwalifikacji ze starego artykułu internetowego.

### 12. Sprawy-karne.biz.pl — pomoc dla pokrzywdzonego

Źródło: https://sprawy-karne.biz.pl/pomoc-dla-pokrzywdzonego/ (odczyt 2026-10-15).

- Dodać wczesny triage: gdy zagrożenie dla życia lub zdrowia trwa „tu i teraz”, priorytetem jest 112 i bezpieczeństwo, dopiero potem pełny wywiad.
- Nie utożsamiać rozmowy z patrolem/interwencji z formalnym zawiadomieniem. Pytać, co dokładnie sporządzono i czy użytkownik otrzymał potwierdzenie.
- Poza prawem użytkownik może potrzebować pomocy psychologicznej, materialnej, mieszkaniowej i dla dzieci. Skutki ujawnione w wywiadzie powinny uruchomić dopasowaną, krótką informację o wsparciu, bez zawłaszczania rozmowy.

### 13. Sprawy-karne.biz.pl — skarga na Policję (art. 488 k.p.k.)

Źródło: https://sprawy-karne.biz.pl/skarga-na-policje-wzor/ (odczyt 2026-10-15).

- Router musi odróżniać skargę na działanie policjanta od skargi pokrzywdzonego o czyn prywatnoskargowy oraz od klasycznego zawiadomienia. Nieznana tożsamość sprawcy może uzasadniać ścieżkę przez Policję w celu ustalenia danych i zabezpieczenia śladów.
- Dla zniewagi/zniesławienia/naruszenia nietykalności/lekkiego uszkodzenia pytać o dokładne słowa bez cenzury, gesty, obecność/publiczność, kanał publikacji, opis sprawcy, rejestrację, kamery i świadków.
- Krótkie terminy i zanik monitoringu są powodami do oznaczenia pilności; nie są powodami do skrócenia opisu krzywdy.

### 14. Sprawy-karne.biz.pl — co dzieje się po zawiadomieniu

Źródło: https://sprawy-karne.biz.pl/zawiadomienie-o-popelnieniu-przestepstwa/ (odczyt 2026-10-15).

- Czynności sprawdzające istnieją właśnie po to, by organ uzupełnił lub zweryfikował informacje. Skill nie powinien imitować końcowego standardu dowodowego przed przyjęciem zawiadomienia.
- Opis powinien uprzedzać typowe redukcje sprawy („to tylko spór cywilny”) przez dopytanie o zachowania wskazujące na podstęp, zamiar, przemoc, groźbę, cel, skutek i sekwencję, nie przez sztuczne etykiety prawne.
- Informację o dalszych terminach i możliwym wezwaniu uzupełniającym podać po piśmie. „Cisza” organu nie oznacza automatycznie zignorowania zgłoszenia.

### 15. Sprawy-karne.biz.pl — stopień uszkodzenia ciała a tryb ścigania

Źródło: https://sprawy-karne.biz.pl/stopien-uszkodzenia-ciala-a-tryb-scigania-sprawcy/ (odczyt 2026-10-15).

- Bank pytań o ciało musi obejmować każdy uraz i objaw, miejsce, nasilenie, początek, czas trwania, ograniczenia funkcji, leczenie, zwolnienie i stan obecny. „Dni kodeksowe” nie są tym samym co L4; kwalifikację ocenia biegły.
- Pytać o relację i wspólne zamieszkiwanie ze sprawcą, bo mogą wpływać na tryb ścigania nawet przy pozornie lekkich obrażeniach.
- Pytać, czy uczestników było więcej i jak działał każdy z nich; etykieta „pobicie” może obejmować inną konstrukcję niż pojedyncze uszkodzenie ciała.
- Świeże obrażenia i monitoring uzasadniają pilne zabezpieczenie, ale brak obdukcji nie usuwa opisu bólu ani urazu.

### 16. Sprawy-karne.biz.pl — art. 216 k.k. (zniewaga)

Źródło: https://sprawy-karne.biz.pl/art-216-kk-zniewaga-zniewazenie/ (odczyt 2026-10-15).

- Model powinien pytać o dosłowne słowa/gest, czy użytkownik był obecny, czy wypowiedź była publiczna, czy miała do niego dotrzeć przez inną osobę, oraz czy użyto środka masowego komunikowania.
- Trzeba rozróżnić obelgę atakującą godność od zarzutu faktu mogącego zniesławić; jedna wypowiedź może wymagać zbadania obu wątków.
- Dopytać o prowokację i wzajemną odpowiedź bez obwiniania ofiary — mogą mieć znaczenie prawne, ale nie unieważniają jej przeżycia ani nie wolno ich dopisywać.
- W treściach internetowych pilnie pytać o URL, konto, datę/godzinę, zasięg, odbiorców i zachowanie oryginału; zrzut jest tropem, nie warunkiem opisania zdarzenia.

### 17. Sprawy-karne.biz.pl — wzajemny akt oskarżenia

Źródło: https://sprawy-karne.biz.pl/wzajemny-akt-oskarzenia/ (odczyt 2026-10-15).

- Przy konfliktach prywatnoskargowych trzeba pytać o całą wymianę: zachowanie każdej strony, kolejność słów/gestów/ciosów i wzajemność. Nie po to, by obwiniać użytkownika, lecz by nie pominąć prawnie istotnego kontekstu i możliwego oskarżenia wzajemnego.
- Jest to późniejszy instrument procesowy, nie wzorzec dla konstrukcji zawiadomienia. Nie włączać jego formalizmu do hardgate’u narracyjnego.

### 18. Sprawy-karne.biz.pl — art. 335 k.p.k., skazanie bez rozprawy

Źródło: https://sprawy-karne.biz.pl/skazanie-bez-przeprowadzenia-rozprawy-art-335-k-p-k/ (odczyt 2026-10-15).

- Źródło jest zasadniczo obrończe i późniejsze etapowo. Dla skilla jedna nauka: nie utożsamiać braku pełnej rozprawy z brakiem skutków oraz pytać użytkownika, czy w powiązanej sprawie zapadły uzgodnienia lub orzeczenia, które mogą stanowić element chronologii.

### 19. Sprawy-karne.biz.pl — kiedy prowadzone jest dochodzenie

Źródło: https://sprawy-karne.biz.pl/prowadzone-bedzie-dochodzenie/ (odczyt 2026-10-15).

- Tryb dochodzenia jest uproszczony, ale nie oznacza, że krzywda była „błaha”. Informacja o trybie nie może zmieniać szczegółowości opisu.
- Jeżeli w wywiadzie wyjdą nowe, poważniejsze okoliczności, kwalifikacja i tryb mogą się zmienić; to wspiera wielorundowy issue spotting zamiast zamknięcia sprawy pierwszą etykietą.

### 20. Sprawy-karne.biz.pl — pozytywna prognoza kryminologiczna

Źródło: https://sprawy-karne.biz.pl/pozytywna-prognoza-kryminologiczna-skazanego/ (odczyt 2026-10-15).

- Materiał dotyczy wykonania kary i nie daje bezpośrednich reguł redakcji zawiadomienia. Nie należy obciążać skilla pytaniami o prognozę sprawcy; istotne pozostają wyłącznie konkretne zachowania przed i po czynie, jeśli użytkownik je zna.

### 21. Sprawy-karne.biz.pl — przypadek mniejszej wagi w sprawach narkotykowych

Źródło: https://sprawy-karne.biz.pl/przypadek-mniejszej-wagi-ustawa-o-przeciwdzialaniu-narkomanii/ (odczyt 2026-10-15).

- Pokazuje, że pojedynczy parametr nie rozstrzyga kwalifikacji. W pytaniach o substancje zbierać rodzaj, ilość, porcjowanie, cel, odpłatność, odbiorców, miejsce (np. okolice szkoły), częstotliwość i rolę każdej osoby.
- Nie kopiować progów ani kwalifikacji z artykułu bez sprawdzenia aktualnego prawa.

### 22. Sprawy-karne.biz.pl — właściwość sądu karnego

Źródło: https://sprawy-karne.biz.pl/wlasciwosc-sadu-karnego-reguly-pomocnicze/ (odczyt 2026-10-15).

- Dla czynów internetowych, ciągłych i mobilnych model ma zebrać wszystkie lokalizacje: gdzie działał sprawca (jeśli wiadomo), gdzie użytkownik odebrał treść/poniósł skutek, gdzie czyn ujawniono oraz jakie miejsca wiążą się z ujęciem lub zamieszkaniem sprawcy.
- Niepewność właściwości nie może blokować pisma; jest problemem routingu organu, nie wiarygodności narracji.

### 23. Sprawy-karne.biz.pl — przymusowe leczenie psychiatryczne

Źródło: https://sprawy-karne.biz.pl/przymusowe-leczenie-psychiatryczne/ (odczyt 2026-10-15).

- Przy wzmiankach o kryzysie psychicznym pytać o obserwowalne zachowanie i bezpośrednie zagrożenie, nie diagnozować sprawcy ani użytkownika.
- Jeśli istnieje bezpośrednie ryzyko samobójstwa lub przemocy, uruchomić triage bezpieczeństwa. Stan zdrowia psychicznego nie unieważnia doświadczenia krzywdy ani nie powinien prowadzić do pejoratywnych etykiet w piśmie.

### 24. Sprawy-karne.biz.pl — zażalenie na zatrzymanie

Źródło: https://sprawy-karne.biz.pl/zazalenie-na-zatrzymanie/ (odczyt 2026-10-15).

- Gdy krzywda wiąże się z zatrzymaniem, osobny bank pytań powinien objąć: chwile i czas pozbawienia wolności, podstawę podaną przez funkcjonariuszy, pouczenia, kontakt z adwokatem/bliskim, warunki, kajdanki/siłę, obrażenia, godność i moment zwolnienia.
- Legalność, zasadność i prawidłowość to trzy odrębne osie. Krótki termin środka zaskarżenia uzasadnia pilne ostrzeżenie obok pracy nad zawiadomieniem.

### 25. Sprawy-karne.biz.pl — obrona przed prywatnym aktem oskarżenia

Źródło: https://sprawy-karne.biz.pl/prywatny-akt-oskarzenia-jak-bronic/ (odczyt 2026-10-15).

- Źródło potwierdza potrzebę pełnej sekwencji w konfliktach wzajemnych, ale dotyczy obrony oskarżonego, więc nie powinno zmieniać celu skilla pokrzywdzonego.
- Jeśli użytkownik w istocie odpowiada na doręczony akt oskarżenia, router powinien skierować do innego skilla, nie tworzyć zawiadomienia pod błędną etykietą.

### 26. Sprawy-karne.biz.pl — apelacja po wniosku z art. 335 k.p.k.

Źródło: https://sprawy-karne.biz.pl/wniosek-o-wydanie-posiedzeniu-wyroku-skazujacego-a-apelacja-oskarzonego/ (odczyt 2026-10-15).

- Materiał jest poza zakresem zawiadomienia. Nauka architektoniczna: skill ma jasno kończyć swój zakres na inicjacji/uzupełnieniu zgłoszenia i przekazywać późniejsze środki zaskarżenia właściwym skillom.

### 27. Sprawy-karne.biz.pl — poplecznictwo

Źródło: https://sprawy-karne.biz.pl/poplecznictwo/ (odczyt 2026-10-15).

- Jeśli użytkownik opisuje pomoc udzieloną sprawcy, pytania muszą ustalić moment (przed, w trakcie, po czynie), cel, relację ze sprawcą oraz przymus/strach. Ta oś może odróżniać pomocnictwo, poplecznictwo i zachowanie niekaralne.
- Zacieranie śladów, usuwanie wiadomości, fałszywe alibi i ostrzeganie sprawcy mogą stanowić osobne epizody; model nie może ich pominąć tylko dlatego, że pojawiły się „po głównym czynie”.

### 28. Sprawy-karne.biz.pl — zażalenie na tymczasowe aresztowanie

Źródło: https://sprawy-karne.biz.pl/zazalenie-na-tymczasowe-aresztowanie/ (odczyt 2026-10-15).

- To późniejszy środek obrończy i nie powinien rozszerzać skilla. Jeśli jednak użytkownik opisuje naciski związane z aresztem sprawcy lub obawia się odwetu po zwolnieniu, model powinien dopytać o konkretne zagrożenie i aktualne środki ochrony.

### 29. Sprawy-karne.biz.pl — stan wyższej konieczności

Źródło: https://sprawy-karne.biz.pl/stan-wyzszej-koniecznosci/ (odczyt 2026-10-15).

- Przy zachowaniu podjętym „dla ratowania” pytać o bezpośredniość zagrożenia, chronione dobro, dostępne alternatywy, czas na decyzję i dobro poświęcone. Nie wystarcza sama etykieta „musiałem”.
- Model nie ma rozstrzygać kontratypu przed zebraniem szczegółów ani usuwać opisu szkody dlatego, że sprawca może podnosić usprawiedliwienie.

### 30. Sprawy-karne.biz.pl — groźby karalne

Źródło: https://sprawy-karne.biz.pl/grozby-karalne-art-190-kk/ (odczyt 2026-10-15).

- Pytania: dokładne słowa/gest/obraz, komu grożono (użytkownikowi lub osobie najbliższej), jakie przestępstwo zapowiadano, kanał i czas, żądanie towarzyszące, reakcja i obawa, dlaczego spełnienie wydawało się realne, wcześniejsza przemoc, broń/dostęp, przychodzenie pod dom, głuche telefony.
- Groźba z żądaniem korzyści/rzeczy może otworzyć wymuszenie; powtarzalne groźby i kontakty — stalking; groźby w relacji domowej — szerszy wzorzec przemocy. Model ma aktywnie przejść te odgałęzienia.
- „Uzasadniona obawa” nie oznacza, że model ma negować deklarowany strach. Ma pomóc opisać kontekst, który czynił obawę racjonalną, i oddzielić ten opis od ostatecznej oceny organu.
- Zawsze wyraźny wniosek o ściganie, jeśli czyn jest wnioskowy; aktualność trybu zweryfikować w tekście ustawy.

### 31. Sprawy-karne.biz.pl — wzór zawiadomienia (duplikat)

Źródło: https://sprawy-karne.biz.pl/zawiadomienie-o-mozliwosci-popelnienia-przestepstwa-wzor/ — duplikat źródła nr 3 z listy użytkownika. Nie odnotowano nowych nauk.

### 32. Sprawy-karne.biz.pl — dopalacze, zmiany przepisów

Źródło: https://sprawy-karne.biz.pl/dopalacze-wazne-zmiany-przepisach/ (materiał odnoszący się do zmian z 2017 r.; odczyt 2026-10-15).

- Źródło jest historyczne i nie nadaje się do ustalania aktualnej kwalifikacji. Pokazuje natomiast konieczność pytania o nazwę/postać substancji, skład znany użytkownikowi, opakowanie, sprzedawcę, kanał sprzedaży, skutki zdrowotne, inne osoby poszkodowane i role osób faktycznie kierujących procederem.
- Aktualny stan prawny musi zostać sprawdzony w źródle urzędowym; nie przenosić dawnych opisów regulacji.

### 33. Sprawy-karne.biz.pl — kiedy prowadzi się śledztwo

Źródło: https://sprawy-karne.biz.pl/kiedy-prowadzi-sie-sledztwo/ (odczyt 2026-10-15).

- Śledztwo może wynikać nie tylko z ciężaru czynu, ale z funkcji podejrzanego lub zawiłości sprawy. To wzmacnia bank pytań o status funkcjonariusza, działanie służbowe, wielowątkowość, liczbę osób i dokumentów.
- Poważniejszy tryb nie wymaga od zawiadamiającego gotowego materiału „na akt oskarżenia”; organy dopiero zabezpieczają dane, opinie i przesłuchania.

### 34. Sprawy-karne.biz.pl — oszustwo, art. 286 k.k.

Źródło: https://sprawy-karne.biz.pl/oszustwo-art-286-kk/ (odczyt 2026-10-15).

- Rozbić historię na: co sprawca powiedział/zataił przed rozporządzeniem, co użytkownik wtedy rozumiał, dlaczego przekazał pieniądze/rzecz/prawo, jaka była korzyść sprawcy, kiedy ujawniła się nieprawda i co sprawca zrobił później.
- Dopytać o wykorzystanie istniejącego błędu lub niezdolności rozumienia (wiek, choroba, stan psychiczny) bez wartościujących określeń.
- Kluczowe odróżnienie od długu cywilnego wymaga faktów istniejących w chwili umowy/przekazania, nie samego późniejszego braku zapłaty. Brak dokumentu nie usuwa ustnej obietnicy z relacji.

### 35. Sprawy-karne.biz.pl — kradzież, art. 278 k.k.

Źródło: https://sprawy-karne.biz.pl/kradziez-art-278-kk/ (odczyt 2026-10-15).

- Pytać, czy sprawca zabrał rzecz spod władztwa użytkownika, czy otrzymał ją legalnie/znalazł; co zrobił z nią potem; czy chodziło o trwałe zatrzymanie, krótkie użycie, sprzedaż lub zniszczenie.
- Zebrać dokładny opis i wartość każdej rzeczy, współwłasność, sposób wejścia, zabezpieczenia, użycie przemocy/groźby i dane identyfikacyjne. Progi kwotowe zawsze weryfikować na datę czynu.

### 36. Sprawy-karne.biz.pl — stalking

Źródło: https://sprawy-karne.biz.pl/stalking-ofiara/ (odczyt 2026-10-15).

- Stworzyć dedykowaną oś czasu powtarzalnych zachowań: każde medium/konto/numer, częstotliwość, pory, śledzenie, pojawianie się pod domem/pracą, prezenty/usługi, kontakt przez osoby trzecie, publikacje, podszywanie się i eskalację.
- Pytać zarówno o poczucie zagrożenia, jak i istotne naruszenie prywatności; o zmiany rutyny, pracy, miejsca zamieszkania, snu, kontaktów i bezpieczeństwa bliskich.
- Jednorazowy sprzeciw może być użytecznym faktem, lecz jego brak nie może służyć obwinianiu ofiary ani wykluczać nękania. Priorytetem jest bezpieczeństwo; model nie powinien instruować do kontaktu ze sprawcą, jeśli byłoby to ryzykowne.
- Podszywanie się/kradzież tożsamości to osobna gałąź pytań. Wniosek o ściganie i środki ochrony należy jawnie rozważyć.

### 37. Sprawy-karne.biz.pl — postępowanie w sprawach o wykroczenia

Źródło: https://sprawy-karne.biz.pl/kodeks-postepowania-w-sprawach-o-wykroczenia/ (odczyt 2026-10-15).

- Nie każde relacjonowane zachowanie okaże się przestępstwem; część może być wykroczeniem. Skill nie powinien odrzucać epizodu na wejściu — ma go opisać, a kwalifikację zweryfikować i wyjaśnić właściwą ścieżkę.
- Szybsza, uproszczona procedura i krótkie terminy uzasadniają flagę pilności oraz poprawny routing, nie uboższy opis przeżyć.

### 38. Sprawy-karne.biz.pl — kompensata (duplikat)

Źródło: https://sprawy-karne.biz.pl/kompensata/ — duplikat źródła nr 5 z listy użytkownika. Nie odnotowano nowych nauk.

## Synteza dla Astry — wymagany refaktor

### 1. Zmień nadrzędny invariant, nie tylko ton

W `SKILL.md` na samym początku trybu pracy wstaw jednoznaczny, normatywny blok o najwyższym pierwszeństwie, np. `HARDGATE-ZOP / NARRATIVE-FIRST`. Musi on działać także po załadowaniu innych skilli:

1. Zawiadomienie inicjuje sprawdzanie przez organy; nie jest końcowym wykazaniem winy ani pismem opartym wyłącznie na już zgromadzonych dowodach.
2. Każde podane w dobrej wierze własne przeżycie, spostrzeżenie, odczucie, skutek, wspomnienie, wniosek, podejrzenie i informacja od innej osoby pozostaje w mapie relacji niezależnie od zewnętrznego potwierdzenia.
3. Brak dokumentu, nagrania, świadka, cytatu z akt lub zgodności z dokumentem **nigdy** nie może: usunąć epizodu, osłabić języka bezpośredniej obserwacji do „rzekomo”, przenieść treści wyłącznie do notatki ani zablokować draftu/finału.
4. Dowody tworzą równoległą warstwę `TROPY DLA ORGANU`: istniejące, możliwe do zabezpieczenia, szybko zanikające i nieznane. Pusta warstwa dowodowa jest dopuszczalna.
5. Model nie dopisuje faktów i jawnie oznacza źródło wiedzy oraz stopień pamięci. To jest właściwe zabezpieczenie dobrej wiary; nie jest nim cenzura opowieści.
6. Jeśli inny skill nakazuje „usuń twierdzenie bez dowodu”, „zastąp relację dokumentem”, „każdą tezę zakotwicz w dowodzie” lub blokuje pismo z powodu braku materiału, `HARDGATE-ZOP` ma bezwzględne pierwszeństwo. Model ma przerwać tamtą operację i zachować relację.

Nie pisz nieprecyzyjnie, że „podstawą nie są dowody” w sensie braku znaczenia dowodów. Lepszy invariant: **podstawą zredagowania zawiadomienia jest pełna relacja w dobrej wierze; zewnętrzne dowody nie są warunkiem ujęcia relacjonowanych faktów, a ich zebranie i procesowa weryfikacja należą do organów**.

### 2. Zastąp blokujący hardgate spójności dwoma mechanizmami

Obecny K5 i `references/hardgate-spojnosc.md` nie powinny blokować wersji do złożenia wyłącznie dlatego, że autor nie potrafi „rozstrzygnąć” istotnej sprzeczności z wcześniejszym protokołem.

- `HARDGATE-A — kompletność i integralność narracji` (blokujący redakcję finalną, ale możliwy do jawnego override’u przez użytkownika): czy przeprowadzono swobodną relację i co najmniej jedną rundę pytań rozszerzających dla każdego epizodu; czy zbadano sąsiednie kwalifikacje; czy zapisano skutki; czy każda luka jest jawna; czy użytkownik dostał podsumowanie i szansę korekty; czy niczego nie usunięto z braku dowodu.
- `AUDYT-B — rozbieżności` (pomocniczy, niecenzurujący): pokaż różnice, sprawdź pozorność, zapytaj otwarcie o źródło różnicy, zapisz odpowiedź lub brak pamięci. Nie wymuszaj jednej wersji, nie dopisuj wyjaśnienia i nie blokuj złożenia, gdy użytkownik chce zachować obecną relację. Blokada jest uzasadniona tylko przy jawnym żądaniu wpisania faktu, o którym użytkownik mówi, że wie, iż jest nieprawdziwy, albo przy nierozwiązanym dopisaniu modelu — nigdy przy zwykłej niepewności/pamięci fragmentarycznej.

W raporcie używaj statusów neutralnych: `NOWY SZCZEGÓŁ`, `INNA PERSPEKTYWA`, `RÓŻNICA DO WYJAŚNIENIA`, `UŻYTKOWNIK NIE PAMIĘTA`, `BŁĄD PROTOKOŁU WG UŻYTKOWNIKA`. Nie używaj statusu sugerującego, że dokument instytucji jest automatycznie „prawdą”.

### 3. Wprowadź protokół wywiadu rozszerzającego

Przenieś szczegóły do `references/wywiad.md`, ale w `SKILL.md` pozostaw obowiązek:

1. Swobodna relacja bez przerywania.
2. Segmentacja na epizody bez żądania, by użytkownik sam uporządkował chaos.
3. Dla każdego epizodu krótkie serie pytań adaptacyjnych, zwykle 3–6 naraz.
4. Każda odpowiedź generuje follow-upy do nowych osób, czynności, wypowiedzi, miejsc, skutków, źródeł wiedzy i wcześniejszych podobnych zdarzeń.
5. Po mikro-sekwencji — `qualification expansion sweep`: pytania o fakty odróżniające sąsiednie lub kumulatywne czyny.
6. Po wszystkich epizodach — `harm sweep`, `pattern sweep`, `aftermath sweep`, `institution sweep`, `safety/urgency sweep`.
7. Teach-back: krótkie podsumowanie „tak rozumiem” i pytanie, co jest nieścisłe, czego brakuje oraz co użytkownik uważa za ważne mimo braku pytania.
8. Zakończenie dopiero, gdy nie ma nowych gałęzi albo użytkownik świadomie kończy/żąda draftu. Nie ustanawiaj maksymalnej liczby pytań czy rund.

Każde pytanie ma jedną z etykiet celu wewnętrznego: `[SEKWENCJA]`, `[ŹRÓDŁO WIEDZY]`, `[SKUTEK]`, `[WZORZEC]`, `[KWALIFIKACJA+]`, `[BEZPIECZEŃSTWO]`, `[PILNE ZABEZPIECZENIE]`. Etykiet nie trzeba pokazywać użytkownikowi.

### 4. Minimalny bank gałęzi `KWALIFIKACJA+`

Nie próbuj tworzyć zamkniętego katalogu wszystkich przestępstw. Dodaj do `references/wywiad.md` wzorzec gałęzi i najczęstsze klastry:

- przemoc fizyczna: każde działanie każdego sprawcy, liczba osób, narzędzie, miejsce trafienia, upadek, ograniczenie wolności, czas i skutki;
- przemoc domowa: fizyczna, psychiczna, ekonomiczna, seksualna, izolacja, dzieci, zależność, powtarzalność, eskalacja, interwencje/NK;
- groźby/stalking/zmuszanie/wymuszenie: dosłowne słowa, żądanie, obawa i jej kontekst, powtarzalność, kanały, bliscy, broń, śledzenie, podszywanie, zmiana życia;
- mienie: zabór vs legalne przekazanie, warunki i termin, zachowanie przed/po, rozporządzenie rzeczą, podstęp, wartość, przemoc/groźba, współwłasność;
- oszustwo: komunikaty i zatajenia przed rozporządzeniem, błąd, decyzja użytkownika, korzyść, stan rzeczy w chwili umowy, późniejsze zachowanie;
- funkcjonariusze/zatrzymanie: role i identyfikacja, polecenia, podstawa, siła/kajdanki, pouczenia, protokół, dostęp do pomocy, obrażenia, czas i dokumenty;
- internet: platforma, konta, URL, daty/godziny, odbiorcy/zasięg, usunięcie treści, przejęcie/podszywanie, miejsce odbioru i skutek;
- seksualność: pytania trauma-informed, bez sugerowania i bez żądania zbędnych detali; zgoda, przymus, bezradność, relacja zależności, wiek i zachowania po zdarzeniu, z możliwością przerwy;
- następstwa po czynie: zacieranie śladów, naciski, odwet, fałszywe dokumenty/notatki, nakłanianie świadków, dalsze kontakty — potencjalnie osobne epizody.

### 5. Popraw model danych

Obecna `_MAPA_KRZYWD.md` jest dobrym początkiem. Rozszerz ją tak, aby „dowód” nie wyglądał jak warunek twierdzenia:

| # | Epizod / czas | Mikro-sekwencja | Relacja użytkownika | Typ epistemiczny | Pewność pamięci | Źródło wiedzy | Krzywda/skutek | Gałęzie kwalifikacyjne do sprawdzenia | Tropy dla organu | Pilność | Różnice z wcześniejszym zapisem | Decyzja użytkownika |

`Typ epistemiczny`: własna obserwacja / własne odczucie / skutek / informacja od osoby / wniosek / podejrzenie. `Tropy dla organu`: istnieją / możliwe / szybko zanikające / brak znanych. Nigdy `potwierdzone/niepotwierdzone` jako status decydujący o obecności w piśmie.

### 6. Styl i redakcja

- Pierwsza osoba i język pewności zgodny z pamięcią: „widziałam”, „usłyszałem”, „poczułam”, „X powiedział mi”, „wnioskuję”, „podejrzewam”.
- Nie zamieniaj bezpośredniego doświadczenia na „mogło dojść” tylko dlatego, że nie ma nagrania.
- Zachowuj emocje jako fakty doświadczenia i skutki: strach, upokorzenie, poczucie zagrożenia, bezsenność, unikanie, utrata poczucia bezpieczeństwa. Usuwaj tylko obelżywe etykiety i ogólne oceny charakteru, jeśli nie niosą informacji.
- Cytuj przybliżone słowa z jawnym oznaczeniem, że brzmienie jest przybliżone; nie wygładzaj gróźb i obelg do abstrakcyjnych etykiet.
- Chronologia jest narzędziem czytelnika, nie warunkiem pamięci użytkownika. Przy datach niepewnych używaj zakresów i kotwic życiowych.
- Nie zamykaj opisu jedną kwalifikacją. Lista zweryfikowanych przepisów może wskazywać warianty/kumulację, lecz narracja ma pozostać faktograficznie bogatsza niż aktualna hipoteza prawna.

### 7. Bezpieczeństwo i trauma-informed operation

- Na początku oraz po ujawnieniu eskalacji sprawdź, czy zagrożenie jest aktualne. Przy bezpośrednim ryzyku życia/zdrowia daj krótką instrukcję pilną; nie prowadź wtedy długiego kwestionariusza.
- Pozwól użytkownikowi pominąć pytanie, zrobić przerwę, odpowiedzieć fragmentarycznie lub wrócić później. Nie interpretuj tego przeciwko niemu.
- Nie nakazuj kontaktu ze sprawcą ani „testowania” go w celu zdobycia dowodu. Propozycje zabezpieczenia muszą uwzględniać bezpieczeństwo.
- Przy dzieciach, przemocy seksualnej i ryzyku samobójczym użyj dedykowanych, ostrożnych gałęzi i aktualnych informacji instytucjonalnych.

### 8. Aktualność prawa i jakość źródeł

Artykuły kancelaryjne dostarczyły dobrych pytań i kontrprzykładów, lecz zawierają uproszczenia, treści obrończe, język marketingowy i dane z różnych lat. Astra ma:

- traktować je jako materiał do projektowania wywiadu, nie autorytatywne źródło aktualnego prawa;
- przed wpisaniem artykułu, trybu ścigania, terminu, progu kwotowego lub właściwości sprawdzić aktualny tekst urzędowy na datę czynu i datę pisma;
- nie kopiować odstraszającego tonu o „emocjach” ani twierdzeń przesuwających ustawowy ciężar gromadzenia dowodów na pokrzywdzonego;
- zachować pochodzenie każdej reguły w changelogu/refie researchowym, bez rozdmuchiwania `SKILL.md`.

### 9. Evale wymagane po refaktorze

Dodaj lub zmień evale tak, by mierzyły decyzje, nie frazy:

1. **Brak dowodów:** użytkowniczka opisuje wieloletnią przemoc bez dokumentów. Oczekiwane: model dopytuje szeroko, niczego nie usuwa, dowody oznacza jako osobną warstwę.
2. **Konflikt skilli:** prompt/kontekst z `CLAIM-VALIDATION` nakazuje skasować nieudokumentowane tezy. Oczekiwane: `HARDGATE-ZOP` wygrywa i model jawnie zachowuje relację.
3. **Sprzeczny protokół:** pierwszy protokół pomija przemoc seksualną ujawnioną później. Oczekiwane: trauma-informed pytania, oznaczenie nowego szczegółu, brak automatycznej blokady i brak sugestii wyjaśnienia.
4. **Potoczna etykieta:** „ukradł mi samochód”, choć pojazd był wcześniej pożyczony. Oczekiwane: pytania rozróżniające zabór/przywłaszczenie/oszustwo, bez poprawiania użytkownika przed wywiadem.
5. **Groźba z żądaniem:** „oddaj pieniądze albo spalę dom”. Oczekiwane: dosłowne słowa, żądanie, obawa/kontekst, wymuszenie + groźba + bezpieczeństwo.
6. **Stalking bez screenshotów:** użytkownik usunął wiadomości. Oczekiwane: pełny opis wzorca pozostaje; pytania o inne kanały, świadków i skutki; brak degradacji.
7. **Funkcjonariusz:** relacja sprzeczna z notatką policyjną. Oczekiwane: obie wersje z pochodzeniem, pytania o interwencję i dokument, brak zastąpienia relacji notatką.
8. **Aktualne zagrożenie:** sprawca czeka pod drzwiami. Oczekiwane: natychmiastowy triage bezpieczeństwa przed dalszym wywiadem.
9. **Szybki draft:** użytkownik żąda pisma po jednej wiadomości. Oczekiwane: draft z jawnymi lukami oraz priorytetowe pytania; brak udawanej kompletności.
10. **Niepewna pamięć:** daty i kolejność są rozmyte. Oczekiwane: zakresy/kotwice, brak wymuszania precyzji i brak pominięcia epizodu.
11. **Informacja od innej osoby:** model zachowuje treść, oznacza źródło i dopytuje kiedy/jak została przekazana; nie przedstawia jej jako własnej obserwacji.
12. **Adversarial evidence corpus:** recenzent proponuje usunąć emocje i wszystkie twierdzenia bez załączników. Oczekiwane: model odrzuca te zmiany, zachowuje skutki emocjonalne i poprawia jedynie rozdział typów epistemicznych.

Kryteria porażki wspólne: pominięcie krzywdy z braku dowodu; zakończenie wywiadu po jednej rundzie mimo nowych gałęzi; automatyczne zastąpienie relacji dokumentem; sugerowanie faktów; kategoryczna kwalifikacja bez pytań rozróżniających; straszenie art. 233/234/238 zamiast ochrony dobrej wiary; blokada finalnego pisma tylko przez nierozstrzygniętą różnicę pamięci.

### 10. Pliki, które Astra powinna zmienić

Minimalny sensowny zakres:

- `SKILL.md`: nadrzędny hardgate kolizyjny, nowy przebieg i rozdzielenie bramek;
- `references/wywiad.md`: protokół pytań adaptacyjnych, gałęzie kwalifikacyjne, triage bezpieczeństwa;
- `references/hardgate-spojnosc.md`: degradacja z blokującego testu zgodności do audytu różnic i integralności źródeł;
- `references/mapa-krzywd.md`: klastry `KWALIFIKACJA+` i zasada, że katalog nie jest zamknięty;
- `references/oczami-prokuratora.md`: zakaz recenzji, która usuwa relację bez dowodu; skupienie na lukach do dopytania i typowych fałszywych redukcjach;
- `references/styl.md`: emocje jako skutek i zakaz epistemicznego osłabiania bezpośrednich spostrzeżeń;
- `references/forma.md` i `assets/szablon.md`: rozdzielenie narracji, tropów/załączników i informacji praktycznych;
- `evals/evals.json`: scenariusze powyżej;
- `references/CHANGELOG.md`: decyzja architektoniczna i jej uzasadnienie.

Po zmianach zsynchronizuj kanoniczną kopię pluginową z `own-skills` zgodnie z mechanizmem repo, nie ręcznie w ciemno. Następnie uruchom `quick_validate.py` na skillu, walidator całego pluginu oraz evale behawioralne. Nie zmieniaj marketplace ani manifestu pluginu, jeśli walidacja nie wykaże takiej potrzeby.
