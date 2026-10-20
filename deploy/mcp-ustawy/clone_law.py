#!/usr/bin/env python3
"""Klonuje repozytoria ustaw z komentarzem wymienione w .gitmodules (ścieżki vendor/law/...) do katalogu docelowego."""
import configparser
import os
import subprocess
import sys

src, dest = sys.argv[1], sys.argv[2]
cp = configparser.ConfigParser()
cp.read(src, encoding="utf-8")
n = 0
for sec in cp.sections():
    path, url = cp[sec].get("path", ""), cp[sec].get("url", "")
    if not path.startswith("vendor/law/"):
        continue
    target = os.path.join(dest, path[len("vendor/law/"):])
    os.makedirs(os.path.dirname(target), exist_ok=True)
    subprocess.run(["git", "clone", "-q", "--depth", "1", url, target], check=True)
    n += 1
print(f"sklonowano {n} repozytoriów aktów do {dest}")
if n == 0:
    sys.exit("brak wpisów vendor/law w .gitmodules")
