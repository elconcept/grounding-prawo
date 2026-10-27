---
name: teczka-sprawy
description: 'Teczka sprawy: spis dokumentów, brief, spis treści i podsumowanie sprawy do DOCX. Używaj przy porządkowaniu akt i przygotowaniu teczki.'
---

## Pamięć sesji — przed pracą i przed odpowiedzią końcową

Przeczytaj `shared/BASIC-MEMORY.md`, `shared/ZASADY-PLUGINU.md` oraz katalog `shared/INDEKS-SKILLI.md`. Przy redakcji pisma wczytaj `shared/STYLE.md`; przy zapisie plików `shared/ARTEFAKTY-SPRAWY.md`. Na wejściu odczytaj kluczowe trwałe ustalenia z `model-memory`, ostatni recap z `main` i sprawę z `legal`; po etapach zapisuj recap sesji w `main/sesje/` i sprawdź odczytem. Do `model-memory` dodawaj wyłącznie nowe, wartościowe key takeaways; nigdy logu sesji. Nowe dokumenty i ustalenia zapisuj w `legal` po każdym zakończonym etapie. Podaj status pamięci i identyfikator notatki; nie zgłaszaj zapisu bez potwierdzenia MCP.

## Repertorium - pierwsze źródło w każdym zadaniu prawnym

Zanim powołasz, ocenisz albo pominiesz przepis, orzeczenie lub kwalifikację, wywołaj przez portal `lex` `repertorium_szukaj_repertorium` (wyszukiwanie semantyczne ustaw, orzeczeń SN, sądów powszechnych, NSA/WSA, TK i decyzji UODO): co najmniej jedno zapytanie o zagadnienie i stan faktyczny (`jurysdykcja="pl"`), osobne dla każdej tezy, zarzutu lub żądania pisma, a przy wątku unijnym (RODO, prawo UE, TSUE) także `"eu"`. Opisuj problem słowami, nie tylko numerem artykułu lub sygnaturą. Trafienia sprawdź w pełnym brzmieniu (`shared/MOD-TEKST-JEDNOLITY.md`) i w treści orzeczenia; fragment z wyniku nie jest cytatem. Zapytania i wykorzystane trafienia zapisz w śladzie przebiegu (`_PRZEBIEGI.md` albo `analiza/_dowody-i-przepisy.md`). Kontrola prawa bez zapytań do Repertorium ma wynik `NOT_CHECKED`; awaria lub brak trafień to wpis w śladzie, po którym szukasz dalej w `ustawy`, `saos`, `nsa`, `uodo`, `eu-sparql`.

# Teczka sprawy

Skrypty są częścią pluginu, a katalog `legal` zawiera materiały spraw.
Ustaw `LEGAL_WORKSPACE` na rzeczywisty katalog projektu. Parametr `--sprawa` wskazuje
katalog względny wobec niego, na przykład `sprawy/nazwa_sprawy`.

1. Uruchom `scripts/dokumenty_sprawy.py --sprawa KATALOG` z katalogu skilla; w razie
   potrzeby dodaj katalog biblioteki opcją `--dodaj`. Sprawdź wykazane braki.
2. Zapisz uzgodniony spis opcją `--wykonaj`. Brief i podsumowanie pozostają treścią
   autora; nie aktualizuj ich automatycznie na podstawie samych nazw plików.
3. `scripts/teczka.py --sprawa KATALOG` składa `00_BRIEF.docx`, `01_SPIS_TRESCI.docx`
   i `02_PODSUMOWANIE.docx`. Wymaga `python-docx` oraz `pandoc`; PyMuPDF jest używane
   do ustalenia liczby stron PDF, jeśli jest dostępne.
4. Sprawdź pliki i zaktualizuj notatkę teczki w Basic Memory oraz recap zgodnie
   z `shared/BASIC-MEMORY.md`.

To składanie dokumentów lokalnych, nie ingest. Do odczytu i ingestu przez sam MCP
używaj `wiki-basic-memory/modules/ingest-wiki`. Host bez dostępu do plików wynikowych nie może deklarować,
że zapisał dokumenty DOCX w lokalnej teczce użytkownika.

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** Aktualna teczka sprawy i jej rejestr dokumentów.
- **Wynik zapisz w:** Brief, spis treści i podsumowanie teczki w katalogu sprawy. (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `pisma-procesowe-v3`
- **Basic Memory (`legal`):** Zaktualizuj notatkę teczki po potwierdzeniu wygenerowanych dokumentów. (protokół: `shared/BASIC-MEMORY.md`)
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
