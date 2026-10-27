# Stan wdrożenia rtk-proxy (rtk llm-proxy) na hoście HolyClaude

Data: 2026-10-24

---

## 1. Co to jest rtk-proxy i rtk pipeline/bulk-read

**rtk-proxy** (wersja 1.0.1, licencja BSL) — lokalny proxy LLM, który:
- Normalizuje wyniki narzędzi (tool results) i przekazuje je dalej do upstreama
- Działa na `127.0.0.1:8080` (OpenAI-kompatybilny endpoint)
- Upstream: OpenRouter (`https://openrouter.ai/api`), model `openrouter/free` (losowy darmowy model)
- Kompresja: aggressive (zmniejsza tokeny w odpowiedziach)
- Baza SQLite: `~/.config/rtk/llm-proxy/rtk-proxy.db` (logi żądań), `rtk-proxy-memory.db` (pamięć kontekstowa)

**rtk pipeline / bulk-read** (część `rtk` 1.0.1, Apache-2.0 + silnik pipeline BSL):
- Pipeline `rtk:delegate-reads` zdefiniowany w `~/.config/rtk/pipeline.toml`
- Dla zadań `bulk-read` i `code-write` używa upstreama `cheap` (OpenRouter free)
- `rtk bulk-read --question "..." <plik>` — odczytuje duże pliki (>350 linii), wysyła do taniego modelu, zwraca tylko odpowiedź (nie całą treść)
- Hook `rtk hook claude` (dodawany przez `agents-sync`) blokuje `Read` całych plików >350 linii i wymusza `rtk bulk-read`
- Wykluczenia: `~/.config/rtk/llm-select.exclude` (domyślnie binarne + `md`, `txt`, `json`, `csv` itd. — akta prawne czyta `Read` w całości)

**Selektor modelu** (`~/.agents/bin/rtk-llm-select`):
- Uruchamiany przez `agents-sync` (SessionStart), w tle
- Testuje kandydatów z `$RTK_LLM_CANDIDATES` (domyślnie: `openrouter/free`, `minimax/m3.1-flash`, `nvidia/nemotron-3.5-lightning`, Gemini)
- Pierwszy działający model trafia do `pipeline.toml`; wynik cache'owany 6 h (`~/.config/rtk/llm-select.json`)
- Klucze: `~/.config/rtk/openrouter.key`, `~/.config/rtk/gemini.key` (nie wypisywane)

---

## 2. Tabela STAN

| Element | Stan | Dowód (polecenie + skrócony wynik) |
|---------|------|-----------------------------------|
| Binarka `rtk-proxy` | **działa** | `rtk-proxy --help` → "Local LLM proxy: normalises tool results, then forwards them upstream" |
| Binarka `rtk llm-proxy` | **działa** | `rtk llm-proxy --help` → "Transparent LLM proxy: run rtk-proxy and point AI agents at it" |
| Proces `rtk-proxy` (PID 17985) | **działa** | `ps aux \| rg rtk` → `rtk-proxy start --bind 127.0.0.1:8080 --openai-upstream https://openrouter.ai/api --compression aggressive --db /home/claude/.config/rtk/llm-proxy/rtk-proxy.db --icm-db /home/claude/.config/rtk/llm-proxy/rtk-proxy-memory.db` |
| Port 8080 (rtk-proxy) | **nasłuchuje** | `ss -ltnp` → `LISTEN 127.0.0.1:8080 users:(("rtk-proxy",pid=17985,fd=13))` |
| `rtk-proxy status` | **działa** | `rtk-proxy status` → "running at 127.0.0.1:8080 (edition local, v1.0.1)" |
| `rtk llm-proxy status` | **działa** | `rtk llm-proxy status` → "running at 127.0.0.1:8080 (edition local, v1.0.1)" |
| Pipeline `pipeline.toml` | **skonfigurowany** | `cat ~/.config/rtk/pipeline.toml` → `extends = "rtk:delegate-reads"`, upstream `cheap` = `openrouter/free`, `api_key_command = "cat /home/claude/.config/rtk/openrouter.key"` |
| Klucz OpenRouter | **istnieje** | `ls -la ~/.config/rtk/openrouter.key` → `-rw------- 1 claude users 74 Oct 23 05:31` |
| Selektor modelu (cache) | **aktualny** | `cat ~/.config/rtk/llm-select.json` → `{"choice": "openrouter:openrouter/free", "ts": 1792858702.93}` (2026-10-23 05:31) |
| Log selektora | **zapisuje** | `cat ~/.config/rtk/llm-select.log` → "rtk-llm-select: openrouter:nvidia/nemotron-3.5-lightning:free (pipeline.toml zaktualizowany)" |
| Baza `rtk-proxy.db` | **istnieje** | `ls -la ~/.config/rtk/llm-proxy/` → `rtk-proxy.db` 36 KB, `rtk-proxy-memory.db` 316 KB |
| Port 8787 (caveman-proxy) | **nasłuchuje** | `ss -ltnp` → `LISTEN 127.0.0.1:8787 users:(("caveman-proxy",pid=4754,fd=12))` — **to caveman-proxy, NIE rtk-proxy** |
| `ANTHROPIC_BASE_URL` (Claude Code) | **wskazuje na caveman-proxy** | `cat ~/.claude/settings.json` → `"ANTHROPIC_BASE_URL": "http://127.0.0.1:8787/w/claude"` |

