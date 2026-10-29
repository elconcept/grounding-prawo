# Zgłoszenia, etap sprawy i odcięcie od pism procesowych

Obowiązuje od v0.9. Źródłem prawdy o tym, co zostało złożone, jest notatka `Zgłoszenia — <Autor>`
w Basic Memory (`legal`, `relacje/<autor-slug>/`). Relacja i log opisują zdarzenia i wypowiedzi; rejestr pism
opisuje wersje projektów. Zgłoszenia zapisuje tylko to, co autor wprost potwierdził.

## 1. Co liczy się jako złożone

- **Złożone** = autor wprost powiedział, że dane zawiadomienie zostało złożone (np. „złożyłem zawiadomienie
  12.09”, „zgłosiłam na policji, mam numer”). Zapisz z cytatem i ID sesji (`#Snnn`).
- **Nie liczą się:** „przygotowałem”, „chcę złożyć”, „mam wydruk”, plik w teczce, podpis pod pismem,
  zapowiedź, wizyta na komisariacie bez wskazania zgłoszenia, wzmianka o interwencji, wniosek modelu.
  Takie informacje idą do sekcji `Do ustalenia` i pytasz autora wprost.
- **Złożone bez daty:** zapisz `data: nieznana` i dopytaj o datę, organ i numer.
- **Zmiana zdania przez autora** („jednak nie złożyłem”): nowy wpis z korektą i odnośnikiem do wcześniejszego;
  nie usuwaj poprzedniego.
- Dla każdego złożonego zawiadomienia zapisz: `Z-ID` (stały, kolejny, np. `Z001`), datę złożenia, organ
  (pełna nazwa i adres sprawdzone wyszukiwaniem, nie z pamięci), tytuł i wersję pisma (ścieżka w `drafty/` lub `output/`),
  epizody (`E…`), czyny z opisem i kwalifikacją (kwalifikację sprawdź urzędowym tekstem; brak przepisu nie blokuje wpisu),
  sygnaturę (gdy znana; inaczej `brak — do ustalenia`), etap (§3), źródło (wypowiedź autora `#Snnn`, dokument organu, potwierdzenie nadania).

## 2. Lista czynów zgłoszonych i sygnatur

Sekcja `Zgłoszone czyny i sygnatury`, jeden wiersz na czyn (zdarzenie + kwalifikacja do weryfikacji):

| Czyn (opis, epizody) | Zgłoszony w | Organ | Sygnatura | Etap | Źródło |
|---|---|---|---|---|---|

- Sygnatura wpisywana tylko z dokumentu organu/sądu albo podana przez autora z oznaczeniem źródła.
  Brak sygnatury nie blokuje wpisu; w polu wpisz `brak` i dopisz pytanie do `Pytania otwarte`.
- Jeden czyn może być zgłoszony w kilku zawiadomieniach — wtedy wiersz wskazuje wszystkie `Z-ID`.
- Czyn, którego autor nie zgłosił, nie trafia do tej listy. Trafia do `Do ustalenia` albo do listy niezgłoszonych
  krzywd (`ciaglosc-sesji.md`, „Dotychczas niezgłoszone krzywdy”).

## 3. Etap sprawy

Etap ustala się dla każdego postępowania osobno, nie dla całej relacji:

| Etap | Znaczenie | Tryb kolejnego pisma |
|---|---|---|
| `przygotowawczy` | postępowanie przygotowawcze, sprawdzające, dochodzenie lub śledztwo przed organem | tor zawiadomienia (§4) |
| `wykroczeniowy` | postępowanie w sprawie o wykroczenie przed organem, przed wpływem wniosku do sądu | tor zawiadomienia (§4); tryb i organ sprawdź urzędowo |
| `sadowy` | sprawa przed sądem (§4a) | pisma procesowe (§4a) |
| `zakonczony` | umorzenie, odmowa, inne rozstrzygnięcie organu (data decyzji i doręczenia) | zażalenie/środek zaskarżenia wg `zazalenie-na-postanowienie-prokuratora`; nie mechaniczne ponowne zgłoszenie |
| `nieustalony` | status nie wynika z materiału ani z wypowiedzi autora | dopytaj przed wyborem formy |

Potoczne „wyjaśniające” nie przesądza rodzaju postępowania; ustal organ i etap z dokumentu lub z wprost podanej informacji.

## 4. Tor zawiadomienia (etapy przed sądem)

Dopóki postępowanie jest przed organem, uzupełnienia, wnioski towarzyszące i nowe zawiadomienia idą **tym samym
torem co zawiadomienie o przestępstwie** (`SKILL.md`, HARDGATE-ZOP / NARRATIVE-FIRST). Nie stosuj do nich
pipeline'u pism procesowych (`pisma-procesowe-v3`, `pisma-proste-v2`) ani ich bramek dowodowych.

- **Uzupełnienie** do sprawy, w której zawiadomienie już złożono: odniesienie do `Z-ID` i sygnatury, tytuł
  „Uzupełnienie zawiadomienia o popełnieniu przestępstwa z dnia …” (`references/forma.md`). Nie zastępuje złożonej wersji.
- **Nowe zawiadomienie:** dotyczy czynu, którego nie ma w `Zgłoszone czyny i sygnatury`. Nowy szczegół lub nowa
  kwalifikacja tego samego zdarzenia nie oznaczają nowego czynu.
