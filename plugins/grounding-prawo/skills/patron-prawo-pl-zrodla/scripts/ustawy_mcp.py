#!/usr/bin/env python3
"""Serwer MCP bazy ustaw z komentarzem (zastępuje konektory `cite` i `isap`).

    python ustawy_mcp.py                       # stdio
    python ustawy_mcp.py --http --port 8080    # Streamable HTTP pod /mcp (+ GET /healthz)

Indeks: zmienna USTAWY_DB (plik SQLite z `ustawy.py buduj`), historia brzmień: USTAWY_LAW_DIR (repo git-as-law).
Wymaga pakietu `mcp>=2,<3`.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.mcpserver import MCPServer  # noqa: E402
from mcp.types import ToolAnnotations  # noqa: E402

import ustawy  # noqa: E402

INSTRUCTIONS = """Baza polskich ustaw: aktualny tekst jednolity kodeksów i Konstytucji (git-as-law, historia nowelizacji)
oraz komentarz do każdego artykułu 32 ustaw. Kolejność: `ustawy_szukaj` (zagadnienie, gdy nie znasz artykułu) ->
`ustawy_artykul` (pełne brzmienie, stan_na, ewentualnie komentarz lub brzmienie na dzień) -> `ustawy_cytat`
(czy fragment, który chcesz zacytować, stoi w brzmieniu). Cytuj wyłącznie pole `tekst` ze statusem FOUND; zawsze
podaj tekst jednolity i stan_na. `zrodlo=komentarz` oznacza brzmienie z opracowania: potwierdź w ELI
(api.sejm.gov.pl) przed cytatem w piśmie. OUT_OF_SCOPE: aktu nie ma w korpusie, szukaj w ELI. Komentarz to
opracowanie, nie źródło prawa."""

RO = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)
server = MCPServer("ustawy", instructions=INSTRUCTIONS)
_baza: ustawy.Baza | None = None


def baza() -> ustawy.Baza:
    global _baza
    if _baza is None:
        _baza = ustawy.Baza(os.environ.get("USTAWY_DB", ustawy.DEFAULT_DB), os.environ.get("USTAWY_LAW_DIR", ustawy.DEFAULT_LAW))
    return _baza


@server.tool(annotations=RO)
def akty() -> list[dict]:
    """Lista aktów w korpusie: identyfikator, skróty (kk, kpk, kpc...), tekst jednolity, stan_na, czy jest komentarz."""
    return baza().akty()


@server.tool(annotations=RO)
def szukaj(q: str, akt: str | None = None, zakres: str | None = None, limit: int = 10) -> list[dict]:
    """Wyszukiwanie pełnotekstowe po przepisach i komentarzach (odmiana i diakrytyki bez znaczenia).

    akt: identyfikator lub skrót (np. kk, kpk, uozp); zakres: 'przepisy' albo 'komentarze'."""
    return baza().szukaj(q, akt, zakres, max(1, min(int(limit), 50)))


@server.tool(annotations=RO)
def artykul(akt: str, art: str, komentarz: bool = False, na_dzien: str | None = None) -> dict:
    """Pełne brzmienie artykułu (np. akt='kpc', art='117^1' albo '117[1]'). na_dzien=RRRR-MM-DD zwraca brzmienie
    obowiązujące tego dnia z historii nowelizacji; komentarz=True dołącza komentarz do artykułu."""
    return baza().artykul(akt, art, komentarz, na_dzien)


@server.tool(annotations=RO)
def cytat(akt: str, art: str, fragment: str, na_dzien: str | None = None) -> dict:
    """Czy fragment występuje dosłownie (bez różnic w odstępach i cudzysłowach) w brzmieniu artykułu.
    Wynik FOUND / NOT_FOUND / NOT_CHECKED."""
    return baza().cytat(akt, art, fragment, na_dzien)


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
        except Exception as exc:  # brak indeksu = niezdrowy kontener
            return JSONResponse({"ok": False, "error": str(exc)}, status_code=503)
        return JSONResponse({"ok": True, "akty": n})

    app.router.routes.append(Route("/healthz", healthz))
    uvicorn.run(app, host=a.host, port=a.port, log_level="warning")


if __name__ == "__main__":
    main()
