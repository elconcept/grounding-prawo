# HARDGATE spójności (F4)

## Po co

Prokurator porówna zawiadomienie z tym, co autor i inne osoby już mówiły organom. Niewyjaśniona
sprzeczność jest gotowym powodem, żeby relacji nie dać wiary. Bramka nie ocenia prawdziwości
relacji (K1). Pilnuje, żeby rozbieżności nie zostały przypadkowe i nienazwane, a jednocześnie
żeby rozbieżności pozorne nie zostały „naprawione” kosztem prawdziwej relacji autora.

## Zakres

- Dotyczy **wersji przeznaczonej do złożenia**. Draft, notatka, wersja robocza: bramka nie blokuje,
  w odpowiedzi dopisek „draft, bramka nieuruchomiona”.
- **Relacje autora pisma** (zakres blokujący): protokoły przesłuchań (jako świadek, pokrzywdzony,
  podejrzany, obwiniony), wyjaśnienia, protokoły ustnych zawiadomień, złożone pisma
  i zawiadomienia, oświadczenia do protokołu.
- **Relacje innych osób** (zakres informacyjny i źródło szczegółów): zeznania świadków,
  współpokrzywdzonych, funkcjonariuszy, notatki służbowe, protokoły czynności. Zgodnie z wytycznymi
  Policji („jak najwięcej konkretnych informacji”) to cenne źródło szczegółów do pisma, ale każda
  taka informacja w piśmie ma wskazane źródło: kto, kiedy, w jakiej formie („Jak zeznała X
  przed [organ] w dniu […], …”; „X powiedziała mi tego samego wieczoru, że …”).
  Rozbieżności autora z cudzymi relacjami nie blokują pisma; autor decyduje, czy i jak je nazwać.
- Nie porównujesz z draftami z `00_sprawy/*/drafty/` (to nie relacje złożone).

## Procedura

1. **Rejestr relacji.** Repo abogada:
   `python3 .Codex/skills/zawiadomienie-o-przestepstwie/scripts/rejestr_relacji.py --osoba "<nazwisko>" [--osoba <inicjały>] [--sygnatura <sygn>] [--tresc]`
   Uruchom dla autora i dla osób, o których wiadomo, że zeznawały. Skrypt wskazuje kandydatów; ty
   sprawdzasz, czyje to relacje. Zawsze zapytaj też użytkownika: „Czy ty albo ktoś inny składał
   w tej sprawie (albo w sprawach powiązanych) zeznania, wyjaśnienia lub pisma, których tu nie ma?”
2. **Lektura.** Każdą relację przeczytaj w całości (sidecar `.md`). Tekst z OCR z blokami
   `review_required` cytuj dopiero po sprawdzeniu w skanie (`ocr_kontrakt.py cytat <stem> "…"`).
3. **Ekstrakcja.** Wypisz twierdzenia faktyczne dotyczące epizodów z mapy, z kotwicą: plik, karta
   lub strona, kto mówi.
4. **Test pozornej sprzeczności** (niżej) - zanim cokolwiek nazwiesz sprzecznością.
5. **Porównanie** z mapą wewnętrzną. Klasy (dla relacji autora):

| Klasa | Kiedy | Co robisz |
|---|---|---|
| zgodne | to samo | nic |
| uzupełnienie | nowy szczegół, który nie przeczy wcześniejszemu (przypomniał się, zauważony później, nikt o to nie pytał) | dozwolone; w piśmie można to powiedzieć naturalnie, jeśli ma znaczenie („Dopiero później przypomniałem sobie, że…”) |
| rozbieżność pozorna | różne słowa, ten sam stan rzeczy; słowo potoczne vs pojęcie prawne; odpowiedź na inaczej postawione pytanie | nie jest sprzecznością; nie blokuje; nie „poprawiasz” autora. Jeśli prokurator może to źle odczytać, pismo może jednym zdaniem wyjaśnić znaczenie słowa |
| rozbieżność drobna | godzina, kolejność, liczba osób, szczegół drugoplanowy | pokaż autorowi, ustal wersję; w piśmie zaznacz, jeśli rozbieżność jest widoczna w aktach |
| sprzeczność | wcześniej X, teraz nie-X w istotnym punkcie, po teście pozornej sprzeczności | ⛔ blokada wersji do złożenia, dopóki autor nie rozstrzygnie |

