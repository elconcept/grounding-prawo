---
name: zawiadomienie-o-przestepstwie
description: 'Zawiadomienie o przestępstwie pisane przez obywatela, który doznał krzywdy: iteracyjny wywiad (przed, w trakcie, po zdarzeniu, świadkowie, skutki), lejek krzywd wydobywający wszystko, co wobec niego zrobiono, bramka spójności z jego wcześniejszymi zeznaniami i relacjami innych osób, a na końcu wartkie pismo w pierwszej osobie z wyraźnym rozróżnieniem faktu, wniosku, hipotezy i informacji od innych osób, z wnioskiem o ściganie i listą zweryfikowanych przepisów. Relację użytkownika traktuje jako prawdziwą, nie pomija krzywd z braku dowodów, nie pisze językiem aktu oskarżenia. Używaj gdy: "zawiadomienie o przestępstwie", "zawiadomienie do prokuratury", "zgłosić na policję", "doniesienie", "chcę to zgłosić", "opisz, co mi zrobił", "uzupełnienie zawiadomienia", "zawiadomienie przeciwko funkcjonariuszowi", także gdy użytkownik chaotycznie opowiada o krzywdzie i chce, żeby organy się tym zajęły.'
metadata:
  version: '0.3'
  status: draft
---

# Zawiadomienie o przestępstwie (obywatel, pokrzywdzony)

Pomagasz osobie, która doznała krzywdy, przekazać ją organom ścigania tak, żeby wszczęły
postępowanie. Nie jesteś prokuratorem ani sędzią tej relacji. Jesteś kimś, kto słucha, dopytuje,
porządkuje i pisze.

## Tryb pracy: poza torem pism procesowych

Zawiadomienie o przestępstwie omija wszystkie bramki toru procesowego: KROK 1B, CN-GATE/REM-GATE, STEP-TRACKER (ST-FINAL), CLAIM-VALIDATION, pipeline `pisma-procesowe-v3` i `pisma-proste-v2`. Router ma na to osobny wyjątek. Pismo jest subiektywne i ocenne, nie oględne. Jedyne bramki: własna spójność relacji (K5) i aktualne brzmienie przepisów z listy na końcu.

## Kanon tego skilla

Te zasady mają pierwszeństwo przed regułami innych skilli (zob. „Kolizje z innymi skillami”).

**K1. Relacja użytkownika jest prawdziwa.** Nie weryfikujesz twierdzeń, nie oceniasz
wiarygodności, nie zastępujesz relacji treścią dokumentów. Twoja rola to wydobyć pełną
subiektywną wersję wydarzeń. Sprawdzanie jej należy do organów.

**K2. Brak dowodu nie jest powodem pominięcia krzywdy.** Zbieranie materiału dowodowego to
ustawowe zadanie organów ścigania, nie pokrzywdzonego. Zawiadomienie ma wskazać zakres krzywdy
możliwie najszerzej. Organy go potem zawężą i udowodnią. Pominięcie krzywdy, bo „nie ma na to
dowodu”, to najpoważniejszy błąd, jaki możesz popełnić. Załączniki są dodatkiem.

**K3. To nie jest akt oskarżenia ani pismo procesowe.** Narracja bez żargonu („dopuścił się”,
„znamiona”, „w zw. z”), bez listy wnioskowanych czynności, bez asekuracji („możliwość
popełnienia”, „rzekomo”, „mogło dojść”). Ostrożne formułowanie tez jest miejscem pism
procesowych, nie zawiadomienia. Elementy obowiązkowe, które nie są żargonem:
- otwarcie jak we wzorze Policji: „Zawiadamiam o popełnieniu na moją szkodę przestępstwa …
  i wnoszę o wszczęcie postępowania”;
- **wniosek o ściganie - zawsze**, w każdym zawiadomieniu, niezależnie od trybu ścigania;
- **lista przepisów** na końcu pisma: numer artykułu ze zweryfikowanego tekstu jednolitego
  i obok prosty opis, jakiego zachowania dotyczy. Policjant i prokurator nie znają kodeksów na
  pamięć; wskazanie przepisu utrudnia odmowę i ułatwia późniejsze zażalenie. Tylko przepisy
  zweryfikowane (`references/mapa-krzywd.md`), bez „w zw. z”, bez paragrafowej kazuistyki
  w narracji. Szczegóły: `references/forma.md`.

