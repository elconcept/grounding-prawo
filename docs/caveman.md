# Caveman — raport wdrożenia

## 1. Co to jest

**Dwie oddzielne rzeczy o tej samej nazwie:**

| Element | Opis |
|---------|------|
| **(a) Skill stylu `caveman`** | Zestaw reguł zwięzłej odpowiedzi (plik `~/.claude/skills/caveman/SKILL.md`, `~/.config/opencode/skills/caveman/SKILL.md`). Warianty: `caveman` (standard), `ultracave` (maksymalna kompresja, `/caveman ultra`), `megacave` (wenyan). Działa na zasadzie: "odpowiedź najpierw, bez ceremoniału, każdy fakt techniczny zostaje". |
| **(b) Platforma `caveman-ai`** | Proxy (`caveman-proxy` na `127.0.0.1:8787` = `ANTHROPIC_BASE_URL` dla Claude), MCP server (`caveman-mcp`: narzędzia `caveman_compress`, `retrieve`, `stats`, `toon_*`), hook `caveman-blocks` (PreToolUse), pamięć `cavemem`, bazy `caveman.db` / `ccr.db`. Konfiguracja w `~/.caveman/` (`caveman.yaml`, `cloud.json`). Input/browse wyłączone (`cloud.json: modules.input=false, modules.browse=false, execute.browse_tool=false`). |

---

## 2. Stan wdrożenia

