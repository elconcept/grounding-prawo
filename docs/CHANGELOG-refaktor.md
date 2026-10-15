# Refaktor korpusu skilli (0.1.1 → 0.2.0, 2026-10-15)

- **Martwe odwołania:** `scripts/lint_refs.py` (2584 → 0, logi historyczne pominięte; w CI). Generator: oznaczanie odwołań do
  skilli spoza pluginu `(poza pluginem)`, kwalifikacja ścieżek do właściwego skilla albo `(brak w pluginie)`, przepisywanie
  ścieżek w modułach scalonych. Odwołania z oznaczeniem są jawnie nieużywalne, nie przepisane merytorycznie.
- **IURA:** moduły typów pism: cofnięcie pozwu, wniosek o rozprawę zdalną, ocena decyzji prokuratora, notatka prawna, memo UE
  (`pisma-procesowe-v3/modules/typy/`); `przeglad-umow` jako referencja `klauzule-kontraktowe-pl`; metodyka SAOS/ISAP w
  `patron-prawo-pl-zrodla/references/iura-metodyka.md`. Wcześniej scalone moduły są większe od oryginałów IURA.
- **Przepływ:** `selection/bridges.yaml` → sekcja MOST w każdym skillu; skill `prowadnik-grounding-prawo`; README.md.
- **Artefakty:** `shared/ARTEFAKTY-SPRAWY.md` (zastępuje brakujący `MOD-PLIKI-INKREMENTALNE`), `_wiedza.md`; usunięty
  `MOD-AUDIT-BUNDLE` (patch 05). Dodany brakujący `shared/MOD-TEKST-JEDNOLITY.md` (bez `lexcache`, z `cite_verify_article`).
- **Nie zrobiono:** scalania skilli o nakładającym się zakresie (zależności, `test-grounding`); zamiast tego reguły
  rozstrzygania w README (sekcja 8) i pole „Nie dubluj” w MOST.
