---
name: kalkulatory-procesowe-pl
description: 'Obliczenia procesowe z kartą do zatwierdzenia: terminy (KC, KPC, KPK, KPW), opłaty sądowe, przedawnienie, odsetki, WPS. Każdy krok ma podstawę prawną; niepewna reguła zatrzymuje wynik.'
license: Apache-2.0
allowed-tools:
- Read
- WebFetch
metadata:
  author: Wiesław Mazur / MateMatic
  version: 1.0.0
  companion_skills: terminy-procesowe-pl, sejm-eli-mcp (konektor)
  data-residency: local
  requires-human-approval: 'true'
  pii-egress: none
  attribution: '{"source": "crankshift/lawpowers", "license": "MIT", "relationship": "pattern-only", "note": "Dekompozycja na 4 kalkulatory i protokół „fetch przed obliczeniem”. Treść, tabele i rachunki napisane od zera na tekstach UKSC/KC/KPC; przy okazji poprawione 4 nieaktualne wartości źródła, m.in. limit opłaty stosunkowej po noweli z 2025 r.\n"}'
---

## Pamięć sesji — przed pracą i przed odpowiedzią końcową

Przeczytaj `shared/BASIC-MEMORY.md`, `shared/ZASADY-PLUGINU.md` oraz katalog `shared/INDEKS-SKILLI.md`. Przy redakcji pisma wczytaj `shared/STYLE.md`; przy zapisie plików `shared/ARTEFAKTY-SPRAWY.md`. Na wejściu odczytaj kluczowe trwałe ustalenia z `model-memory`, ostatni recap z `main` i sprawę z `legal`; po etapach zapisuj recap sesji w `main/sesje/` i sprawdź odczytem. Do `model-memory` dodawaj wyłącznie nowe, wartościowe key takeaways; nigdy logu sesji. Nowe dokumenty i ustalenia zapisuj w `legal` po każdym zakończonym etapie. Podaj status pamięci i identyfikator notatki; nie zgłaszaj zapisu bez potwierdzenia MCP.

## Repertorium - pierwsze źródło w każdym zadaniu prawnym

Zanim powołasz, ocenisz albo pominiesz przepis, orzeczenie lub kwalifikację, wywołaj przez portal `lex` `repertorium_szukaj_repertorium` (wyszukiwanie semantyczne ustaw, orzeczeń SN, sądów powszechnych, NSA/WSA, TK i decyzji UODO): co najmniej jedno zapytanie o zagadnienie i stan faktyczny (`jurysdykcja="pl"`), osobne dla każdej tezy, zarzutu lub żądania pisma, a przy wątku unijnym (RODO, prawo UE, TSUE) także `"eu"`. Opisuj problem słowami, nie tylko numerem artykułu lub sygnaturą. Trafienia sprawdź w pełnym brzmieniu (`shared/MOD-TEKST-JEDNOLITY.md`) i w treści orzeczenia; fragment z wyniku nie jest cytatem. Zapytania i wykorzystane trafienia zapisz w śladzie przebiegu (`_PRZEBIEGI.md` albo `analiza/_dowody-i-przepisy.md`). Kontrola prawa bez zapytań do Repertorium ma wynik `NOT_CHECKED`; awaria lub brak trafień to wpis w śladzie, po którym szukasz dalej w `isap`, `saos`, `nsa`, `uodo`, `eu-sparql`.

# Kalkulatory procesowe PL - żywe parametry, nigdy sama liczba

## Filozofia

**Parametry procesu cywilnego żyją krócej niż jakikolwiek plik.** Stopa
referencyjna NBP zmienia się kilka razy w roku i ciągnie za sobą wszystkie
odsetki. Tabele opłat nowelizowane są bez rozgłosu: 23 września 2025 r.
maksimum opłaty stosunkowej spadło z 200 000 zł do 100 000 zł - kalkulator,
który tego nie zauważył, myli się o sto tysięcy złotych i robi to z pełnym
przekonaniem. Kalkulator liczący na przeterminowanych stawkach jest gorszy
niż brak kalkulatora.

Stąd trzy zasady, wspólne dla wszystkich czterech rachunków:

