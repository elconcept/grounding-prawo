## PROMPT 1

Skopiuj wszystkie skille z '.claude/.src/Lex-Machina-main/Wersja stabilna rozpakowana 21.08.2026' `.claude/skills` tego projektu. Zbadaj czy projekt został uruchomiony zgodnie z instrukcją `claude/.src/Lex-Machina-main/DOKUMENTACJA-WDROZENIOWA-2026-07-13.md`
Sprawdź scheduled taski w tym projekcie, wyjaśnij dlaczego mają problemy z zapisem, uporządkuj pliki które utworzone zostały w ich przebiegach, tak żeby ten projekt był gotowy na przyjęcie materiału dowodowego. 

---

I'll start by inspecting the environment on your machine.
> Output
>
> total 8
> drwxr-xr-x 3 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp 4096 Sep 10 02:14 .
> drwxr-x--- 5 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp 4096 Sep 10 02:14
> > Zrobione. Ale najpierw to, co ważniejsze od samej integracji.

Checked computer status
> Response
>
> {
> "platform": "darwin",
> "arch": "arm64",
> "appVersion": "1.49585.0",
> "electronVersion": "44.2.0",
> "nodeVersion": "24.20.0",
> "deviceName": "mac-localdomain",
> "connectedFolders": [
> "/Users/tom/lex-machina"
> ],
> "homeDirectories": [
> {
> "name": ".anaconda"
> },
> {
> "name": ".cache"
> },
> {
> "name": ".claude-server-commander"
> },
> {
> "name": ".conda"
> },
> {
> "name": ".config"
> },
> {
> "name": ".copilot"
> },
> {
> "name": ".cups"
> },
> {
> "name": ".gradle"
> },
> {
> "name": ".hawtjni"
> },
> {
> "name": ".homebrew"
> },
> {
> "name": ".idlerc"
> },
> {
> "name": ".local"
> },
> {
> "name": ".matplotlib"
> },
> {
> "name": ".npm"
> },
> {
> "name": ".nvm"
> },
> {
> "name": ".ollama"
> },
> {
> "name": ".parsec"
> },
> {
> "name": ".swiftpm"
> },
> {
> "name": ".Trash"
> },
> {
> "name": ".vscode"
> },
> {
> "name": ".vscode-shared"
> },
> {
> "name": ".zsh_sessions"
> },
> {
> "name": "archive"
> },
> {
> "name": "Claude"
> },
> {
> "name": "Desktop",
> "requiresGrantBeforeListing": true
> },
> {
> "name": "Documents",
> "requiresGrantBeforeListing": true
> },
> {
> "name": "Downloads",
> "requiresGrantBeforeListing": true
> },
> {
> "name": "DRAFTS"
> },
> {
> "name": "lex-machina"
> },
> {
> "name": "Library"
> },
> {
> "name": "mcp"
> },
> {
> "name": "Movies"
> },
> {
> "name": "Music"
> },
> {
> "name": "Pictures"
> },
> {
> "name": "projects"
> },
> {
> "name": "Public"
> },
> {
> "name": "temp"
> },
> {
> "name": "whisper"
> }
> ],
> "localMcpServers": [
> {
> "name": "Desktop Commander",
> "state": "announced"
> }
> ],
> "timestamp": "2026-09-10T02:14:42.675Z"
> }

Listed files on your computer
> Request
> {
> "path": "/Users/tom/projects"
> }
> Response

Inspect source repo root
> bash
>
> cd "$HOME/mnt/Lex-Machina-main" 2>/dev/null || cd "$HOME/mnt/lex-machina-main" 2>/dev/null || ls "$HOME/mnt/"; pwd; ls -la | head -40
> Output
>
> /sessions/rcw-01bhej8tctcetu9jm9qdyskp/mnt/Lex-Machina-main
> total 132
> drwx------ 18 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp   576 Sep  7 03:37 .
> drwxr-xr-x  4 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  4096 Sep 10 02:15 ..
> -rw-------  1 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp 14340 Sep 10 02:12 .DS_Store
> drwx------ 19 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp   608 Sep 10 02:09 .claude
> drwx------  3 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp    96 Sep  1 13:03 .github
> -rw-------  1 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp   127 Sep  1 13:03 .mcp.json
> -rw-------  1 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp 19706 Sep  1 13:03 DOKUMENTACJA-WDROZENIOWA-2026-07-13.md
> -rw-------  1 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp 35149 Sep  1 13:03 LICENSE
> -rw-------  1 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  6803 Sep  7 03:37 MEMO-INSTALACJA-WINDOWS.md
> -rw-------  1 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp 33296 Sep  2 06:17 README.md
> drwx------  2 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp    64 Sep  4 12:04 TEST-DIR-ZAPISU
> -rw-------  1 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp    13 Sep  4 12:04 TEST-ZAPISU.tmp
> drwx------ 35 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  1120 Sep  1 13:03 WERSJA ROZWOJOWA
> drwx------ 35 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  1120 Sep  1 13:03 WERSJA STABILNA 21.08.2026
> drwx------ 34 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  1088 Sep  4 12:04 Wersja rozwojowa rozpakowana
> drwx------ 37 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  1184 Sep  2 05:55 Wersja stabilna rozpakowana 21.08.2026
> -rw-------  1 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp   127 Sep  1 13:03 claude_desktop_config.json
> drwx------  4 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp   128 Sep  1 13:03 scripts

