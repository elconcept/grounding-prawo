# Bramka redakcji pisma (kontrole mechaniczne)

Kopia części kontraktu pluginu, która dotyczy zawiadomienia. Każda nowa wersja pisma wychodzącego przechodzi poniższe
kontrole; oceniają one zawsze najnowszą wersję.

## Wdrożenie natychmiast

Raport kontroli nie kończy pracy nad zarzutem. Zarzut formalny (typografia, myślnik, dwukropek w środku zdania,
równoważnik w punkcie, zdanie zbyt długie, wypełniacz, pisownia, placeholder, pozostałość Markdown, utrata treści)
popraw od razu w nowej wersji (`_vN+1`, bez zmian śledzonych), po czym powtórz kontrole od tej, która zarzut wykryła.
Zmiana tekstu unieważnia wcześniejsze kontrole tej wersji. Zarzut merytoryczny (teza, dobór dowodów, długość wywodu,
kwalifikacja) przedstaw autorowi w rozmowie do decyzji; zarzutu formalnego nie przekazuj autorowi do decyzji.
Pismo wychodzi, gdy na najnowszej wersji nie ma otwartego zarzutu.

Zarzuty zapisuj w `output/<nazwa>/_KONTROLA_vN.md` (wiersz `Wersja: <nazwa>_vN.docx`, sekcja `## Zarzuty`):

```
- [FORMALNY] [WDROŻONY] akapit 12 - dwukropek w środku zdania; rozbite na dwa zdania w v14.
- [MERYTORYCZNY] [DO DECYZJI AUTORA] część III - wątek kamery przeważa nad żądaniem.
```

Statusy: `OTWARTY`, `WDROŻONY`, `DO DECYZJI AUTORA`, `ODRZUCONY: <powód>`. Brak zarzutów: `- brak`.
Zasada HARDGATE-ZOP ma pierwszeństwo: żaden zarzut nie może prowadzić do usunięcia epizodu, skutku ani cytatu autora.

## Kontrole mechaniczne

- `scripts/lint_pisma.py <docx>`: myślnik, półpauza w zdaniu, dwukropek w środku zdania, zdanie ponad 35 słów,
  pozostałości Markdown, placeholdery. Błąd lintu to zarzut formalny.
- `scripts/retencja_pisma.py <poprzednia> [<starsze> ...] <nowa> --wyjatki _ZMIANY_vN.md`: każdy cytat, godzina, data,
  karta akt, sygnatura i kwota każdej wcześniejszej wersji jest w nowej, a liczba słów nie maleje. Świadome usunięcie
  wpisuje się do `_ZMIANY_vN.md` z powodem.
- `scripts/render_pismo.py` odrzuca nagłówki `###` i głębsze; nie obchodź tego wpisywaniem znaczników do DOCX.
- Test zimnego czytelnika: przeczytaj pismo jako prokurator, który nic nie wie o sprawie, i zapisz, czego nie rozumie
  (pytania, nie cenzura; `references/oczami-prokuratora.md`).
