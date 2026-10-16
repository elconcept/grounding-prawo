# grounding-prawo

Prywatny marketplace z jednym pluginem do praktyki prawa polskiego (Claude Desktop, Cowork, Code; ChatGPT/Codex). Łączy silnik
Lex Machina, skille weryfikacji MateMatic, skille własne i wiedzę z pluginu IURA; zasada: **źródłem tezy o przepisie lub orzeczeniu
jest narzędzie MCP albo dokument, nigdy pamięć modelu.**

To repo służy do rozwijania pluginu. **Jak pracować ze skillami nad sprawą** (ścieżki A-E, katalog skilli, konektory MCP, kolizje,
komendy): `legal/PRZEWODNIK.md` i `legal/CLAUDE.md` w katalogu spraw. Reguły, które model dostaje razem z pluginem:
`plugins/grounding-prawo/skills/shared/ZASADY-PLUGINU.md`, `ARTEFAKTY-SPRAWY.md`, `FORMAT-PISMA.md`.

Plugin jest **generowany** - nie edytuj `plugins/grounding-prawo/` ręcznie (sekcja [Utrzymanie](#utrzymanie)); zasady pracy nad repo: `AGENTS.md`.

## 1. Instalacja

Repozytorium jest prywatnym marketplace z jednym pluginem (`grounding-prawo`). Wersja semver (tylko manifest Codex): `selection/selection.yaml`.

| Klient | Jak |
|---|---|
| **Claude Code** | `claude plugin marketplace add elconcept/grounding-prawo`, potem `claude plugin install grounding-prawo@grounding-prawo` |
| **Claude Desktop / Cowork** | Ustawienia organizacji → Plugins → dodaj marketplace z GitHub (repo `elconcept/grounding-prawo`; repo prywatne, więc wymaga autoryzacji GitHub). Po synchronizacji plugin pojawia się w katalogu konta. Wymaga uprawnień zarządzania pluginami. |
| **ChatGPT / Codex** | `codex plugin marketplace add elconcept/grounding-prawo`, potem `codex plugin add grounding-prawo`. Aplikacja ChatGPT korzysta z tego samego manifestu `.codex-plugin`. |

Po instalacji sprawdź w **nowej rozmowie**: „Użyj prowadnik-grounding-prawo i powiedz, co potrafi plugin”. Skille z błędem
ładowania nie pojawią się na liście.

Konektory prawnicze ładuje `.mcp.json` pluginu: jeden serwer `lex` → `https://lex.xlap.pl/mcp` (portal Cloudflare z
logowaniem OAuth). Przy pierwszym użyciu host poprosi o autoryzację. Bez niej skille działają, ale nie mogą podawać
przepisów ani sygnatur (zob. [10. Problemy](#10-rozwiązywanie-problemów)).

Pełna lista kontroli instalacji i granice testów: `_log/marketplace-validation.md`. Test CLI nie dowodzi synchronizacji konta
Claude/Cowork ani aktywacji w ChatGPT - to potwierdza dopiero odczyt skilla w nowej rozmowie.

### Aktualizacje

- Manifest pluginu nie ma pola `version`, więc każda zmiana na `main` to nowa wersja (SHA commita).
- Claude Desktop / Cowork (marketplace w claude.ai): aktualizacja automatyczna; nowa wersja działa w nowej rozmowie.
- Claude Code z marketplace GitHub: auto-update jest domyślnie **wyłączony** dla marketplace spoza Anthropic. Włącz: `/plugin` →
  Marketplaces → grounding-prawo → Enable auto-update, albo `"autoUpdate": true` przy `grounding-prawo` w `extraKnownMarketplaces`
  (`~/.claude/settings.json`). Ręcznie: `claude plugin update grounding-prawo@grounding-prawo`.

---

## Utrzymanie

```bash
python3 -I scripts/build.py              # generuje plugins/grounding-prawo z selekcji
python3 -I scripts/validate_marketplace.py
python3 -I scripts/lint_refs.py          # martwe odwołania do skilli i plików
node plugins/grounding-prawo/skills/citation-grounding-pl/scripts/test-grounding.mjs
claude plugin validate plugins/grounding-prawo
```

| Co zmienić | Gdzie |
|---|---|
| lista skilli, wersja | `selection/selection.yaml` |
| przepływ i mosty między skillami | `selection/bridges.yaml` |
| skill własny, typ pisma | `own-skills/<nazwa>/` (+ wpis `fold_into` w selekcji dla typów pism) |
| plik dopisany do pluginu (np. `shared/ARTEFAKTY-SPRAWY.md`) | `selection/overlay/` |
| zmiana skilla z upstreamu | `selection/patches/NN-*.patch` (nigdy w `vendor/`) |
| reguła generująca (np. oznaczanie odwołań) | `scripts/build.py` |

Historia selekcji: `_log/selekcja.md`, `_log/skill-triage.md`, `_log/source-map.md`.
