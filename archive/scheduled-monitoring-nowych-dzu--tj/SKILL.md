---
name: monitoring-nowych-dzu--tj
description: Monitoring nowych Dz.U. / t.j. — TRYB DZU skilla audyt-systemu-v4
---

Pracujesz w repozytorium projektu `lex-machina` (podpięty folder). KORZEŃ PROJEKTU to katalog zawierający `.claude/skills/`. Wszystkie ścieżki poniżej są względne wobec korzenia projektu. Ta sesja startuje BEZ pamięci poprzednich rozmów — wykonaj poniższe kroki samodzielnie, opierając się wyłącznie na plikach skilla i weryfikacji online (isap.sejm.gov.pl, eli.gov.pl, pomocniczo dziennikustaw.gov.pl / sip.lex.pl / gofin.pl / infor.pl / prawo.pl), NIGDY z pamięci.

1. Wczytaj `.claude/skills/audyt-systemu-v4/SKILL.md` oraz jego references: `AUDIT-JOURNAL.md`, `WARN-OTWARTE.md`, `CHECKLIST-DEDUP.md` i NAJNOWSZY `mapa_dzu_YYYY-MM-DD.md` (pole `references:` w SKILL.md wskazuje, która mapa jest ⭐ AKTUALNA). Wczytaj też `.claude/skills/prawo-polskie-v2/ROUTING-MAP.md` oraz każdy `.claude/skills/dr-01..dr-16*/MAPA-AKTOW.md`.

2. FAZA 0 — ustal wynik ostatniego audytu, otwarte flagi, kontekst.

3. FAZA 3 w całości: 3-PULL (DR-MAPA-AKTOW → ROUTING-MAP → mapa_dzu), 3A (nowe teksty jednolite kluczowych aktów: KC, KPC, KPK, KRO, KP, KSH, KPA, PB, PrFarm, PIT, CIT, OrdPod, PrNotariat — pozycje wyższe niż ostatnio odnotowane), 3B (statusy OK→PREV + nowe wiersze), 3C (rozporządzenia „do weryfikacji" z WARN-OTWARTE.md), 3D (tabela MONITORING — przejdź ją WIERSZ PO WIERSZU, nie wybiórczo; akty, które weszły w życie, przenieś do tabeli głównej).

4. Priorytet: pozycje ⏳ OCZEKUJE / ⚡ WCHODZI-90DNI z MONITORING, wszystkie ⚠️ ALERT z poprzednich audytów, kluczowe kodeksy z kroku 3A.

5. FAZA 7A — dopisz wpis `## AUDYT-YYYY-MM-DD[litera]` na KOŃCU `AUDIT-JOURNAL.md`. FAZA 7B — jeśli są zmiany, utwórz nową generację `mapa_dzu_YYYY-MM-DD.md`; jeśli nie ma zmian, odnotuj to wprost w dzienniku.

6. ⚠️ ZAPIS: katalog `.claude/skills/` w tym projekcie jest ZAPISYWALNY. Zapisuj zmiany BEZPOŚREDNIO w `.claude/skills/audyt-systemu-v4/references/`. NIE produkuj plików „do wklejenia" ani archiwów `.skill` — to była obejściowa procedura dla montażu read-only i już nie obowiązuje. Po zmianie liczby lub numeracji map zaktualizuj pole `references:` w `audyt-systemu-v4/SKILL.md` (która mapa jest ⭐ AKTUALNA) i dopisz wpis do `references/CHANGELOG.md`.

7. Po zapisie uruchom `python3 .claude/skills/audyt-systemu-v4/scripts/ci_check_shared.py --repo-root .claude/skills` i dopisz wynik do wpisu w dzienniku.

8. Dopisz jedno zdanie podsumowania do `08-audyt/LOG-PRZEBIEGOW.md` (data, zakres, co zmieniono).

9. Zakończ krótkim podsumowaniem w czacie: co sprawdzono, co się zmieniło (lub „brak zmian"), gdzie zapisano.

Nie zgaduj żadnego numeru Dz.U. — każda zmiana musi być potwierdzona online przed zapisaniem. Zgodność numeru z oczekiwaniem NIE jest dowodem tożsamości aktu (lekcja F-82/F-104).
