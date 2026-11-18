# CHAT-MODULE-INDEX — lokalizacja, selekcja i wyjątki

Źródłowe tabele i semantyka wyboru G/H/I/K/J0–J21/MA w `SKILL.md` i `references/mod-J0-routing.md` pozostają nadrzędne. Poniższy indeks jest tylko katalogiem dostępnych plików, bez dodatkowego routingu.

## PRIMARY G/H/I/K

- `references/b2b-podwykonawcze.md`
- `references/umowy-o-prace.md`
- `references/zakaz-konkurencji.md`
- `references/poufnosc-nda.md`

## DOMAIN J and MA

- `references/mod-FA-founders-dokumenty-zalozycielskie.md`
- `references/mod-J0-routing.md`
- `references/mod-J1-najem.md`
- `references/mod-J10-ubezpieczenia.md`
- `references/mod-J2-nieruchomosci.md`
- `references/mod-J21-rodo-archiwizacja-regulaminy.md`
- `references/mod-J3-dystrybucja.md`
- `references/mod-J4-finansowanie.md`
- `references/mod-J5-umowy-wykonawcze.md`
- `references/mod-J6-it-konsorcjum.md`
- `references/mod-J7-pzp.md`
- `references/mod-J8-b2c.md`
- `references/mod-J9-ip-prawa-autorskie.md`
- `references/mod-MA-transakcje.md`

## SHARED contract modules

- `references/mod-shared-abusive-clauses.md`
- `references/mod-shared-ai-act.md`
- `references/mod-shared-alt-drafts.md`
- `references/mod-shared-antywzorce-jezykowe.md`
- `references/mod-shared-diff-intelligence.md`
- `references/mod-shared-economic.md`
- `references/mod-shared-esg.md`
- `references/mod-shared-fallback-library.md`
- `references/mod-shared-fm-hardship.md`
- `references/mod-shared-ius-cogens.md`
- `references/mod-shared-legal-design.md`
- `references/mod-shared-lifecycle.md`
- `references/mod-shared-missing-clause.md`
- `references/mod-shared-model-umowy.md`
- `references/mod-shared-neg-strategia.md`
- `references/mod-shared-orzecznictwo-umow.md`
- `references/mod-shared-regulatory-horizon.md`
- `references/mod-shared-rodo.md`
- `references/mod-shared-ryzyko-kwant.md`
- `references/mod-shared-wykladnia.md`
- `references/mod-shared-zlote-reguly.md`

## CORE and routing

- `references/mod-core-checklist.md`
- `references/mod-J0-routing.md`

## Generator library

- `references/generator/boilerplate-strukturalne.md`
- `references/generator/doktryna-uzupelnienie.md`
- `references/generator/essentialia-regulaminy-i-korporacyjne.md`
- `references/generator/kategorie-klauzul-taksonomia.md`
- `references/generator/legal-design-produkcyjny.md`
- `references/generator/rdzen-generowania.md`
- `references/generator/style-format-generowania.md`

## Workflows

- `workflows/generator-dokumentow-hr-rodo.md`
- `workflows/generator-dokumentow-korporacyjnych.md`
- `workflows/generator-regulaminu.md`
- `workflows/generator-umowy.md`
- `workflows/ocena-drugiej-strony.md`
- `workflows/popraw-fragment.md`
- `workflows/triage-szybki.md`
- `workflows/weryfikacja-spojnosci-odeslan.md`

## CUAD 41 categories

- `modules/klauzule-kontraktowe-pl/MODULE.md`
- `modules/klauzule-kontraktowe-pl/references/przeglad-umow.md`

## Deterministic tools

- `scripts/kontrakt_rachunek.py`
- `scripts/test_kontrakt_rachunek.py`
- `references/szukaj_klauzul_uokik.py`

## Benchmark only

- `benchmark/posiane-wady/README.md`
- `benchmark/posiane-wady/manifesty/instrukcja-sedziego.md`
- `benchmark/posiane-wady/manifesty/manifest.yaml`
- `benchmark/posiane-wady/umowy/01-czysta-b2b.md`
- `benchmark/posiane-wady/umowy/02-jawne-nda.md`
- `benchmark/posiane-wady/umowy/03-ukryte-wdrozenie.md`
- `benchmark/posiane-wady/umowy/04-matematyczna-tm.md`
- `benchmark/posiane-wady/umowy/05-adwersarialne-injection.md`
- `benchmark/posiane-wady/wyniki/oceny/README.md`

## Dwa istotne aliasy z archiwum
- **Kalkulator:** historyczne `shared/tools/kontrakt_rachunek.py` jest nieobecne w kanonicznym `shared`; prawidłowa obecna ścieżka to `scripts/kontrakt_rachunek.py` (źródło i 15 testów).
- **Plan regresji:** `references/REGRESSION-TEST-PLAN.md` jest historycznym odwołaniem, ale pliku brak; użyj jedynie istniejących fixture w `benchmark/posiane-wady/` i bez zmyślania planu.
- **Wewnętrzna ścieżka CUAD:** `modules/klauzule-kontraktowe-pl/references/przeglad-umow.md` istnieje jako plik podrzędny modułu, nie jako `references/przeglad-umow.md` w korzeniu.
- **Prawa:** `NOTICE` i `LICENSE` (GPLv3) skilla, `modules/klauzule-kontraktowe-pl/LICENSE` oraz wskazane plikowe atrybucje Apache-2.0 pozostają zachowane.
