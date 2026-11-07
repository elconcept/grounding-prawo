# Bramka redakcji pisma

Kontrakt dla każdego hosta i modelu, który redaguje pismo wychodzące (pismo procesowe, wniosek, skarga,
zawiadomienie, wezwanie). Repozytorium sprawy może egzekwować go skryptem (w `legal`:
`_narzedzia/bramka_redakcji.py`, hooki Claude Code i check CI). Kontrakt obowiązuje także bez skryptu.

## Etapy i kolejność

Każda wersja pisma przechodzi etapy w tej kolejności. Każdy etap ocenia tę samą, najnowszą wersję.

1. `zrodla`: zapytania semantyczne w Repertorium i w PrawMi dla każdej tezy pisma, weryfikacja trafień
   (`ZASADY-PLUGINU.md`, „Gdzie szukać”, pkt 4).
2. `pisz-po-polsku`: redakcja językowa (skill `pisz-po-polsku`).
3. `humanizer`: usunięcie wzorców AI (skill `humanizer-pl`) z bramką `audyt_po_przepisaniu.py`
   uruchomioną na tekście poprzedniej i nowej wersji tego samego formatu (MD z MD albo DOCX z DOCX).
   Audyt ocenia redakcję, więc przed nim usuń z obu tekstów numerację punktów i fragmenty dopisane
   w etapie `zrodla` (nowe orzeczenia i decyzje); te sprawdza raport `zrodla`. Wynik `OK`, `PASS` albo `UWAGI`
   przechodzi, `BLOKADA` oznacza poprawkę przepisania.
4. `marko`: recenzja treści (skill `marko-pl-content`); pełny werdykt i zarzuty idą też do odpowiedzi w czacie.
5. `sedzia`: test zimnego czytelnika (skill `pierwsze-wrazenie-sedziego-pl`); przy zawiadomieniu czytelnikiem jest prokurator.
6. `wiernosc` (tylko zawiadomienia i pisma do BSWP o naruszeniach): skill `deliverable-fidelity-pl` oraz
   `shared/scripts/retencja_pisma.py` wobec poprzedniej wersji.

## Wdrożenie natychmiast

Raport etapu nie kończy pracy nad zarzutem. Zarzut formalny (typografia, myślnik, dwukropek w zdaniu,
równoważnik w punkcie, zdanie zbyt długie, wypełniacz, pisownia, placeholder, pozostałość Markdown, utrata treści)
model poprawia od razu w nowej wersji pisma (`_vN+1`, bez zmian śledzonych). Potem uruchamia ponownie etapy
od tego, który zarzut wykrył. Zmiana tekstu unieważnia wszystkie wcześniejsze etapy tej wersji.
Zarzut merytoryczny (teza, dobór dowodów, długość wywodu, kwalifikacja) model przedstawia autorowi w czacie do decyzji.
Pismo wychodzi, gdy na najnowszej wersji nie ma żadnego otwartego zarzutu.

## Format raportu etapu

Raport to plik Markdown w folderze pisma (`output/<nazwa>/_KONTROLA_<etap>_vN.md`). Zawiera wiersz
`Wersja: <nazwa>_vN.docx` i sekcję `## Zarzuty`. Każdy zarzut to jeden wiersz:

```
- [FORMALNY] [WDROŻONY] akapit 12 - dwukropek w środku zdania; rozbite na dwa zdania w v14.
- [FORMALNY] [ODRZUCONY: formuła ustawowa] akapit 3 - „ustawa z dnia … r. – Kodeks cywilny”.
- [MERYTORYCZNY] [DO DECYZJI AUTORA] część III - wątek kamery przeważa nad żądaniem.
```

Statusy: `OTWARTY`, `WDROŻONY`, `DO DECYZJI AUTORA`, `ODRZUCONY: <powód>`. Na najnowszej wersji nie zostaje żaden
`OTWARTY`; zarzut formalny nie może mieć statusu `DO DECYZJI AUTORA`. Brak zarzutów zapisuje się wierszem `- brak`.
Raport `marko` zawiera wiersz `Werdykt: katastrofa|słabe|przeciętne|ok`; werdykt `słabe` albo `katastrofa`
oznacza nową wersję i ponowną recenzję. Raport `humanizer` zawiera wiersz `audyt_po_przepisaniu: PASS`.
Raport `sedzia` zawiera wiersz `Przekonanie: niski|średni|wysoki`.

Raport `zrodla` zawiera wiersze zapytań `- PrawMi <narzędzie>: <zapytanie> → <trafienia>` i
`- Repertorium (pl|eu): <zapytanie> → <trafienia>` oraz listę wszystkich sygnatur i decyzji z tekstu pisma:
`- [ORZECZENIE] II AKa 373/20 | SA Białystok 2020 | verify_ruling, SAOS 412345 | cytat sprawdzony`,
`- [DECYZJA] DS.523.399.2021 | Prezes UODO | search_uodo_decisions | brzmienie sprawdzone`,
`- [SPRAWA] II W 1342/26 | sygnatura własnej sprawy`. Pismo bez wiersza `[ORZECZENIE]` ani `[DECYZJA]`
wychodzi tylko z wierszem `BEZ ORZECZEŃ: decyzja autora <data>`.

## Kontrole mechaniczne

- `shared/scripts/lint_pisma.py <docx>`: myślnik, półpauza w zdaniu, dwukropek w środku zdania, zdanie ponad
  35 słów, pozostałości Markdown, placeholdery. Błąd lintu to zarzut formalny.
- `shared/scripts/retencja_pisma.py <poprzednia> <nowa> --wyjatki _ZMIANY_vN.md`: każdy cytat, godzina, data,
  karta akt, sygnatura i kwota poprzedniej wersji jest w nowej, a liczba słów nie maleje. Świadome usunięcie
  wpisuje się do `_ZMIANY_vN.md` z powodem.
- `format-pisma/render_pismo.py` odrzuca nagłówki `###` i głębsze; nie wolno ich obchodzić wpisaniem znaczników do DOCX.
