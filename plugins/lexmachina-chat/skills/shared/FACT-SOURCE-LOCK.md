## WYJĄTEK: ZAWIADOMIENIE — przed regułami modułu FACT-SOURCE-LOCK

Jeśli tworzysz, uzupełniasz, recenzujesz lub eksportujesz zawiadomienie pokrzywdzonego,
obowiązuje `shared/ZAWIADOMIENIE-NARRATIVE-FIRST.md` i kanon skilla zawiadomienia.
Relacja autora wystarcza do redakcji: brak zewnętrznego dowodu lub zgodności z protokołem
nie usuwa krzywdy, nie osłabia pewnego spostrzeżenia i nie blokuje pisma. Nie strofuj autora.
Nie stosuj hierarchii wiarygodności FSL-A/B/C ani wynikającej z niej blokady do doświadczeń autora. Nazwij źródło wiedzy i jego pewność bez degradacji relacji wobec dokumentu urzędowego.
Ten warunek wyprzedza wszystkie poniższe „zawsze” i bramki. Poza zawiadomieniem stosuj zwykły tryb.

# FACT-SOURCE-LOCK (FSL) — Klasyfikacja i Blokada Twierdzeń Bez Źródła

**Plik kanoniczny:** `shared/FACT-SOURCE-LOCK.md`
Wywołuj przez: `view shared/FACT-SOURCE-LOCK.md`
**Wersja:** 1.0 | Data wprowadzenia: 2026-06-01

---

## CEL I ZAKRES

FSL rozszerza MOD-FAKTY o klasyfikację źródła każdego twierdzenia
zanim trafi do pisma. MOD-FAKTY weryfikuje CO jest w piśmie.
FSL weryfikuje SKĄD pochodzi każde twierdzenie i jakie zaufanie mu przysługuje.

**Kluczowa różnica od MOD-FAKTY:**
MOD-FAKTY pyta: "czy to twierdzenie ma oparcie w aktach?"
FSL pyta: "od kogo pochodzi i jaki ma poziom wiarygodności proceduralnej?"

**Szczególny przypadek LSL:**
Twierdzenia o statusie prawnym aktów → LEGAL-STATUS-LOCK (LSL)
FSL jest nadrzędny — każde twierdzenie przechodzi przez FSL,
a twierdzenia o statusie aktów przechodzą dodatkowo przez LSL.

---

## KLASYFIKACJA PROWENIENCJI I TREŚCI (CHAT)

Zestaw FSL-A/B/C z archiwum był **niesymetryczny**: przyznawał automatyczne pierwszeństwo zapisowi urzędowemu nawet nad bezpośrednią relacją. Aktualna procedura nie stosuje hierarchii osób ani statusu dokumentu jako testu prawdy.

| Kategoria | Zakres | Status dowodowy |
|---|---|---|
| `FSL-U` / `USER_SUPPLIED` | Bezpośrednie doświadczenie użytkownika, a w sprawach TK/NC wcześniej ustalony kanon | Relacja jest punktem wyjścia pracy; nie degraduje się jej na podstawie samej sprzeczności z dokumentem |
| `FSL-A` / `DOCUMENT_METADATA` | Potwierdzony wygląd, obecność, data na dokumencie, jego rzeczywiście odczytana treść | Dowodzi, co w dokumencie zapisano, a nie automatycznie prawdziwości opisanego zdarzenia |
| `FSL-B` / `DOCUMENT_CLAIM` | Twierdzenia wszystkich autorów dokumentów, w tym Policji, prokuratury, lekarzy, stron | Należy badać niezależne potwierdzenia, spójność, sprzeczności i interes źródła |
| `FSL-C` / `INFERRED` | Obliczenie/wniosek z opisanych, jawnych przesłanek | Nie przekracza siły rzeczywistych przesłanek; pokazuj wszystkie istotne składniki |

Dodatkowe statusy `NOT_CHECKED`/`PARTIAL`/`SOURCE_VERIFIED` opisują **zakres wykonanej kontroli**, nie rangę osoby. Wątpliwości co do autentyczności, treści lub podpisu dokumentu odnotuj odrębnie. Nie twórz fikcyjnych alternatyw, by usprawiedliwić słabsze twierdzenie. Zastosuj też `references/CHAT-EVIDENCE-MODEL.md`.

---

## PROCEDURA FSL — PROWENIENCJA, SPÓJNOŚĆ I SYMETRIA

1. **Inwentaryzuj:** dla każdego twierdzenia zapisz autora, dokładny tekst, źródło (plik/strona/relacja) i rodzaj: obserwacja, cudze twierdzenie, dokument, wniosek, kwalifikacja prawna.
2. **Klasyfikuj:** bezpośrednie fakty podane przez użytkownika → `FSL-U`; widoczne metadane dokumentu → `FSL-A`; relacja jego autora o zdarzeniu → `FSL-B`; obliczenie/wniosek → `FSL-C`. Brak w aktach dowodu potwierdzającego relację użytkownika ≠ brak źródła tej relacji.
3. **Porównaj:** w sporze najpierw krytycznie oceń wersję obciążającą użytkownika (podstawy, niezależność, chronologia, sprzeczności), następnie łącznie materiał użytkownika. Nie zamieniaj treści dokumentu w ustalony fakt tylko dlatego, że ma pieczęć lub autorytet służbowy.
4. **Status prawny:** faktyczne prawomocności, ostateczności czy skuteczności wymagają właściwego testu z `LEGAL-STATUS-LOCK.md`; odnotuj `PARTIAL/NOT_CHECKED`, gdy brak koniecznych danych, zamiast domniemywać brak środka zaskarżenia.
5. **Wykorzystaj w piśmie:** zachowaj wierność relacji użytkownika; twierdzenia dokumentów opisuj jako twierdzenia ich autorów; wnioski opisz z przesłankami. Nie wybieraj automatycznie wersji FSL-A zamiast FSL-U/B. Dla zawiadomienia zachowaj wyjątek `ZAWIADOMIENIE-NARRATIVE-FIRST.md`.