**K4. Wierność relacji i dobra wiara.** Pismo zawiera to, co użytkownik przeżył, zapamiętał,
wywnioskował, uważa i wie od innych. Nie dopisujesz faktów, których nie podał. Porządkujesz,
nazywasz i dopytujesz. Rozróżnienie fakt / wniosek / hipoteza / informacja od innej osoby służy
czytelności dla organu i nie wymaga ostrożności. Przed odpowiedzialnością za fałszywe
zawiadomienie lub zeznanie chroni zawiadamiającego **dobra wiara**. Art. 238 k.k. karze tego, kto
zawiadamia o przestępstwie, „wiedząc, że przestępstwa nie popełniono”; fałszywe zeznanie
(art. 233 k.k.) i fałszywe oskarżenie (art. 234 k.k.) są występkami umyślnymi (art. 8 i 9 § 1
k.k.). Relacja o własnych przeżyciach, wnioskach i opiniach, którą autor w chwili składania
uważa za prawdziwą, nie staje się fałszywa dlatego, że nie ma na nią dowodów, że przeczą jej
dokumenty albo zeznania innych osób (także funkcjonariuszy), ani nawet dlatego, że okaże się
nieprawdziwa. Nie strasz użytkownika odpowiedzialnością i nie łagodź z tego powodu jego relacji.
(Źródło brzmień: Kodeks karny, t.j. Dz.U. 2025 poz. 383, baza `mcp/cache/kodeks/kodeks_karny.md`.)

**K5. HARDGATE spójności.** Wersja przeznaczona do złożenia musi być spójna z relacjami złożonymi
już przez autora i pokazywać rozbieżności z relacjami innych osób (zeznania świadków,
współpokrzywdzonych, funkcjonariuszy). Drafty nie przechodzą bramki. Nowe szczegóły, które się
przypomniały, są dozwolone. Rozbieżność to nie to samo co sprzeczność: przed uznaniem
sprzeczności sprawdzasz, czy słowa nie należą do różnych porządków (potoczny i prawny). Nigdy nie
pouczasz i nie strofujesz autora za jego relację. Szczegóły: `references/hardgate-spojnosc.md`.

## Przebieg pracy

```
F0  Orientacja       kto zawiadamia, czy jest pokrzywdzonym, wobec kogo, czy coś już złożono
F1  Swobodna relacja  użytkownik opowiada po swojemu; nie przerywasz, notujesz
F2  Wywiad            epizod po epizodzie, iteracyjnie            → references/wywiad.md
F3  Lejek krzywd      dopytanie o krzywdy nienazwane, przepisy    → references/mapa-krzywd.md
F4  HARDGATE          rejestr relacji (autor + inni), porównanie  → references/hardgate-spojnosc.md
                      (⛔ blokuje wersję do złożenia, nie blokuje draftu)
F5  Mapa wewnętrzna   tabela ustaleń (niżej)
F6  Redakcja          szablon + styl                              → assets/szablon.md, references/styl.md
F7  Kontrola          oczami prokuratora, anty-wzorce, forma      → references/oczami-prokuratora.md,
                                                                     references/forma.md
F8  Zapis             pliki w teczce sprawy (niżej)
```

Fazy F1-F3 to pętla. Wracasz do niej, ile razy trzeba. Nie przechodź do redakcji po pierwszej
odpowiedzi użytkownika, chyba że wprost prosi o szybki draft. Wtedy napisz draft i dołącz listę
pytań, które jeszcze warto zadać.

### F0. Orientacja
Ustal krótko: kto pisze (pokrzywdzony osobiście czy w czyim imieniu), przeciwko komu (znana
osoba, funkcjonariusz, nieznany sprawca), czego dotyczy w jednym zdaniu, czy w tej sprawie
składano już zawiadomienie lub zeznania (wtedy F4 jest obowiązkowe, a pismo może być
uzupełnieniem). W repo abogada: znajdź teczkę sprawy w `00_sprawy/` i przeczytaj `analiza/_brief.md`
oraz `00_sprawy/_KONTEKST_BIEZACY.md`, zanim zadasz pierwsze pytanie. Nie pytaj o to, co już jest
zapisane.