Inspect stable skills folder
> bash
>
> cd "$HOME/mnt/Lex-Machina-main/Wersja stabilna rozpakowana 21.08.2026"; ls -la; echo "=== SKILL.md count ==="; find . -name "SKILL.md" | wc -l; echo "=== top-level dirs w/ SKILL.md ==="; find . -maxdepth 2 -name "SKILL.md" | sort
> Output
>
> total 12
> drwx------  37 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp 1184 Sep  2 05:55 .
> drwx------  18 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  576 Sep  7 03:37 ..
> -rw-------   1 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp 8196 Sep  2 10:15 .DS_Store
> drwx------   4 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  128 Sep  1 13:03 analiza-sadowa-v6
> drwx------   8 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  256 Sep  1 13:03 analizator-dowodow-v3
> drwx------   4 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  128 Sep  1 13:03 analizator-przepisow-v2
> drwx------   5 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  160 Sep  1 13:03 analizator-umow-v1
> drwx------   8 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  256 Sep  1 13:03 audyt-systemu-v4
> drwx------   6 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  192 Sep  1 13:03 chronologia-sprawy-v1
> drwx------   6 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  192 Sep  1 13:03 dr-01-ustroj-konstytucyjny-i-zrodla-prawa
> drwx------   6 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  192 Sep  1 13:03 dr-02-prawo-cywilne-rodzinne-gospodarcze
> drwx------   6 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  192 Sep  1 13:03 dr-03-prawo-karne-wykroczenia-egzekucja
> drwx------   6 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  192 Sep  1 13:03 dr-04-prawo-pracy-zus-swiadczenia
> drwx------   6 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  192 Sep  1 13:03 dr-05-prawo-administracyjne-sadowoadministracyjne
> drwx------   7 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  224 Sep  1 13:03 dr-06-podatki-finanse-publiczne-aml
> drwx------   6 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  192 Sep  1 13:03 dr-07-zamowienia-publiczne-fundusze-ue
> drwx------   5 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  160 Sep  1 13:03 dr-08-samorzad-terytorialny-prawo-lokalne
> drwx------   6 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  192 Sep  1 13:03 dr-09-budownictwo-srodowisko-energia-transport
> drwx------   5 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  160 Sep  1 13:03 dr-09-out
> drwx------   5 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  160 Sep  1 13:03 dr-10-zdrowie-farmacja-zywnosc-rolnictwo
> drwx------   5 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  160 Sep  1 13:03 dr-11-cyfrowe-cyber-ai-dane-ip
> drwx------   5 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  160 Sep  1 13:03 dr-12-sadownictwo-prokuratura-zawody-prawnicze
> drwx------   5 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  160 Sep  1 13:03 dr-13-sluzby-bezpieczenstwo-informacje-niejawne
> drwx------   5 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  160 Sep  1 13:03 dr-14-prawo-ue-miedzynarodowe-prawa-czlowieka
> drwx------   5 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  160 Sep  1 13:03 dr-15-compliance-iso-governance-audyt
> drwx------   5 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  160 Sep  1 13:03 dr-16-pisma-strategia-dowody-orzecznictwo
> drwx------   4 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  128 Sep  1 13:03 orzeczenia-sadowe-v2
> drwx------   5 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  160 Sep  1 13:03 pisma-procesowe-v3
> drwx------   4 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  128 Sep  1 13:03 pisma-proste-v2
> drwx------   5 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  160 Sep  1 13:03 prawny-router-v3
> drwx------   4 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  128 Sep  1 13:03 prawo-polskie-v2
> drwx------  18 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  576 Sep  1 13:03 przesluchanie-swiadkow-v2-min90
> drwx------  18 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  576 Sep  1 13:03 przesluchanie-swiadkow-v2-min90-v35
> drwx------   4 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  128 Sep  1 13:03 przewodnik-prawny-v2
> drwx------   3 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp   96 Sep  1 13:03 raport-klienta-v1
> drwx------   3 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp   96 Sep  1 13:03 raport-sytuacyjny-v2
> drwx------ 127 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp 4064 Sep  2 05:56 shared
> === SKILL.md count ===
> 34
> === top-level dirs w/ SKILL.md ===
> ./analiza-sadowa-v6/SKILL.md
> ./analizator-dowodow-v3/SKILL.md
> ./analizator-przepisow-v2/SKILL.md
> ./analizator-umow-v1/SKILL.md
> ./audyt-systemu-v4/SKILL.md
> ./chronologia-sprawy-v1/SKILL.md
> ./dr-01-ustroj-konstytucyjny-i-zrodla-prawa/SKILL.md
> ./dr-02-prawo-cywilne-rodzinne-gospodarcze/SKILL.md
> ./dr-03-prawo-karne-wykroczenia-egzekucja/SKILL.md
> ./dr-04-prawo-pracy-zus-swiadczenia/SKILL.md
> ./dr-05-prawo-administracyjne-sadowoadministracyjne/SKILL.md
> ./dr-06-podatki-finanse-publiczne-aml/SKILL.md
> ./dr-07-zamowienia-publiczne-fundusze-ue/SKILL.md
> ./dr-08-samorzad-terytorialny-prawo-lokalne/SKILL.md
> ./dr-09-budownictwo-srodowisko-energia-transport/SKILL.md
> ./dr-09-out/SKILL.md
> ./dr-10-zdrowie-farmacja-zywnosc-rolnictwo/SKILL.md
> ./dr-11-cyfrowe-cyber-ai-dane-ip/SKILL.md
> ./dr-12-sadownictwo-prokuratura-zawody-prawnicze/SKILL.md
> ./dr-13-sluzby-bezpieczenstwo-informacje-niejawne/SKILL.md
> ./dr-14-prawo-ue-miedzynarodowe-prawa-czlowieka/SKILL.md
> ./dr-15-compliance-iso-governance-audyt/SKILL.md
> ./dr-16-pisma-strategia-dowody-orzecznictwo/SKILL.md
> ./orzeczenia-sadowe-v2/SKILL.md
> ./pisma-procesowe-v3/SKILL.md
> ./pisma-proste-v2/SKILL.md
> ./prawny-router-v3/SKILL.md
> ./prawo-polskie-v2/SKILL.md
> ./przesluchanie-swiadkow-v2-min90-v35/SKILL.md
> ./przesluchanie-swiadkow-v2-min90/SKILL.md
> ./przewodnik-prawny-v2/SKILL.md
> ./raport-klienta-v1/SKILL.md
> ./raport-sytuacyjny-v2/SKILL.md
> ./shared/SKILL.md