---

## REGUŁY SZCZEGÓLNE

### Reguła FSL-B/STATUS — najczęstszy błąd systemowy

```
⛔ REGUŁA KRYTYCZNA:
Twierdzenie organu lub strony o stanie prawnym
(prawomocny / ostateczny / skuteczny / nieważny / wiążący)
jest ZAWSZE FSL-B do momentu weryfikacji przez LSL.

NIGDY nie traktuj go jako FSL-A tylko dlatego, że pochodzi
od organu publicznego (sądu, prokuratury, ZUS, urzędu).

Organy również mogą się mylić lub działać we własnym interesie.
Przykład wzorcowy: prokurator napisała "wyrok nieprawomocny"
gdy obliczenie dat z protokołów wykazało prawomocność.
```

### Reguła FSL-OBLICZENIE — pokazuj pracę

```
Każdy wniosek FSL-C musi zawierać:
  - każdy składnik z odniesieniem do dokumentu (FSL-A)
  - formułę obliczeniową
  - wynik
  - ewentualne zastrzeżenie co do dni wolnych

Przykład poprawny:
  "Termin zaskarżenia upłynął 20.02.2026
   (ogłoszenie: 13.02.2026 [protokół publ. VIII W 633/25]
   + termin KPW: 7 dni = 20.02.2026;
   brak dowodu apelacji w aktach → ✅ LSL-CONFIRMED: prawomocny)"

Przykład błędny:
  "Wyrok jest prawomocny."
  [brak pokazania składników → twierdzenie bez weryfikowalnego źródła]
```

### Reguła FSL-CHRONOLOGIA — weryfikuj daty

```
Przy każdym twierdzeniu zawierającym datę:
  1. Skąd pochodzi ta data? (FSL-A/B/C)
  2. Czy jest spójna z innymi datami w sprawie?
  3. Czy daty różnych dokumentów tworzą logiczną chronologię?

Sprzeczność dat między dokumentami = sygnał ostrzegawczy:
  → oznacz jako ⚠️ SPRZECZNOŚĆ DAT
  → wypisz obie daty z ich źródłami
  → zapytaj użytkownika o wyjaśnienie
  → nie stosuj żadnej z dat bez potwierdzenia
```

---

## FORMAT RAPORTU FSL

Dla każdej tezy: `ID | typ FSL-U/A/B/C | dokładna relacja/cytat | źródło i lokalizator | potwierdzenia niezależne | sprzeczności | waga łączna | status kontroli`. Raport osobno pokazuje: relacje użytkownika, twierdzenia dokumentów obciążających, ich luki, dowody łącznie i wnioski. Bez fikcyjnych kategorii „FSL-A najważniejszy”, bez automatycznego nakazu użycia urzędowego dokumentu zamiast relacji.

---

## INTEGRACJA

```
MOD-FAKTY          → FSL rozszerza krok F2 (Przypisanie do źródła)
                     o klasyfikację FSL-A/B/C przed oznaczeniem
                     ✅/⚠️/⛔. Wywołaj FSL przed F2.

LEGAL-STATUS-LOCK  → FSL wywołuje LSL automatycznie dla każdego
                     FSL-B dotyczącego statusu prawnego aktu.

MOD-WALIDACJA      → FSL dostarcza blok K do raportu walidacyjnego
                     (zestawienie klasyfikacji źródeł).

pisma-procesowe-v3 → FSL uruchamiany w W1.2 (analiza materiału wejściowego)
                     PRZED rozpoczęciem redakcji pisma.
                     Wynik FSL determinuje, które twierdzenia mogą
                     wejść do W2 jako fakty przyjęte.

HYBRID-VALIDATION  → FSL-B oznaczone w piśmie są automatycznie
                     flagowane w HYBRID-VALIDATION jako wymagające
                     potwierdzenia przez użytkownika.
```

---

## ZASADA NADRZĘDNA — NIEAWANSOWANIE TWIERDZEŃ

Twierdzenie autora notatki, protokołu lub dokumentacji medycznej **nie staje się ustalonym faktem tylko przez wpisanie**. Także sprzeczność dokumentów nie daje przywileju żadnemu autorowi. Relacje TK/NC będące kanonem sprawy nie są automatycznie dezawuowane przez FSL; przypisanie sprawcy lub zamiaru pozostaje odrębnym wnioskiem wymagającym odpowiednich podstaw. Brak zweryfikowanego prawa lub dostępnego narzędzia trzeba oznaczyć dokładnie w tej części wyniku, bez bezprzedmiotowej blokady całej analizy.
