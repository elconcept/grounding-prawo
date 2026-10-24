# rtk — instrukcja dla właściciela

## Co to jest i po co

rtk (rtk-ai/rtk, wersja 1.0.1) to wysokowydajny proxy CLI, które filtruje i podsumowuje wyjścia poleceń systemowych zanim trafią do kontekstu LLM. Każde polecenie Bash agenta przechodzi przez `ctx-guard` → `rtk rewrite` (jeśli pasuje reguła) lub `rtk run` (fallback). Wynik >150 linii lub >10 KB jest przycinany (początek, błędy, koniec); pełny log ląduje w `/tmp/ctx-logs/`. Dzięki temu kontekst LLM nie rozrasta się śmieciami (progress bars, verbose logs, powtarzające się linie), a Ty masz dostęp do pełnego wyjścia przez `rtk recall <hash>`.

## Jak działa (mechanizm)

1. **Hook** — każde wywołanie Bash agenta idzie przez `~/.agents/bin/ctx-guard` (hook PreToolUse dla Bash; osobny hook Read `rtk hook claude` odrzuca odczyt całego pliku >350 linii).
2. **Rewrite** — `ctx-guard` wywołuje `rtk rewrite "$CMD"`. Jeśli polecenie ma zdefiniowaną regułę kompresji (np. `git`, `rg`, `docker`, `pytest`), `rtk rewrite` drukuje przepisane polecenie (np. `rtk git status`) i zwraca exit code 0 (auto-allow) lub 3 (ask — wymaga zgody agenta).
3. **Brak reguły** — `rtk rewrite` zwraca 1 (nic nie drukuje) → `ctx-guard` uruchamia oryginał przez `rtk run -c "$CMD"`, co nadal filtruje stdout/stderr przez pipeline (domyślny filtr `smart`: 2-liniowe podsumowanie).
4. **Przycinanie** — `ctx-cap` (wywoływany przez `rtk run`) przycina output >150 linii / >10 KB. Pełny output w `/tmp/ctx-logs/<timestamp>.log`.
5. **Recall** — hint w przyciętym outputcie: `[ctx-cap] full log: /tmp/ctx-logs/... (hash: abc123)`. `rtk recall abc123` odtwarza pełne wyjście.
6. **Konfiguracja** — `~/.agents/README.md` opisuje integrację; `~/.agents/bin/ctx-guard`, `ctx-cap`, `rtk-llm-select` to skrypty hooków. Reguły kompresji w `rtk` (wbudowane + projektowe TOML przez `rtk trust`).

## Główne polecenia

| Polecenie | Co robi | Kiedy użyć |
|-----------|---------|------------|
| `rtk run -c "cmd"` | Uruchamia polecenie przez shell z filtrowaniem (fallback gdy brak reguły rewrite) | Każde polecenie agenta bez dedykowanej reguły; ręczne testy |
| `rtk run ls -la` | Uruchamia `ls` z kompaktowym outputem (proxy do natywnego) | Zamiast `ls` — oszczędza tokeny |
| `rtk read <plik> [--level minimal\|aggressive] [-m N]` | Czyta plik z inteligentnym filtrowaniem (signatury, importy) | Duże pliki zamiast `cat`; `--level aggressive` = tylko sygnatury |
| `rtk recall <hash> [--full]` | Odtwarza pełny output przycięty przez ctx-cap | Gdy `[ctx-cap]` pokaże hash — sprawdź co zostało ucięte |
| `rtk recall --list` | Lista przechowywanych wpisów recovery | Szukasz hasha z przeszłości |
| `rtk rewrite "cmd"` | Przepisuje surowe polecenie na ekwiwalent RTK (single source of truth dla hooków) | Debug hooków, sprawdź czy reguła istnieje |
| `rtk pipe -f <filter>` | Czyta stdin, aplikuje filtr, drukuje przefiltrowany output (Unix pipe mode) | Potoki: `kubectl logs pod | rtk pipe -f kubectl` |
| `rtk config --create` | Tworzy domyślny plik konfiguracyjny | Pierwsza konfiguracja projektu |
| `rtk config recall <sqlite\|tee\|disabled>` | Ustawia tryb recovery (sqlite = trwały, tee = pliki, disabled = wyłącz) | Zmiana strategii przechowywania pełnych logów |
| `rtk trust` | Ufa projektowym filtrów TOML w cwd | Włącza custom reguły kompresji dla repo |
| `rtk untrust` | Cofa ufność dla projektowych filtrów | Wyłącza custom reguły |
| `rtk verify` | Weryfikuje integralność hooków i testy inline TOML | CI, debug problemów z hookami |
| `rtk gain` | Podsumowanie oszczędności tokenów i historia | Monitoring efektywności kompresji |
| `rtk discover` | Wykrywa przeoczone oszczędności z historii Claude Code | Audyt: co można skompresować a nie jest |
| `rtk session` | Pokazuje adopcję RTK w sesjach Claude Code | Raportowanie użycia w zespole |
| `rtk grep "pattern" <path>` | Kompaktowy grep — strip whitespace, truncate, group by file | Zamiast `rg`/`grep` — mniejszy output |
| `rtk rg "pattern" <path>` | Kompaktowy ripgrep — natywne rg + ten sam filtr co grep | Gdy potrzebujesz speed rg + kompresja |
| `rtk git <subcmd>` | Git z kompaktowym outputem (log, diff, status, itp.) | Zamiast `git` — krótsze logi, diffy |
| `rtk docker <subcmd>` | Docker z kompaktowym outputem | `docker ps`, `logs`, `build` bez progress bars |
| `rtk test` | Uruchamia testy i pokazuje tylko failure | CI, szybki feedback |
| `rtk err` | Uruchamia polecenie, pokazuje tylko błędy/warningi | Debug: "co się zepsuło?" |
| `rtk summary` | Uruchamia polecenie, pokazuje heurystyczne podsumowanie (2 linie) | Szybki orientacyjny status |
| `rtk bypass "cmd"` | Uruchamia bez filtrowania, ale trackuje usage | Gdy filtr psuje output (binary, interactive) |
| `rtk ls` / `rtk tree` / `rtk find` | Kompaktowe odpowiedniki `ls`, `tree`, `find` | Eksploracja fs bez spamowania kontekstu |

