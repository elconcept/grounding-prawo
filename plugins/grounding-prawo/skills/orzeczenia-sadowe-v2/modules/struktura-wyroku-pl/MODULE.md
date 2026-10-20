# Moduł `struktura-wyroku-pl` skilla `orzeczenia-sadowe-v2`

> Dawniej osobny skill; scalony, żeby ta sama funkcja nie była powielana. Ścieżki `scripts/`, `references/` itd. są względne wobec tego katalogu.
>
> Zastosowanie: rozbiór orzeczenia na sentencję, ratio decidendi, obiter dicta i votum separatum

# Struktura wyroku PL - rozłóż orzeczenie i streść ekstraktywnie

## Filozofia

**Streszczenie wyroku, które parafrazuje, zmyśla.** Model „podsumowując" uzasadnienie często
przesuwa akcenty albo dopisuje tezę, której sąd nie postawił. Ten skill robi inaczej: segmentuje
orzeczenie na role retoryczne i streszcza **ekstraktywnie** - wybiera i cytuje zdania źródłowe,
nie przepisuje ich własnymi słowami. To, co czytasz w streszczeniu, jest słowami sądu.

Mechaniczna segmentacja + ekstrakcja kluczowych zdań. Parafraza i ocena zostają prawnikowi.

## Role retoryczne polskiego orzeczenia

Segmentuj tekst na poniższe role (nie każde orzeczenie ma wszystkie):

1. **Komparycja** - sygnatura, sąd, skład, data, strony, przedmiot sprawy.
2. **Sentencja (rozstrzygnięcie)** - co sąd orzekł (oddala, zasądza, uchyla, zmienia). Sedno wyniku.
3. **Stan faktyczny** - ustalenia faktyczne przyjęte za podstawę.
4. **Przebieg postępowania** - co działo się w instancjach niżej / wcześniej.
5. **Zarzuty i wnioski stron** - podstawy zaskarżenia, żądania, stanowiska.
6. **Podstawa prawna** - powołane przepisy (przekaż do citation-grounding-pl/modules/ekstraktor-cytatow-pl).
7. **Rozważania sądu** - rozumowanie prawne, wykładnia, subsumcja.
8. **Teza / ratio decidendi** - reguła rozstrzygająca, dla której wyrok jest cytowany.
9. **Zdanie odrębne** - jeśli jest (votum separatum), oznacz osobno - to nie jest stanowisko sądu.

## Workflow

2. **Segmentuj** na role powyżej - przypisz fragmenty, oznacz role nieobecne.
3. **Streść ekstraktywnie** - dla każdej istotnej roli wybierz 1-3 zdania KLUCZOWE i zacytuj je
   dosłownie (z offsetem/stroną), nie parafrazuj.
4. **Wskaż ratio** - jedno-dwa zdania, dla których to orzeczenie się powołuje (zacytuj, nie streszczaj).
5. **Wypisz powołane przepisy i orzeczenia** - przekaż do citation-grounding-pl/modules/ekstraktor-cytatow-pl, a dalej do
   citation-grounding-pl do weryfikacji.

## Format wyjścia

```
ORZECZENIE: <sąd>, <sygnatura>, <data>
ROZSTRZYGNIĘCIE (sentencja): "<cytat sentencji>"

STRESZCZENIE EKSTRAKTYWNE (cytaty źródłowe):
- Stan faktyczny: "<zdanie kluczowe>" (s.X)
- Zarzuty: "<...>" (s.X)
- Rozważania sądu: "<zdanie nośne rozumowania>" (s.X)

TEZA / RATIO: "<cytat zdania rozstrzygającego>" (s.X)

POWOŁANE: art. ... ; orzeczenia ...  -> do weryfikacji (citation-grounding-pl/modules/ekstraktor-cytatow-pl -> citation-grounding-pl)
ROLE NIEOBECNE: <lista, jeśli brak np. zdania odrębnego>
```

## Granice

- Streszczenie jest ekstraktywne - wierne słowom sądu, ale to nadal wybór zdań; pełną wykładnię
  i ocenę linii orzeczniczej robi prawnik.
- Skill nie ocenia trafności orzeczenia ani nie buduje glosy - dostarcza uporządkowany,
  cytowalny szkielet do dalszej pracy.
- Role retoryczne to model polskiego uzasadnienia; nietypowa struktura (np. orzeczenia TSUE,
  postanowienia wpadkowe) może wymagać ręcznej korekty segmentacji.

## Atrybucja

Metoda (segmentacja orzeczenia przez role retoryczne zdań + streszczenie ekstraktywne) oparta na
**OpenNyAI / Opennyai** (Legal-NLP-EkStep), licencja **MIT**. Indyjskie role i modele NLP porzucone;
role retoryczne polskiego orzeczenia, reguły ekstrakcji i format wyjścia to oryginalne opracowanie
MateMatic. Interpretacja MateMatic, nie stanowisko NRA ani KRRP.

