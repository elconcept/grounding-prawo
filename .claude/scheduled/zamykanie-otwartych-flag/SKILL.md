---
name: zamykanie-otwartych-flag
description: Zamykanie otwartych flag — TRYB WARN-CLOSE skilla audyt-systemu-v4
---

Pracujesz w repozytorium projektu `lex-machina` (podpięty folder). KORZEŃ PROJEKTU to katalog zawierający `.claude/skills/`. Wszystkie ścieżki są względne wobec korzenia projektu. Sesja startuje BEZ pamięci poprzednich rozmów.

Uruchom `.claude/skills/audyt-systemu-v4/SKILL.md` w TRYBIE WARN-CLOSE.

1. Wczytaj `.claude/skills/audyt-systemu-v4/references/WARN-OTWARTE.md` — zacznij od TABLICY STERUJĄCEJ (sekcja A: flagi wykonalne sesją audytową). Flagi z sekcji B (zależne od dewelopera/środowiska) POMIŃ — sesja ich nie zamknie.
2. Weź flagi wg priorytetu z tablicy. Dla każdej: ustal stan faktyczny w plikach systemu i — gdy flaga dotyczy przepisu lub numeru Dz.U. — potwierdź online (RZĄD 1: ISAP/ELI). Nie zamykaj flagi na podstawie samej zgodności rejestrów wewnętrznych.
3. Zamknięcie flagi = USUŃ jej wiersz z WARN-OTWARTE.md (tablica + sekcja szczegółowa) i dopisz PEŁNY opis naprawy do `references/AUDIT-JOURNAL.md` na końcu pliku, z numerem flagi w tytule wpisu. Naprawa częściowa = skróć wiersz do tego, co ZOSTAŁO; opisu wykonanej części nie umieszczaj w WARN-OTWARTE.md.
4. Po każdej zmianie liczby flag zaktualizuj licznik w TABLICY STERUJĄCEJ oraz pole „kolejny wolny numer".

⚠️ ZAPIS: katalog `.claude/skills/` jest ZAPISYWALNY. Zapisuj BEZPOŚREDNIO. NIE produkuj plików „do wklejenia" ani archiwów `.skill`.

Po zapisie: `python3 .claude/skills/audyt-systemu-v4/scripts/ci_check_shared.py --repo-root .claude/skills`; wynik dopisz do wpisu. Dopisz jedno zdanie podsumowania do `08-audyt/LOG-PRZEBIEGOW.md`.