1. **Najpierw parametry, potem rachunek.** Każdy kalkulator otwiera tabela
   "Aktualne parametry - POBIERZ przed obliczeniem": skąd wziąć żywą wartość,
   jaki jest fallback i z jaką datą weryfikacji. Protokół niżej.
2. **Nigdy sama liczba.** Wynik to pełny rachunek: wejście, każdy krok
   z podstawą prawną (artykuł, ustęp), wynik DRAFT, flagi ryzyka. Kwota bez
   rachunku jest nieweryfikowalna, a nieweryfikowalna kwota opłaty czy odsetek
   jest bezużyteczna.
3. **Fail-closed i bramka człowieka.** Niepewna reguła = tag `[DO SPRAWDZENIA]`
   i blokada zatwierdzenia, nie założenie. Kartę obliczenia zatwierdza
   pełnomocnik - dopiero wtedy kwota istnieje operacyjnie (wzorzec
   terminy-procesowe-pl).

## Cztery kalkulatory - routing

| Pytanie | Kalkulator | Metodyka |
|---|---|---|
| ile wynosi opłata od pozwu / apelacji / wniosku | opłata sądowa (UKSC) | [references/oplata-sadowa.md](references/oplata-sadowa.md) |
| czy roszczenie przedawnione, do kiedy dochodzić | przedawnienie (art. 117-125 KC) | [references/przedawnienie.md](references/przedawnienie.md) |
| ile odsetek i według jakiej stopy | odsetki (KC + transakcje handlowe) | [references/odsetki.md](references/odsetki.md) |
| jaka wartość sporu - właściwość, tryb, opłata | WPS (art. 19-26 KPC) | [references/wps.md](references/wps.md) |

Rachunki bywają sprzężone - typowa kolejność przy pozwie o zapłatę:
**WPS -> opłata sądowa** (opłata stosunkowa liczy się OD WPS), a odsetki
i przedawnienie liczone równolegle. Czytaj tylko plik potrzebnego kalkulatora.

## Protokół parametrów - obowiązkowy przed każdym rachunkiem

1. **POBIERZ** żywe wartości ze źródła wskazanego w tabeli parametrów
   kalkulatora (WebFetch na wskazany adres; teksty ustaw najlepiej przez
   konektor `sejm-eli-mcp` / ISAP ELI).
2. **PORÓWNAJ** z fallbackiem z tabeli. Różnica = licz na wartości pobranej
   i zgłoś rozjazd w karcie obliczenia (to sygnał, że plik metodyki wymaga
   aktualizacji).
3. **NIE MOŻESZ POBRAĆ** (brak sieci, źródło blokuje, konektor niedostępny) =
   licz na fallbacku i OBOWIĄZKOWO oznacz wynik:
   `[PARAMETRY Z DNIA 2026-07-13 - zweryfikuj przed użyciem]`.
   Karta z tą etykietą nie nadaje się do wniesienia opłaty ani do pisma
   bez ręcznej weryfikacji parametrów.

Data 2026-07-13 to dzień weryfikacji fallbacków tej wersji pliku. Rejestr
aktów bazowych (UKSC, KC, KPC, ustawa o transakcjach handlowych) pilnowany
jest mechanicznie: `scripts/wachta-parametrow-kalkulatorow.mjs` (brak w pluginie) w CI raz
w miesiącu porównuje stan ISAP z `parametry-baseline.json` i alarmuje, gdy
akt został uchylony albo zmieniony po dacie baseline.

## Format wyniku - karta obliczenia (szablon dosłowny)

```
KARTA OBLICZENIA - DRAFT (brudnopis rachunku, nie decyzja)

Kalkulator    : [opłata sądowa / przedawnienie / odsetki / WPS]
Sprawa        : [opis; np. sygn. akt I C NN/RR]
Parametry     : [pobrane RRRR-MM-DD z <źródło> / FALLBACK Z DNIA 2026-07-13 - zweryfikuj]

Wejście:
  [np. WPS 48 250 zł; pismo: pozew; tryb: zwykły]

Rachunek:
  krok 1: [treść kroku] (podstawa: [przepis]) [zweryfikowane / DO SPRAWDZENIA]
  krok 2: ...

WYNIK (DRAFT): [kwota / data / werdykt]

Flagi ryzyka:
  - [np. pismo sprzed 23.09.2025 - stary limit opłaty, przepis przejściowy]
  - [np. sporna data wymagalności - przyjęto wariant ostrożny]

STATUS: DO ZATWIERDZENIA PRZEZ CZŁOWIEKA
Zatwierdził(a): __________________  Data: __________
```

