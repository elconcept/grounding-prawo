#!/usr/bin/env python3
"""Claude Code / Codex hook: point the model at the legal memory protocol.

The session brief, project mapping and post-compaction checkpoint come from the
`basic-memory-nas` plugin. This hook adds only the legal-specific pointer and
must stay consistent with it: one project `main`, sessions in legal/sessions.
No network calls, credentials, transcript upload or local state.
"""
from __future__ import annotations
import json
import sys


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        event = {}
    name = event.get("hook_event_name", "") if isinstance(event, dict) else ""
    if name == "SessionStart":
        print(
            "Basic Memory (grounding-prawo): projekt `main`, wszystko dla spraw pod `legal/` "
            "(checkpointy `legal/sessions/` type: session, decyzje `legal/decyzje/`, zadania `legal/zadania/`, "
            "teczki `legal/sprawy/<katalog>/`). Przed pierwszą odpowiedzią merytoryczną zorientuj się "
            "(`bm-orient` albo `bm_search` w `legal/sessions`), a przy pracy nad sprawą przeczytaj "
            "`shared/BASIC-MEMORY.md`. Każdy zapis potwierdź `bm_read`; bez sekretów."
        )
    elif name == "PreCompact":
        print(
            "Przed kompakcją zapisz checkpoint skillem `bm-checkpoint`: projekt `main`, folder "
            "`legal/sessions/`, type: session (cel, działania, decyzje, wyniki, błędy, następny krok). "
            "Potwierdź odczytem `bm_read`."
        )


if __name__ == "__main__":
    main()
