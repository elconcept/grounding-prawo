---
name: teczka-sprawy
description: Odświeża spis dokumentów teczki i składa brief, spis treści oraz podsumowanie kancelaryjne do DOCX w lokalnym katalogu sprawy.
---

## Pamięć sesji — przed pracą i przed odpowiedzią końcową

Przeczytaj `shared/BASIC-MEMORY.md`, `shared/ZASADY-PLUGINU.md` oraz katalog `shared/INDEKS-SKILLI.md`. Na wejściu odczytaj adekwatny kontekst z projektu `model-memory` i sprawy z `legal`; przed odpowiedzią końcową zapisz lub zaktualizuj recap w `model-memory` i sprawdź odczytem. Nowe dokumenty i ustalenia zapisuj w `legal` po każdym zakończonym etapie. Podaj status pamięci i identyfikator notatki; nie zgłaszaj zapisu bez potwierdzenia MCP.

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
używaj `ingest-wiki`. Host bez dostępu do plików wynikowych nie może deklarować,
że zapisał dokumenty DOCX w lokalnej teczce użytkownika.

## MOST - miejsce w przepływie grounding-prawo

- **Wejście z:** Aktualna teczka sprawy i jej rejestr dokumentów.
- **Wynik zapisz w:** Dokumenty kancelaryjne w teczce wskazanej przez użytkownika. (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)
- **Następny krok:** `pisma-procesowe-v3`
- **Basic Memory (`legal`):** Zaktualizuj notatkę teczki po potwierdzeniu wygenerowanych dokumentów. (protokół: `shared/BASIC-MEMORY.md`)
- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).
