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
            "Wspólna pamięć LLM: użyj połączonego MCP Basic Memory, "
            "wyszukaj stosowny kontekst projektu model-memory "
            "(UUID 50c6d08c-2e2f-4c94-9afb-5d2478ae821b), "
            "niezależnie od legal. Starsze recapy można odczytać z main. "
            "W trakcie sesji zapisuj trwałe preferencje i decyzje do model-memory, "
            "materiały prawne i źródła wyłącznie do legal; po zapisie sprawdź odczytem. "
            "Nie przesyłaj całych rozmów i nie zapisuj sekretów."
        )
    elif name == "PreCompact":
        print(
            "Przed kompakcją utrwal ważne decyzje, niezakończone kroki i wyniki "
            "tej sesji w Basic Memory model-memory przez dostępne narzędzia MCP, "
            "w legal umieszczaj tylko materiały sprawy. Potwierdź odczyt."
        )


if __name__ == "__main__":
    main()
