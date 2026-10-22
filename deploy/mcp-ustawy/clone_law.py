#!/usr/bin/env python3
"""Klonuje repozytoria aktów z .gitmodules: vendor/law/... (komentarze, płytko) i vendor/law-git/... (git-as-law, z historią
commitów, bo stan na dzień i ostatnia nowelizacja pochodzą z logu)."""
import configparser
import os
import subprocess
import sys

src, dest = sys.argv[1], sys.argv[2]
dest_git = sys.argv[3] if len(sys.argv) > 3 else None
cp = configparser.ConfigParser()
cp.read(src, encoding="utf-8")
n = 0
for sec in cp.sections():
    path, url = cp[sec].get("path", ""), cp[sec].get("url", "")
    if path.startswith("vendor/law/"):
        target, opts = os.path.join(dest, path[len("vendor/law/"):]), ["--depth", "1"]
    elif path.startswith("vendor/law-git/") and dest_git:
        target, opts = os.path.join(dest_git, path[len("vendor/law-git/"):]), ["--filter=blob:none"]
    else:
        continue
    os.makedirs(os.path.dirname(target), exist_ok=True)
    subprocess.run(["git", "clone", "-q", *opts, url, target], check=True)
    n += 1
print(f"sklonowano {n} repozytoriów aktów do {dest}")
if n == 0:
    sys.exit("brak wpisów vendor/law w .gitmodules")
