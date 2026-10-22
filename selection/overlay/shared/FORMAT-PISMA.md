# FORMAT-PISMA - standard wyglądu pisma (DOCX do wydruku)

Obowiązuje każdy skill, który wydaje pismo do podpisu i złożenia: `pisma-proste-v2`, `pisma-procesowe-v3`
(wszystkie typy w `modules/typy/`), `zawiadomienie-o-przestepstwie`, `rodo-dsar-pl`. Ma pierwszeństwo przed
regułami czcionki i nagłówka w tych skillach (np. „Times New Roman 12 pt”, „tytuł pogrubiony”).
Nie dotyczy notatek i analiz wewnętrznych.

Wzór: rzeczywiste pismo adwokata złożone w sądzie (`INBOX/sample_pismo_w_sprawie.pdf`, poza repozytorium).

Przed redakcją wczytaj `shared/STYLE.md`. Publikację i historię wersji prowadź według
`shared/ARTEFAKTY-SPRAWY.md`: wersje Markdown zostają w `drafty/<pismo>/`, jedyny DOCX pisma jest w `legal/output/`.

## Narzędzie

Pismo powstaje z pliku źródłowego `.md` przez renderer, nie przez ręczny HTML, pandoc ani ad hoc DOCX.
Źródło `.md` (każda wersja `_vN`) leży w `<sprawa>/drafty/<pismo>/`, DOCX w `legal/output/`; obok DOCX nie ma
sidecara `.md`. Renderer wołaj przez `shared/format-pisma/wersja_pisma.py`, który pilnuje tego podziału:

```bash
python3 -I <skills>/shared/format-pisma/wersja_pisma.py nowe --md <sprawa>/drafty/<pismo>/<plik>_v1.md --output legal/output
```

PDF nie powstaje: użytkownik redaguje DOCX w Wordzie, drukuje i podpisuje. Składnię metryki i treści opisuje
docstring `render_pismo.py`.

- Kolejna wersja istniejącego pisma nie jest nowym renderem do `output/`: powstaje jako redline na DOCX
  z `output/` (`wersja_pisma.py start` i `redline`, cykl w `shared/ARTEFAKTY-SPRAWY.md`). Ręczne zmiany autora
  w DOCX `start` wypisuje jako różnice; przenieś je do nowej wersji `.md` w `drafty/`.
- `render_pismo.py --nadpisz` i ręczny render do `output/` są zakazane dla pisma, które ma już DOCX.
- Celuj w jedną stronę przy piśmie odpowiadającym na wezwanie lub pytanie sądu: tylko odpowiedź,
  krótka podstawa i wniosek.

## Krój i rozmiar

- Georgia 10 pt w całym piśmie. Gdy Georgii nie ma w systemie, może zostać krój zbliżony (szeryfowy,
  np. Gelasio, Charter) - DOCX wskazuje Georgię, a Word użytkownika ją wyświetli i wydrukuje.
- 14 pt mają tylko: imię i nazwisko (nazwa) nadawcy oraz nazwa organu adresata.
- 12 pt: wydział, oddział lub inna podjednostka organu (`adresat_jednostka`), np. „III Wydział Karny”.
- Tytuł pisma: wersaliki rozstrzelone, 12 pt, wyśrodkowany, bez pogrubienia; podtytuł 10 pt.
- Cytat blokowy 9,5 pt, wcięty z obu stron. Stopka: tylko numer strony z prawej.
- Tekst wyjustowany, interlinia ok. 1,25, odstęp 6 pt po akapicie. A4, marginesy 2-2,5 cm.

## Nagłówek

```
                                                Kraków, dnia 15 października 2026 r.
Jan Kowalski                                   ← 14 pt
ul. Przykładowa 1/2, 30-001 Kraków                     ← ulica/osiedle, kod, miasto: JEDNA linia
tel. 600 000 000, e-mail: …                          ← jedna linia

                                      Sąd Okręgowy w Krakowie   ← organ 14 pt, wyrównanie do prawej
                                            III Wydział Karny   ← podjednostka 12 pt, do prawej
                             ul. Przy Rondzie 7, 31-547 Kraków   ← 10 pt, jedna linia, do prawej

Sygn. akt:        III Ko 1/26                       ← etykieta i wartość w kolumnach
Wnioskodawca:     Jan Kowalski
```

- Telefon i e-mail nadawcy: wpisz, jeśli znasz je z dokumentów sprawy (wcześniejsze pisma, profil).
  Jeśli nie znasz - zapytaj użytkownika przed wygenerowaniem pisma. Nie zgaduj i nie wstawiaj
  pustych pól. Oświadczenie o nieposiadaniu telefonu lub e-maila wpisuj tylko na polecenie użytkownika.
- Blok adresata w całości wyrównany do prawej (Align Right), bez wcięcia.
- Adres organu sprawdź w dokumentach sprawy albo wyszukiwaniem, nie z pamięci.
- Podpis: imię i nazwisko autora pod miejscem na podpis; bez tytułu zawodowego i numeru wpisu.

