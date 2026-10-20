# Moduł `ekstraktor-cytatow-pl` skilla `citation-grounding-pl`

> Dawniej osobny skill; scalony, żeby ta sama funkcja nie była powielana. Ścieżki `scripts/`, `references/` itd. są względne wobec tego katalogu.
>
> Zastosowanie: ekstrakcja wszystkich powołań (sygnatury, ECLI, Dz.U., ELI, przepisy, tamże/op. cit.) przed weryfikacją

# Ekstraktor cytatów PL - znajdź każdy cytat, zanim go zweryfikujesz

## Filozofia

**Zweryfikować można tylko to, co się najpierw znajdzie.** Grounding cytatu (citation-grounding-pl)
sprawdza, czy dany cytat istnieje w źródle - ale działa na liście cytatów, którą ktoś musi najpierw
zebrać. Ten skill jest tym front-endem: przechodzi pismo i wypisuje WSZYSTKIE odwołania, tak by żadne
nie wymknęło się weryfikacji. Pominięty cytat to cytat niesprawdzony.

Ekstrakcja jest **mechaniczna** (wzorce + reguły, nie LLM) - to celowe: model na etapie znajdowania
cytatów mógłby jeden przeoczyć albo dopowiedzieć. Lokalnie, RODO-safe.

## Trzy kroki (za eyecite, zlokalizowane do PL)

1. **Ekstrakcja** - rozpoznaj i wyłap każde odwołanie wg wzorców PL poniżej.
2. **Agregacja** - rozwiąż odwołania skrótowe (tamże / op. cit. / wyżej powołany wyrok) do
   antecedentów wg reguł wrażliwych na wskaźnik (poniżej), żeby policzyć je jako jeden cytat, nie kilka.
3. **Przekazanie** - oddaj ustrukturyzowaną listę do citation-grounding-pl do weryfikacji string-match.

## Wzorce odwołań (PL)

### Sygnatury orzeczeń
- **SN / sądy powszechne**: izba rzymska + litera wydziału + numer/rok, np. `II CSK NN/RR`, `I KZP NN/RR`, `III CZP NN/RR` (NN = numer, RR = rok - placeholdery).
- **Sądy administracyjne**: NSA `II FSK NNNN/RR`; WSA z oznaczeniem siedziby przez ukośnik, np. `III SA/Wa NNN/RR`, `I SA/Gd NN/RR`.
- **Trybunał Konstytucyjny**: `K 1/20`, `P 7/19`, `SK 3/18`, `Ts 45/20`.
- **KIO** (zamówienia publiczne): `KIO NNN/RR`, sprawy łączone `KIO NNN/RR, KIO NNN/RR`.
- **TSUE**: `C-123/20`, odwoławcze `C-123/20 P`, sprawy połączone `C-123/20 i C-124/20`; Sąd UE `T-456/19`.

### ECLI
- Polski: `ECLI:PL:SN:2015:IICSK24515`, `ECLI:PL:NSA:2018:...`.
- Unijny: `ECLI:EU:C:2020:559`, `ECLI:EU:T:2019:...`.

### Akty prawne (Dz.U. / M.P. / ELI / UE)
- `Dz.U. RRRR poz. NNNN`, `Dz.U. z RRRR r. poz. NNNN`, starszy format `Dz.U. z RRRR r. Nr N, poz. NNNN`.
- `M.P. 2019 poz. 50`; `Dz.Urz. UE L 119` (RODO), `Dz.Urz. UE C ...`.
- ELI URI Sejmu, np. `.../DU/2020/1234`.

### Powołane przepisy
- `art. 415 KC`, `art. 5 ust. 1 lit. a RODO`, `art. 233 § 1 KPC`, `§ 3 ust. 2` (akt wykonawczy).

## Agregacja - odwołania skrótowe (antecedenty PL)

Formy skrótowe mają **różne reguły rozwiązywania** - nie wolno wszystkich odsyłać do najbliższego
antecedentu:

- `tamże` / `ibidem` / `j.w.` - bezpośrednio poprzedzające źródło.
- `op. cit.` / `cyt. wyżej` - często niosą **wskaźnik**, który wygrywa z bliskością: nazwisko autora,
  fragment tytułu, numer przypisu ("Radwański, op. cit., s. 120"). Rozwiązuj najpierw po wskaźniku;
  do bliskości sięgaj tylko przy odwołaniu gołym.
- Formy opisowe (`wyżej powołany wyrok`, `powołane orzeczenie`, `tak też`) - dopasuj po opisanych
  atrybutach (sąd, sygnatura, przedmiot), nie po samej pozycji w tekście.

Gdy pasuje więcej niż jeden antecedent albo żaden - oznacz odwołanie **nierozwiązane - do przeglądu
ręcznego** zamiast zgadywać: błędne sklejenie po cichu zlewa dwa różne źródła w jedno. Rozwiązane
odwołanie policz jako ten sam cytat co antecedent, ale zachowaj miejsce wystąpienia.

## Format wyjścia

```
ZNALEZIONE CYTATY (n):
| # | Typ | Cytat (znormalizowany) | Wystąpienia (offset/strona) | Antecedent (jeśli skrót) |
| 1 | orzeczenie SN | II CSK NN/RR | s.3, s.7 (tamże) | - |
| 2 | przepis | art. 415 KC | s.4 | - |
| 3 | akt | Dz.U. RRRR poz. NNNN | s.2 | - |

DO WERYFIKACJI: przekaż kolumnę "Cytat" do citation-grounding-pl.
```

## Granice

- Ekstrakcja wyłapuje odwołania o znanym formacie. Cytat opisowy bez sygnatury („wyrok SN w sprawie
  rękojmi") nie ma czego dopasować - oznacz jako `bez sygnatury, do ręcznego sprawdzenia`.
- To nie jest weryfikacja istnienia - od tego jest citation-grounding-pl. Ten skill mówi „co jest
  cytowane", nie „czy cytat prawdziwy".
- Wzorce pokrywają najczęstsze formaty; nietypowy zapis sygnatury może umknąć - przy audycie
  wysokiej stawki przejrzyj też ręcznie.

## Atrybucja

Architektura (ekstrakcja -> agregacja -> adnotacja, logika antecedentów) zainspirowana **eyecite**
(Free Law Project), licencja **BSD-2-Clause**. Amerykańskie wzorce reporterów porzucone; wzorce
sygnatur PL, ECLI, Dz.U./ELI i reguły antecedentów to oryginalne opracowanie MateMatic.
Interpretacja MateMatic, nie stanowisko NRA ani KRRP.