| Komponent | Gdzie | Stan | Dowód |
|-----------|-------|------|-------|
| Skill `caveman` (Claude) | `~/.claude/skills/caveman/SKILL.md` | **OK** | Plik istnieje, 89 linii, reguły kompletne |
| Skill `caveman` (OpenCode) | `~/.config/opencode/skills/caveman/SKILL.md` | **OK** | Symlink z `~/.agents/skills/caveman` (agents-sync) |
| Skill `ultracave` (Claude) | `~/.claude/skills/ultracave/SKILL.md` | **OK** | Plik istnieje, 63 linie |
| Skill `ultracave` (OpenCode) | `~/.config/opencode/skills/ultracave/SKILL.md` | **OK** | Symlink z `~/.agents/skills/ultracave` |
| Hook `caveman-style` (Claude) | `~/.claude/settings.json` → `SessionStart`, `UserPromptSubmit`, `SubagentStart` | **OK** | `jq -r '.hooks.SessionStart[]?.hooks[]?.command' ~/.claude/settings.json \| grep caveman-style` |
| Hook `caveman-style` (Codex) | `~/.codex/hooks.json` → `SessionStart`, `UserPromptSubmit`, `SubagentStart` | **OK** | `jq -r '.hooks.SessionStart[]?.hooks[]?.command' ~/.codex/hooks.json \| grep caveman-style` |
| Hook `caveman-style` (OpenCode) | plugin `~/.config/opencode/plugins/caveman-style.ts` → `~/.agents/integrations/opencode/caveman-style.ts` (`chat.message` + `experimental.chat.system.transform`; pomija wykonawców `delegate`) | **OK** (od 2026-10-24) | `opencode run` z pytaniem o prompt systemowy zacytował `STYL ODPOWIEDZI: caveman (wymuszony hookiem caveman-style).` |
| `caveman-proxy` (Claude) | `~/.claude/settings.json` → `ANTHROPIC_BASE_URL=http://127.0.0.1:8787/w/claude` + native-hook na `SessionStart`/`UserPromptSubmit`/`PreToolUse`/`PostToolUse`/`Stop`/`PreCompact`/`SubagentStart` | **DZIAŁA CZĘŚCIOWO** | Zwraca tylko znacznik sesji `[[caveman-session-v1 ...]]`, **NIE wstrzykuje reguł stylu** |
| `caveman-proxy` (Codex) | `~/.codex/hooks.json` → native-hook na 11 zdarzeniach (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`, `Stop`, `SessionEnd`) | **DZIAŁA CZĘŚCIOWO** | Ten sam problem — brak wstrzyknięcia reguł stylu |
| `caveman-proxy` (OpenCode) | plugin `~/.config/opencode/plugins/caveman-native.js` (pack 2.2.0, wpis `~/.caveman/integrations/opencode.json`, zainstalowany 2026-10-18) | **DZIAŁA CZĘŚCIOWO** | Wywołuje `native-hook`; jak w Claude: znacznik sesji, bez reguł stylu |
| Moduły platformy | `~/.caveman/cloud.json` | output, waste-fixes, routing, scripts: włączone; input, browse: wyłączone | `jq -c .modules ~/.caveman/cloud.json` |
| Globalny wyłącznik | `CAVEMAN_STYLE=0` | **DOSTĘPNY** | Hook `caveman-style` sprawdza tę zmienną na początku |

---

## 3. Co nie działało i dlaczego

**Objaw:** Mimo `CLAUDE.md` / `AGENTS.md` z zapisem "domyślnie caveman", model pisał długie odpowiedzi z wstępami, podsumowaniami, uprzejmościami.

**Przyczyna:** `caveman-proxy` z `native-hook claude` podpięty pod wszystkie hooki Claude Code **tylko generuje znacznik sesji** (`[[caveman-session-v1 sid=... sig=...]]`). Nie wstrzykuje reguł stylu do kontekstu modelu (brak `additionalContext`). Model więc **nie ładuje skilla** i nie zna reguł.

**Rozwiązanie 2026-10-24:** Nowy hook `~/.agents/bin/caveman-style` (Python) rejestrowany przez `agents-sync` (sekcja 4c) na `SessionStart`, `UserPromptSubmit`, `SubagentStart` w **Claude** (`~/.claude/settings.json`) i **Codex** (`~/.codex/hooks.json`). Hook dokleja `additionalContext` z krótkimi regułami caveman przy każdym poleceniu użytkownika.

**Wyłączanie w sesji:** Prompt zawierający `"normal mode"` lub `"stop caveman"` → tworzy plik `~/.cache/caveman-style/<sesja>.off`. Włączanie: `"/caveman"` lub `"caveman mode"` → usuwa plik `.off`. Globalnie: `CAVEMAN_STYLE=0`.

**Praca prawna:** Do 2026-10-24 instancja `holyclaude-legal` miała zakaz caveman (pisma procesowe). Od 2026-10-24 praca prawna przeniesiona do Cowork → **caveman obowiązuje wszędzie bez wyjątków**.

---

## 4. Plan poprawy wdrożenia

| # | Krok | Plik / Komenda | Status |
|---|------|----------------|--------|
| 1 | **ZROBIONE 2026-10-24**: Hook `caveman-style` dla Claude i Codex | `~/.agents/bin/caveman-style` + `agents-sync` sekcja 4c | ✅ |
| 2 | **ZROBIONE 2026-10-24**: Globalny wyłącznik `CAVEMAN_STYLE=0` | Zmienna w hooku | ✅ |
| 3 | **ZROBIONE 2026-10-24**: Usunięcie wyjątku caveman dla pracy prawnej (praca prawnicza w Cowork) | `~/.agents/AGENTS.md`, sekcja „Styl i skille” | ✅ |
| 4 | **ZROBIONE 2026-10-24**: Reguły `caveman-style` w OpenCode | Plugin `~/.agents/integrations/opencode/caveman-style.ts`, link tworzy `agents-sync` | ✅ |
| 5 | **ISTNIEJE**: Integracja `caveman-proxy` dla OpenCode | `~/.config/opencode/plugins/caveman-native.js` | ✅ |
| 6 | **TEST**: Pomiar długości odpowiedzi przed/po | `wc -l` / `wc -w` na transkryptach `~/.claude/projects/*/*.jsonl` (pole `assistant` message `content`) | ⏳ |
| 7 | **ZROBIONE 2026-10-24**: Test `claude -p` w świeżej sesji | `claude -p "Wyjaśnij, czym jest git rebase i kiedy go używać."` → 178 słów, bez wstępu i zakończenia | ✅ |
| 8 | **ZROBIONE 2026-10-24**: Wyłączanie/włączanie w sesji | `normal mode` → brak wyjścia hooka; `/caveman` → reguły wracają | ✅ |
| 9 | **OPCJONALNIE**: Wyłączyć `caveman-proxy` native-hook (zostawić tylko `caveman-style`) | Usuń `caveman-proxy native-hook` z `SessionStart`/`UserPromptSubmit` w `settings.json` / `hooks.json` (zostaw `PreToolUse`/`PostToolUse` dla `caveman-blocks`) | ⏳ |

---

## 5. Weryfikacja

```bash
# Hook caveman-style działa:
echo '{"hook_event_name":"UserPromptSubmit","session_id":"t","prompt":"x"}' | ~/.agents/bin/caveman-style | head -c 200
# Wynik: {"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"STYL ODPOWIEDZI: caveman...

# Rozmiar raportu:
wc -l docs/caveman.md
```

---

## 6. Kluczowe pliki

| Plik | Rola |
|------|------|
| `~/.claude/skills/caveman/SKILL.md` | Pełne reguły stylu (standard) |
| `~/.config/opencode/skills/caveman/SKILL.md` | To samo dla OpenCode (symlink) |
| `~/.claude/skills/ultracave/SKILL.md` | Reguły maksymalnej kompresji |
| `~/.agents/bin/caveman-style` | Hook wstrzykujący reguły (Python) |
| `~/.caveman/cloud.json` | Konfiguracja platformy (moduły, telemetria) |
| `~/.caveman/caveman.yaml` | Konfiguracja providerów (Vertex AI) |
| `~/.claude/settings.json` | Hooki Claude (caveman-proxy + caveman-style) |
| `~/.codex/hooks.json` | Hooki Codex (caveman-proxy + caveman-style) |
| `~/.agents/integrations/opencode/caveman-style.ts` | Plugin OpenCode wstrzykujący reguły |
| `~/.config/opencode/plugins/caveman-native.js` | Plugin OpenCode platformy caveman-ai (`native-hook`) |
