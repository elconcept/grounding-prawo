#!/usr/bin/env python3
"""Tekst pisma z DOCX (po przyjęciu zmian śledzonych) albo z Markdown (bez frontmattera).

Wspólny moduł skryptów `lint_pisma.py` i `retencja_pisma.py`. Uruchomiony samodzielnie wypisuje tekst:

    python3 pismo_tekst.py <pismo.docx|pismo.md>
"""
import re
import sys
import zipfile


def z_docx(path):
    x = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    x = re.sub(r"<w:del\b[^>]*/>", "", x)
    x = re.sub(r"<w:del\b[^>]*>.*?</w:del>", "", x, flags=re.S)
    akapity = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", x, flags=re.S):
        t = "".join(a if a else ("\t" if b else "\n")
                    for a, b, _ in re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>|(<w:tab/>)|(<w:br/>)", p))
        akapity.append(t)
    t = "\n".join(akapity)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&apos;", "'")):
        t = t.replace(a, b)
    return t.strip() + "\n"


def z_md(path):
    t = open(path, encoding="utf-8").read()
    if t.startswith("---"):
        k = t.find("\n---", 3)
        if k != -1:
            t = t[k + 4:]
    return t.strip() + "\n"


def tekst(path):
    if path == "-":
        return sys.stdin.read()
    return z_docx(path) if path.lower().endswith(".docx") else z_md(path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.stdout.write(tekst(sys.argv[1]))
