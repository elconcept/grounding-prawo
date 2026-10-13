"""Serwer MCP (STDIO) dla markitdown-vision.

Jedno narzedzie, convert_to_markdown, dostepne zarowno dla Claude (przez MCP)
jak i dla uzytkownika (przez dowolnego innego klienta MCP albo bezposrednio
przez CLI `markitdown-vision`, patrz __main__.py).
"""

from __future__ import annotations

from pathlib import Path

from mcp.server.mcpserver import MCPServer

from ._core import convert_file

mcp = MCPServer("markitdown-vision")


@mcp.tool()
def convert_to_markdown(path: str) -> str:
    """Konwertuje plik (PDF, obraz, DOCX, PPTX, XLSX, ...) do pliku .md obok
    niego, o tej samej nazwie bazowej. Automatycznie uzywa Google Cloud
    Vision OCR dla samodzielnych obrazow oraz dla PDF-ow (i DOCX/PPTX/XLSX
    z osadzonymi obrazami) bez warstwy tekstowej. Zwraca sciezke wynikowego
    pliku .md."""
    output_path = convert_file(Path(path))
    return str(output_path)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
