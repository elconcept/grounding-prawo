# Build provenance i source of truth — grounding-prawo

## Potwierdzony stan na 2026-11-23

Na `main` istnieją **dwa różne produkty**:

- `plugins/grounding-prawo/` — *generowany* przez `scripts/build.py`; katalog `plugins/.../skills/` jest usuwany i odtwarzany. Nie edytuj go ręcznie.
- `plugins/lexmachina-chat/` — *bezpośrednio utrzymywany*, 12 skilli; builder `scripts/build.py` go nie buduje ani nie dotyka. Walidator: `scripts/validate_chat_plugin.py`.

Podstawowa mapa źródła:
```
vendor/packs/LexMachina/Wersja rozwojowa rozpakowana/<skill>/
vendor/packs/awesome-matematic-skills/<bundle>/skills/<skill>/
own-skills/<skill>/
                |
                v
selection/selection.yaml  (keep/drop/from, merge_into, fold_into, metadata)
                |
                v
scripts/build.py
   1. kopiuje SKILL.md i zasoby źródeł do plugins/grounding-prawo/skills/
   2. kopiuje selection/overlay/ (nakładając na skopiowane źródła)
   3. nakłada posortowane selection/patches/*.patch (obecnie 13)
   4. modyfikuje nazwy MCP, fold_into, merge_into i usuwa reguły
   5. dołącza the-ocr, kontrakt dokumentów i migruje odwołania
   6. scrub: usuwa klauzule anonimizacji i odwołania poza pluginem
   7. dodaje MOST z selection/bridges.yaml i protokół sesji
   8. normalize_skill, scripts/retire_layers.py (transformacje proceduralne)
   9. przywraca humanizer-pl z own-skills (VERBATIM), filtruje governance
  10. generuje indeks skilli, hooks, commands, manifesty i .mcp.json
                |
                v
plugins/grounding-prawo/ (DYSTRYBUCJA)
```

**Źródło prawdy jest złożone**, nie stanowi go ani `vendor/`, ani sam `selection.yaml`. Skład kontroluje `selection/selection.yaml`; treść końcową wyznaczają razem przypięte źródła, `own-skills/`, `selection/overlay/`, `selection/patches/`, `selection/bridges.yaml`, `scripts/build.py` oraz `scripts/retire_layers.py`. Wygenerowany katalog to artefakt, nie miejsce do manualnych poprawek.

W `selection.yaml` wykryto 70 pozycji `keep` (24 LexMachina, 19 MateMatic, 27 własnych), z których część jest łączona w moduły, a nie emitowana jako osobne skille. Przepływ jest ciężki, m.in. `selection/patches/01-prawny-router-v3-bez-anonimizacji.patch` (~80 kB) oraz `scripts/retire_layers.py` (~33 kB); przenoszenie skilla 1:1 nie jest równoważne wynikowi builda.

## MateMatic: odpięto forka

`vendor/packs/awesome-matematic-skills` wskazuje bezpośrednio na `https://github.com/matematicsolutions/awesome-matematic-skills-pl.git`, commit `7e15bbea11c2fb8862a965505d86a7d0de3fd92d`. Porównanie repo z wcześniejszym `elconcept/awesome-matematic-skills@8e916898a5ffac02c1c9fee692c6f70a13e7dd75` wykazało dokładnie jeden dodany plik w forku: `.github/workflows/fixture-baseline.yml`. Pozostałe pliki źródłowe identyczne; nie przenosimy workflow do submodułu, tylko utrzymujemy jego wywołania w głównym CI.

## Co faktycznie testujemy

1. **Source contract**: oryginalne fixture i skrypty w upstream MateMatic, bez overlayu (regresje dostawcy).
2. **LawBenchmark reference**: kanoniczne pytania, klucze, historyczne karty, judge/verification; daje weryfikację parserów i oceniania *historycznych* odpowiedzi, nie nowego pluginu.
3. **Built adapter**: trzeba uruchomić `scripts/build.py` z przypiętymi submodułami i rzeczywiście testować `plugins/grounding-prawo`, w tym skrypt grounding, redline DOCX, scalone moduły, lokalne testy oraz połączenia.
4. **Live LLM A/B**: oddzielny jeszcze NIEPODŁĄCZONY runner dla *aktualnego* zestawu skilli i tych samych promptów/ustawień; osobna niezależna ocena prawna. Bez tego wynik jakości nie istnieje.
5. **Release sync**: wygenerowane `plugins/` musi odpowiadać wynikowi buildera; obecna stara walidacja build-plugin wykazała 8 plików różnicy po zmianie MateMatic, a więc nie można deklarować kompletnej synchronizacji produkcyjnego artefaktu.

Repo pracuje tylko na `main`; bez branchy i worktree. Nie modyfikujemy submodułów MateMatic ani LawBenchmark. Każde ulepszenie jest osobnym etapem i wymaga obydwu kontrolowanych przebiegów.
