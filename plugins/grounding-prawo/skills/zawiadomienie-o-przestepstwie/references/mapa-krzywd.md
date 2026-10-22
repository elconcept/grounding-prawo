# Lejek krzywd (F3)

Mapa służy do zadawania pytań, do kontroli kompletności (K2) i do listy przepisów na końcu pisma
(K3). W narracji pisma przepisów nie ma - jest opis zdarzeń w słowach autora.

## Jak używać

Po wywiadzie o epizodzie przejdź kategorie i zapytaj o te, które pasują do sytuacji, ale nie
padły: „Czy w tej sytuacji zdarzyło się też, że…?”. Każde „tak” to nowy wiersz mapy wewnętrznej,
także bez dowodu. Nie pytaj o wszystkie kategorie przy każdym epizodzie. Wybierz te, które
wynikają z okoliczności (np. interwencja policji → kategorie funkcjonariusza; konflikt sąsiedzki
→ mienie, mir domowy, groźby, nagrywanie).

Do listy przepisów w piśmie trafia przepis, gdy zachowanie opisane przez autora odpowiada
brzmieniu przepisu w jego słowach (nie gdy „jest udowodnione”). Przy wątpliwości dopytaj o fakty rozróżniające. Warianty lub kumulację przedstaw
po sprawdzeniu ich podstaw, nie dopisuj automatycznie obu przepisów.

## Otwarty katalog i KWALIFIKACJA+

Katalog nie ogranicza zakresu krzywd. Wątek spoza tabeli zostaje w mapie i piśmie także bez
ustalonego przepisu. Bank gałęzi w [wywiad.md](wywiad.md) służy rozszerzaniu: groźba → żądanie /
nękanie / przemoc domowa; rzecz zabrana → przekazanie / przywłaszczenie / podstęp; interwencja →
siła / wolność / dokument / naciski. Rozważ oddzielne epizody po głównym czynie.
Nie wyprowadzaj kwalifikacji z samego „tak” na pytanie ogólne ani nie zawężaj opisu do jednego przepisu.

## Źródło i weryfikacja

Poniższe brzmienia i tryby to historyczny punkt wyjścia, nie gwarancja aktualności. Przed użyciem
w piśmie sprawdź urzędowy tekst na datę czynu i pisma, zmiany oraz wejście w życie; zapisz źródło,
wersję i datę sprawdzenia. Ta zasada dotyczy także każdego przepisu już obecnego w tabeli.
Nie powielaj publikatora ani dawnych progów z pamięci. Przy braku dostępu pomiń niezweryfikowaną
kwalifikację, zachowując pełny opis i jawną lukę w analizie poza pismem.


- Kodeks karny: tekst jednolity **Dz.U. 2025 poz. 383** (ELI `DU/2025/383`; najnowszy t.j. według
  ELI, sprawdzone 09.10.2026), brzmienia z bazy `mcp/cache/kodeks/kodeks_karny.md` (wersja od
  21.07.2026). Ślad: MCP `ustawy` (`ustawy_akty`, tytuł „Kodeks karny”).