6. **Rozstrzygnięcie sprzeczności** należy do autora:
   - (a) koryguje nową relację, albo
   - (b) podtrzymuje nową wersję. Wtedy pismo wprost wskazuje: „W protokole z dnia … zapisano, że …
     To nie oddaje tego, co się stało / pomyliłem się, ponieważ …” (stres, ból, pytanie nie padło,
     protokół zapisał skrót, nie czytałem protokołu przed podpisem, przypomniałem sobie później).
   Nie podsuwasz wyjaśnienia. Pytasz autora, skąd jego zdaniem różnica.
7. **Raport bramki** w odpowiedzi i jako dopisek przebiegu w `drafty/<pismo>/_HARDGATE.md`:

```
HARDGATE: [PRZESZŁA | ZABLOKOWANA]
Relacje autora porównane: <data, organ, sygnatura, karta, plik>
Relacje innych osób użyte / porównane: <osoba, data, organ, plik>
| # | Punkt | Wcześniej (kto, plik, k.) | Teraz | Klasa | Uzasadnienie klasy | Decyzja autora |
```

## Test pozornej sprzeczności

Zanim uznasz coś za sprzeczność, odpowiedz na cztery pytania:
1. **Czy to te same pojęcia?** Słowo potoczne („partner”, „mieszkamy razem”, „pobił”, „ukradł”)
   i pojęcie prawne („osoba najbliższa”, „wspólne pożycie”, „pobicie” z art. 158, „kradzież”)
   to różne porządki. Odpowiedź w jednym nie przesądza drugiego.
2. **Na jakie pytanie odpowiadała osoba?** Pytanie sądu o „stosunek do strony” dotyczy relacji
   prawnej (pokrewieństwo, małżeństwo, wspólne pożycie), nie emocjonalnej ani towarzyskiej.
3. **Czy obie wypowiedzi mogą być jednocześnie prawdziwe?** Jeśli tak - to nie sprzeczność.
4. **Czy znam definicję prawną z bazy, a nie z pamięci?** Jeśli nie, nie rozstrzygaj; oznacz
   do weryfikacji i nie blokuj.

**Ton:** nigdy nie pouczasz i nie strofujesz autora („to niespójne”, „pani wcześniej zeznała coś
innego”, „to podważy wiarygodność”). Rozbieżność pokazujesz rzeczowo jako pytanie.

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

## Sprzeczność z dokumentami instytucji (poza bramką)

Notatki policyjne, protokoły czynności, dokumentacja medyczna, pisma urzędów mogą opisywać
zdarzenie inaczej niż autor. To nie blokuje pisma i nie jest „prawdą” zastępującą relację (K1).
W piśmie: nazwij dokument i rozbieżność, przedstaw wersję autora („W notatce z interwencji
napisano, że …; tak nie było. …”). Jeśli autor uważa, że dokument jest nieprawdziwy, to osobny
epizod do lejka krzywd (art. 271 § 1 k.k. - poświadczenie nieprawdy przez funkcjonariusza).

## Przypadki szczególne

- **Zeznania odwołane lub wycofane** (np. oświadczenie o wycofaniu zeznań): ujmij w rejestrze
  zarówno zeznanie, jak i oświadczenie o wycofaniu. Porównuj z uwzględnieniem wycofania. Autor
  decyduje, czy i jak pismo o tym mówi.
- **Odmowa zeznań, odstąpienie od przesłuchania:** brak relacji nie jest sprzecznością.
- **Relacja z innej sprawy o tym samym zdarzeniu:** obejmij bramką (prokurator może ją pozyskać).
- **Autor nie pamięta, co zeznał, a protokołu nie ma w repo:** zapisz to w raporcie jako lukę;
  zaproponuj wniosek o wgląd w akta jako krok poza pismem.

## TODO v0.3
