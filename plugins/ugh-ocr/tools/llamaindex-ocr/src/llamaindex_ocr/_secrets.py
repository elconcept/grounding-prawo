"""Ladowanie klucza API LlamaCloud.

Kolejnosc: zmienna srodowiskowa LLAMA_CLOUD_API_KEY, potem plik sekretow
globalny (~/.claude/secrets/llamacloud_api_key.txt). Klucz NIGDY nie jest
hardcoded w kodzie -- poprzednia wersja tego skryptu miala klucz wpisany
wprost w zrodle (patrz legacy_batch_script.py.bak), co jest zlym nawykiem
(klucz trafia do historii gita/kopii pliku przy kazdym udostepnieniu kodu).
"""

from __future__ import annotations

import os
from pathlib import Path

SECRET_FILE = Path.home() / ".claude" / "secrets" / "llamacloud_api_key.txt"


def load_api_key() -> str:
    env_key = os.environ.get("LLAMA_CLOUD_API_KEY", "").strip()
    if env_key:
        return env_key

    if SECRET_FILE.exists():
        key = SECRET_FILE.read_text(encoding="utf-8").strip()
        if key:
            return key

    raise RuntimeError(
        "Brak klucza LlamaCloud. Ustaw zmienna srodowiskowa LLAMA_CLOUD_API_KEY "
        f"albo zapisz klucz (bez cudzyslowow, bez nowej linii) w {SECRET_FILE}"
    )