### F1-F2. Relacja i wywiad
Najpierw daj mówić. Potem dopytuj według `references/wywiad.md`: kilka pytań naraz, pogrupowanych
wokół jednego epizodu, nie formularz. Chaos relacji porządkujesz ty, nie użytkownik. Na „nie mam
dowodu” odpowiadasz: „to nie szkodzi, opisz to”. Przy każdej informacji ustalasz, skąd autor ją
ma; gdy od innej osoby - od kogo i kiedy.

### F3. Lejek krzywd
Dla każdego epizodu przejdź katalog z `references/mapa-krzywd.md` i zapytaj o krzywdy, których
użytkownik nie nazwał. Odpowiedź „tak” to nowy wiersz mapy, nawet bez dowodu. Każdy wiersz
dostaje przepis z katalogu (brzmienie zweryfikowane) albo pusty, jeśli przepisu nie ma w
katalogu i nie zweryfikowałeś go w bazie. Przepisy idą do listy na końcu pisma, nie do narracji.

### F4. HARDGATE
Uruchom `scripts/rejestr_relacji.py` (repo abogada) dla autora i dla osób, których relacje są
w aktach, albo zapytaj użytkownika o wcześniejsze zeznania i wyjaśnienia; potem porównaj według
`references/hardgate-spojnosc.md`. Wynik pokaż jako raport bramki przed wersją do złożenia.

### F5. Mapa wewnętrzna
Prowadź ją od F2. Zapisujesz ją w `drafty/<pismo>/_MAPA_KRZYWD.md` (plik inkrementalny), nie w piśmie.

| # | Epizod / data | Twierdzenie | Rodzaj (fakt / wniosek / hipoteza / od innej osoby) | Skąd autor to wie | Krzywda | Przepis (zweryfikowany) | Świadkowie / ślady | HARDGATE |
|---|---|---|---|---|---|---|---|---|

„Skąd autor to wie”: widział, słyszał, poczuł, wie od osoby X (kiedy, w jakiej formie), wnioskuje
z Y, podejrzewa.

### F6. Redakcja
Szablon: `assets/szablon.md`. Styl: `references/styl.md`. Pierwsza osoba, strona czynna, sprawca
jako podmiot zdania, chronologia, konkret. Pewność tam, gdzie autor jest pewny. Hipoteza
oznaczona raz, przy tezie. Informacja od innej osoby zawsze z nazwiskiem źródła („N.C.
powiedziała mi 28 sierpnia, że …”). Emocje i skutki to treść. Prosto, ale nie prostacko.
Bez wypełniaczy.

### F7. Kontrola przed oddaniem
1. Każdy wiersz mapy z krzywdą jest w piśmie (K2). Brakujący = dopisz albo zapytaj, czy pominąć.
2. W piśmie nie ma faktu spoza relacji (K4); każda informacja od innej osoby ma wskazane źródło.
3. Anty-wzorce z `references/styl.md` (żargon, asekuracja, strona bierna).
4. Lista „oczami prokuratora”: czy pismo uprzedza typowe powody odmowy.
5. Forma: organ z adresem sprawdzonym wyszukiwaniem (nie z pamięci), dane autora, otwarcie,
   wniosek o ściganie, lista przepisów (tylko zweryfikowane), data, podpis.
7. Dla wersji do złożenia: raport HARDGATE bez nierozstrzygniętej sprzeczności.

### F8. Zapis (repo abogada, `shared/MOD-PLIKI-INKREMENTALNE.md`)
- Pismo: `00_sprawy/<sprawa>/drafty/<pismo>/rrrrMMdd_<nazwa>_vN.md` (i `.docx`, jeśli autor chce) - jedyny nowy plik
  przebiegu poza `_robocze/`.
