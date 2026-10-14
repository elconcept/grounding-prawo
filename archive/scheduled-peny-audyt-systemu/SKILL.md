---
name: peny-audyt-systemu
description: Pełny audyt systemu — TRYB AUTO skilla audyt-systemu-v4
---

Pracujesz w repozytorium projektu `lex-machina` (podpięty folder). KORZEŃ PROJEKTU to katalog zawierający `.claude/skills/`. Wszystkie ścieżki są względne wobec korzenia projektu. Sesja startuje BEZ pamięci poprzednich rozmów.

Uruchom `.claude/skills/audyt-systemu-v4/SKILL.md` w TRYBIE AUTO: Fazy 0–7 w całości, bez menu interaktywnego.

⚠️ ZAPIS: katalog `.claude/skills/` jest ZAPISYWALNY. Zapisuj zmiany BEZPOŚREDNIO w drzewie skilli. NIE produkuj plików „do wklejenia" ani archiwów `.skill`.

Obowiązkowo:
- FAZA 7A — wpis `## AUDYT-YYYY-MM-DD[litera]` na KOŃCU `audyt-systemu-v4/references/AUDIT-JOURNAL.md`.
- Aktualizacja `references/WARN-OTWARTE.md` wraz z TABLICĄ STERUJĄCĄ (licznik flag) i polem „kolejny wolny numer".
- Po zapisie: `python3 .claude/skills/audyt-systemu-v4/scripts/ci_check_shared.py --repo-root .claude/skills` oraz `python3 .claude/skills/audyt-systemu-v4/scripts/run_regression_suite.py --repo-root .claude/skills`; wynik obu dopisz do wpisu w dzienniku.
- Jedno zdanie podsumowania do `08-audyt/LOG-PRZEBIEGOW.md`.

Zakaz cytowania numerów Dz.U. i sygnatur z pamięci — każde powołanie weryfikuj online przed zapisem.
