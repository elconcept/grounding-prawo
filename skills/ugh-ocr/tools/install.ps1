# Instaluje ugh-ocr, llamaindex-ocr i markitdown-vision jako globalne
# polecenia CLI (Windows). markitdown-ocr nie ma wlasnego polecenia -- to
# biblioteka, od ktorej zalezy markitdown-vision (sciezka wzgledna w
# pyproject.toml, bez osobnego kroku instalacji).
#
# Wymaga: uv (https://docs.astral.sh/uv/).
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Error "Brak 'uv' na PATH. Zainstaluj: irm https://astral.sh/uv/install.ps1 | iex"
    exit 1
}

uv python install 3.12

foreach ($pkg in @("markitdown-vision", "llamaindex-ocr", "ugh-ocr")) {
    Write-Host "=== instaluje $pkg ==="
    Push-Location (Join-Path $here $pkg)
    try {
        uv sync
        uv tool install --editable . --reinstall
    } finally {
        Pop-Location
    }
}

Write-Host ""
Write-Host "Gotowe. Jesli polecenia nie sa rozpoznawane, uruchom 'uv tool update-shell'"
Write-Host "i otworz nowy terminal."
