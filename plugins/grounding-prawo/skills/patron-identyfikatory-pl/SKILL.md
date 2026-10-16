---
name: patron-identyfikatory-pl
description: Walidacja sum kontrolnych PESEL, NIP i REGON oraz formatu KRS, data urodzenia z PESEL, a także wyciąganie z tekstu polskich sygnatur akt (SN, NSA, WSA, KIO, TK, sądy powszechne), numerów CELEX i ELI, odwołań do Dz.U., nazw spółek z formą prawną i osób z rolą procesową. Użyj przy analizie umów, pism i akt - do wyłapania błędnych numerów, zebrania stron i powołanych orzeczeń albo ustalenia, do którego pionu sądów należy sygnatura.
---

## Pamięć sesji — przed pracą i przed odpowiedzią końcową

Przeczytaj `shared/BASIC-MEMORY.md` i `shared/ZASADY-PLUGINU.md`. Na wejściu odczytaj kontekst sprawy z projektu `legal`; przed odpowiedzią końcową zapisz lub zaktualizuj recap tej sesji w projekcie `main` i sprawdź odczytem zapis. Nowe dokumenty i ustalenia zapisuj w `legal` po każdym zakończonym etapie. Podaj status pamięci i identyfikator notatki; nie zgłaszaj zapisu bez potwierdzenia MCP.

# Identyfikatory i encje prawa polskiego

Skrypt: `scripts/pl_entities.py` w katalogu tego skilla (Python 3, bez zależności, offline).

```bash
python3 scripts/pl_entities.py validate nip 526-104-08-28   # kod 0 = poprawny, 1 = błędna suma
python3 scripts/pl_entities.py pesel-info 44051401458      # data urodzenia i płeć
python3 scripts/pl_entities.py extract umowa.txt           # JSON: typ, wartość, pozycja
python3 scripts/pl_entities.py extract umowa.txt --all     # także numery z błędną sumą
```

## Zastosowania
- **Kontrola numerów w umowie lub piśmie:** `extract --all` i zgłoś każde `"poprawny": false` -
  zwykle to literówka w PESEL, NIP albo REGON strony.
- **Strony umowy:** typ `FIRMA` (nazwa z formą prawną) i `OSOBA` (imię i nazwisko po roli:
  Pan/Pani, adw., r.pr., powód, pozwany, świadek...). Istnienie i reprezentację spółki potwierdź
  w KRS: `mcp__krs__get_entity` albo `mcp__krs__get_board` (numer z typu `KRS`).
- **Powołane orzeczenia:** podtyp `SYGNATURA` wskazuje bazę: `SN`, `SAD_POWSZECHNY`, `TK`, `KIO` →
  `mcp__saos__search_by_case`; `NSA`, `WSA` → `mcp__nsa__search_by_case`.
- **Akty:** `DZ_U` (Dz.U. 2018 poz. 1000), `ELI`, `CELEX` (np. 32016R0679) → `mcp__isap__get_act`,
  `mcp__eu-sparql__search_by_celex`.

## Algorytmy

| Numer | Reguła |
|---|---|
| PESEL | 11 cyfr; wagi 1-3-7-9-1-3-7-9-1-3; cyfra kontrolna = (10 - suma mod 10) mod 10. Miesiąc +80 dla XIX w., +20 dla XXI w. (+40, +60 dalej); 10. cyfra nieparzysta = mężczyzna |
| NIP | 10 cyfr (dopuszczalne `-` i spacje); wagi 6-5-7-2-3-4-5-6-7; suma mod 11 = cyfra kontrolna; wynik 10 = numer niepoprawny |
| REGON 9 | wagi 8-9-2-3-4-5-6-7; suma mod 11, wynik 10 → 0 |
| REGON 14 | pierwsze 9 cyfr jak wyżej + wagi 2-4-8-5-0-9-7-3-6-1-2-4-8, mod 11 (10 → 0) |
| KRS | 10 cyfr, bez publicznej sumy kontrolnej - tylko format; istnienie przez konektor `krs` |

## Sygnatury

| Pion | Przykłady | Rozpoznanie |
|---|---|---|
| SN | III CZP 11/13, IV CSK 123/15 | wydział I-VII + 2-4 wielkie litery + nr/rok |
| NSA | II FSK 1234/20, I OSK 5/21 | I-III + FSK / OSK / OPS / GSK / FPS / FSW / FZ |
| WSA | II SA/Wa 100/26 | I-IV + SA/<skrót miasta> |
| KIO | KIO 123/21, KIO/UZP 100/12 | prefiks KIO |
| TK | K 12/19, SK 5/20, P 7/18 | K, P, U, SK, Kp, Kpt, Pp |
| Sądy powszechne | I C 100/26, II K 200/24, I ACa 1234/23, XXV C 1500/23 | wydział I-XXXIX + repertorium (C, K, P, U, W, Ns, Nc, Ca, ACa, AKa...) |

Wzorzec SN obejmuje każdy kod z wielkich liter, więc przy identycznym dopasowaniu skrypt wybiera
NSA dla kodów FSK/OSK/GSK itd.

Ograniczenia: osoba bez roli przed nazwiskiem („Jan Kowalski zawarł...”) nie zostanie wykryta;
nazwa firmy wymaga formy prawnej (sp. z o.o., S.A., sp. k., s.c. ...).

---
Źródło: Patron (MateMatic Solutions, AGPL-3.0) - `backend/src/lib/pl-entities/checksums.ts`,
`regex.ts` (ADR-0008), `lib/pseudonim/plDetector.ts`. Odwołania do Dz.U. i dane z PESEL -
dodane w tym porcie.

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** tekst z sygnaturami, PESEL, NIP, KRS, ELI
- **Wynik zapisz w:** wynik walidacji w `_robocze/` (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `ekstraktor-cytatow-pl`, `citation-grounding-pl`
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
