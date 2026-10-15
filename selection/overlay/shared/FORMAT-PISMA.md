# FORMAT-PISMA - standard wyglądu pisma (DOCX do wydruku)

Obowiązuje każdy skill, który wydaje pismo do podpisu i złożenia: `pisma-proste-v2`, `pisma-procesowe-v3`
(wszystkie typy w `modules/typy/`), `zawiadomienie-o-przestepstwie`, `rodo-dsar-pl`. Ma pierwszeństwo przed
regułami czcionki i nagłówka w tych skillach (np. „Times New Roman 12 pt”, „tytuł pogrubiony”).
Nie dotyczy notatek i analiz wewnętrznych.

Wzór: rzeczywiste pismo adwokata złożone w sądzie (`INBOX/sample_pismo_w_sprawie.pdf`, poza repozytorium).

## Narzędzie

Pismo powstaje z pliku źródłowego `.md` przez renderer, nie przez ręczny HTML ani ad hoc DOCX:

```bash
python3 -I <skills>/shared/format-pisma/render_pismo.py drafty/<pismo>/<plik>.md
```

Artefaktem końcowym jest `.docx` ze źródłem `.md` obok (sidecar). PDF nie powstaje: użytkownik
redaguje DOCX w Wordzie, drukuje i podpisuje. Składnię metryki i treści opisuje docstring skryptu.

- Renderer nie nadpisuje istniejącego `.docx` (mógł być poprawiony ręcznie). Gdy użytkownik zmienił
  DOCX, kolejne poprawki nanoś w tym DOCX albo uzgodnij z nim, czy wygenerować nową wersję
  (`--nadpisz` albo nowa nazwa, np. `_v2`).
- Zmianę w DOCX dokonaną przez użytkownika przenieś też do sidecara `.md`, żeby źródło odpowiadało plikowi.
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
- Pełnomocnik: pod podpisem rola („Za uczestnika - pełnomocnik”), nazwisko i nr wpisu.

## Wyróżnienia: pogrubienie i podkreślenie

- Pogrubienie i podkreślenie służą wyłącznie do wskazania sędziemu zdania, tezy lub fragmentu, na
  którym opiera się pismo: odpowiedzi na pytanie sądu, wniosku, kluczowego zarzutu, rozstrzygającego słowa
  w cytacie. Podkreślenie jest równorzędne z pogrubieniem (praktyka pism procesowych); w cytacie
  podkreślaj pojedyncze słowa, na które zwracasz uwagę.
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

## Kontrola przed wydaniem

1. Renderer przeszedł bez błędu; ostrzeżenie o wyróżnieniach rozpatrzone.
2. Telefon i e-mail nadawcy podane albo potwierdzone przez użytkownika jako nieznane.
3. W folderze pisma są tylko `.md` (źródło) i `.docx`; nie ma PDF.
4. Treść mieści się w zakładanej objętości; podpis nie zostaje sam na stronie.