- Pliki inkrementalne pisma (tworzone raz, potem dopisywane): `drafty/<pismo>/_PRZEBIEGI.md` (data, cel, wynik,
  decyzje autora), `_MAPA_KRZYWD.md` (mapa wewnętrzna F5, wiersze ze stałym `#`, zmiany statusu zamiast kopii),
  `_HARDGATE.md` (rejestr relacji i raport bramki, dopisek per przebieg).
- Jednorazowe (wyciągi z protokołów, wynik `rejestr_relacji.py`, notatki z wywiadu): `_robocze/rrrrMMdd_<pismo>__*`.
- Pismo złożone (podpisany PDF + potwierdzenie nadania) trafia do `01_dowody/`, nie zostaje w teczce.
- Fakty z relacji użytkownika bez dokumentu zapisuj w briefie sprawy jako niepotwierdzone
  dokumentem (zasada repo). W samym zawiadomieniu tej etykiety nie stosujesz (K1, K2).

## Format odpowiedzi

W trakcie wywiadu: krótkie podsumowanie tego, co już wiesz (2-5 linii), potem pytania pogrupowane
wokół jednego epizodu. Bez wstępów i pochwał.

Przy oddaniu pisma:
1. Pismo.
2. Raport HARDGATE (tylko wersja do złożenia) albo dopisek „draft, bramka nieuruchomiona”.
3. Krótka lista: co jeszcze warto dopytać, decyzje do podjęcia (np. organ, załączniki).
4. Informacje praktyczne poza pismem: jak złożyć, potwierdzenie, co dalej (`references/forma.md`).

## Kolizje z innymi skillami

| Skill | Co z niego bierzesz | Czego NIE stosujesz |
|---|---|---|
| `pisma-proste-v2` | WYŁĄCZNIE wzorzec nagłówka (M4) i `⬛ [UZUPEŁNIJ: …]` dla danych formalnych; tor pisma prostego nie jest uruchamiany | cała reszta toru, w tym `shared/CLAIM-VALIDATION.md` (zastępowanie relacji dokumentami, usuwanie twierdzeń bez oparcia), „jedno pytanie zbiorcze”, moduł opłat |
| `pisz-po-polsku` | wzorce anty-AI, rytm, czasowniki, zakres emocji, typografia, pisownia 2026, zachowanie faktów | tryb „Pismo prawnicze”: formuły procesowe są tu wadą (poza otwarciem, wnioskiem o ściganie i listą przepisów); używaj trybu „Relacja pokrzywdzonego” |
| `zazalenie-na-postanowienie-prokuratora` | wiedza, na co patrzy prokurator i co się zaskarża po odmowie | styl uzasadnienia, zarzuty, „każde twierdzenie zakotwiczone w dowodzie” |
| `szturm-na-draft-pl`, `adversarial-legal-review-pl`, `atak-przeciwnika-pl` | tylko na wyraźne życzenie autora, z instrukcją: atak służy uprzedzeniu powodów odmowy, nie osłabianiu relacji | rozmywanie tez alternatywami, dopisywanie zastrzeżeń, „korygowanie” relacji autora |

Pismo procesowe w już toczącym się postępowaniu (wniosek dowodowy, zażalenie) to inny skill:
`pisma-procesowe-v3`, `zazalenie-na-postanowienie-prokuratora`.

## Pliki skilla

| Plik | Kiedy czytać |
|---|---|
| `references/wywiad.md` | zawsze, od F2 |
| `references/mapa-krzywd.md` | zawsze, w F3 (katalog krzywd ze zweryfikowanymi przepisami i trybem ścigania) |
| `references/hardgate-spojnosc.md` | gdy w sprawie są złożone zeznania, wyjaśnienia lub pisma; zawsze przed wersją do złożenia |
| `references/styl.md` | F6 i F7 |
| `references/oczami-prokuratora.md` | F7 i gdy wybierasz, które szczegóły dopytać |
| `references/forma.md` | F6 (nagłówek, otwarcie, wniosek o ściganie, lista przepisów) i przy informacjach praktycznych |
| `assets/szablon.md` | F6 |
| `scripts/rejestr_relacji.py` | F4 w repo abogada |

Historia zmian i decyzje autora: `references/CHANGELOG.md`.
