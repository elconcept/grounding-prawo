# desloppify — instrukcja dla właściciela

## Co to jest i po co

desloppify to narzędzie CLI do śledzenia zdrowia bazy kodu. Uruchamia detektory (unused, dead-code, complexity, dupes, itp.), buduje trwały stan (`state.json`), generuje priorytetyzowany plan naprawczy i pokazuje postęp wymiarami (security, maintainability, style). Działa jak "living backlog": po każdym `scan` widzisz co się poprawiło, co pogorszyło, i co robić jako kolejne. Integruje się z AI asystentami przez skill — agent widzi `next`, `plan`, `show` i naprawia problemy sekwencyjnie.

## Jak działa (mechanizm)

1. **Scan** — `desloppify scan` uruchamia detektory per język (Tree-sitter, LSP, regex), zapisuje wyniki do `state.json` (hash pliku + issue ID + status), generuje diff względem poprzedniego skanu.
2. **Stan** — `state.json` to źródło prawdy: każdy issue ma status (open/fixed/auto_resolved/false_positive/wontfix/deferred), notatki, atestacje naprawy.
3. **Plan** — warstwa nad kolejką: `desloppify plan` buduje priorytetyzowaną listę (score, cluster, skip, focus). Subkomendy: `queue`, `resolve`, `skip`, `cluster`, `focus`, `triage`.
4. **Wykonanie** — `desloppify next` pokazuje kolejny element do zrobienia. Agent naprawia, robi `scan`, issue przechodzi w `fixed` (wymaga `--attest` przy `plan resolve`).
5. **Review** — `desloppify review` to subiektywna ocena LLM (architektura, naming, design) — importuje do stanu jako oddzielne measure.

## Główne polecenia

| Polecenie | Co robi | Kiedy użyć |
|-----------|---------|------------|
| `desloppify scan` | Uruchamia wszystkie detektory, aktualizuje stan, pokazuje diff | Po zmianach w kodzie, przed pracą, w CI |
| `desloppify status` | Pełny dashboard: score, wymiary, postęp, coaching | Szybki przegląd zdrowia projektu |
| `desloppify next` | Pokazuje kolejny element z execution queue | Start sesji naprawczej — "co robię teraz?" |
| `desloppify plan` | Generuje pełny priorytetyzowany plan (markdown) | Planowanie sprintu, przegląd backlogu |
| `desloppify plan queue` | Kompaktowa tabela elementów execution queue | Szybki podgląd kolejki bez markdowna |
| `desloppify plan resolve <id> --attest "..."` | Oznacza issue jako naprawiony (score movement + next step) | Po naprawie issue — wymaga atestacji |
| `desloppify plan skip <pattern> [--permanent\|--false-positive]` | Pomija issue (tymczasowo/permanentnie/fp) | False positive, debt zaakceptowany, wontfix |
| `desloppify plan cluster create <name> <pattern>` | Grupuje powiązane issue w klaster | Refaktoring wieloplakowy, feature work |
| `desloppify plan focus <cluster>` | Zwęża scope do klastra | Praca nad jedną obszarem |
| `desloppify show <pattern>` | Wykopuje issue po pliku/katalogu/detektorze/ID | Rozbicie problemu na konkretne pliki |
| `desloppify show --chronic` | Pokazuje issue reopened 2+ razy | Wykrywanie problemów systemowych |
| `desloppify autofix` | Auto-fix mechanicznych issue (unused imports, formatting) | Szybkie wyczyszczenie przed recenzją |
| `desloppify suppress <pattern>` | Permanently ciszy issue pasujące do wzorca | False positive, który nie da się naprawić |
| `desloppify exclude <pattern>` | Wyklucza ścieżki ze skanowania | Generated code, vendor, migration scripts |
| `desloppify review --run-batches --parallel --scan-after-import` | Uruchamia subiektywną recenzję LLM i importuje do stanu | Code review aspektów, których detektory nie łapią |
| `desloppify config` | Pokazuje/ustawia konfigurację projektu | Zmiana profilu, badge, lang-opt |
| `desloppify setup` | Instaluje globalny skill dla AI asystentów | Jednorazowo na maszynie developera |

## Typowy przebieg pracy

```bash
# 1. Pełny skan na start / w CI
desloppify scan --profile full

# 2. Zobacz dashboard
desloppify status

# 3. Wygeneruj plan i zobacz kolejkę
desloppify plan
desloppify plan queue

# 4. Weź pierwszy element
desloppify next

# 5. Pracuj nad issue (np. unused::src/foo.tsx::React)
#    — edytuj kod, usuń import

# 6. Zeskamuj naprawę (wymaga atestacji)
desloppify plan resolve "unused::src/foo.tsx::React" --attest "removed unused import, verified no runtime deps"

# 7. Przeskanuj ponownie — issue znika z open, score rośnie
desloppify scan

# 8. Powtarzaj: next -> fix -> resolve -> scan
#    Gdy queue pusta: desloppify backlog --count 20 (sprawdź co dalej)
```

## Dobre praktyki i błędy do unikania

- **Zawsze atestuj `resolve`** — bez `--attest` komenda odrzuci; to wymusza świadome potwierdzenie naprawy.
- **Używaj `--skip-slow` w CI** — detektory duplikatów (dupes) są wolne; `desloppify scan --skip-slow --profile ci`.
- **Nie pomijaj `scan` po `resolve`** — stan się nie zaktualizuje, `next` pokaże stary issue.
- **Klastrowaj przed masową naprawą** — `plan cluster create refactor-auth "auth::*"` → `plan focus refactor-auth` → pracuj w obrębie fokusa.
- **`suppress` vs `exclude`** — `suppress` ciszy issue (zostaje w stanie, widoczne w `show --status all`), `exclude` usuwa ścieżkę ze skanowania w ogóle.
- **`--force-resolve` tylko z `--attest`** — omija ochronę suspect-detector (gdy detektor poszedł do 0 legalnie).
- **Profile** — `objective` (tylko twarde metryki), `full` (wszystko), `ci` (szybki, bez dupes). Domyślny: `full`.
- **`review` to nie `scan`** — review importuje subiektywne measure, nie nadpisuje detektorów. Użyj `--scan-after-import` by zaktualizować stan po review.
- **State file** — domyślnie `.desloppify/state.json` w root projektu. Nie commituj go do gita (w `.gitignore`); commituj `.desloppify/config.toml`.
