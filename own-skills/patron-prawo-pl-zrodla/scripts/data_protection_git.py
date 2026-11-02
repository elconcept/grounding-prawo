"""Kuratorowane źródła ochrony danych w korpusie USTAWY (bez translacji).

Pliki są pobierane z przypiętych commitów Git i sprawdzane po Git blob SHA
przez fetch_data_protection.py. Ten moduł wyodrębnia wyłącznie artykuły.
Nie rekonstruuje zmian prawa z historii commitów i nie twierdzi, że snapshoty
są aktualne. Dotychczasowe źródło krajowej ustawy UODO pozostaje bez zmian.
"""
from __future__ import annotations

from pathlib import Path
import re
import sqlite3

SPECS = (
    {
        "file": "rodo-pl.md", "akt": "rodo", "eli": "CELEX:32016R0679",
        "tytul": "RODO — rozporządzenie (UE) 2016/679 (polski snapshot EUR-Lex)",
        "tekst_jednolity": "02016R0679-20160504",
        "stan_na": "2016-05-04", "zrodlo": "git-snapshot-pl",
        "count": 99, "format": "eu",
        "url": "https://eur-lex.europa.eu/legal-content/PL/TXT/?uri=CELEX:32016R0679",
    },
    {
        "file": "led-pl.md", "akt": "led", "eli": "CELEX:32016L0680",
        "tytul": "Dyrektywa (UE) 2016/680 — ochrona danych przez organy ścigania (PL)",
        "tekst_jednolity": "02016L0680-20160504",
        "stan_na": "2016-05-04", "zrodlo": "git-snapshot-pl",
        "count": 65, "format": "eu",
        "url": "https://eur-lex.europa.eu/legal-content/PL/TXT/?uri=CELEX:32016L0680",
    },
    {
        "file": "dodo-pl.md", "akt": "dodo", "eli": "DU/2019/125",
        "tytul": "DODO — ustawa o danych osobowych przetwarzanych w związku ze zwalczaniem przestępczości",
        "tekst_jednolity": "DU/2019/125 (tekst pierwotny; NIE tekst jednolity)",
        "stan_na": "2018-12-14", "zrodlo": "git-as-law-snapshot",
        "count": 108, "format": "pl",
        "url": "https://eli.gov.pl/eli/DU/2019/125/ogl",
    },
)


def extract_articles(source: str, fmt: str) -> list[tuple[str, str]]:
    if fmt == "eu":
        pattern = re.compile(r"(?m)^Artykuł\s+(\d{1,3}[a-z]?)\s*$")
    elif fmt == "pl":
        pattern = re.compile(r"(?m)^#{4,6}\s+Art\.\s*(\d{1,3}[a-z]?)\.\s*$")
    else:
        raise ValueError(f"Nieznany format: {fmt}")
    matches = list(pattern.finditer(source))
    results = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(source)
        article = match.group(1).lower()
        text = source[match.start():end].strip()
        if not text or article in {key for key, _ in results}:
            raise ValueError(f"Duplikat / pusty artykuł: {article}")
        results.append((article, text))
    return results


def build_data_protection(con: sqlite3.Connection, source_dir: str | Path) -> tuple[int, int]:
    """Zaindeksować trzy przypięte źródła; w razie braków przerwać build."""
    directory = Path(source_dir)
    acts = articles = 0
    for spec in SPECS:
        path = directory / spec["file"]
        source = path.read_text(encoding="utf-8")
        pairs = extract_articles(source, spec["format"])
        numbers = [a for a, _ in pairs]
        expected = [str(i) for i in range(1, spec["count"] + 1)]
        if numbers != expected:
            raise ValueError(
                f"{spec['akt']}: niepełna lub niespójna numeracja: "
                f"oczekiwano 1–{spec['count']}, otrzymano {len(numbers)}: {numbers[:6]} ... {numbers[-6:]}"
            )
        if con.execute("SELECT 1 FROM akty WHERE akt=?", (spec["akt"],)).fetchone():
            raise ValueError(f"{spec['akt']}: duplikat istniejącego aktu (nie nadpisuję)")
        # Kolumna opracowanie służy do identyfikacji konkretnego źródła Git.
        con.execute(
            "INSERT INTO akty (akt, tytul, tekst_jednolity, eli, opracowanie, zrodlo, stan_na, ostatnia_zmiana) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (
                spec["akt"], spec["tytul"], spec["tekst_jednolity"], spec["eli"],
                str(path), spec["zrodlo"], spec["stan_na"], spec["url"],
            ),
        )
        for nr, text in pairs:
            con.execute(
                "INSERT INTO artykuly (akt, art, jednostka, brzmienie, komentarz, plik) "
                "VALUES (?,?,?,?,?,?)",
                (spec["akt"], nr, "", text, "", f"ochrona-danych/{spec['file']}"),
            )
        acts += 1
        articles += len(pairs)
    return acts, articles