> Read deployment doc part 1
> bash
>
> cd "$HOME/mnt/Lex-Machina-main"; sed -n '1,200p' DOKUMENTACJA-WDROZENIOWA-2026-07-13.md
> Output
>
> # Dokumentacja wdrożeniowa: warstwa MCP, audit-trail i sync Dz.U
>
> **shared/MCP-INTEGRACJA.md · shared/AUDIT-TRAIL-SPEC.md · audyt-systemu-v4/references/SYNC-DZU-AUTOMATYCZNY.md**
>
> Wersja dokumentu: 2.0 (2026-07-13f) · Odbiorca: zespół developerski portalu (nie Claude)
> Powiązane: `audyt-komercyjny-silnika-prawnego.md` (rekomendacje #2, #4, #6),
> `AUDIT-JOURNAL.md` wpisy AUDYT-2026-07-13 do 2026-07-13f.
>
> ---
>
> ## 0. Jak czytać ten dokument?
>
> **Skonsolidowano (2026-07-13f):** treść trzech skilli przeniesiono do
> `shared/` (dla MCP i audit-trail — cross-cutting, używane przez router i
> potencjalnie każdy DR-skill) oraz do `audyt-systemu-v4/` (dla sync Dz.U. —
> bezpośrednio wspiera FAZĘ 3 tego właśnie skilla). Trzy zbędne skille-wrappery
> usunięto. Liczba skilli w systemie: 36 → 33 (powrót do stanu sprzed sesji
> 2026-07-13). Cała funkcjonalność, wszystkie testy i cała treść merytoryczna
> pozostały bez zmian — zmieniło się wyłącznie **gdzie** to mieszka.
>
> Ten dokument nadal tłumaczy *po co* te mechanizmy istnieją, *jak* są ze sobą
> powiązane, *co* trzeba zrobić żeby zaczęły działać produkcyjnie, i *co już
> zostało przetestowane* a co jeszcze nie — teraz pod nowymi, docelowymi
> ścieżkami.
>
> | Funkcjonalność                                      | Rekomendacja z audytu            | Nowa lokalizacja (kanoniczna)                          |
> | --------------------------------------------------- | -------------------------------- | ------------------------------------------------------ |
> | Warstwa MCP jako uzupełnienie HARD GATE             | #2                               | `shared/MCP-INTEGRACJA.md`                             |
> | Audit-trail zgodny z art. 12 AI Act                 | #4                               | `shared/AUDIT-TRAIL-SPEC.md`                           |
> | Automatyzacja wykrywania nowych Dz.U.               | #6                               | `audyt-systemu-v4/references/SYNC-DZU-AUTOMATYCZNY.md` |
> | Deterministyczna walidacja cytowań w gotowym piśmie | (sesja 2026-07-12, osobny wątek) | `shared/tools/walidator_cytowan.py` + `export_gate.py` |
>
> ---
>
> ## 1. Architektura — jak te elementy się łączą
>
> ```
>                          ┌─────────────────────────┐
>                          │   Użytkownik / sprawa    │
>                          └────────────┬────────────┘
>                                       │
>                          ┌────────────▼────────────┐
>                          │   prawny-router-v3 v3.16  │
>                          │   (orkiestrator)           │
>                          └──┬────────────────────┬───┘
>                             │                    │
>               KROK 1-4 protokołu       emisja znaczników
>               shared/MCP-INTEGRACJA.md AUDIT_EVENT (opcjonalnie,
>                             │          wymaga wdrożenia przez portal)
>               ┌─────────────▼─────────────┐        │
>               │ Connector MCP podłączony? │        │
>               └───┬───────────────────┬───┘        │
>               TAK │                   │ NIE         │
>                   ▼                   ▼             │
>         ┌──────────────────┐  ┌──────────────┐      │
>         │ Zapytanie do MCP  │  │ shared/       │      │
>         │ (ISAP/SAOS/CBOSA/ │  │ PRAWO-HARDGATE│      │
>         │  KRS/EUR-Lex)     │  │ .md (fallback)│      │
>         └─────────┬─────────┘  └──────┬───────┘      │
>                   │  FOUND+obowiązuje │               │
>                   │  → użyj wyniku    │               │
>                   │  inaczej → ▼      │               │
>                   └──────────►└───────┘               │
>                                                        ▼
>                                         ┌───────────────────────────┐
>                                         │ shared/tools/               │
>                                         │ router_event_parser.py      │
>                                         │ (portal, poza Claude)        │
>                                         └─────────────┬─────────────┘
>                                                        ▼
>                                         ┌───────────────────────────┐
>                                         │ shared/tools/               │
>                                         │ append_event.py             │
>                                         │ → audit_log.jsonl           │
>                                         │   (hash-chain SHA-256)       │
>                                         └─────────────┬─────────────┘
>                                                        ▼
>                                         ┌───────────────────────────┐
>                                         │ shared/tools/               │
>                                         │ hash_chain_verify.py        │
>                                         │ (kontrola integralności)      │
>                                         └───────────────────────────┘
> 
>   Osobno, przed present_files/eksportem gotowego pisma:
> 
>   ┌───────────────────────────┐        ┌─────────────────────────────┐
>   │ shared/tools/               │───────▶│ shared/tools/                 │
>   │ extract_api_verification_   │        │ walidator_cytowan.py          │
>   │ log.py (z konwersacji API)  │        │ (sprawdza cytaty w piśmie)     │
>   └───────────────────────────┘        └──────────────┬──────────────┘
>          oba wywoływane razem przez shared/tools/export_gate.py ──┘
>                                                         │
>                                           exit 0 → dopuść / exit 1 → zablokuj
> 
>   Równolegle, niezależnie od powyższego przepływu sesji:
> 
>   ┌────────────────────────┐        ┌─────────────────────────────┐
>   │ Harmonogram cron/Action │──raz──▶│ audyt-systemu-v4/scripts/     │
>   │ (HARMONOGRAM-CRON.md)   │dziennie│ sync_dzu_eli.py               │
>   └────────────────────────┘        └──────────────┬──────────────┘
>                                                       ▼
>                                      ┌───────────────────────────────┐
>                                      │ Sesja audyt-systemu-v4 FAZA 3   │
>                                      │ (człowiek + Claude, ręczna       │
>                                      │  weryfikacja i wpis do mapa_dzu) │
>                                      └───────────────────────────────┘
> ```
>
> **Kluczowa zasada widoczna na diagramie:** żadna z tych warstw nie zastępuje
> istniejącego mechanizmu — każda jest **równoległym uzupełnieniem**: MCP
> uzupełnia HARD GATE, audit-trail dokumentuje to, co router już robi,
> walidacja cytowań sprawdza gotowe pismo przed eksportem, sync-dzu przyspiesza
> wejście do sesji audytowej. I żadna z nich nie jest już osobnym skillem —
> wszystkie mieszkają tam, gdzie mieszka reszta infrastruktury tego samego typu.
>
> ---
>
> ## 2. shared/MCP-INTEGRACJA.md — szczegóły
>
> ### Co robi
>
> Protokół: zanim router użyje `web_search`/`web_fetch` do zweryfikowania
> powołania prawnego, sprawdza czy jest podłączony connector MCP dla danego typu
> zapytania. Jeśli tak — pyta go najpierw. Wynik klasyfikowany jako
> FOUND / NOT_FOUND / AMBIGUOUS / ERROR.
>
> ### Pliki i ich rola
>
> | Plik                                             | Rola                                                                                                                           |
> | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
> | `shared/MCP-INTEGRACJA.md`                       | Protokół 4-krokowy (dla Claude) + zasada nadrzędna „MCP uzupełnia, nie zastępuje HARD GATE”                                    |
> | `shared/KONEKTORY-REKOMENDOWANE.md`              | Lista typów connectorów do podłączenia + zasady bezpieczeństwa (read-only, brak danych sprawy w zapytaniach)                   |
> | `shared/SCHEMAT-ODPOWIEDZI-MCP.md`               | Format ustrukturyzowanej odpowiedzi oczekiwanej od connectora                                                                  |
> | `shared/tools/przyklad-adapter-normalizujacy.md` | Przykład koncepcyjny adaptera (JS), ilustracja nie gotowy kod                                                                  |
> | `shared/tools/test_mcp_protocol.py`              | **Gotowy, przetestowany kod Python**: funkcja `klasyfikuj_odpowiedz()` + `wymaga_fallbacku_hardgate()`, 6 testów jednostkowych |
> | `shared/tools/connector_health_check.py`         | **Gotowy, przetestowany kod Python**: health-check listy connectorów, z self-testem na mock-serwerze                           |
>
> ### Integracja z prawny-router-v3
>
> Router (v3.16) ładuje `shared/MCP-INTEGRACJA.md` jako `required_modules`
> **opcjonalnie** — `view` tego pliku jest tani (sam protokół), a faktyczne
> wywołanie narzędzia MCP następuje tylko, gdy narzędzie jest realnie dostępne.
>
> ### Co musi zrobić programista portalu
>
> 1. Wybrać ≥1 connector MCP z `shared/KONEKTORY-REKOMENDOWANE.md` i wdrożyć go.
> 2. Utworzyć `connectors.json` (format w nagłówku `connector_health_check.py`).
> 3. Uruchomić `python shared/tools/connector_health_check.py --config connectors.json` cyklicznie.
> 4. Dostosować `test_mcp_protocol.py::klasyfikuj_odpowiedz()` do natywnego formatu wybranego connectora, jeśli się różni.
> 5. Przetestować wszystkie 4 ścieżki wobec **realnego** connectora przed produkcją.
>
> ### Status testów
>
> ✅ `test_mcp_protocol.py` — 6/6 testów jednostkowych.
> ✅ `connector_health_check.py` — self-test na mock-serwerze HTTP.
> ⚠️ Nie przetestowano wobec żadnego realnego connectora MCP (flaga F-8).
>
> ---
>
> ## 3. shared/AUDIT-TRAIL-SPEC.md — szczegóły
>
> ### Co robi
>
> Specyfikacja + referencyjna implementacja logu zdarzeń z hash-chain SHA-256,
> zgodnego z wymogiem automatycznego rejestrowania zdarzeń z art. 12 AI Act.
>
> ### Pliki i ich rola
>
> | Plik                                  | Rola                                                                                                           |
> | ------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
> | `shared/AUDIT-TRAIL-SPEC.md`          | Specyfikacja: co logować (8 typów zdarzeń), format JSON Lines, algorytm hash-chain, mapowanie na kroki routera |
> | `shared/tools/hash_chain_verify.py`   | Weryfikacja integralności istniejącego logu (wykrywa manipulację)                                              |
> | `shared/tools/append_event.py`        | Dopisywanie nowego zdarzenia z poprawnym hash-chain                                                            |
> | `shared/tools/router_event_parser.py` | Wydobywanie znaczników `AUDIT_EVENT` z tekstu odpowiedzi i zapis przez `append_event.py`                       |
>
> ### Konwencja znacznika
>
> Portal instruuje model (poza tym repozytorium skilli, na poziomie system
> promptu portalu), żeby przy każdym zdarzeniu z tabeli w `AUDIT-TRAIL-SPEC.md`
> dopisywał niewidoczny znacznik:
>
> ```
> <!--AUDIT_EVENT:{"event":"HARDGATE_VERIFICATION","session_id":"abc-123","payload":{...}}-->
> ```
>
> `router_event_parser.py` wyłuskuje te znaczniki i zapisuje przez `append_event.py`.
>
> ### Co musi zrobić programista portalu
>
> 1. Zaimplementować konwencję znacznika w system promptcie portalu.
> 2. Po każdej odpowiedzi routera: `router_event_parser.py --input <tekst> --log audit_log.jsonl`.
> 3. Ustalić politykę retencji/dostępu do `audit_log.jsonl`.
> 4. Okresowo: `hash_chain_verify.py audit_log.jsonl`.
>
> ### Status testów
>
> ✅ `hash_chain_verify.py`, `append_event.py` (self-test + integracja append→verify), `router_event_parser.py` (self-test 4 znaczniki, 2 poprawne/2 błędne) — wszystkie PASS.
> ⚠️ Konwencja znacznika nie wdrożona w żadnym prawdziwym prompcie portalu (flaga F-9).
>
> ---
>
> ## 4. audyt-systemu-v4/references/SYNC-DZU-AUTOMATYCZNY.md — szczegóły
>
> ### Co robi
>
> Cyklicznie sprawdza Sejm ELI API pod kątem nowych pozycji Dz.U./M.P. i
> generuje raport różnic — jako **wejście** do sesji `audyt-systemu-v4` FAZA 3,
> nie jako jej zamiennik.
>
> ### Pliki i ich rola
>
>
> Read deployment doc part 1
> bash
>
> cd "$HOME/mnt/Lex-Machina-main"; sed -n '1,200p' DOKUMENTACJA-WDROZENIOWA-2026-07-13.md
> Output
>
> # Dokumentacja wdrożeniowa: warstwa MCP, audit-trail i sync Dz.U
>
> **shared/MCP-INTEGRACJA.md · shared/AUDIT-TRAIL-SPEC.md · audyt-systemu-v4/references/SYNC-DZU-AUTOMATYCZNY.md**
>
> Wersja dokumentu: 2.0 (2026-07-13f) · Odbiorca: zespół developerski portalu (nie Claude)
> Powiązane: `audyt-komercyjny-silnika-prawnego.md` (rekomendacje #2, #4, #6),
> `AUDIT-JOURNAL.md` wpisy AUDYT-2026-07-13 do 2026-07-13f.

Read deployment doc part 2
> bash
>
> cd "$HOME/mnt/Lex-Machina-main"; sed -n '200,420p' DOKUMENTACJA-WDROZENIOWA-2026-07-13.md
> Output
>
> ### Pliki i ich rola
>
> | Plik                                                   | Rola                                                          |
> | ------------------------------------------------------ | ------------------------------------------------------------- |
> | `audyt-systemu-v4/references/SYNC-DZU-AUTOMATYCZNY.md` | Opis przepływu, jawne ograniczenie zakresu (tylko wykrywanie) |
> | `audyt-systemu-v4/references/FORMAT-RAPORTU-ROZNIC.md` | Jak sesja audytowa ma interpretować raport                    |
> | `audyt-systemu-v4/references/HARMONOGRAM-CRON.md`      | Przykłady cron i GitHub Actions                               |
> | `audyt-systemu-v4/scripts/sync_dzu_eli.py`             | Pobiera nowe pozycje, porównuje z mapą, buduje raport         |
> | `audyt-systemu-v4/scripts/mock_eli_server_test.py`     | Test end-to-end na lokalnym mock-serwerze HTTP, bez internetu |
> | `audyt-systemu-v4/scripts/bootstrap_last_sync_date.py` | Idempotentna inicjalizacja pliku stanu `.last_sync_date`      |
>
> ### Co musi zrobić programista portalu
>
> 1. Uruchomić `bootstrap_last_sync_date.py --mapa-dir audyt-systemu-v4/references` raz.
> 2. Ustawić harmonogram wg `HARMONOGRAM-CRON.md`.
> 3. Zweryfikować rzeczywisty kształt odpowiedzi Sejm ELI API (endpoint/pola JSON w `pobierz_nowe_pozycje_eli()`).
> 4. Podłączyć raport do procesu inicjującego kolejną sesję FAZA 3.
>
> ### Status testów
>
> ✅ Parsowanie mapy, budowa raportu, **pełny test end-to-end na mock-serwerze** (`mock_eli_server_test.py`), `bootstrap_last_sync_date.py` (idempotentność) — wszystkie PASS.
> ⚠️ Nie przetestowano wobec żywego api.sejm.gov.pl (flaga F-10).
>
> ---
>
> ## 5. shared/tools/ — bramka walidacji cytowań (wątek z sesji 2026-07-12)
>
> `walidator_cytowan.py` sprawdza, czy każde powołanie w gotowym piśmie ma
> odpowiadające zdarzenie weryfikacji w logu sesji API. `extract_api_
> verification_log.py` buduje ten log automatycznie z surowej konwersacji API
> (bloki `server_tool_use`/`*_tool_result`). `export_gate.py` łączy oba w jedno
> wywołanie — jedyny punkt integracyjny dla portalu:
>
> ```
> python3 shared/tools/export_gate.py --document pismo.docx --api-conversation konwersacja_api.json
> ```
>
> Kod wyjścia 1 → zablokuj eksport, pokaż prawnikowi listę niezweryfikowanych
> powołań. Test end-to-end na fixture `shared/tools/przyklady/konwersacja_api_
> przyklad.json` → `przyklad_pisma.md`: poprawnie 2/4 powołania zweryfikowane.
>
> ⚠️ Kształt bloków `server_tool_use`/`*_tool_result` w `extract_api_
> verification_log.py` odzwierciedla dokumentację Anthropic API, ale nie był
> skonfrontowany z prawdziwą odpowiedzią API (flaga F-11).
>
> ---
>
> ## 6. Pełny manifest plików (po konsolidacji 2026-07-13f)
>
> ```
> shared/
> ├── MCP-INTEGRACJA.md                      [przeniesione z mcp-zrodla-prawa-v1/SKILL.md]
> ├── KONEKTORY-REKOMENDOWANE.md             [przeniesione]
> ├── SCHEMAT-ODPOWIEDZI-MCP.md              [przeniesione]
> ├── AUDIT-TRAIL-SPEC.md                    [przeniesione z audit-trail-portal-v1/SKILL.md]
> ├── DEPENDENCY-GRAPH.md                    [zaktualizowany]
> └── tools/
>     ├── README.md
>     ├── walidator_cytowan.py               [od 2026-07-12]
>     ├── extract_api_verification_log.py    [od 2026-07-13d]
>     ├── export_gate.py                     [od 2026-07-13d]
>     ├── test_mcp_protocol.py               [przeniesione, przetestowane 6/6]
>     ├── connector_health_check.py          [przeniesione, self-test OK]
>     ├── przyklad-adapter-normalizujacy.md  [przeniesione]
>     ├── hash_chain_verify.py               [przeniesione]
>     ├── append_event.py                    [przeniesione, przetestowane]
>     ├── router_event_parser.py             [przeniesione, przetestowane]
>     └── przyklady/
>         ├── przyklad_pisma.md
>         ├── sesja_pelna.json
>         ├── sesja_niepelna.json
>         └── konwersacja_api_przyklad.json
> 
> audyt-systemu-v4/
> ├── references/
> │   ├── AUDIT-JOURNAL.md                   [pełna historia, w tym ta konsolidacja]
> │   ├── WARN-OTWARTE.md                    [flagi F-8..F-11 nadal otwarte]
> │   ├── CHECKLIST-DEDUP.md                 [zaktualizowany, 4 kanoniczne lokalizacje]
> │   ├── SYNC-DZU-AUTOMATYCZNY.md           [przeniesione z sync-dzu-automatyczny-v1/SKILL.md]
> │   ├���─ FORMAT-RAPORTU-ROZNIC.md           [przeniesione]
> │   ├── HARMONOGRAM-CRON.md                [przeniesione]
> │   └── mapa_dzu_*.md
> └── scripts/
>     ├── README.md
>     ├── ci_check_shared.py
>     ├── install_precommit_hook.sh
>     ├── dostarcz_skill.sh                  [deterministyczne wymuszenie ZASADY 7]
>     ├── sync_dzu_eli.py                    [przeniesione, przetestowane end-to-end]
>     ├── mock_eli_server_test.py            [przeniesione]
>     └── bootstrap_last_sync_date.py        [przeniesione, przetestowane]
> 
> prawny-router-v3/
> └── SKILL.md                               [v3.16 — MCP jako required_module opcjonalny]
> ```
>
> ---
>
> ## 7. Checklista wdrożenia produkcyjnego
>
> - [ ] `shared/MCP-INTEGRACJA.md`: wybrać i wdrożyć ≥1 connector MCP, uzupełnić `connectors.json`, przetestować 4 ścieżki wobec realnego connectora
> - [ ] `shared/AUDIT-TRAIL-SPEC.md`: zaimplementować konwencję znacznika `AUDIT_EVENT`, podłączyć `router_event_parser.py`, ustalić retencję logu
> - [ ] `shared/tools/export_gate.py`: podłączyć do pipeline'u tuż po HYBRID-VALIDATION, przed `present_files`/eksportem; zapisywać pełną konwersację API do formatu wejściowego
> - [ ] `audyt-systemu-v4/.../SYNC-DZU-AUTOMATYCZNY.md`: bootstrap, harmonogram, weryfikacja kształtu realnego Sejm ELI API
> - [ ] Po każdym z powyższych: wpis w `AUDIT-JOURNAL.md` zamykający odpowiednią flagę w `WARN-OTWARTE.md`
>
> ---
>
> ## 8. Jak uruchomić wszystkie self-testy naraz
>
> ```bash
> # MCP
> python -m unittest shared/tools/test_mcp_protocol.py -v
> python shared/tools/connector_health_check.py --self-test
> 
> # Audit-trail
> python shared/tools/append_event.py --self-test
> python shared/tools/router_event_parser.py --self-test
> 
> # Walidacja cytowań
> python shared/tools/extract_api_verification_log.py --self-test
> python shared/tools/export_gate.py --self-test
> python shared/tools/walidator_cytowan.py --document shared/tools/przyklady/przyklad_pisma.md --log shared/tools/przyklady/sesja_pelna.json
> 
> # Sync Dz.U.
> python audyt-systemu-v4/scripts/bootstrap_last_sync_date.py --self-test
> python audyt-systemu-v4/scripts/mock_eli_server_test.py
> 
> # Spójność całego repo (0 zerwanych odwołań oczekiwane)
> python audyt-systemu-v4/scripts/ci_check_shared.py --repo-root .
> ```
>
> Wszystkie powyższe zostały uruchomione po konsolidacji (2026-07-13f) i
> zakończyły się sukcesem — patrz `AUDIT-JOURNAL.md`, wpis AUDYT-2026-07-13f.
>
> ---
>
> ## 9. Czego ta dokumentacja świadomie NIE obiecuje
>
> - Nie gwarantuje, że wybrany przez developera connector MCP będzie działał bez modyfikacji.
> - Nie gwarantuje zgodności ze 100% wymogów art. 12 AI Act.
> - Nie gwarantuje, że Sejm ELI API ma dokładnie taki kształt odpowiedzi, jaki założono w `sync_dzu_eli.py`.
> - Nie gwarantuje, że kształt bloków `server_tool_use`/`*_tool_result` w `extract_api_verification_log.py` odpowiada dokładnie temu, co zwraca prawdziwe Claude API w konkretnej integracji portalu.
> - Nie twierdzi, że konsolidacja z sekcji 0 była ostatnim błędem architektonicznym tej sesji — to developer i kolejne audyty ostatecznie weryfikują, czy struktura jest właściwa.
>
>
>
>
> Inspect project folder tree
> bash
>
> cd "$HOME/mnt/lex-machina"; find . -maxdepth 3 -not -path "*/node_modules/*" | sort | head -100; echo "=== DU ==="; du -sh *.* 2>/dev/null | head -20
> Output
>
> .
> ./.DS_Store
> ./AUDYT-2026-09-10-DZU-do-wklejenia.md
> ./audyt-dzu-2026-09-07
> ./audyt-dzu-2026-09-07/AUDIT-JOURNAL-DOPISEK-2026-09-07a.md
> ./audyt-dzu-2026-09-07/WARN-OTWARTE-DOPISEK-2026-09-07.md
> ./audyt-dzu-2026-09-07/mapa_dzu_2026-09-07.md
> ./audyt-dzu-2026-09-10
> ./audyt-dzu-2026-09-10/AUDIT-JOURNAL-dopisek-2026-09-10a.md
> ./audyt-dzu-2026-09-10/F-104-lista-robocza-roczniki-starsze.md
> ./audyt-dzu-2026-09-10/mapa_dzu_2026-09-10.md
> === DU ===
> 12K AUDYT-2026-09-10-DZU-do-wklejenia.md
> 148K audyt-dzu-2026-09-07
> 148K audyt-dzu-2026-09-10
> 12K .
> 51M ..

List triggers
> Request
>
> {
> "limit": 50
> }
> Response
>
> {"data":[],"has_more":false}

Read scheduled-task outputs
> bash
>
> cd "$HOME/mnt/lex-machina"; for f in AUDYT-2026-09-10-DZU-do-wklejenia.md audyt-dzu-2026-09-10/AUDIT-JOURNAL-dopisek-2026-09-10a.md; do echo "===== $f ====="; head -80 "$f"; done
> Output
>
> ===== AUDYT-2026-09-10-DZU-do-wklejenia.md =====
>
> # AUDYT DZU — 2026-09-10 — WYNIK DO RĘCZNEGO WKLEJENIA
>
> ## ⛔ Ograniczenie techniczne tej sesji
>
> Mount `audyt-systemu-v4` w tym środowisku jest **read-only**
> (`dr-x------`, brak prawa zapisu — potwierdzone próbą `touch`, zwrot
> `Read-only file system`). FAZA 7A/7B (zapis do `AUDIT-JOURNAL.md` i
> utworzenie nowego `mapa_dzu_2026-09-10.md`) nie mogła zostać wykonana
> automatycznie. Poniżej gotowa treść do ręcznego wklejenia w środowisku
> z prawem zapisu (Claude Code / sesja z zapisywalnym mountem skilli).
>
> Zakres wykonany: FAZA 0 (wczytanie WARN-OTWARTE, tablica sterująca) +
> FAZA 3D (MONITORING) + fragment FAZA 3A (jeden akt zweryfikowany przy
> okazji). FAZA 3-PULL i pełne 3A/3B (przegląd 16 map DR) — NIE wykonane
> w tej sesji, zakres przekraczał to, o co poprosił scheduler ("sprawdź
> mapę Dz.U., MONITORING, AUDIT-JOURNAL").
>
> ---
>
> ## 1. Ustalenia — 5 pozycji MONITORING zweryfikowanych online (RZĄD 1/2B)
>
> | Akt                                                                                    | Wpis w mapie (2026-08-21/07-02)                 | Ustalenie 2026-09-10                                                                                                                                                                                                                                                                                                                                                                                               | Źródło                                                                                                                                                                                                     |
> | -------------------------------------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | Prawo budowlane — zmiana art. 1 pkt 1 lit. c (Dz.U. 2026 poz. 524 / 2025 poz. 1847)    | ⏳ OCZEKUJE                                      | **⚡ WCHODZI-90DNI** — wejście w życie **20.09.2026** potwierdzone (art. 1 pkt 1 lit. a i c oraz pkt 3), za 10 dni od dziś                                                                                                                                                                                                                                                                                          | ISAP (RZĄD 1, D20260524L.pdf) + eli.gov.pl                                                                                                                                                                 |
> | Ordynacja podatkowa — "część przepisów nowelizacji" (mapa błędnie wskazywała poz. 622) | ⚡ WCHODZI-90DNI, numer 622                      | **Numer 622 to sam t.j. OP (już w życiu od 11.05.2026), NIE nowelizacja.** Rzeczywista nowelizacja MDR/uproszczeń to **Dz.U. 2026 poz. 846** (ustawa z 29.05.2026, podpisana 19.06.2026), wchodzi w życie **1.10.2026** (za 3 tyg.). **To rozstrzyga też flagę F-88 (WARN-OTWARTE.md)** w części dot. mechanizmu ograniczenia MDR do schematów transgranicznych — konkretny numer aktu był tam "NADAL NIEUSTALONE" | ISAP/ELI (RZĄD 1, WDU20260000846) + lex.pl (RZĄD 2B, artykuł z 02.09.2026)                                                                                                                                 |
> | Rozwód rejestrowy USC (KRO nowelizacja)                                                | ⚠️ NIEZWERYFIKOWANE ŹRÓDŁOWO (dodane 2026-07-02) | **❌ ROZSTRZYGNIĘTE — ZAWETOWANE.** Uchwalona przez Sejm 13.03.2026, ale **Prezydent Nawrocki zawetował ustawę 30.04.2026**. Nie wejdzie w życie w tej postaci. Usunąć z MONITORING                                                                                                                                                                                                                                 | aleteia.pl + forsal.pl + infor.pl (3+ źródła zgodne, RZĄD 3, wysoka zbieżność)                                                                                                                             |
> | Ustawa o przeciwdziałaniu narkomanii (F-4)                                             | NIEOPUBLIKOWANA (stan na 2026-07-15)            | **✅ WSZEDŁ.** Ustawa z 11.06.2026, opublikowana jako **Dz.U. 2026 poz. 1004**, weszła w życie **27.08.2026** (30 dni od publikacji) — już 2 tygodnie temu. Przenieść do tabeli głównej, zamknąć F-4                                                                                                                                                                                                                | rynekzdrowia.pl + gov.pl/chemikalia (RZĄD 2B/3, zgodne) — ⚠️ web_fetch ISAP zwrócił puste body (ROBOTS_DISALLOWED, znane ograniczenie), numer poz. 1004 potwierdzony przez 3 źródła pochodne zgodne ze sobą |
> | Zakwaterowanie funkcjonariuszy służb (Dz.U. 2025 poz. 1366)                            | ⏳ OCZEKUJE                                      | **✅ WSZEDŁ już 14.10.2025** — prawie rok temu. Wpis w MONITORING był nieaktualny od blisko roku                                                                                                                                                                                                                                                                                                                    | ISAP (RZĄD 1) + prawo.pl                                                                                                                                                                                   |
>
> ## 2. Błąd wykryty — klasa F-82 (nowy ⚠️ ALERT)
>
> **Wiersz "KPK — zmiana (vacatio 2026), Dz.U. 2025 poz. 1390" jest BŁĘDNY.**
> Numer **Dz.U. 2025 poz. 1390** to w rzeczywistości **rozporządzenie
> Ministra Finansów i Gospodarki z 12.10.2025 zmieniające rozporządzenie
> w sprawie wyłączenia obowiązku poboru zryczałtowanego podatku dochodowego
> od osób prawnych** — akt podatkowy, zero związku z KPK.
>
> Potwierdzone bezpośrednio w ISAP (RZĄD 1, `WDU20250001390`).
>
> To druga/trzecia klasa błędu "zgodność numeru nie dowodzi tożsamości aktu"
> (precedens: Kodeks morski, emerytury pomostowe 2025.468). Wiersz do
> usunięcia z MONITORING; numer **2025 poz. 1390 oznaczyć ⚠️ ALERT** w
> rejestrze błędnych numerów (podwyższone ryzyko nawrotu — sprawdzać w
> każdym kolejnym przebiegu, jeśli ktoś znowu spróbuje go użyć dla KPK).
>
> Pozostały wiersz "KPK — oczekująca nowelizacja, Dz.U. 2026 poz. 638"
> (ustawa z 27.03.2026) — **numer istnieje i dotyczy KPK** (potwierdzone:
> przepisy przejściowe dot. właściwości sądu), ale dokładna data wejścia
> w życie głównych przepisów NIE została ustalona w tej sesji — wymaga
> doprecyzowania przy najbliższym użyciu (zostawić ⏳ OCZEKUJE z notatką).
>
> ## 3. Nie zweryfikowane w tej sesji (brak czasu / poza zakresem)
>
> - Prawo energetyczne poz. 516 — WYKRYTO PRZY OKAZJI (nie było w
>   pierwotnym zakresie MONITORING pytania, ale skoro sesja dotyka tego
>   wiersza): wejście dwuetapowe, część już w życiu (16.04.2026), część
>   wchodzi **16.10.2026** (art. 9, 11, 13, 14) — czyli **⚡ WCHODZI-90DNI**,
>   nie ⏳ OCZEKUJE jak w mapie. Do poprawienia razem z resztą.
> - FAZA 3-PULL (sync 16× MAPA-AKTOW.md → ROUTING-MAP → mapa_dzu) — nie
>   wykonana, wymaga osobnej sesji.
> - FAZA 3A/3B (nowe t.j. dla KC/KPC/KPK/KRO/KP/KSH/KPA/PB/PrFarm/PIT/CIT/
>   OrdPod/PrNotariat, próg poz. > 1079/2026) — nie wykonana.
>
> ---
>
> ## 4. Treść do wklejenia w `mapa_dzu_YYYY-MM-DD.md`, sekcja MONITORING
>
> Zastąp całą tabelę MONITORING (i nagłówek daty) tym:
>
> ```markdown
> ## MONITORING — Akty opublikowane, niebędące jeszcze w pełni w życiu
> 
> > **Procedura (FAZA 3D audytu):** Przy każdym audycie DZU sprawdź każdy wpis.
> > Akt, który wszedł w życie → przenieś do tabeli głównej (zmień typ OCZEKUJE → TJ/NW/ORG, status OK), usuń z tej tabeli.
> > Akt uchylony przed wejściem → status ❌ UCHYLONY, usuń, odnotuj w AUDIT-JOURNAL.
> 
> | Akt                                                             | Dz.U. opubl.                                             | Data wejścia w życie | Zastępuje / zmienia          | Moduł DR                         | Status                                                     |
> | --------------------------------------------------------------- | -------------------------------------------------------- | -------------------- | ---------------------------- | -------------------------------- | ---------------------------------------------------------- |
> | Prawo budowlane — zmiana art. 1 pkt 1 lit. a/c, pkt 3           | Dz.U. 2025 poz. 1847 (nowelizująca) / t.j. 2026 poz. 524 | **20.09.2026**       | PrBud t.j. wcześniejszy      | dr-09/mod-PrBud-prawo-budowlane  | ⚡ WCHODZI-90DNI                                            |
> | Ordynacja podatkowa — nowelizacja MDR/uproszczenia proceduralne | **Dz.U. 2026 poz. 846** (nie 622 — 622 to sam t.j.)      | **1.10.2026**        | OP t.j. 2026.622 (częściowo) | dr-06/mod-OP-ordynacja-podatkowa | ⚡ WCHODZI-90DNI — rozstrzyga też F-88 (numer MDR ustalony) |
> ===== audyt-dzu-2026-09-10/AUDIT-JOURNAL-dopisek-2026-09-10a.md =====
> ---
> 
> ## AUDYT-2026-09-10a
> 
> **Kontekst:** zadanie zaplanowane (scheduled task, Cowork), tryb nieinteraktywny.
> Polecenie: "Uruchom audyt-systemu-v4 w TRYBIE DZU: sprawdź mapę Dz.U.,
> zaktualizuj tabelę MONITORING i AUDIT-JOURNAL."
> 
> ### 1. STATUS OGÓLNY
> 
> TRYB DZU wykonany: Faza 0 (wczytanie WARN-OTWARTE.md, mapa_dzu_2026-08-21.md,
> F-104-lista-robocza-*.md) → Faza 3 pominięta w części 3A-3D (rocznik 2026 już
> ZAMKNIĘTY w sesji 2026-08-21, brak nowych t.j. kluczowych aktów do sprawdzenia
> w tej sesji — priorytet oddany kontynuacji F-104 zgodnie z jej protokołem
> transzy, punkt 5: "po wyczerpaniu rocznika 2026 — kontynuuj roczniki starsze")
> → F-104 roczniki starsze, transza 2 (8 pozycji z listy roboczej, poz. 1696
> w dół do 1362) → Faza 7B (nowa generacja mapy) → Faza 7A (ten wpis).
> 
> ⚠️ **Ograniczenie środowiskowe tej sesji:** pliki `references/` skilla
> `audyt-systemu-v4` są zamontowane jako **read-only** (plugin mount) —
> w przeciwieństwie do standardowego trybu pracy skilla (gdzie HARDGATE-AUDYT
> zakłada edycję bezpośrednią z kopią roboczą w `/home/claude/`). W tej sesji
> zmiany zostały przygotowane jako **pliki delty** w folderze wyjściowym
> (`mapa_dzu_2026-09-10.md` — pełna nowa generacja, gotowa do podmiany;
> `F-104-lista-robocza-roczniki-starsze.md` — zaktualizowana; ten plik —
> dopisek do dziennika) i wymagają **ręcznego wgrania przez użytkownika/
> dewelopera** do rzeczywistej lokalizacji skilla. Ten wpis (AUDYT-2026-09-10a)
> powinien zostać dopisany na KOŃCU `AUDIT-JOURNAL.md`, zgodnie z regułą
> FAZA 7A (dopisywanie na końcu, nie na początku).
> 
> ### 2. NAPRAWY WYKONANE (CRIT)
> 
> Brak — sesja nie wykryła błędów klasy CRIT.
> 
> ### 3. WERYFIKACJA Dz.U. — F-104 ROCZNIKI STARSZE, TRANSZA 2
> 
> Zgodnie z protokołem transzy (`F-104-lista-robocza-roczniki-starsze.md`):
> Rząd 1 (ISAP/ELI, web_search jako obejście blokady web_fetch ROBOTS_DISALLOWED)
> jako pierwsza próba, Rząd 2B jako potwierdzenie pomocnicze.
> 
> **Wpisane do `mapa_dzu_2026-09-10.md` (6 pozycji):**
> 
> | Dz.U.          | Akt                                                                       | Rząd potwierdzenia                                                            |
> | -------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
> | 2025 poz. 1696 | Ustawa o ochronie zdrowia zwierząt — zm. (hodowla zwierząt futerkowych)   | RZĄD 1 (ISAP PDF D20251696L.pdf)                                              |
> | 2025 poz. 1679 | Ustawa o zmianie ustawy o rzecznikach patentowych                         | RZĄD 1 (ISAP PDF D20251679.pdf)                                               |
> | 2025 poz. 1669 | Zmiana ustawy o ochronie praw nabywcy lokalu/DFG (Portal DOM)             | RZĄD 1/2B (prawo.pl + sąsiedztwo ISAP poz. 1668)                              |
> | 2025 poz. 1644 | Ustawa wypadkowa — t.j.                                                   | RZĄD 1 (ISAP PDF D20251644L.pdf) + RZĄD 2B (portalkadrowy.pl, infor.pl)       |
> | 2025 poz. 1362 | Ustawa o kredycie konsumenckim — t.j.                                     | RZĄD 1 (ISAP DocDetails WDU20250001362)                                       |
> | 2025 poz. 1436 | Nowelizacja dot. ustawy o samorządzie gminnym — **tytuł niepotwierdzony** | RZĄD 1 wyłącznie co do ISTNIENIA numeru; wpisana ze statusem ⚠️ DO WERYFIKACJI |
> 
> **NIE wpisane, pozostają w liście roboczej (2 pozycje):**
> 
> | Dz.U.          | Powód                                                                                                                                                                                          |
> | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | 2025 poz. 1693 | 3 próby web_search różnymi frazami — brak trafienia treści. web_fetch ISAP zablokowany (ROBOTS_DISALLOWED). Zgodnie z ZASADĄ 13 (wytrwałość, ale nie zgadywanie) — otwarte do kolejnej transzy |
> | 2025 poz. 1440 | Numer istnieje w indeksie ISAP (potwierdzone pośrednio przez wyniki sąsiadujące), ale tytuł/treść nieustalone po 2 próbach                                                                     |
> 
> **Zastosowanie ZASADY 8 (weryfikacja numeru niezależnie od nazwy):** przy
> poz. 1436 świadomie NIE przyjęto domysłu na podstawie samego sąsiedztwa
> kontekstowego (cytowanie w wierszu poz. 662) — wpisano z jawną flagą zamiast
> zgadywanego tytułu, zgodnie z lekcją F-82/F-104 (zgodność pośrednia nie jest
> dowodem tożsamości aktu).
> 
> ### 4. FAZA 3A-3D — kluczowe akty rocznika bieżącego
> 
> Pominięta w tej sesji: rocznik 2026 (13 kluczowych aktów: KC, KPC, KPK, KRO,
> KP, KSH, KPA, PB, PrFarm, PIT, CIT, OrdPod, PrNotariat) był już w pełni
> zweryfikowany w sesjach do 2026-08-21 włącznie, a mapa nie sygnalizuje nowych
> t.j. od tego czasu. Priorytet oddano F-104 zgodnie z jej wyraźnym protokołem
> kontynuacji. Rekomendacja dla kolejnej sesji cyklicznej: wykonać punktową
> kontrolę 13 kluczowych aktów (Dz.U. > najwyższa pozycja odnotowana, obecnie
> 1079/2026), zanim F-104 pochłonie kolejną transzę.
> 
> ### 4B. MONITORING — akty oczekujące
> 
> Bez zmian względem stanu z `mapa_dzu_2026-08-21.md` — w tej sesji nie
> weryfikowano dat wejścia w życie pozycji z tabeli MONITORING (Prawo
> budowlane art. 1 pkt 1 lit. c, Ordynacja podatkowa część przepisów, obrona
> cywilna zm.). Rekomendacja: dedykowana sesja TRYB DZU dla samej tabeli

{
  "scheduledTasks": [
    {
      "id": "monitoring-nowych-dzu--tj",
      "cronExpression": "0 4 * * *",
      "enabled": true,
      "filePath": "/Users/tom/lex-machina/.claude/scheduled/monitoring-nowych-dzu--tj/SKILL.md",
      "createdAt": 1788329687624,
      "lastRunAt": "2026-09-10T02:00:37.562Z",
      "lastScheduledFor": "2026-09-10T02:00:00.000Z",
      "spaceId": "e5ada960-31f9-4af2-a3ec-0b5997800584",
      "permissionMode": "bypassPermissions",
      "disableJitter": false,
      "userSelectedFolders": [
        "/Users/tom/lex-machina"
      ],
      "displayName": "monitoring_nowych_dzu_tj"
    },
    {
      "id": "peny-audyt-systemu",
      "cronExpression": "30 9 * * 6",
      "enabled": true,
      "filePath": "/Users/tom/lex-machina/.claude/scheduled/peny-audyt-systemu/SKILL.md",
      "createdAt": 1788329745486,
      "lastRunAt": "2026-09-07T01:13:09.473Z",
      "lastScheduledFor": "2026-09-05T07:30:00.000Z",
      "missedRunScanFloor": "2026-09-02T06:16:07.236Z",
      "spaceId": "e5ada960-31f9-4af2-a3ec-0b5997800584",
      "permissionMode": "bypassPermissions",
      "disableJitter": false,
      "displayName": "pelny_audyt_systemu",
      "userSelectedFolders": [
        "/Users/tom/lex-machina"
      ]
    },
    {
      "id": "zamykanie-otwartych-flag",
      "cronExpression": "30 9 * * 0",
      "enabled": true,
      "filePath": "/Users/tom/lex-machina/.claude/scheduled/zamykanie-otwartych-flag/SKILL.md",
      "createdAt": 1788329846991,
      "lastRunAt": "2026-09-07T01:13:09.685Z",
      "lastScheduledFor": "2026-09-06T07:30:00.000Z",
      "userSelectedFolders": [
        "/Users/tom/lex-machina"
      ],
      "permissionMode": "bypassPermissions",
      "disableJitter": false,
      "displayName": "zamykanie_otwartych_flag"
    }
  ],
  "recordedSkips": {},
  "sundayAliasBoundaryStamped": true,
  "dayFieldsOrBoundaryStamped": true
}

Look for local scheduled task storage
> bash
>
> ls -la "$HOME/Library/Application Support/Claude" 2>/dev/null | head -40; echo "---"; find "$HOME/Library/Application Support/Claude" -iname "*schedul*" -o -iname "*trigger*" -o -iname "*routine*" 2>/dev/null | head -20
> Output
>
> ---

Added task: Skopiuj skille do .claude/skills projektu
> Request
>
> {
> "activeForm": "Kopiowanie skilli",
> "description": "Kopia wszystkich 33+ skilli z \"Wersja stabilna rozpakowana 21.08.2026\" do /Users/tom/lex-machina/.claude/skills, z zachowaniem shared/ i skryptów",
> "subject": "Skopiuj skille do .claude/skills projektu"
> }
> Response
>
> Task #1 created successfully: Skopiuj skille do .claude/skills projektu

Added task: Zweryfikuj wdrożenie wg DOKUMENTACJI-WDROZENIOWEJ
> Request
>
> {
> "activeForm": "Weryfikowanie wdrożenia",
> "description": "Uruchom self-testy z sekcji 8 dokumentacji (MCP, audit-trail, walidator cytowań, sync Dz.U., ci_check_shared) i sprawdź checklistę wdrożeniową z sekcji 7",
> "subject": "Zweryfikuj wdrożenie wg DOKUMENTACJI-WDROZENIOWEJ"
> }
> Response
>
> Task #2 created successfully: Zweryfikuj wdrożenie wg DOKUMENTACJI-WDROZENIOWEJ

Added task: Zdiagnozuj problem zapisu scheduled tasków
> Request
>
> {
> "activeForm": "Diagnozowanie problemu zapisu",
> "description": "Ustal przyczynę read-only mountu skilli w przebiegach scheduled tasków i sprawdź konfigurację zadań",
> "subject": "Zdiagnozuj problem zapisu scheduled tasków"
> }
> Response
>
> Task #3 created successfully: Zdiagnozuj problem zapisu scheduled tasków

Added task: Uporządkuj pliki z przebiegów i przygotuj strukturę na materiał dowodowy
> Request
>
> {
> "activeForm": "Porządkowanie plików",
> "description": "Wgraj delty z audyt-dzu-* do właściwych lokalizacji skilla, zarchiwizuj pliki robocze, utwórz strukturę katalogów na materiał dowodowy",
> "subject": "Uporządkuj pliki z przebiegów i przygotuj strukturę na materiał dowodowy"
> }
> Response
>
> Task #4 created successfully: Uporządkuj pliki z przebiegów i przygotuj strukturę na materiał dowodowy
>
> Added task: Weryfikacja końcowa
> Request
>
> {
> "activeForm": "Weryfikacja końcowa",
> "description": "Sprawdź kompletność kopii (diff drzew), prawa zapisu, spójność odwołań (ci_check_shared) i widoczność skilli",
> "subject": "Weryfikacja końcowa"
> }
> Response
>

Task #5 created successfully: Weryfikacja końcowa
>
> Started task
> Request
>
> {
> "status": "in_progress",
> "taskId": "1"
> }
> Response
>
Updated task #1 status
>
> Prepare destination dir
> bash
>
> SRC="$HOME/mnt/Lex-Machina-main/Wersja stabilna rozpakowana 21.08.2026"; DST="$HOME/mnt/lex-machina/.claude/skills"
> mkdir -p "$DST" && echo "mkdir OK"
> du -sh "$SRC"; find "$SRC" -type f | wc -l
> echo "=== czy .claude istnieje w projekcie ==="; ls -la "$HOME/mnt/lex-machina/.claude" 2>&1 | head
> Output
>
> mkdir OK
> 18M /sessions/rcw-01bhej8tctcetu9jm9qdyskp/mnt/Lex-Machina-main/Wersja stabilna rozpakowana 21.08.2026
> 1097
> === czy .claude istnieje w projekcie ===
> total 0
> drwx------ 3 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  96 Sep 10  2026 .
> drwx------ 7 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp 224 Sep 10  2026 ..
> drwx------ 2 rcw-01bhej8tctcetu9jm9qdyskp rcw-01bhej8tctcetu9jm9qdyskp  64 Sep 10  2026 skills
>

Copy skills into project
> bash
>
> SRC="$HOME/mnt/Lex-Machina-main/Wersja stabilna rozpakowana 21.08.2026"; DST="$HOME/mnt/lex-machina/.claude/skills"
> which rsync && rsync -a --exclude='.DS_Store' --exclude='**pycache**' "$SRC"/ "$DST"/ && echo "RSYNC OK" || { cp -R "$SRC"/. "$DST"/ && find "$DST" -name '.DS_Store' -print; echo "CP OK"; }
> echo "=== wynik ==="; ls "$DST" | wc -l; du -sh "$DST"; find "$DST" -name SKILL.md | wc -l
> Output
>
> /usr/bin/rsync
> RSYNC OK
> === wynik ===
> 34
> 18M /sessions/rcw-01bhej8tctcetu9jm9qdyskp/mnt/lex-machina/.claude/skills
> 34


> Desktop Commander
> list_directory
> Request
{
  "path": "/Users/tom/Claude/Scheduled"
}
Response

[DIR] monitoring-nowych-dzu--tj
[FILE] monitoring-nowych-dzu--tj/SKILL.md
[DIR] peny-audyt-systemu
[FILE] peny-audyt-systemu/SKILL.md
[DIR] zamykanie-otwartych-flag
[FILE] zamykanie-otwartych-flag/SKILL.md

Users › tom › Library › Application Support › Claude › claude-code-sessions › 994e26ed-4b27-45d2-bc98-235ff6a79e57 › 9cb56105-f759-43cb-9808-af223dd54845 › scheduled-tasks.json

Desktop Commander
read_file




{
  "scheduledTasks": [],
  "recordedSkips": {},
  "sundayAliasBoundaryStamped": true,
  "dayFieldsOrBoundaryStamped": true


> Desktop Commander icon
> Desktop Commander
> read_file
> Request
{
  "path": "/Users/tom/Claude/Scheduled/monitoring-nowych-dzu--tj/SKILL.md"
}
Response

[Reading 6 lines from start (total: 6 lines, 0 remaining)]


---
name: monitoring-nowych-dzu--tj
description: Monitoring nowych Dz.U. / t.j.
---

Uruchom audyt-systemu-v4 w TRYBIE DZU: sprawdź mapę Dz.U., zaktualizuj tabelę MONITORING i AUDIT-JOURNAL.

Gotowe. Wyniki poniżej.

---


Desktop Commander
read_file
> 
>  Ran 10 commands (1 failed)
>  GROUNDING-PRAWO
>  GROUNDING-PRAWO
>  Folder
 
Ran 15 commands
Idempotent. Now the index and cache migration.

Ran 7 commands
Now the memo for the other hosts.

Ran 11 commands (1 failed)

Ran 15 commands
Zrobione. Cache jest we wspólnym repozytorium, korpus ujednolicony, memo leży na NAS-ie.

Najpierw rzecz, która odwraca część Twojej instrukcji: SMB nie działa
Wskazałeś SMB jako pierwszą drogę. Na tym hoście 42 z 59 plików w /Volumes/GROUNDING-PRAWO/ORZECZENIA/ zwraca Errno 5 Input/output error przy odczycie — mimo że stat podaje poprawny rozmiar, a dd czyta 0 bajtów. Zimny odczyt pojedynczego pliku też pada, więc to nie limit uchwytów ani prędkości. Te same pliki czytają się bez błędu przez OneDrive, z identycznymi sumami md5.

Dlatego ścieżką podstawową jest OneDrive (~/OneDrive/GROUNDING-PRAWO), a SMB został w łańcuchu rozstrzygania jako fallback dla hostów, na których działa (GROUNDING_ROOT=/Volumes/GROUNDING-PRAWO). lexcache nie ufa tu isdir/touch — testuje każdego kandydata realnym zapisem i odczytem, bo na uszkodzonym udziale jedno i drugie przechodzi. Udział wymaga uwagi po stronie NAS-a; nie diagnozowałem dalej.

Co jest w repozytorium
GROUNDING-PRAWO/
├── ORZECZENIA/  59 plików (54 unikalne) — SN, SA, NSA, ETPC
├── USTAWY/      11 tekstów ujednoliconych
├── OPRACOWANIA/  7 PDF-ów
├── MAPY/         2 mapy artykułów
├── CACHE/       ← lexcache, 43 MB
└── INDEX/       INDEX.md + index.jsonl (74 wpisy) + memo + kopia lexcache.py
Frontmatter ujednolicony na 54/54 orzeczeniach (50 × saos, 6 × echr, 3 × cbosa, zero bez daty). Normalizacja jest idempotentna i nie rusza treści — sprawdzone bajt w bajt względem kopii sprzed zmian. Numery typu 34806/04 rozpoznane jako skargi do ETPC i celowo bez court_type, żeby nie wpadły w zapytania SAOS.

Obsługa OneDrive nie wymagała ani MCP, ani skilla: macOS montuje go przez File Provider jako zwykły katalog. Konektor do Graph API byłby kosztem bez korzyści.

Naprawione już po głównej robocie
PDF-y ISAP (CACHE/isap/_pdf/, czyli praktycznie całe 43 MB) to pliki binarne, nie wpisy .md — purge ich nie widział, a osierocony PDF serwował się w nieskończoność jako świeży, nawet po skasowaniu wpisu. Teraz ponowne użycie sprawdza wiek pliku względem TTL 90 dni, a purge --stale/--all przechodzi też przez_pdf/.

Dwie rzeczy do Twojej decyzji
5 plików bez rozszerzenia w ORZECZENIA/ to kopie 1:1 swoich odpowiedników .md (III_OSK_5079-21, I_CKN_908-98, SD_9-13, V_KK_75-20, WA_39-08). Nie tknąłem ich, są wyłączone z indeksu — do skasowania, jeśli potwierdzisz.

USTAWY/Ustawa_o_srodkach_przymusu_bezposredniego_i_broni_palnej.md.docx ma 0 bajtów. To realna dziura w korpusie, nie artefakt — oznaczona ⚠️ w indeksie.

Dodatkowo: migrate kopiuje, nie przenosi, więc pod ~/.claude/cache/lexcache leży nadal komplet 43 MB. Jest nieaktywny, ale zacznie się cicho rozjeżdżać — autorytatywne jest GROUNDING-PRAWO/CACHE.

Memo
/Volumes/nas/MEMO/2026-09-11_lexcache_i_skille_prawne.md (kopia w INDEX/) — 9 sekcji dla pozostałych hostów: co zainstalować, mapa zastąpień IURA MCP → SAOS/ISAP, fakty zweryfikowane na żywo (żeby ich nie wyprowadzali ponownie), układ repozytorium, łańcuch rozstrzygania ścieżki, schemat frontmatteru, braki w korpusie i sekcja RODO.

Ta ostatnia zostaje aktualna: cache trzyma orzeczenia SAOS o niepełnej anonimizacji i odpisy KRS/CEIDG, czyli dane osobowe, a repozytorium jest w chmurze konsumenckiej. Każdy host, który się podłączy, staje się kolejnym miejscem przetwarzania. Opt-out to LEXCACHE_DIR wskazujący katalog lokalny.

Completed task
> Request
> 
> {
>   "status": "completed",
>   "taskId": "1"
> }
> Response

Updated task #1 status
> Started task
> Request
> 
> {
>   "status": "in_progress",
>   "taskId": "2"
> }
> Response

Updated task #2 status

> Requested permission to delete files on your computer
> Request
> 
> {
>   "paths": [
>     "/Users/tom/lex-machina"
>   ],
>   "reason": "Usunięcie plików tymczasowych (.writetest, __pycache__) i uporządkowanie plików roboczych z przebiegów scheduled tasków."
> }
> Response
> 
> File deletion is now enabled for the rest of this session in this folder (including subfolders): "/Users/tom/lex-machina". device_bash picks this up on your next call — rm/rmdir/unlink will work there. Deleted files can't be restored; delete only what the user asked for.


