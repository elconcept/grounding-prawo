"""Wyjatek dla bledow koncowych, ktore CLI ma pokazac uzytkownikowi ladnie
sformatowane (bez surowego Pythonowego tracebacku)."""

from __future__ import annotations


class UghOcrError(Exception):
    def __init__(self, title: str, detail: str = "", hint: str = "") -> None:
        super().__init__(title)
        self.title = title
        self.detail = detail
        self.hint = hint
