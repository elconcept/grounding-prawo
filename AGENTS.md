# grounding-prawo - praca nad pluginem

To repo służy do **doskonalenia pluginu i refaktoru skilli**. Nie prowadzi się tu spraw prawnych: praca
prawnicza odbywa się w katalogu `legal` (volume1/legal, Synology Drive, repo `elconcept/legal`): `AGENTS.md` (zasady;
`CLAUDE.md` tylko go dołącza) i `PRZEWODNIK.md` (ścieżki, skille, MCP, komendy) mówią, jak używać zainstalowanego pluginu.
Wiki spraw jest w Basic Memory (projekt `legal`), nie w plikach `legal`. Reguły dla modelu pracującego nad sprawą są w
pluginie: `selection/overlay/shared/ZASADY-PLUGINU.md` (marketplace nie instaluje CLAUDE.md ani README.md). Wejście do
pracy prawnej: `prawny-router-v3` (dawny `prowadnik-grounding-prawo` jest z nim scalony; `build.py` przepisuje stare odwołania).

## Układ repo
| Ścieżka | Rola |
|---|---|
| `plugins/grounding-prawo/` | **Generowane** przez `scripts/build.py`. Nie edytuj ręcznie. |
| `selection/selection.yaml` | Źródło prawdy: które skille, skąd (`lex`, `awe:<pakiet>`, `own`, `vendor:`), opisy, scalenia (`merge_into`: cały skill jako moduł `<host>/modules/<nazwa>/MODULE.md`; `fold_into`: typ pisma lub referencja). |
| `selection/patches/`, `selection/overlay/` | Patche na kopię upstreamu i pliki dopisane do pluginu (`shared/`). |
| `own-skills/` | Skille własne (bez upstreamu). Tu się je edytuje. |
| `vendor/` | Submoduły git: `packs/` (LexMachina, awesome-matematic-skills, legal-verify, commercial-legal, awesome-legaltech, awesome-legal-data), `docs/`, `general/`, `mcp/` (serwery MCP, działają w Dockerze za `lex.xlap.pl/mcp`), `law/` (37 ustaw z komentarzem do każdego artykułu, źródło bazy ustaw). Tylko do odczytu - zmiany jako patch albo reguła w `build.py`. |
| `deploy/` | Wdrożenia na NAS: `mcp-ustawy/` (serwer MCP bazy ustaw). |
| `scripts/` | `build.py` (budowa), `validate_marketplace.py`, `lint_refs.py` (martwe odwołania), `report.py`. |
| `archive/` | Kosz odroczonego usuwania; usuwa wyłącznie właściciel. |
| `.claude-plugin/`, `.agents/plugins/` | Manifesty marketplace (Claude Code, Codex). |
| `.claude/skills/`, `.agents/skills/` | Skille do pracy nad repo (`fastmcp-builder`, `marketplace-installer`), nie część pluginu. |

## Cykl zmiany
1. Zmień `own-skills/`, `selection/` albo `scripts/build.py` (nigdy `plugins/` ani `vendor/`).
2. `python3 scripts/build.py` → `python3 scripts/validate_marketplace.py` → `python3 scripts/lint_refs.py`.
3. Commit razem ze zregenerowanym `plugins/`. Push na `main` = wydanie: manifest Claude nie ma pola `version`,
   więc klienci aktualizują się po SHA commita (przypięta wersja blokowała aktualizacje). Wersja semver jest tylko w manifeście Codex.
4. Aktualizacja upstreamu: `git submodule update --remote vendor/packs/<nazwa>`, build, przegląd różnic w `plugins/`.

## Zasady
- Reguły i instrukcje, które model ma dostać przy pracy nad sprawą, wpisuj do skilli lub `shared/` pluginu,
  nie do CLAUDE.md/README.md: tych plików marketplace nie dostarcza.
- Decyzje właściciela (14.10.2026): brak anonimizacji i zakazu chmury w skillach, MCP tylko przez portal,
  profil MAX bez bramek kosztu, `zawiadomienie-o-przestepstwie` omija tor procesowy routera.
- Decyzje właściciela (20.10.2026): bez Paperless, MinIO i EUREKA; ingest PDF do R2, Markdown do Basic Memory;
  pisma bez tytułu zawodowego i numeru wpisu; skille o tej samej funkcji scalone w moduły; komendy tylko tam, gdzie
  nie zastępuje ich skill (`/transkrypcja`).
- Nowa funkcja skilla, który już istnieje: dopisz ją do niego albo jako moduł (`merge_into`), nie jako nowy skill.
- Materiał do doskonalenia skilli: transkrypcje sesji w `INBOX/` (poza gitem; komenda `/transkrypcja` w `legal`) i lekcje
  w `legal/sprawy/<sprawa>/_wiedza.md`. Uwagę ogólną przenoś do skilla albo `shared/`, uwagę jednej sprawy zostaw w `_wiedza.md`.
- Git jest kopią zapasową: commituj wszystko, co brudne, także cudze zmiany.
- Opis ścieżek i konektorów dla użytkownika: `README.md`.
