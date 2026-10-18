---
description: Domknij pracę nad sprawą - przebiegi, lekcje (_wiedza.md), teczka i stan w Basic Memory.
argument-hint: [katalog sprawy]
---

Domykasz pracę: $ARGUMENTS

1. `drafty/<pismo>/_PRZEBIEGI.md`: data, cel, wersje, soczewki (ścieżki w `_robocze/`), decyzje użytkownika, co otwarte.
2. `<teczka>/_wiedza.md`: lekcje na kolejne pisma - uwagi użytkownika do treści i formy, fakty doprecyzowane przez użytkownika
   (oznacz „relacja”), błędy modelu. Uwagi ogólne (nie tylko tej sprawy) zgłoś jako kandydatów do pluginu (`grounding-prawo`).
3. Basic Memory, projekt `legal`, teczka `sprawy/<katalog>/`: w notatce teczki zaktualizuj `## Stan`, `## Terminy`, `## Decyzje użytkownika`,
   `## Lekcje`, `## Relacje`; notatka pisma w `sprawy/<katalog>/pisma/` - wersja, ścieżka pliku, wynik kontroli, status, termin i sposób złożenia.
   Nie przepisuj wiki hurtem; nowe dokumenty i ustalenia zapisz i zweryfikuj przez skill `ingest-wiki`.
4. Stan bieżący sprawy (następny krok, data) zostaje w `## Stan` teczki Basic Memory z pkt 3; nie zakładaj osobnego pliku stanu.
5. Esencję z `_robocze/` przenieś do plików `_*.md`; nie zostawiaj raportów poza `_robocze/`.
6. Jeśli w sesji użyto skilli i ich zachowanie warto poprawić - zaproponuj `/transkrypcja`.