## Typowy przebieg pracy

```bash
# 1. Agent wywołuje Bash (np. git status) → ctx-guard → rtk rewrite
#    Jeśli reguła istnieje: rtk rewrite drukuje "rtk git status" (exit 0/3)
#    Jeśli nie: ctx-guard robi rtk run -c "git status"

# 2. Output >150 linii → ctx-cap przycina, pokazuje hint:
#    [ctx-cap] truncated: 234 lines -> 150 (hash: a1b2c3d4)
#    [ctx-cap] full log: /tmp/ctx-logs/1700000000000000000.log (hash: a1b2c3d4)

# 3. Potrzebujesz pełnego outputu:
rtk recall a1b2c3d4 --full

# 4. Czytasz duży plik — zamiast cat (hook odrzuci >350 linii):
rtk read src/big.ts --level aggressive -m 80
#    lub pierwsze N linii:
rtk read src/big.ts --head-lines 100

# 5. Debug: dlaczego hook nie przepisał?
rtk rewrite "kubectl get pods -n prod"
#    exit 1 = brak reguły, exit 0/3 = przepisano

# 6. Włączasz custom reguły dla repo:
rtk trust
#    (wymaga .rtk/filters.toml w root projektu)

# 7. Sprawdzasz oszczędności:
rtk gain
```

## Dobre praktyki i błędy do unikania

- **Nie walkuj z hookiem** — `# ctx:raw` na początku polecenia Bash wyłącza przepisywanie i przycinanie dla tego wywołania (np. `# ctx:raw docker logs -f container`).
- **Nie czytaj `cat` dużych plików** — hook Read (`rtk hook claude`) odrzuci odczyt >350 linii. Użyj `rtk read plik --level minimal` lub `--head-lines N`.
- **`rtk run` vs `rtk rewrite`** — `rewrite` to tylko translacja (dla hooka), `run` to wykonanie z filtrem. W ręcznej pracy używaj `rtk run` lub po prostu wpisuj polecenie (hook zrobi resztę).
- **Recovery mode** — domyślnie `sqlite` (trwały, indeksowany). `tee` = pliki w `/tmp/ctx-logs/`, `disabled` = brak recall. Zmień: `rtk config recall tee`.
- **Hash recall** — unikalny prefiks hasha wystarczy (`rtk recall a1b2`).
- **Filtry projektowe** — `.rtk/filters.toml` w root repo. `rtk trust` włącza, `rtk untrust` wyłącza. `rtk verify` testuje.
- **`bypass` tylko awaryjnie** — omija pipeline, ale loguje usage. Nie używaj jako defaultu.
- **Verbose** — `-v`/`-vv`/`-vvv` przed subcommandem (np. `rtk -vv run -c "cmd"`) pokazuje co pipeline robi.
- **`--skip-env`** — ustawia `SKIP_ENV_VALIDATION=1` dla child process (Next.js, tsc, lint, prisma) — przydatne gdy te narzędzia wymagają specyficznego env.
- **Nie usuwaj `/tmp/ctx-logs/`** — to cache recall. Czyści się samo (TTL), ale ręczne `rm` traci historię recall.

## Integracja z agentami (kontekst)

- **Claude Code / Codex / OpenCode** — hook `ctx-guard` jest wywoływany automatycznie przy każdym `Bash` tool call.
- **`~/.agents/README.md`** — dokumentacja architektury: `ctx-guard` → `rtk rewrite` → `rtk run` → `ctx-cap` → `recall`.
- **`rtk-llm-select`** — wybiera model do podsumowania (gdy filtr `smart` używa LLM). Konfigurowalne zmiennymi env.
- **Skill `peer-agent-collaboration`** — orkiestrator deleguje wykonawcy; wykonawca też przechodzi przez ctx-guard (ten sam mechanizm).
