---
name: fastmcp-builder
description: Buduj nowy MCP server (lub retrofit istniejacego) z 5 elementami zwalidowanymi na dograh v1.31.0 - FastMCP(instructions=) z procedural orchestration, drift test, dwukanalowy auth X-API-Key LUB Bearer, OTel atrybut org_id dla per-tenant routing, ToolAnnotations dla read-only. Uzywaj gdy zaczynasz nowy MCP server (saos/eu-compliance/anonimizacja/pomoc-prawna/kio/isap/inny), retrofit istniejacego do tego patternu, dodajesz nowy tool do MCP, debugujesz dlaczego LLM nie wywoluje Twoich tooli w odpowiedniej kolejnosci, lub gdy klient MCP (Claude Code/Cursor) nie autoryzuje. Trigger - "nowy MCP", "buduj MCP server", "FastMCP", "instructions MCP", "dryft testu MCP", "Claude Code MCP", "auth MCP", "OTel MCP", "FastMCP setup", "retrofit MCP", "tools MCP audit", "tools MCP nie sa wywolywane".
license: Apache-2.0
attribution:
  source: dograh-hq/dograh
  url: https://github.com/dograh-hq/dograh
  license: BSD-2-Clause
  relationship: pattern-only
  note: >
    Wzorzec źródłowy dla FastMCP(instructions=) i orkiestracji proceduralnej. Treść, testy driftu i kanon napisane od zera.
allowed-tools: [Read, Write, Edit]
requires-human-approval: false
---
# fastmcp-builder

Wzorzec kanoniczny dla MCP serverow. Walidowany empirycznie na [dograh-hq/dograh](https://github.com/dograh-hq/dograh) v1.31.0 (production system, 3-4 dni release cycle, 2.6k gwiazdek, drift testy w CI, BSD-2).

## Kiedy uzywac

- Nowy MCP server od pierwszego commita
- Retrofit istniejacych
- Audit istniejacego MCP server (czy ma 5 elementow)
- Debug: LLM nie wywoluje tooli w odpowiedniej kolejnosci, klient MCP nie autoryzuje, error_codes ginace dla LLM

## 5 elementow kanonu

### 1. `FastMCP(instructions=...)` z procedural orchestration

Instrukcje wstrzykiwane do system promptu kazdego klienta MCP. LLM widzi je PRZED pierwszym tool call.

**Tresc:**
- Call order (ktora kolejnosc wywolywac tools)
- Error handling (jak iteorwac po failed tool call)
- Hard constraints (czego NIE robic)
- Field conventions (kanoniczne nazwy, format ID)
- Style (preferencje przy wyborze toolow gdy wiele rozwiazan)

**Anti-content:**
- NIE re-enumerowac tool signatures (drift - signatury sa w `tools/list`)
- NIE re-enumerowac error_codes (drift - error_codes w tool docstring)
- NIE per-field guidance (to lezy w `PropertySpec.llm_hint`)

Wzor (Python):
```python
from fastmcp import FastMCP
from .instructions import MY_MCP_INSTRUCTIONS
from .tools.foo import foo_tool
from .tools.bar import bar_tool

mcp = FastMCP("mcp-saos", instructions=MY_MCP_INSTRUCTIONS)

for _tool in (foo_tool, bar_tool):
    mcp.tool(_tool)
```

### 2. Drift test (`tests/test_mcp_instructions_drift.py`)

Fail jesli:
- Instructions wymienia tool nie registered
- Tool ma error_code ktorego nie ma w docstring

Wzor w `examples/test_instructions_drift.py`.

### 3. Auth dwukanalowy X-API-Key LUB Bearer

FastMCP domyslnie stripuje `Authorization` header. **MUSISZ** explicit `get_http_headers(include={"authorization"})`.

```python
from fastmcp.server.dependencies import get_http_headers

async def authenticate_mcp_request() -> User:
    headers = get_http_headers(include={"authorization"})
    api_key = headers.get("x-api-key")
    if not api_key:
        auth = headers.get("authorization", "")
        if auth.lower().startswith("bearer "):
            api_key = auth.split(" ", 1)[1].strip()
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key - send X-API-Key or Authorization: Bearer <key>",
        )
    return await _handle_api_key_auth(api_key)
```

### 4. OTel atrybut `<server>.org_id` per-tenant routing

Per-org routing do Langfuse/observability:

```python
from opentelemetry import trace

span = trace.get_current_span()
if span.is_recording():
    org_id = user.selected_organization_id
    span.set_attribute("mcp.org_id", str(org_id))
    span.set_attribute("mcp.user_id", str(user.id))
    span.set_attribute("langfuse.user.id", str(user.id))
```

**WAZNE rozroznienie z dograh-auth:**
- `<server>.org_id` (np. `dograh.org_id`) triggeruje per-org Langfuse project routing dla **pipeline spans**
- Dla **MCP traffic** uzyj `mcp.org_id` zeby zostalo na default (developer-facing) project
- Bez tego rozroznienia traffic deweloperski miesza sie z produkcyjnym multi-tenant

### 5. ToolAnnotations dla read-only tools

Pozwala klientowi MCP automatycznie zatwierdzac wywolania bez monitu (`readOnlyHint=True` + `destructiveHint=False`).

```python
from mcp.types import ToolAnnotations

_READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    idempotentHint=True,
    destructiveHint=False,
    openWorldHint=False,
)

for _tool in (list_docs, search_docs, read_doc):
    mcp.tool(_tool, annotations=_READ_ONLY)
```

## Templatey gotowe do skopiowania

W `examples/`:
- `server.py` - kanon setup FastMCP + registration
- `instructions.py` - szkielet z 4 sekcjami (Call order / Allowed shape / Iterating on errors / Style)
- `auth.py` - dwukanalowy + OTel
- `test_instructions_drift.py` - drift test do CI

## Smoke test po wdrozeniu

```bash
claude mcp add --transport http <name> https://<your-mcp>/api/v1/mcp/ \
  --header "X-API-Key: <key>"
claude mcp list
# Powinno wyswietlic <name> + status connected + tools count
```

W Claude Code: "List my <resources> via <name>" - czy LLM wywoluje tool wlasciwy?

## Anti-patterns do unikania

| Anti-pattern | Konsekwencja |
|---|---|
| Restating tool signatures w instructions | Drift, signatury rosna z kodu |
| Re-enumerating error_codes w instructions | Drift, error_codes rosna z docstring |
| Hardcoded API key validation w kazdym tool | Reuse `authenticate_mcp_request()` |
| Stdlib `logging.info(request_body)` | Loguruj sekrety. Uzyj Loguru z masking PII |
| Brak ToolAnnotations na read-only | Klient pyta o approval przy kazdym wywolaniu |
| Single-channel auth (tylko X-API-Key lub tylko Bearer) | Niektorzy klienci wysylaja drugi - 401 |
| Brak OTel atrybutow org_id | Brak per-tenant observability w multi-tenant |

## Walidowane na

- **dograh v1.31.0** ([dograh-hq/dograh](https://github.com/dograh-hq/dograh), BSD-2) - source pattern, production 3-4 dni release cycle
- Kluczowe pliki referencyjne (kanon): `api/mcp_server/server.py`, `api/mcp_server/instructions.py`, `api/mcp_server/auth.py` w upstream repo

## Linki

- [dograh-hq/dograh](https://github.com/dograh-hq/dograh) - source pattern (BSD-2)
- [mcp-eu-compliance v0.2.0](https://github.com/elconcept/mcp-eu-compliance) - MCP z pelnym kanonem (TS adaptacja Python wzorca)
