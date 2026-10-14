#!/usr/bin/env python3
"""Tekst dokumentu ze znacznikami [Page N] - z PDF, DOCX albo gotowego Markdown (np. po OCR).

Numer strony w cytacie [[page:N||quote:...]] to kolejny znacznik [Page N] w wyniku,
nie numer wydrukowany w stopce dokumentu.

  doc_to_text.py umowa.pdf                     tekst na stdout
  doc_to_text.py teczka/* --out-dir teksty/    wiele plikow naraz
  doc_to_text.py skan.md --page-sep hr         strony rozdzielone linia '---'
  doc_to_text.py skan.md --page-sep '^=== strona \\d+ ===$'   wlasny separator (regex)

Markdown (the-ocr, Chandra/Datalab, LlamaParse, markitdown): strony rozpoznawane same po
  [Page N] | ## Page N, # Strona N | <!-- page N --> | <!-- PageBreak --> |
  {N}------ (Datalab paginate) | znak \\f
Linia '---' (the-ocr, LlamaParse) moze byc zwykla linia pozioma Markdown, wiec dzieli
strony tylko z --page-sep hr albo gdy frontmatter ma ocr_backend (the-ocr), a innych
znacznikow brak. Frontmatter YAML jest pomijany. Bez znacznikow - jedna strona.

PDF z plikiem .md o tej samej nazwie obok (umowa.pdf + umowa.md) - brany jest .md,
bo OCR dobrym modelem jest lepszy niz warstwa tekstu PDF; --no-md wylacza.
PDF bez .md: pdftotext (poppler-utils), strony po \\f. DOCX: jedna strona.
"""
import argparse
import re
import subprocess
import sys
import zipfile
from html import unescape
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A﻿?---\n(.*?)\n---\n", re.S)
NUMBERED_MARKERS = [
    re.compile(r"^\[Page\s+(\d+)\]\s*$", re.M),
    re.compile(r"^#{1,6}\s*(?:Page|Strona)\s+(\d+)\s*$", re.M | re.I),
    re.compile(r"^<!--\s*(?:page|strona)[\s:_-]*(\d+)\s*-->\s*$", re.M | re.I),
    re.compile(r"^\{(\d+)\}-{10,}\s*$", re.M),
]
BREAK_MARKERS = [
    re.compile(r"^<!--\s*page\s*break\s*-->\s*$", re.M | re.I),
    re.compile(r"\f"),
]
HR_RE = re.compile(r"^[ \t]*---[ \t]*$", re.M)


def _trim(pages: list) -> list:
    while pages and not pages[0].strip():
        pages.pop(0)
    while pages and not pages[-1].strip():
        pages.pop()
    return pages or [""]


def _split_numbered(rx: re.Pattern, body: str) -> list:
    # Z grupa w regexie split zwraca [przed, nr1, tekst1, nr2, tekst2, ...].
    parts = rx.split(body)
    texts = parts[2::2]
    if texts:
        texts[0] = parts[0] + texts[0]  # tytul przed pierwszym znacznikiem -> strona 1
    return _trim(texts) if texts else [body]


def split_markdown(text: str, page_sep: str | None = None) -> list:
    fm = FRONTMATTER_RE.match(text)
    meta, body = (fm.group(1), text[fm.end():]) if fm else ("", text)
    if page_sep == "hr":
        return _trim(HR_RE.split(body))
    if page_sep:
        return _trim(re.split(page_sep, body, flags=re.M))
    for rx in NUMBERED_MARKERS:
        if rx.search(body):
            return [BREAK_MARKERS[0].sub("", page) for page in _split_numbered(rx, body)]
    for rx in BREAK_MARKERS:
        if rx.search(body):
            return _trim(rx.split(body))
    if re.search(r"^ocr_backend:", meta, re.M) and HR_RE.search(body):
        return _trim(HR_RE.split(body))
    return [body]


def pages_of(p: Path, prefer_md: bool = True, page_sep: str | None = None) -> list:
    s = p.suffix.lower()
    if s == ".pdf" and prefer_md and p.with_suffix(".md").exists():
        md = p.with_suffix(".md")
        print(f"{p.name}: uzywam {md.name} zamiast warstwy tekstu PDF", file=sys.stderr)
        pages = split_markdown(md.read_text(encoding="utf-8", errors="replace"), page_sep)
        if len(pages) == 1:
            print(f"uwaga: {md.name} nie ma znacznikow stron - cytaty dostana str. 1 "
                  "(--no-md bierze strony z PDF)", file=sys.stderr)
        return pages
    if s == ".pdf":
        try:
            out = subprocess.run(["pdftotext", "-layout", str(p), "-"], check=True,
                                 capture_output=True, text=True).stdout
        except FileNotFoundError:
            sys.exit("Brak pdftotext - zainstaluj: sudo apt install poppler-utils")
        return _trim(out.split("\f"))
    if s == ".docx":
        with zipfile.ZipFile(p) as z:
            xml = z.read("word/document.xml").decode("utf-8", errors="replace")
        xml = re.sub(r"</w:p>", "\n", xml)
        return [unescape(re.sub(r"<[^>]+>", "", xml))]
    return split_markdown(p.read_text(encoding="utf-8", errors="replace"), page_sep)


def to_text(p: Path, prefer_md: bool = True, page_sep: str | None = None) -> str:
    pages = pages_of(p, prefer_md, page_sep)
    return "\n".join(f"[Page {i}]\n{page.strip()}\n" for i, page in enumerate(pages, 1))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out-dir", help="zapisz <nazwa>.txt w tym katalogu zamiast na stdout")
    ap.add_argument("--no-md", action="store_true", help="dla PDF nie uzywaj .md o tej samej nazwie")
    ap.add_argument("--page-sep", help="'hr' (linia ---) albo regex linii rozdzielajacej strony")
    a = ap.parse_args(argv)
    done = set()
    for f in a.files:
        p = Path(f)
        if a.out_dir and p.stem in done:
            continue  # umowa.pdf i umowa.md daja ten sam wynik
        text = to_text(p, not a.no_md, a.page_sep)
        if a.out_dir:
            out = Path(a.out_dir)
            out.mkdir(parents=True, exist_ok=True)
            target = out / (p.stem + ".txt")
            target.write_text(text, encoding="utf-8")
            done.add(p.stem)
            print(f"{p} -> {target} ({text.count('[Page ')} str.)", file=sys.stderr)
        else:
            sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