- Przepis spoza katalogu: najpierw MCP `ustawy` (`ustawy_artykul` dla ELI t.j.; wyszukaj „Art. N.”)`
  (PDF z adresu w odpowiedzi MCP pobierz `curl` i odczytaj przez `pdftotext -layout`, `shared/MOD-TEKST-JEDNOLITY.md`). Bez weryfikacji
  przepis nie trafia do pisma.
- Wykroczenia (Kodeks wykroczeń): katalog jeszcze ich nie obejmuje - zob. TODO.

## Tryb ścigania

Wniosek o ściganie jest w każdym zawiadomieniu (decyzja autora 09.10.2026). Kolumna „tryb” mówi
autorowi, czego się spodziewać:
- **z urzędu** - organ działa sam;
- **na wniosek** - bez wniosku organ nie wszczyna (art. 17 § 1 pkt 10 k.p.k.); po złożeniu wniosku
  postępowanie toczy się z urzędu (art. 12 § 1 k.p.k.);
- **oskarżenie prywatne** - organ może odesłać do drogi prywatnej; poinformuj autora poza pismem,
  opisu krzywdy nie usuwaj (często zbiega się z czynami ściganymi z urzędu).

## Katalog (v0.2) - przepisy zweryfikowane w Dz.U. 2025 poz. 383

| Kategoria | Pytania kontrolne | Przepis i opis prosty (do listy w piśmie) | Tryb |
|---|---|---|---|
| Naruszenie nietykalności | Czy ktoś cię dotknął, popchnął, przytrzymał, uderzył? | art. 217 § 1 k.k. - uderzenie lub inne naruszenie nietykalności cielesnej | oskarżenie prywatne (§ 3) |
| Obrażenia, uszczerbek na zdrowiu | Czy były obrażenia, ból, leczenie? Jak długo trwały skutki (do 7 dni / dłużej)? | art. 157 § 1 k.k. - uszkodzenie ciała lub rozstrój zdrowia ponad 7 dni; art. 157 § 2 k.k. - do 7 dni; art. 156 § 1 k.k. - ciężki uszczerbek | § 1 i art. 156 z urzędu; § 2 oskarżenie prywatne, chyba że pokrzywdzony to osoba najbliższa zamieszkująca ze sprawcą (§ 4) |
| Pobicie (kilku sprawców) | Czy atakowała więcej niż jedna osoba? Czy było zagrożenie życia lub poważnych obrażeń? | art. 158 § 1 k.k. - udział w pobiciu narażającym na niebezpieczeństwo utraty życia lub poważnych obrażeń | z urzędu |
| Narażenie na niebezpieczeństwo | Czy ktoś naraził cię na bezpośrednie niebezpieczeństwo śmierci lub ciężkiego uszczerbku (np. duszenie, ucisk szyi, porzucenie w stanie zagrożenia)? | art. 160 § 1 k.k. (§ 2: gdy sprawca miał obowiązek opieki) | z urzędu (§ 3 nieumyślne - na wniosek) |
| Groźby | Czy ktoś zapowiedział, że coś ci zrobi (tobie, bliskim)? Czy się przestraszyłeś, że to spełni? | art. 190 § 1 k.k. - groźba popełnienia przestępstwa, która wzbudza uzasadnioną obawę | na wniosek (§ 2); art. 12 § 4 k.p.k. pozwala organowi ścigać mimo braku wniosku przy obawie przed odwetem |
| Zmuszanie | Czy ktoś przemocą lub groźbą zmusił cię do czegoś albo do znoszenia czegoś? Czy uporczywie utrudniał korzystanie z mieszkania? | art. 191 § 1 k.k. - zmuszanie przemocą lub groźbą; art. 191 § 1a k.k. - uporczywe utrudnianie korzystania z mieszkania | na wniosek (§ 3) |
| Pozbawienie wolności | Czy nie mogłeś odejść, zostałeś zamknięty, przetrzymany? Jak długo? | art. 189 § 1 k.k. - pozbawienie wolności (§ 2: ponad 7 dni; § 2a: osoba nieporadna; § 3: szczególne udręczenie) | z urzędu |
| Nękanie, podszywanie się | Czy to się powtarzało: telefony, wiadomości, obserwowanie, pojawianie się? Czy ktoś podszywał się pod ciebie? | art. 190a § 1 k.k. - uporczywe nękanie (zagrożenie, poniżenie, udręczenie, naruszenie prywatności); § 2 - podszywanie się, wykorzystanie wizerunku lub danych | na wniosek (§ 4) |
| Zabieg medyczny bez zgody | Czy wykonano wobec ciebie badanie, zabieg, podanie leku bez zgody? | art. 192 § 1 k.k. - zabieg leczniczy bez zgody pacjenta | na wniosek (§ 2) |
| Naruszenie miru domowego | Czy ktoś wszedł albo nie chciał wyjść z twojego domu, mieszkania, ogrodzonej posesji, mimo sprzeciwu? | art. 193 § 1 k.k. - wdarcie się do cudzego domu, mieszkania, ogrodzonego terenu lub nieopuszczenie go wbrew żądaniu | na wniosek (§ 2) |
| Przemoc seksualna | Czy doszło do czynności seksualnej bez zgody, przemocą, groźbą, podstępem? | art. 197 § 1-2 k.k. | z urzędu |
| Znęcanie się | Czy krzywdy powtarzały się ze strony osoby najbliższej albo osoby, od której jesteś zależny? | art. 207 § 1 k.k. - znęcanie się fizyczne lub psychiczne (§ 1a: osoba nieporadna) | z urzędu |
| Zniesławienie | Czy ktoś rozpowiadał o tobie nieprawdę, która może cię poniżyć lub narazić na utratę zaufania? | art. 212 § 1 k.k. (§ 2: media, internet) | oskarżenie prywatne (§ 4) |
| Zniewaga | Czy ktoś cię obrażał, przy kim? | art. 216 § 1 k.k. (§ 2: media, internet) | oskarżenie prywatne (§ 5) |
| Funkcjonariusz: przekroczenie uprawnień, niedopełnienie obowiązków | Czy policjant, urzędnik zrobił coś, czego nie powinien, albo nie zrobił, co powinien (nie przyjął zgłoszenia, nie udzielił pomocy, użył siły)? | art. 231 § 1 k.k. - funkcjonariusz publiczny przekracza uprawnienia lub nie dopełnia obowiązków na szkodę interesu prywatnego | z urzędu |
| Funkcjonariusz: przemoc dla uzyskania zeznań | Czy przemocą lub groźbą chciano wymusić od ciebie wyjaśnienia, informację, oświadczenie? | art. 246 k.k. | z urzędu |
| Znęcanie nad zatrzymanym | Czy byłeś zatrzymany / pozbawiony wolności i ktoś się nad tobą znęcał (albo funkcjonariusz na to pozwolił)? | art. 247 § 1 k.k.; § 3 - funkcjonariusz, który dopuszcza do znęcania | z urzędu |
| Nieprawdziwy dokument urzędowy | Czy notatka, protokół, opis interwencji poświadcza nieprawdę? | art. 271 § 1 k.k. - funkcjonariusz poświadcza w dokumencie nieprawdę co do okoliczności mającej znaczenie prawne | z urzędu |
| Wyłudzenie poświadczenia nieprawdy | Czy ktoś podstępem doprowadził urzędnika do wpisania nieprawdy (np. fałszywe zgłoszenie na ciebie)? | art. 272 k.k. | z urzędu |
| Fałszywe oskarżenie, fałszywe zeznania na twoją szkodę | Czy ktoś świadomie oskarżył cię przed policją, sądem o coś, czego nie zrobiłeś, albo zeznał nieprawdę? | art. 234 k.k. - fałszywe oskarżenie; art. 233 § 1 k.k. - fałszywe zeznania; art. 238 k.k. - zawiadomienie o przestępstwie, o którym wiadomo, że go nie popełniono | z urzędu |
| Inwigilacja, nagrywanie, podsłuch | Czy ktoś zakładał lub używał urządzenia nagrywającego, podsłuchu, kamery, żeby zdobyć informacje o tobie? | art. 267 § 3 k.k. - urządzenie podsłuchowe, wizualne lub inne w celu uzyskania informacji | na wniosek (§ 5: § 1-4) |
| Dostęp do kont, poczty, urządzeń | Czy ktoś wszedł na twoje konta, telefon, pocztę, przełamał zabezpieczenie? | art. 267 § 1-2 k.k. | na wniosek |
| Zniszczenie, usunięcie zapisu informacji | Czy ktoś skasował, zniszczył, zmienił twoje nagrania, dane, zapisy? | art. 268 § 1-2 k.k. | na wniosek (§ 4) |
| Ujawnienie informacji przez funkcjonariusza | Czy funkcjonariusz ujawnił komuś informacje o tobie uzyskane służbowo? | art. 266 § 2 k.k. | z urzędu (§ 3 dotyczy § 1) |
| Dokumenty | Czy ktoś zabrał, ukrył, zniszczył twój dokument albo posłużył się twoim dowodem tożsamości? | art. 275 § 1 k.k.; art. 276 k.k. | z urzędu |
| Zniszczenie, uszkodzenie rzeczy | Co zostało zniszczone, uszkodzone? Wartość w przybliżeniu? | art. 288 § 1 k.k. (§ 2: mniejsza waga) | na wniosek (§ 4) |
| Kradzież | Czy coś zginęło, ktoś zabrał twoją rzecz? | art. 278 § 1 k.k. | z urzędu; na wniosek, gdy na szkodę osoby najbliższej (§ 4) |
| Przywłaszczenie | Czy ktoś zatrzymał twoją rzecz, nie oddał rzeczy powierzonej? | art. 284 § 1-2 k.k. | z urzędu; na wniosek, gdy na szkodę osoby najbliższej (§ 4) |
| Oszustwo | Czy ktoś wprowadził cię w błąd, żebyś oddał pieniądze lub mienie? | art. 286 § 1 k.k. | z urzędu; na wniosek, gdy na szkodę osoby najbliższej (§ 4) |
| Odwet | Czy coś z tego stało się po tym, jak wcześniej coś zgłosiłeś albo zeznawałeś? | (może być odrębnym czynem; ustal działanie, cel, czas i zweryfikuj kwalifikację) | - |
| Przemoc wobec bliskich, w obecności dzieci | Czy krzywda dotknęła też innych? Czy widziały to dzieci? | (zależnie od czynu; osobne zawiadomienie lub wątek, gdy pokrzywdzona jest inna osoba) | - |

## Osoba najbliższa (art. 115 § 11 k.k.) - uwaga dla trybu i AUDYTU-B

Brzmienie: „Osobą najbliższą jest małżonek, wstępny, zstępny, rodzeństwo, powinowaty w tej samej
linii lub stopniu, osoba pozostająca w stosunku przysposobienia oraz jej małżonek, a także osoba
pozostająca we wspólnym pożyciu.” Od tego zależy m.in. tryb przy art. 157 § 2, 284, 286 i
zastosowanie art. 207. „Wspólne pożycie” to pojęcie prawne, a nie potoczne „partner”, „mieszkamy
razem”: według uchwały 7 sędziów SN z 25.02.2016, I KZP 20/15, wymaga jednocześnie więzi duchowej
(emocjonalnej), fizycznej i gospodarczej (wspólne gospodarstwo domowe); obiektywnie usprawiedliwiony
brak jednej z nich nie wyklucza pożycia. Zob. `hardgate-spojnosc.md`, „Pozorne sprzeczności”.

## Poza dotychczasowym katalogiem — sprawdzaj zależnie od sprawy
- Kodeks wykroczeń (t.j. do ustalenia w ELI): szkoda w mieniu do progu wykroczenia, złośliwe niepokojenie, nieobyczajny wybryk.
- Ustawa o Policji / środki przymusu bezpośredniego - jako kontekst do art. 231 (nie do listy przepisów karnych).
- Kategorie specyficzne dla spraw z repo (monitoring, psychiatria, toksykologia) z teczek `00_sprawy/`.
