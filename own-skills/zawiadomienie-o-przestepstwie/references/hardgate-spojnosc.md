# AUDYT-B — rozbieżności i integralność źródeł (F4)

Nazwa pliku jest zachowana dla istniejących odwołań. Od v0.4 nie jest to blokujący test
zgodności. HARDGATE-A jest opisany w SKILL.md. Dokument instytucji nie ma automatycznego
pierwszeństwa przed relacją; audyt pomaga świadomie pokazać różnice, nie rozstrzyga prawdy.

## Procedura

1. Ustal dostępne złożone relacje autora i innych osób: protokoły, zeznania, wyjaśnienia,
   pisma i notatki. Nie traktuj draftu jako wcześniejszego złożonego oświadczenia.
   W repo abogada można użyć `scripts/rejestr_relacji.py --osoba "<nazwisko>" --tresc`
   (ścieżka względem folderu skilla). Skrypt daje kandydatów, nie ustala autorstwa.
   Zapytaj o brakujące wcześniejsze relacje; brak akt oznacz jako ograniczenie zakresu,
   nie przeszkodę do złożenia.
2. Czytaj dostępne relacje w kontekście pytania i całego opisu epizodu. Zapisz autora,
   datę, plik, stronę/kartę i brzmienie. Niepewny OCR sprawdź w skanie przed cytowaniem;
   jeśli skan niedostępny, nie przypisuj autorowi pewnego cytatu.
3. Porównaj z mapą: te same zdarzenia, zakres czasu, sens słów i perspektywa? Pominięcie
   szczegółu nie jest jego zaprzeczeniem. Nie przesądzaj na podstawie samych etykiet
   „partner”, „obcy”, „pobicie” czy „kradzież”. Definicje prawne sprawdzaj osobno.
4. Pokaż różnicę rzeczowo. Zapytaj otwarcie: „Jak rozumiesz różnicę między tym zapisem
   a tym, co pamiętasz teraz?”. Nie podsuwaj stresu, traumy lub błędu protokolanta jako
   wyjaśnienia. Zapisz odpowiedź, odmowę wyjaśnienia lub brak pamięci.
5. Zachowaj aktualną relację z jej źródłem i pewnością. Przy materialnej różnicy zaproponuj
   nazwanie jej w piśmie bez rozstrzygania: „W protokole zapisano X. Dziś pamiętam Y.
   Nie potrafię wyjaśnić tej różnicy” — ostatnie zdanie tylko jeśli autor tak odpowiedział.
   Autor może podtrzymać aktualną relację bez wyjaśnienia; nie blokuj złożenia.

## Statusy i decyzje

| Status | Znaczenie / działanie |
|---|---|
| ZGODNE | Nie wymaga osobnego komentarza w piśmie. |
| NOWY SZCZEGÓŁ | Nowe wspomnienie lub pominięty wcześniej wątek; dopytaj, nie traktuj jako automatycznej sprzeczności. |
| INNA PERSPEKTYWA | Inny obserwator, zakres pytania albo znaczenie słowa; zachowaj pochodzenie obu opisów. |
| RÓŻNICA DO WYJAŚNIENIA | Także istotne X / nie-X: pytanie do autora, bez obowiązku rozstrzygnięcia przed złożeniem. |
| UŻYTKOWNIK NIE PAMIĘTA | Nie wypełniaj luki; zakresy i niepewność pozostają jawne. |
| BŁĄD PROTOKOŁU WG UŻYTKOWNIKA | To stanowisko autora, nie ustalenie modelu; zachowaj jego opis błędu. |

Nierozstrzygnięta różnica, brak dokumentu i fragmentaryczna pamięć nie blokują pisma.
Zatrzymaj tylko przedstawianie świadomego fałszu jako faktu lub nierozwiązany dopisek modelu;
usuń taki dopisek i kontynuuj pozostałą część. Nie utożsamiaj rozbieżności ze świadomym fałszem.

## Raport poza pismem

W repo dopisz do `_HARDGATE.md`, poza nim podaj krótko przy wyniku:

```text
AUDYT-B: wykonany / częściowy (brak materiału) / brak znanych wcześniejszych relacji
Zakres: autor, data, organ, sygnatura, plik i karta/strona; ograniczenia dostępu/OCR
| # epizodu | Wcześniej (źródło) | Teraz (źródło) | Status | Odpowiedź / brak pamięci | Decyzja autora |
```

## Pozorne sprzeczności

Sprawdź znaczenie słów, pytanie, czas i możliwość współistnienia obu wypowiedzi.
Nie zakładaj automatycznie ani sprzeczności, ani jej pozorności bez kontekstu.
Jeśli potrzebna definicja prawna jest niezweryfikowana, zostaw ocenę otwartą.

### Wzorzec błędu (przypadek z repo, opis autora 09.10.2026)

