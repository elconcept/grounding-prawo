# Moduł `ocena-outputu-pl` skilla `szturm-na-draft-pl`

> Dawniej osobny skill; scalony, żeby ta sama funkcja nie była powielana. Ścieżki `scripts/`, `references/` itd. są względne wobec tego katalogu.
>
> Zastosowanie: soczewka: karta ocen 1-5 (poprawność, kompletność, jasność, jurysdykcja, ugruntowanie)

# Ocena outputu PL - karta ocen przed wysyłką

## Filozofia

**Zanim wyślesz, oceń - i oddziel to, co sprawdzalne, od tego, co trzeba osądzić.** Output AI bywa
gładki i przekonujący, a mimo to błędny. Ten skill ocenia go w dwóch warstwach: obiektywnej
(fakty, które da się sprawdzić mechanicznie) i subiektywnej (jakość, którą trzeba osądzić wg jawnej
rubryki). Dwie warstwy, bo mylenie ich to źródło fałszywej pewności - „brzmi dobrze" nie znaczy
„cytaty się zgadzają".

Skill **ocenia**, nie poprawia i nie wysyła. Decyzję podejmuje prawnik; karta ocen daje podstawę.

## Warstwa 1 - obiektywna (sprawdzalne mechanicznie)

Deleguj do narzędzi, nie zgaduj:
- **Cytaty i przepisy** - czy istnieją w źródle słowo w słowo (citation-grounding-pl), czy wszystkie
  wyłapane (citation-grounding-pl/modules/ekstraktor-cytatow-pl).
- **Sygnatury / ELI** - czy realne i poprawnie zapisane.
- **Kompletność ustaleń** - czy żadna flaga RED nie wypadła z podsumowania (deliverable-fidelity-pl).

Wynik obiektywny jest binarny per pozycja: zgadza się / nie zgadza. Choćby jeden niezgodny cytat =
output nie jest gotowy, niezależnie od oceny subiektywnej.

## Warstwa 2 - subiektywna (rubryka 1-5, LLM-as-judge)

Oceń wg jawnej rubryki, każdy wymiar 1-5 z jednozdaniowym uzasadnieniem:

| Wymiar | 1 | 5 |
|---|---|---|
| Poprawność prawna | teza błędna lub nieoparta | teza trafna i oparta na normie |
| Kompletność | pomija istotne kwestie | obejmuje wszystko, co istotne dla pytania |
| Jasność | mętne, niespójne | precyzyjne, czytelne dla odbiorcy |
| Zgodność z jurysdykcją | myli porządki/przepisy | trafne dla prawa polskiego/UE |
| Ugruntowanie (anty-halucynacja) | twierdzenia bez podstawy | każde twierdzenie ma oparcie |

### NIEPEWNE zamiast liczby - ocena pierwszej klasy

Gdy sędzia nie ma podstaw, by wystawić liczbę, NIE wystawia jej. Zamiast wymuszonej trójki
wpisuje **NIEPEWNE** z podkategorią i wskazaniem, jakiego dowodu brakuje:

- **NIEWYSTARCZAJĄCY_DOWÓD** - oceny nie da się wystawić bez materiału, którego nie ma
  w sesji (np. brak tekstu źródłowego wyroku II CSK NN/RR, brak umowy, do której output
  się odwołuje). Wpisz, CZEGO brakuje i skąd to wziąć.
- **DOKUMENT_NIEJEDNOZNACZNY** - materiał jest, ale nie rozstrzyga (dwuznaczna klauzula,
  sprzeczne fragmenty, pytanie klienta dopuszcza dwie wykładnie). Wpisz, NA CZYM polega
  niejednoznaczność.

Reguły twarde:
- NIEPEWNE nie wchodzi do średniej i nie wolno go cicho zamienić na 3 - wymuszona
  środkowa ocena to przemilczenie niepewności, dokładnie to, co ten skill ma łapać.
- NIEPEWNE w wymiarze Poprawność prawna lub Ugruntowanie -> decyzja co najwyżej
  **Pełna weryfikacja**.
- NIEPEWNE w pozostałych wymiarach -> decyzja co najwyżej **Popraw**.

To slogan "AI, która wie, czego nie wie" jako pole w karcie ocen, nie deklaracja.

## Decyzja

- **Wyślij** - warstwa 1 czysta, zero NIEPEWNYCH, średnia subiektywna ≥ 4, żaden wymiar < 3.
- **Popraw** - warstwa 1 czysta, ale któryś wymiar subiektywny 2-3 (wskaż który) albo
  NIEPEWNE poza wymiarami krytycznymi.