Karta bez sekcji "Rachunek" jest nieważna - kwota nigdy nie wychodzi ze
skilla bez rachunku i podstaw prawnych.

## Bramka człowieka - granice skilla

- **Wynik to brudnopis.** Opłatę wnosi, zarzut przedawnienia podnosi, kwotę
  odsetek do pozwu wpisuje człowiek - po własnej weryfikacji rachunku.
- **Każdy tag `[DO SPRAWDZENIA]` i etykieta `[PARAMETRY Z DNIA ...]` blokują
  zatwierdzenie** do czasu weryfikacji.
- **Rozbieżność = eskalacja.** Gdy rachunek pełnomocnika i karta dają różne
  kwoty, nie uśredniaj - rozstrzyga człowiek po powrocie do brzmienia przepisu.
- Skill NIE wnosi opłat, NIE składa pism, NIE rozstrzyga sporów o fakty
  (sporna data doręczenia lub wymagalności = flaga i wariant ostrożny,
  nie przesądzenie).
- Wynik nie jest poradą prawną; przed błędem chroni rachunek + tagi + ta
  bramka, nie nota prawna.

## Companion skills

- **terminy-procesowe-pl** - inna oś: tam KIEDY upływa termin czynności,
  tu ILE wynosi kwota (opłata, odsetki, WPS) i CZY roszczenie żyje.
  Przedawnienie liczone jest tutaj, bo to termin materialny z własną
  mechaniką (koniec roku kalendarzowego), ale kartę terminu zawitego
  procesowego rób tamtym skillem.
- **sejm-eli-mcp (konektor)** - preferowana droga pobrania aktualnego
  brzmienia UKSC/KC/KPC (krok 1 protokołu parametrów).

## Weryfikacja źródeł

- Przepisy przywołane w plikach metodyki opisują stan na dzień weryfikacji
  fallbacków - przy każdym użyciu brzmienie sprawdzane jest na dzień
  obliczenia (protokół parametrów, krok 1). Ustawy okołoprocesowe zmieniają
  się szybciej niż ten plik - przykład limitu opłaty z 2025 r. wyżej.
- Tagi pewności wg fundamentu weryfikacyjnego: **zweryfikowane** (przepis
  lub stawka sprawdzone w sesji, z datą) / **[DO SPRAWDZENIA]** (blokuje
  zatwierdzenie karty).
- Skill działa lokalnie na danych sprawy (RODO-safe); jedyny ruch na
  zewnątrz to odpytanie publicznych źródeł (ISAP/ELI, NBP, Monitor Polski)
  o treść przepisów i wysokość stóp.


## MODUŁY SCALONE

Ten skill obejmuje funkcje dawnych osobnych skilli. Wczytaj moduł, gdy zadanie go dotyczy; reguły tego skilla obowiązują także w module.

| Moduł | Zastosowanie | Plik |
|---|---|---|
| `terminy-procesowe-pl` | terminy procesowe i materialne krok po kroku (KC art. 110-116, KPC, KPK, KPW) z kartą terminu | `modules/terminy-procesowe-pl/MODULE.md` |

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** dane o roszczeniu (kwota, daty) z `analiza/_brief.md`
- **Wynik zapisz w:** wartości (opłata, WPS, odsetki, przedawnienie) wpisane do pisma i `analiza/_dowody-i-przepisy.md` (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `pisma-procesowe-v3`
- **Basic Memory (`legal`):** czytaj teczkę (decyzje, lekcje) i `orzeczenia/`; załóż albo zaktualizuj notatkę pisma w `sprawy/<katalog>/pisma/` (wersja, ścieżka, status) (protokół: `shared/BASIC-MEMORY.md`)
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
