#!/usr/bin/env bash
# Instaluje ugh-ocr, llamaindex-ocr i markitdown-vision jako globalne
# polecenia CLI (macOS/Linux). markitdown-ocr nie ma wlasnego polecenia --
# to biblioteka, od ktorej zalezy markitdown-vision (instalowana automatycznie
# przez sciezke wzgledna w pyproject.toml, nie wymaga osobnego kroku).
#
# Wymaga: uv (https://docs.astral.sh/uv/). Instalator sam sciaga Pythona 3.12
# przez `uv python install`, jesli brak.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v uv >/dev/null 2>&1; then
    echo "Brak 'uv' na PATH. Zainstaluj: curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
    exit 1
fi

uv python install 3.12

for pkg in markitdown-vision llamaindex-ocr ugh-ocr; do
    echo "=== instaluje $pkg ==="
    (cd "$HERE/$pkg" && uv sync && uv tool install --editable . --reinstall)
done

echo
echo "Gotowe. Jesli 'ugh-ocr' / 'llamaindex-ocr' / 'markitdown-vision' nie sa"
echo "rozpoznawane jako polecenia, dodaj katalog narzedzi uv do PATH:"
echo "  uv tool update-shell"
echo "(potem otworz nowy terminal)."
