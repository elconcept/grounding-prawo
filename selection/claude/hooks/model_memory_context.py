#!/usr/bin/env python3
"""Claude Code hook: inject MCP memory retrieval/checkpoint instructions.

No network calls, credentials, transcript upload, or local memory duplicates.
Real reads/writes remain LLM tool calls to the authenticated Basic Memory MCP.
"""
from __future__ import annotations
import json
import sys


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        event = {}
    name = event.get("hook_event_name", "")
    if name == "SessionStart":
        print(
            "Basic Memory: odczytaj z model-memory tylko kuratorowane, kluczowe i trwałe ustalenia "
            "(UUID 50c6d08c-2e2f-4c94-9afb-5d2478ae821b), a z main najnowszy "
            "recap odpowiedni do bieżącej sesji. W legal są źródła, sprawy i notatki dowodowe. "
            "Prowadź dziennik zmian i recapy sesji wyłącznie w main/sesje/. "
            "Model-memory aktualizuj selektywnie tylko przy nowych key takeaways "
            "przydatnych w przyszłości, nigdy automatycznie całym recapem. "
            "Po zapisie potwierdź odczytem, nie zapisuj sekretów."
        )
    elif name == "PreCompact":
        print(
            "Przed kompakcją zapisz/uzupełnij recap bieżącej sesji wyłącznie "
            "w Basic Memory main/sesje/ (działania, decyzje, wyniki, błędy, kolejny krok). "
            "Sprawdź odczytem. Model-memory to curated key takeaways: aktualizuj "
            "tylko jeśli sesja wnosi wartościową trwałą zasadę lub preferencję; "
            "nie zapisuj tam dziennika. Legal zawiera fakty i źródła spraw."
        )

if __name__ == "__main__":
    main()