## Rewizja oceny - monotoniczność i kotwica

Karta ocen bywa wystawiana dwa razy: po pierwszym przebiegu i po poprawkach. Drugi przebieg
jest miejscem, w którym ocena po cichu rośnie, bo autor zna już zarzuty i umie je opowiedzieć.
Stąd dwie reguły twarde.

**Monotoniczność.** Rewizja może obniżyć decyzję zawsze i z dowolnego powodu. Podniesienie
wymaga **nowego dowodu**, nie nowego uzasadnienia. Nowy dowód to ponowny przebieg warstwy 1
z innym wynikiem albo materiał, którego wcześniej nie było w sesji (dosłany wyrok, dosłana
umowa). Zdanie „po namyśle to jednak wystarczające" nie jest dowodem i nie podnosi oceny.

**Kotwica.** Dopóki którakolwiek z poniższych pozycji jest otwarta, decyzja nie może wyjść
powyżej **Pełna weryfikacja**, niezależnie od średniej subiektywnej i niezależnie od tego, jak
dobrze brzmi uzasadnienie:

- cytat, przepis albo sygnatura niezgodne ze źródłem w warstwie 1,
- flaga RED, która wypadła z podsumowania (`deliverable-fidelity-pl`),
- NIEPEWNE w wymiarze Poprawność prawna albo Ugruntowanie.

Kotwicę zdejmuje wyłącznie ponowny przebieg narzędzia, które ją postawiło. Osąd sędziego jej
nie zdejmuje. To ta sama zasada, którą stosuje `agentic-risk-asi-pl` przy dotkliwości ustaleń:
dowód bezpośredni nie podlega negocjacji.

Każdą zablokowaną próbę podniesienia zapisz w karcie - widok „ktoś próbował przesunąć ocenę
i czym to uzasadnił" bywa cenniejszy od samej oceny.

## Format wyjścia

```
WARSTWA 1 (obiektywna): cytaty OK/X | przepisy OK/X | sygnatury OK/X | kompletność OK/X
WARSTWA 2 (rubryka 1-5):
  Poprawność prawna: 4 - <uzasadnienie>
  Kompletność: 3 - <...>
  Jasność: 5 - <...>
  Zgodność z jurysdykcją: NIEPEWNE (NIEWYSTARCZAJĄCY_DOWÓD) - output opiera się na wyroku
    II CSK NN/RR, którego tekstu nie ma w sesji; brakuje: treść uzasadnienia (saos-orzecznictwo (poza pluginem))
  Ugruntowanie: 4 - <...>
  Średnia: 4.0 (z 4 wymiarów liczbowych; NIEPEWNE poza średnią)
KOTWICE: brak (albo: cytat II CSK NN/RR niezgodny - decyzja ograniczona do Pełnej weryfikacji)
DECYZJA: Popraw (Kompletność 3 - brak omówienia przedawnienia; Zgodność z jurysdykcją
NIEPEWNE - uzupełnij tekst wyroku przed wysyłką)
```

Przy rewizji dopisz jedną linię:

```
REWIZJA #2: decyzja Popraw -> Popraw. Odrzucone podniesienie do Wyślij: uzasadnienie bez
nowego dowodu (warstwa 1 nie była powtórzona).
```

## Granice

- Warstwa 1 nie zastępuje narzędzi, które wywołuje - jest ich agregatorem do jednej decyzji.
- Skill ocenia output, nie tworzy go i nie poprawia.

## Atrybucja

Metoda dwuwarstwowa (obiektywne dopasowanie + subiektywna rubryka LLM-as-judge w skali 1-5) oparta na
**DISC-Law-Eval** z projektu DISC-LawLLM (Fudan DISC Lab), licencja **Apache-2.0**. Chińskie dane
egzaminacyjne i model-sędzia porzucone; wymiary rubryki, progi decyzji i kotwice PL to oryginalne
opracowanie MateMatic. Interpretacja MateMatic, nie stanowisko NRA ani KRRP.

Wzorzec dodany w v1.1.0: NIEPEWNE jako ocena pierwszej klasy (podkategorie
NIEWYSTARCZAJĄCY_DOWÓD / DOKUMENT_NIEJEDNOZNACZNY, wymóg wskazania brakującego dowodu,
zakaz wymuszonej trójki) z AnttiHero/lavern (Apache 2.0), adaptacja od zera - podkategorie,
reguły decyzji i polska semantyka to opracowanie MateMatic.