- **Wniosek towarzyszący** w tym etapie (np. uzupełniające przesłuchanie, zabezpieczenie) też na torze zawiadomienia:
  relacja zachowana, weryfikacja prawa dotyczy wyłącznie przepisów, na które się powołuje.

## 4a. Odcięcie: sprawa przed sądem

Odcięcie następuje, gdy postępowanie przygotowawcze się zakończyło i sprawa jest przed sądem, czyli wpłynął do sądu
akt oskarżenia, prywatny akt oskarżenia, wniosek o ukaranie albo inne pismo wszczynające postępowanie sądowe.
Wpis: data wpływu i sygnatura sądowa w `Zgłoszone czyny i sygnatury`, etap `sadowy`.

Od odcięcia obowiązują zasady **pism procesowych** (`pisma-procesowe-v3`, a dla krótkich pism `pisma-proste-v2`):

- zawiadomienie-o-przestepstwie **nie generuje** kolejnego zawiadomienia o tych samych zdarzeniach;
- ustal rolę autora w tym postępowaniu (oskarżyciel posiłkowy, oskarżyciel prywatny, świadek, osoba bez roli procesowej)
  i dopuszczalną czynność; to przesądza, czy pismo w ogóle przysługuje;
- terminy i wymogi formalne sprawdzaj w aktualnym tekście ustawy; nie przenoś progów dowodowych z relacji;
- relacja i log w Basic Memory pozostają źródłem: nowe fakty z relacji trafiają do pisma procesowego zgodnie z rolą autora;
- zasady relacji (K1–K4) nie są w tym torze obowiązujące; obowiązują reguły pism procesowych.

Sprawa wraca do etapu przygotowawczego (np. zwrot sprawy, uzupełnienie postępowania): ustal to urzędowo i przywróć tor §4.
Nie zakładaj powrotu z samej relacji autora.

## 5. Wybór kolejnego pisma

Dla każdego epizodu z relacji sprawdź:

1. Czyn nieobjęty żadnym `Z-ID` → nowe zawiadomienie (§4), chyba że dołącza do postępowania już prowadzonego — wtedy uzupełnienie.
2. Czyn zgłoszony, etap `przygotowawczy` lub `wykroczeniowy` → uzupełnienie wskazujące `Z-ID` i sygnaturę (§4).
3. Czyn w sprawie `sadowy` → pismo procesowe (§4a), bez nowego zawiadomienia.
4. Czyn `zakonczony` → środek zaskarżenia wg właściwego skilla, po sprawdzeniu decyzji i terminu.
5. Każdy epizod ma wpis w piśmie albo jawne wyłączenie przez autora. Nie pomijaj krzywdy tylko dlatego, że wymaga innego pisma.

## 6. Wejście: weryfikacja i tworzenie systemu plików

Przy każdym wejściu w relację (przed pierwszym pytaniem):

1. **Sprawdź pliki.** `list_directory(project="legal", dir_name="relacje/<autor-slug>")`, potem `read_note`
   (co najmniej `include_content=False` z checksum). Oczekiwane notatki: `Relacja zdarzeń — <Autor>`,
   `Log zeznań — <Autor>`, `Rejestr pism — <Autor>`, `Pytania otwarte — <Autor>`, `Zgłoszenia — <Autor>`, katalog `wersje/`.
2. **Brak systemu (pierwsze utworzenie).** Jeśli brakuje `Zgłoszenia` albo wszystkich notatek, **przed utworzeniem czegokolwiek**
   poproś autora o przesłanie **wszystkich złożonych zawiadomień** (pliki, skany lub tekst) razem z potwierdzeniami nadania,
   pismami organu o wszczęciu, odmowie, wezwaniu lub zawieszeniu oraz pismami sądu, jeśli są. Napisz wprost:
   „Do założenia systemu potrzebuję wszystkich złożonych zawiadomień. Jeśli żadnego nie złożono, napisz to wprost.”
   Czekaj na odpowiedź. Wspomnienia zbieraj w rozmowie i zapisz po założeniu systemu. Brak zgłoszeń
   zapisuj tylko po wyraźnym oświadczeniu autora (`Złożone: brak — oświadczenie autora #Snnn`).
3. **Uzupełnienie braków.** Istniejące notatki nie są nadpisywane. Brakujące utwórz według `basic-memory-relacja.md`.
   Porównaj: każdy `Z-ID` z rejestru o statusie ZŁOŻONE ma wpis w `Zgłoszenia`; każde złożone zawiadomienie z przesłanych
   materiałów ma `Z-ID`; sygnatury z dokumentów są w liście. Rozbieżności idą do `Do ustalenia` i do pytania
   (AUDYT-B, nie blokuje).
4. **Log i wynik.** Dopisz wpis logu `porzadkowanie` z listą: zweryfikowane, utworzone, uzupełnione, brakujące.
   W odpowiedzi podaj tę samą listę jednym blokiem, bez historii.

## 7. Zapis po zmianie zgłoszeń

Po każdej wypowiedzi, która zmienia `Zgłoszenia` (złożenie, data, organ, sygnatura, etap, decyzja organu):
1. wpis logu (rodzaj `ustalenie_z_dokumentu` albo `szczegol`/`korekta`, z cytatem autora);
2. aktualizacja `Zgłoszenia` (nowy `Z-ID` lub zmiana wiersza; wpisy nie są usuwane);
3. aktualizacja `Rejestr pism` (status pisma) i `Pytania otwarte`;
4. odczyt potwierdzający.