N.C. zeznała w sądzie, na pytanie o stosunek do strony, że T.K. jest dla niej osobą obcą.
W zawiadomieniu opisywała T.K. jako partnera i wspólne mieszkanie. AI uznało to za sprzeczność
i krytycznie redagowało relację N.C. To był błąd merytoryczny i błąd tonu:
- „osoba najbliższa” (art. 115 § 11 k.k.) obejmuje m.in. „osobę pozostającą we wspólnym
  pożyciu” - to pojęcie prawne;
- wspólne pożycie wymaga jednocześnie trzech więzi - uchwała składu 7 sędziów SN z 25 lutego 2016 r., I KZP 20/15 (SAOS id 244683, odczyt 10.10.2026): „Zawarty w art. 115 § 11 k.k. zwrot «osoba pozostająca we wspólnym pożyciu» określa osobę, która pozostaje z inną osobą w takiej relacji faktycznej, w której pomiędzy nimi istnieją jednocześnie więzi duchowe (emocjonalne), fizyczne oraz gospodarcze (wspólne gospodarstwo domowe). Ustalenie istnienia takiej relacji, tj. «pozostawania we wspólnym pożyciu», jest możliwe także wtedy, gdy brak określonego rodzaju więzi jest obiektywnie usprawiedliwiony.”
  Wcześniej: postanowienie SN z 4 marca 2015 r., IV KO 98/14 (SAOS id 168509): wspólne pożycie nie
  zachodzi „zawsze wtedy, gdy wspólnemu zamieszkiwaniu towarzyszy silna, pozytywna więź
  emocjonalna”. Citator (SAOS, 10.10.2026): uchwała powoływana przez sądy powszechne do 04.2024,
  bez późniejszego odmiennego stanowiska SN w SAOS (pokrycie SAOS jest nierówne). Doktryna:
  M. Kubica, „Osoba pozostająca we wspólnym pożyciu na tle doktryny i judykatury w prawie karnym
  materialnym i procesowym”, Opolskie Studia Administracyjno-Prawne XV/3 (2017), s. 94-99
  (`04_opracowania/View of A person living in actual co-habitation…pdf`, sidecar `.md`): więź
  duchowa = m.in. zaufanie, szacunek, lojalność; gospodarcza = wspólne prowadzenie gospodarstwa
  domowego; fizyczna = współżycie;
- w praktyce: **duchowa** - zaufanie i uczucie (sama troska nie wystarcza), **gospodarcza** -
  wspólny budżet i wspólne gospodarstwo (samo wspólne mieszkanie ani składka na rachunki nie
  wystarcza), **fizyczna** - współżycie, którego obiektywnie usprawiedliwiony brak (choroba,
  wyjazd) nie wyłącza pożycia, a którego obecność sama niczego nie przesądza;
- N.C. mieszkała z T.K., współżyła z nim, troszczyli się o siebie i nazywała go partnerem
  (słowo zwyczajowe), ale nie było zaufania, wspólnego budżetu ani wspólnego gospodarstwa. Odpowiedź
  „obcy” była prawdziwa i zgodna z prawem; opis w zawiadomieniu też był prawdziwy.
Klasa poprawna: **rozbieżność pozorna**. Co wolno: jedno zdanie w piśmie, jeśli autor chce
(„Mówię o T.K. «partner», bo tak się potocznie mówi; nie prowadziliśmy wspólnego gospodarstwa
ani budżetu”). Czego nie wolno: blokować, „korygować” relacji, sugerować nieprawdy.

## Różnice z dokumentami instytucji

Notatki policyjne, protokoły czynności, dokumentacja medyczna, pisma urzędów mogą opisywać
zdarzenie inaczej niż autor. To nie blokuje pisma i nie jest „prawdą” zastępującą relację (K1).
W piśmie: nazwij dokument i rozbieżność, przedstaw wersję autora („W notatce z interwencji
napisano, że …; tak nie było. …”). Jeśli autor uważa, że dokument jest nieprawdziwy, to osobny
wątek do dopytania o powstanie, autora i treść dokumentu; sama różnica nie przesądza
poświadczenia nieprawdy ani świadomości funkcjonariusza. Kwalifikację sprawdź osobno.

## Przypadki szczególne

- **Zeznania odwołane lub wycofane** (np. oświadczenie o wycofaniu zeznań): ujmij w rejestrze
  zarówno zeznanie, jak i oświadczenie o wycofaniu. Porównuj z uwzględnieniem wycofania. Autor
  decyduje, czy i jak pismo o tym mówi.
- **Odmowa zeznań, odstąpienie od przesłuchania:** brak relacji nie jest sprzecznością.
- **Relacja z innej sprawy o tym samym zdarzeniu:** obejmij audytem (prokurator może ją pozyskać).
- **Autor nie pamięta, co zeznał, a protokołu nie ma w repo:** zapisz to w raporcie jako lukę;
  zaproponuj wniosek o wgląd w akta jako krok poza pismem.
