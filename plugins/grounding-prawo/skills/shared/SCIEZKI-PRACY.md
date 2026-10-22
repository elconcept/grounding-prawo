# Wybór celu pracy - początek prawny-router-v3

Ustal cel z rozmowy; pytaj tylko o brakującą informację. Odczyt i zapis pamięci obowiązują wszystkie ścieżki.

| Cel | Działanie |
|---|---|
| Otwarcie pracy nad sprawą | sekcja „Otwarcie sprawy” poniżej, potem właściwa ścieżka |
| Dokument do odczytu lub ingestu | `odczyt-dokumentow` (skan, podpis, odczyt); ingest: `wiki-basic-memory` |
| Pytania do wiki, synteza wiedzy, kontrola jakości wiki | `wiki-basic-memory` |
| Analiza akt | `odczyt-dokumentow`, `chronologia-sprawy-v1`, `analizator-dowodow-v3`, domena DR, `analiza-sadowa-v6` |
| Nowe pismo | sekcja „Nowe pismo” poniżej |
| Zawiadomienie pokrzywdzonego | bezpośrednio `zawiadomienie-o-przestepstwie`; wyjątek od toru procesowego routera |
| Kontrola lub poprawa istniejącego pisma | `szturm-na-draft-pl` (pętla soczewek do `GOTOWE`) |
| Przepis, orzeczenie, akt UE, decyzja UODO | `patron-prawo-pl-zrodla`, następnie `analizator-przepisow-v2` lub `orzeczenia-sadowe-v2` |
| Termin, opłata, odsetki, przedawnienie, WPS | `kalkulatory-procesowe-pl` |
| Umowa | `analizator-umow-v1`, ewentualnie `redline-docx-pl` |
| Żądanie dotyczące danych osobowych | `rodo-dsar-pl` |
| Zamknięcie pracy | sekcja „Zamknięcie pracy” poniżej |

`prawo-polskie-v2` wybiera domenę DR wewnątrz routera. `przewodnik-prawny-v2` jest jego fallbackiem, gdy
problemu nie da się jeszcze zakwalifikować. Nie rozpoczynaj nowej rundy wyboru ścieżki po każdym skillu.
Wyniki i źródła przekazuj dalej; istniejących odczytów, ekstrakcji i kontroli nie powtarzaj bez powodu.

## Otwarcie sprawy

1. Ustal katalog teczki w `legal/sprawy/` (dopasuj sygnaturę, numer procedury, organ i nazwiska do nazwy katalogu oraz do
   notatek `sprawy/` w Basic Memory). Przy wątpliwości zapytaj jednym pytaniem: 2-3 kandydatów i opcja „nowa teczka”
   (`shared/ARTEFAKTY-SPRAWY.md`, „Teczka sprawy”). Do odpowiedzi nie zapisuj pisma.
2. Przeczytaj w tej kolejności: `analiza/_brief.md`, `_wiedza.md` teczki (lekcje z poprzednich pism obowiązują),
   `analiza/_dokumenty.md`, ostatnie wpisy `_PRZEBIEGI.md`.
3. Basic Memory, projekt `legal`: odczytaj notatkę teczki w `sprawy/<katalog>/` (`type: sprawa`; znajdź ją `search_notes` po nazwie katalogu albo sygnaturze). Brak teczki: załóż ją teraz
   (`write_note`, `directory: sprawy/<katalog>`, `type: sprawa`, układ jak w `shared/BASIC-MEMORY.md`), powiąż z notatkami
   `postepowania/` (szukaj po sygnaturze). Potem `build_context` z teczki i `search_notes` po nazwiskach. Ustalenia wiki to relacja
   do sprawdzenia w aktach, nie dowód.
4. Odpowiedz krótko: stan sprawy z datą źródła, najbliższy termin, czego brakuje w aktach, proponowana ścieżka i pierwszy skill.
   Nie zaczynaj pisać pisma, zanim użytkownik potwierdzi cel.

## Nowe pismo

Presja terminu nie zwalnia z tej ścieżki; skraca tylko liczbę iteracji.

1. Kontekst jak przy otwarciu sprawy, z ustaloną teczką. Dokumenty, na które pismo odpowiada, przeczytaj w całości.
   Zagadnienie pisma najpierw w Repertorium (`repertorium_szukaj_repertorium`), zanim powołasz przepis lub orzeczenie.
2. Generator: `pisma-procesowe-v3` (typ pisma), `pisma-proste-v2` (wezwania, wnioski, krótkie odpowiedzi),
   `zawiadomienie-o-przestepstwie` albo `rodo-dsar-pl`.
3. Przepisy i orzeczenia wyłącznie ze źródeł według `patron-prawo-pl-zrodla`; termin przez `kalkulatory-procesowe-pl`.
4. Format: `shared/FORMAT-PISMA.md`; pliki według `shared/ARTEFAKTY-SPRAWY.md` (wersje MD w `drafty/<pismo>/`, jeden DOCX w
   `legal/output/`: `shared/format-pisma/wersja_pisma.py nowe`, kolejne wersje `start` + `redline`, na końcu `sprawdz`).
   Telefon i e-mail nadawcy: zapytaj, jeśli nie są znane.
5. Redakcja według `shared/STYLE.md`: teza i najmocniejszy fakt na początku punktu, każda myśl raz, stanowisko strony bez
   przejmowania wersji organu.
6. Kontrola: `szturm-na-draft-pl` na gotowej wersji.
7. Przebieg w `drafty/<pismo>/_PRZEBIEGI.md`, lekcje w `_wiedza.md`; w Basic Memory notatka pisma w `sprawy/<katalog>/pisma/`
   (`type: pismo`, `status`, `dotyczy`) zakładana przy v1 i aktualizowana przy każdej wersji.

## Zamknięcie pracy

1. `drafty/<pismo>/_PRZEBIEGI.md`: data, cel, wersje, soczewki (ścieżki w `_robocze/`), decyzje użytkownika, co otwarte.
2. `_wiedza.md` teczki: lekcje na kolejne pisma (uwagi użytkownika do treści i formy, doprecyzowane fakty oznaczone „relacja”,
   błędy modelu). Uwagi ogólne zgłoś jako kandydatów do pluginu.
3. Basic Memory, teczka `sprawy/<katalog>/`: `## Stan`, `## Terminy`, `## Decyzje użytkownika`, `## Lekcje`, `## Relacje`;
   notatka pisma: wersja, ścieżka pliku, wynik kontroli, status, termin i sposób złożenia. Nowe dokumenty przez `wiki-basic-memory`.
4. Esencję z `_robocze/` przenieś do plików `_*.md`; recap sesji w `main` według `shared/BASIC-MEMORY.md`.
