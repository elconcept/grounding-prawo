#!/usr/bin/env python3
"""Pobierz niezmienne, wersjonowane w Git źródła korpusu ochrony danych.

Celowo NIE pobiera całych repozytoriów legalize-eu/legalize-pl/public-data.
Pobiera tylko cztery pliki z przypiętych commitów i weryfikuje ich Git blob SHA.
Przypięty snapshot NIE jest automatycznie aktualnym stanem prawnym.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.request
from pathlib import Path

# Pochodzenie polskiego tekstu RODO oraz LED: EUR-Lex/CELLAR -> eudirective.
# Historia zmian RODO: odrębny, referencyjny git-as-law legalize-dev/legalize-eu.
# DODO: polski git-as-law legalize-dev/legalize-pl (oryginalna wersja historyczna).
SOURCES = {
    "rodo-pl.md": {
        "repo": "eudirective/public-data",
        "commit": "6650d22a40379c8f2182b0086c24fded22262055",
        "path": "source-library/core/pl/eu/eu_32016r0679_PL.md",
        "blob": "c81b05bec10f6ce89e6762679d3ac615e6b9f67c",
        "identyfikator": "CELEX:32016R0679",
        "edycja": "02016R0679-20160504",
    },
    "led-pl.md": {
        "repo": "eudirective/public-data",
        "commit": "6650d22a40379c8f2182b0086c24fded22262055",
        "path": "source-library/core/pl/eu/eu_32016l0680_PL.md",
        "blob": "fada1c362d3d0acac42ad4e99933bf8f94f9a826",
        "identyfikator": "CELEX:32016L0680",
        "edycja": "02016L0680-20160504",
    },
    "dodo-pl.md": {
        "repo": "legalize-dev/legalize-pl",
        "commit": "663baba7eff0730cb169bca8df2de0fc1ef4b46d",
        "path": "pl/DU-2019-125.md",
        "blob": "618d14201905a4483435c54bfb1637ab94eae436",
        "identyfikator": "DU/2019/125",
        "edycja": "tekst pierwotny 2018-12-14 (NIE ujednolicony)",
    },
    "rodo-git-as-law-en.md": {
        "repo": "legalize-dev/legalize-eu",
        "commit": "cf58758b3956abd728899a347837b19b49ea6945",
        "path": "eu/6e/32016R0679.md",
        "blob": "d1d852c631a329e672efc230402a8d948b7aecf1",
        "identyfikator": "CELEX:32016R0679",
        "edycja": "historyczny punkt git-as-law 2016-05-04; angielska referencja, NIE indeksowana",
    },
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\\0" + data).hexdigest()


def download(out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    items = {}
    for filename, src in SOURCES.items():
        url = f"https://raw.githubusercontent.com/{src['repo']}/{src['commit']}/{src['path']}"
        req = urllib.request.Request(url, headers={"User-Agent": "mcp-ustawy-pinned-legal-corpus/1"})
        with urllib.request.urlopen(req, timeout=35) as response:
            # Limit na plik; nie pobieramy przypadkowo wielkich danych.
            data = response.read(2_000_001)
        if not data or len(data) > 2_000_000:
            raise ValueError(f"{filename}: niedozwolony rozmiar: {len(data)}")
        actual_blob = git_blob_sha(data)
        if actual_blob != src["blob"]:
            raise ValueError(f"{filename}: Git blob SHA mismatch {actual_blob} != {src['blob']}")
        text = data.decode("utf-8")
        if filename.endswith("-pl.md") and filename != "dodo-pl.md":
            if "Representation language: `PL`" not in text or src["edycja"] not in text:
                raise ValueError(f"{filename}: inna edycja lub język niż zadeklarowane")
        if filename == "dodo-pl.md" and 'eli: "DU/2019/125"' not in text:
            raise ValueError(f"{filename}: niezgodny identyfikator ELI")
        tmp = out_dir / f".{filename}.tmp"
        tmp.write_bytes(data)
        os.replace(tmp, out_dir / filename)
        items[filename] = {
            **src, "url": url, "sha256": hashlib.sha256(data).hexdigest(),
            "rozmiar_bajtow": len(data),
        }
    meta = {
        "ostroznosc": "Historyczne snapshoty Git: NIE poświadczają aktualnego stanu prawnego; porównaj z EUR-Lex i ELI.",
        "sources": items,
    }
    tmp_meta = out_dir / ".manifest.json.tmp"
    tmp_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp_meta, out_dir / "manifest.json")
    return meta


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    meta = download(args.out)
    print("Pobrano i zweryfikowano", len(meta["sources"]), "źródła Git.")
