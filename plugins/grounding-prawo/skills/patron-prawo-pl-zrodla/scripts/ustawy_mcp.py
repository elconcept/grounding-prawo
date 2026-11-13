#!/usr/bin/env python3
"""⚖️ MCP-USTAWY — wybrane akty i komentarze, lokalna baza SQLite.

Uruchomienie: python ustawy_mcp.py [--http --port 8080]
Bazę buduje ustawy.py z submodułów komentarzy oraz git-as-law.
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Literal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.mcpserver import MCPServer  # noqa: E402
from mcp.types import ToolAnnotations  # noqa: E402

import ustawy  # noqa: E402

INSTRUCTIONS = """⚖️ USTAWY · 📜 PRZEPIS · ✧ KOMENTARZ
Jeden odczyt lokalnej, wyselekcjonowanej bazy: artykuł i komentarz interpretacyjny.
Wywołaj przepis(akt, art) z domyślnym widokiem 'oba', żeby otrzymać tekst oraz
komentarz do stosowania danego przepisu. 'tekst' lub 'komentarz' ogranicza rozmiar
odpowiedzi, kiedy potrzebujesz tylko jednej warstwy.
Akty: skrót (np. kpk, kpc, kc, kpw, uozp) albo identyfikator katalogowy.
OUT_OF_SCOPE znaczy, że aktu nie ma w wybranym korpusie — znajdź go w Repertorium/ELI.
Pole tekst to treść przepisu z opisanym stanem źródła; komentarz stanowi
opracowanie AI, a nie orzecznictwo, źródło prawa ani poradę prawną.
Wyszukiwanie tematyczne i orzecznictwo realizuj przez Repertorium.
"""

RO = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)
server = MCPServer("ustawy", instructions=INSTRUCTIONS)
_baza: ustawy.Baza | None = None


def baza() -> ustawy.Baza:
    global _baza
    if _baza is None:
        _baza = ustawy.Baza(os.environ.get("USTAWY_DB", ustawy.DEFAULT_DB))
    return _baza


@server.tool(annotations=RO)
def przepis(akt: str, art: str, widok: Literal["oba", "tekst", "komentarz"] = "oba") -> dict:
    """Odczytaj ARTYKUŁ i KOMENTARZ AI z wybranych polskich aktów. Podaj skrót aktu (np. 'uozp', 'kpk', 'kpc', 'kc') oraz numer artykulu (np. '23', '306', '117^1'). Komentarz pochodzi z repozytorium opracowań i nie zawiera orzecznictwa."""
    wynik = baza().artykul(akt, art, komentarz=widok != "tekst")
    wynik["emblemat"] = "⚖️ USTAWY · 📜 PRZEPIS · ✧ KOMENTARZ"
    if widok == "komentarz":
        wynik.pop("tekst", None)
    return wynik


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--http", action="store_true")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8080")))
    a = ap.parse_args()
    if not a.http:
        server.run("stdio")
        return
    import uvicorn
    from starlette.responses import JSONResponse
    from starlette.routing import Route

    app = server.streamable_http_app(stateless_http=True, json_response=True, host=a.host)

    async def healthz(_request):
        try:
            n = len(baza().akty())
        except Exception as exc:
            return JSONResponse({"ok": False, "error": str(exc)}, status_code=503)
        return JSONResponse({"ok": True, "akty": n})

    app.router.routes.append(Route("/healthz", healthz))
    uvicorn.run(app, host=a.host, port=a.port, log_level="warning")


if __name__ == "__main__":
    main()