## Wyróżnienia: pogrubienie i podkreślenie

- Pogrubienie i podkreślenie służą wyłącznie do wskazania sędziemu fragmentu, na którym opiera się
  pismo: przede wszystkim uchybienia organu (brak protokołu, brak pouczenia, sprzeczność w dokumentacji),
  kluczowego zarzutu albo rozstrzygającego słowa w cytacie. Nie wyróżniaj własnej odpowiedzi na pytanie
  sądu ani własnej oceny. W krótkim piśmie strony wystarcza jedno wyróżnienie albo żadne. Podkreślenie
  jest równorzędne z pogrubieniem (praktyka pism procesowych); w cytacie podkreślaj pojedyncze słowa.
- Nie pogrubiaj elementów formalnych: nagłówka, nazwisk, nazwy sądu w nagłówku, tytułu, śródtytułów,
  etykiet („Sygn. akt”), numerów punktów, dat, kwot w petitum (chyba że kwota jest sporna).
- Nie zastępuj struktury pogrubieniem: zamiast pogrubionego śródtytułu użyj numerowanego punktu
  („1. Co do zażalenia na zatrzymanie: …”) albo nagłówka `#`/`##` renderera (wersaliki, bez pogrubienia).
- Limit orientacyjny: 1 wyróżnienie na ok. 250 słów, nie więcej niż 1 w akapicie. Renderer ostrzega
  po przekroczeniu - wtedy zostaw tylko te, bez których sędzia mógłby przeoczyć tezę.

## Treść

- Układ punktowy jak we wzorze: punkty `1.`, `2.` z wcięciem wiszącym, podpunkty `a)`, `b)`; kolejne
  akapity punktu wcięte do jego tekstu.
- Na końcu: wniosek końcowy, podpis z prawej (linia kropkowana, imię i nazwisko), pod nim „Załączniki:”
  z numerowaną listą, jeśli są.
- Bez emoji, symboli i znaczników Markdown w gotowym piśmie.

## Redakcja i dynamika (wzory: `INBOX/III_RNs_1279_25_*` - pisma adwokata)

- Pierwsze zdanie punktu to odpowiedź na pytanie sądu albo teza. Potem „Wyjaśniam, że:” i podpunkty
  `a)`, `b)`, `c)`: jedna myśl i jej dowód w nawiasie w każdym. Najmocniejszy fakt idzie na początek.
- Krótkie zdania, bez zdań wielokrotnie złożonych. Każda myśl pada raz.
- Treść wcześniejszego pisma, wniosku lub zawiadomienia powtarzaj tylko skrótowo i tylko wtedy, gdy jest
  potrzebna; zwykle wystarczy odesłanie („wniosek, część …”, „pismo z 7 stycznia 2026 r.”).
- „k. N” oznacza wyłącznie karty akt sprawy, w której składasz pismo. Dokument z innej sprawy powołuj jako
  załącznik do wcześniejszego pisma („załącznik nr 4 do wniosku”) albo dołącz kopię jako nowy załącznik
  z opisem „(k. N akt sprawy …)”, albo napisz wprost, że znajduje się w aktach tamtej sprawy.
- Załączniki tylko wtedy, gdy sąd ich potrzebuje do rozstrzygnięcia i nie ma ich w aktach; dokument z innej sprawy, którą sąd
  może sam sprawdzić po sygnaturze, wystarczy wskazać. Nie powtarzaj adresu innego sądu, gdy jest taki sam jak adresata.
- Nie upraszczaj stanowiska strony do wersji organu: gdy strona kwestionuje podstawę czynności, nie pisz,
  że czynność nastąpiła „na zgłoszenie o X” jako o jej przyczynie; opisz, co organ zrobił i co powiedział.
- Kontrola przed wydaniem treści jest dwuetapowa i obowiązkowa, w tej kolejności:
  1. `pisz-po-polsku` - szlif językowy (z bramką `audyt_po_przepisaniu.py`),
  2. `humanizer-pl` - niezmodyfikowany upstream usuwający resztki wzorców AI.
  Potem `pierwsze-wrazenie-sedziego-pl`, a przy tezie spornej `atak-przeciwnika-pl`.
  Nie wolno pominąć żadnego etapu ani zamienić kolejności.

## Kontrola przed wydaniem

1. Pismo przeszło obowiązkowo `pisz-po-polsku`, a potem `humanizer-pl` (ta kolejność); żaden etap nie został pominięty.
2. Renderer przeszedł bez błędu; ostrzeżenie o wyróżnieniach rozpatrzone.
3. Telefon i e-mail nadawcy podane albo potwierdzone przez użytkownika jako nieznane.
4. W `drafty/<pismo>/` są tylko wersje `.md`, w `legal/output/` jeden `.docx` pisma; nie ma PDF
   (`wersja_pisma.py sprawdz --output legal/output` = `PASS`).
5. Treść mieści się w zakładanej objętości; podpis nie zostaje sam na stronie.