---

## 3. Którzy agenci używają rtk-proxy i jak

| Agent | Używa rtk-proxy (8080)? | Konfiguracja / sposób |
|-------|------------------------|----------------------|
| **Claude Code** | **NIE** | `ANTHROPIC_BASE_URL=http://127.0.0.1:8787/w/claude` → caveman-proxy. Hook `rtk hook claude` aktywny (Read >350 linii → `rtk bulk-read`), ale zapytania LLM idą przez caveman-proxy. |
| **Codex** | **NIE** | `~/.codex/config.toml`: `model_provider = "caveman"`, `[model_providers.caveman]` → `base_url = "http://127.0.0.1:8787/chatgpt"`. Żaden wpis nie wskazuje na 8080. |
| **OpenCode** | **NIE** | `~/.config/opencode/opencode.json`: provider `openrouter` (bezpośrednio), `google-vertex`, `opencode`. Brak konfiguracji proxy na 8080. Plugin `ctx-guard.ts` przepusza bash przez `ctx-guard`, nie przez rtk-proxy. |

**Wniosek**: rtk-proxy **działa i nasłuchuje na 8080**, ale **żaden z trzech agentów (Claude, Codex, OpenCode) nie jest do niego podpięty**. Wszyscy korzystają z caveman-proxy (8787) lub bezpośrednio z OpenRouter/Vertex.

---

## 4. Braki do pełnego wdrożenia — konkretne kroki z komendami

Fakty, które ograniczają wdrożenie:
- `usage_records` w `rtk-proxy.db` ma 0 wierszy: od startu 2026-10-23 05:32 przez proxy nie przeszło żadne żądanie.
- Proces uruchomiono ręcznie, bez `--anthropic-upstream`; domyślny upstream Anthropic to `https://api.anthropic.com`,
  a ruch Claude idzie dziś przez caveman-proxy (`:8787`), który ma własną kompresję i routing.
- `~/.agents/bin/agents-sync` (sekcja 4) celowo usuwa `ANTHROPIC_BASE_URL` wskazujący na `127.0.0.1:8080`.
  Bezpośrednie przepięcie Claude na rtk-proxy zostanie cofnięte przy następnym starcie sesji.
- Upstream OpenAI proxy to OpenRouter z modelem `openrouter/free`. Klient OpenAI podpięty pod `:8080` dostanie
  darmowy model, a nie ten, który wybrał.

| # | Krok | Komenda / akcja |
|---|------|-----------------|
| 1 | Decyzja właściciela: łańcuch czy tylko pipeline. Opcja A: agent → caveman-proxy → rtk-proxy → dostawca. Opcja B: rtk-proxy nieużywany, zostaje tylko `rtk bulk-read` (pipeline działa bez proxy). | Brak komendy: wybór funkcjonalny. |
| 2 | (A) Test łańcucha bez zmiany agentów: wyślij jedno żądanie Anthropic przez proxy i sprawdź zapis w bazie. | `curl -s http://127.0.0.1:8080/v1/messages -H 'content-type: application/json' -H 'anthropic-version: 2023-06-01' -H "x-api-key: $KLUCZ" -d '{"model":"claude-haiku-4-5","max_tokens":8,"messages":[{"role":"user","content":"ok"}]}'` potem `sqlite3 ~/.config/rtk/llm-proxy/rtk-proxy.db 'select count(*) from usage_records'` |
| 3 | (A) Upstream caveman-proxy → rtk-proxy: w `~/.caveman/caveman.yaml` dodać dostawcę `anthropic` z `base_url: http://127.0.0.1:8080`, restart caveman-proxy. | Edycja `caveman.yaml` + restart procesu `caveman-proxy`. |
| 4 | (A) Trwały start rtk-proxy (dziś proces ręczny, zniknie po restarcie kontenera). | Usługa s6 w init kontenera albo `rtk-proxy service start` (wymaga systemd --user; w s6 nie działa). |
| 5 | (B) Zatrzymanie nieużywanego procesu i poprawka README. | `rtk-proxy stop`; w `~/.agents/README.md` zapisać „rtk-proxy zatrzymany, używany tylko pipeline”. |
| 6 | Obie opcje: README `~/.agents/README.md` mówi „rtk-proxy nieuruchomiony”, a proces działa od 2026-10-23 05:32 (PID 17985). | Poprawić wiersz w README po decyzji z kroku 1. |
