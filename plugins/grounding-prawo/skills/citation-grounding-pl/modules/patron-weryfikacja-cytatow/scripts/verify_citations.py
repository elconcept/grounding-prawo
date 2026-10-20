#!/usr/bin/env python3
"""Mechaniczna weryfikacja cytatow wzgledem tekstu zrodlowego (stdlib, offline, zero LLM).

Port z Patrona (MateMatic Solutions, AGPL-3.0):
  backend/src/lib/citation/grounding.ts          - normalizacja, luki [...], exact -> tolerant
  backend/src/lib/citation/mcp-grounding.ts      - cytaty w blockquote/cudzyslowach, kotwice
  backend/src/lib/citation/heuristicCitations.ts - nieoznaczone odwolania (art., §, sygn.)

Tryby:
  verify_citations.py ODPOWIEDZ.md --source doc-0=umowa.pdf --source doc-1=aneks.docx
      cytaty z bloku <CITATIONS> [{"ref","doc_id","page","quote"}] wg doc_id
  verify_citations.py ODPOWIEDZ.md --tabular --source umowa.pdf
      cytaty [[page:N||quote:...]] z przegladu tabelarycznego
  verify_citations.py ODPOWIEDZ.md --quotes --source wynik_saos.txt --source wynik_isap.txt
      cytaty w blockquote (> ...) i cudzyslowach wzgledem wynikow narzedzi MCP
  verify_citations.py --quote "tekst cytatu" --source plik.txt
      pojedynczy cytat

Statusy: ZWERYFIKOWANY (doslownie), ZMODYFIKOWANY (drobne roznice - sprawdz),
NIEZWERYFIKOWANY (brak trafienia - mozliwa halucynacja), BRAK_ZRODLA.
Kod wyjscia 1, gdy jakikolwiek cytat jest NIEZWERYFIKOWANY lub BRAK_ZRODLA.
Skrypt sprawdza ISTNIENIE tekstu w zrodle, nie to, czy cytat wspiera teze.
"""
import argparse
import json
import re
import subprocess
import sys
import zipfile
from html import unescape
from pathlib import Path

MODIFIED_RATIO_THRESHOLD = 0.15
QUOTE_CHARS = re.compile(r"[„”“»«’‘'`]")
DASHES = re.compile(r"[—–]")
GAP_RE = re.compile(r"\s*(?:\[\s*\.\.\.\s*\]|\.\.\.|…)\s*")

# --- Wczytywanie zrodel -----------------------------------------------------


def load_text(path: str) -> str:
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".pdf" and p.with_suffix(".md").exists():
        # Gotowy OCR obok PDF (umowa.pdf + umowa.md) jest lepszym zrodlem niz pdftotext.
        p, suffix = p.with_suffix(".md"), ".md"
    if suffix in (".md", ".markdown"):
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = re.match(r"\A﻿?---\n.*?\n---\n", text, re.S)
        return text[fm.end():] if fm else text
    if suffix == ".docx":
        with zipfile.ZipFile(p) as z:
            xml = z.read("word/document.xml").decode("utf-8", errors="replace")
        xml = re.sub(r"</w:p>", "\n", xml)
        xml = re.sub(r"<w:tab/>", "\t", xml)
        return unescape(re.sub(r"<[^>]+>", "", xml))
    if suffix == ".pdf":
        try:
            return subprocess.run(["pdftotext", "-layout", str(p), "-"], check=True,
                                  capture_output=True, text=True).stdout
        except FileNotFoundError:
            sys.exit("Brak pdftotext (sudo apt install poppler-utils) - albo podaj tekst .txt")
    return p.read_text(encoding="utf-8", errors="replace")


# --- Algorytm (grounding.ts) ------------------------------------------------


def normalize(s: str) -> str:
    s = re.sub(r"-\s*\n\s*", "", s or "")
    s = QUOTE_CHARS.sub('"', s)
    s = DASHES.sub("-", s)
    return re.sub(r"\s+", " ", s.lower()).strip()


def split_gaps(q: str) -> list:
    return [seg.strip() for seg in GAP_RE.split(q) if seg.strip()]


def edit_distance(a: str, b: str) -> int:
    if abs(len(a) - len(b)) > 40:
        return max(len(a), len(b))
    prev = list(range(len(a) + 1))
    for j in range(1, len(b) + 1):
        cur = [j] + [0] * len(a)
        bj = b[j - 1]
        for i in range(1, len(a) + 1):
            cur[i] = min(prev[i] + 1, cur[i - 1] + 1, prev[i - 1] + (a[i - 1] != bj))
        prev = cur
    return prev[len(a)]


def best_approx(seg: str, src: str) -> tuple:
    """Dopasowanie przyblizone przez kotwice (shingle 3 slow), jak mcp-grounding.ts.
    Brak kotwic = brak trafienia (kierunek bezpieczny)."""
    L = len(seg)
    if L == 0 or len(src) < L:
        return L, -1
    words = seg.split(" ")
    n = 3 if len(words) >= 3 else len(words)
    shingles = []
    for i in range(0, len(words) - n + 1, max(1, (len(words) - n + 1) // 12 or 1)):
        sh = " ".join(words[i:i + n])
        shingles.append((sh, len(" ".join(words[:i])) + (1 if i else 0)))
    candidates = set()
    for sh, off in shingles:
        pos, hits = src.find(sh), 0
        while pos != -1 and hits < 50:
            base = pos - off
            for d in range(-3, 4):
                c = base + d
                if 0 <= c <= len(src) - L:
                    candidates.add(c)
            pos, hits = src.find(sh, pos + 1), hits + 1
    best = (L, -1)
    for c in sorted(candidates):
        dist = edit_distance(seg, src[c:c + L])
        if dist < best[0]:
            best = (dist, c)
            if dist == 0:
                break
    return best


def verify_one(quote: str, source) -> dict:
    if source is None or not normalize(source):
        return {"status": "BRAK_ZRODLA", "ratio": 1.0, "offset": -1, "uwaga": "nie dostarczono tekstu zrodlowego"}
    src = normalize(source)
    segs = split_gaps(normalize(quote.replace("[[PAGE_BREAK]]", " ... ")))
    if not segs:
        return {"status": "BRAK_ZRODLA", "ratio": 1.0, "offset": -1, "uwaga": "pusty cytat"}
    cursor, first, exact = 0, -1, True
    for seg in segs:
        idx = src.find(seg, cursor)
        if idx == -1:
            exact = False
            break
        first = idx if first == -1 else first
        cursor = idx + len(seg)
    if exact:
        return {"status": "ZWERYFIKOWANY", "ratio": 0.0, "offset": first}
    worst, first = 0.0, -1
    for seg in segs:
        dist, at = best_approx(seg, src)
        worst = max(worst, dist / len(seg) if seg else 1.0)
        first = at if first == -1 else first
    if worst <= MODIFIED_RATIO_THRESHOLD:
        return {"status": "ZMODYFIKOWANY", "ratio": round(worst, 3), "offset": first,
                "uwaga": "drobne roznice (interpunkcja/uciecie) - sprawdz oryginal"}
    return {"status": "NIEZWERYFIKOWANY", "ratio": round(worst, 3), "offset": first,
            "uwaga": "brak trafienia - potencjalna halucynacja"}


# --- Wyciaganie cytatow z odpowiedzi ----------------------------------------

CITATIONS_RE = re.compile(r"<CITATIONS>\s*(\[.*?\])\s*(?:</CITATIONS>|$)", re.S)
CITATIONS_BLOCK_RE = re.compile(r"<CITATIONS>[\s\S]*?(?:</CITATIONS>|$)")
TABULAR_RE = re.compile(r"\[\[page:([^|\]]+)\|\|quote:(.+?)\]\]", re.S)
INLINE_RE = re.compile(r"[„\"«]([^„\"”«»\n]{10,}?)[”\"»]")
HEURISTIC = [
    ("sygnatura", re.compile(r"sygn\.\s*(?:akt\s*)?[IVXLCDM]+\s+[A-Z]{1,4}\s+\d+/\d{2,4}", re.I)),
    ("przepis", re.compile(r"art\.\s*\d+[a-z]?(?:\s*ust\.\s*\d+)?", re.I)),
    ("paragraf", re.compile(r"§\s*\d+(?:\s*ust\.\s*\d+)?")),
]


def mcp_quotes(answer: str) -> list:
    text = CITATIONS_BLOCK_RE.sub("", answer)
    out, block = [], []

    def flush():
        joined = " ".join(block).strip().strip("„\"“«‚'").rstrip("”\"“»‘'").strip()
        if len(joined.split()) >= 3:
            out.append({"quote": joined[:600], "rodzaj": "blockquote"})
        block.clear()

    rest = []
    for line in text.splitlines():
        if line.lstrip().startswith(">"):
            content = line.lstrip()[1:].strip()
            if content:
                block.append(content)
            continue
        if block:
            flush()
        rest.append(line)
    if block:
        flush()
    for m in INLINE_RE.finditer("\n".join(rest)):
        q = m.group(1).strip()
        if len(q) >= 25 and len(q.split()) >= 5:
            out.append({"quote": q[:600], "rodzaj": "inline"})
    return out[:40]


def unmarked_refs(answer: str) -> list:
    prose = answer.split("<CITATIONS>")[0]
    found = []
    for kind, rx in HEURISTIC:
        for m in rx.finditer(prose):
            found.append((m.start(), -len(m.group(0)), kind, re.sub(r"\s+", " ", m.group(0))))
    found.sort()
    kept, last = [], -1
    for start, neg, kind, match in found:
        if start >= last:
            kept.append({"odwolanie": match, "rodzaj": kind})
            last = start - neg
    return kept


# --- CLI --------------------------------------------------------------------


def parse_sources(values) -> dict:
    sources = {}
    for v in values or []:
        key, sep, path = v.partition("=")
        if sep and not Path(v).exists():
            sources[key] = load_text(path)
        else:
            sources.setdefault("*", "")
            sources["*"] += "\n" + load_text(v)
    return sources


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("answer", nargs="?", help="plik z odpowiedzia modelu (markdown)")
    ap.add_argument("--source", action="append", help="doc_id=sciezka albo sama sciezka (.txt/.md/.docx/.pdf)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--tabular", action="store_true", help="cytaty [[page:N||quote:...]]")
    mode.add_argument("--quotes", action="store_true", help="blockquote i cudzyslowy wzgledem wynikow MCP")
    mode.add_argument("--quote", help="pojedynczy cytat")
    ap.add_argument("--json", action="store_true", help="wynik jako JSON")
    a = ap.parse_args(argv)

    sources = parse_sources(a.source)
    fallback = sources.get("*")
    results = []

    if a.quote:
        results.append({"cytat": a.quote, **verify_one(a.quote, fallback)})
        refs = []
    else:
        if not a.answer:
            ap.error("podaj plik odpowiedzi albo --quote")
        answer = Path(a.answer).read_text(encoding="utf-8", errors="replace")
        if a.answer.endswith(".jsonl"):
            # Wyniki przegladu tabelarycznego: cytaty siedza w polach summary/reasoning.
            parts = []
            for line in answer.splitlines():
                try:
                    cell = json.loads(line)
                except json.JSONDecodeError:
                    continue
                parts += [str(cell.get("summary", "")), str(cell.get("reasoning", ""))]
            answer = "\n".join(parts)
        refs = unmarked_refs(answer)
        if a.tabular:
            for m in TABULAR_RE.finditer(answer):
                results.append({"strona": m.group(1), "cytat": m.group(2).strip(),
                                **verify_one(m.group(2), fallback)})
        elif a.quotes:
            all_src = "\n".join(sources.values()) if sources else None
            for q in mcp_quotes(answer):
                results.append({"rodzaj": q["rodzaj"], "cytat": q["quote"], **verify_one(q["quote"], all_src)})
        else:
            m = CITATIONS_RE.search(answer)
            entries = json.loads(m.group(1)) if m else []
            for e in entries:
                src = sources.get(str(e.get("doc_id")), fallback)
                results.append({"ref": e.get("ref"), "doc_id": e.get("doc_id"), "strona": e.get("page"),
                                "cytat": e.get("quote", ""), **verify_one(e.get("quote", ""), src)})

    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    blokada = any(r["status"] in ("NIEZWERYFIKOWANY", "BRAK_ZRODLA") for r in results)
    report = {"podsumowanie": counts, "blokada": blokada, "wyniki": results,
              "nieoznaczone_odwolania": refs}

    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for r in results:
            label = r.get("ref") or r.get("rodzaj") or (f"str. {r['strona']}" if r.get("strona") else "-")
            q = r["cytat"].replace("\n", " ")
            print(f"[{label}] {r['status']:<16} ratio={r['ratio']:<5} {q[:90]}{'...' if len(q) > 90 else ''}")
        if not results:
            print("brak cytatow do sprawdzenia")
        print(f"\npodsumowanie: {counts or '-'}; blokada: {'TAK' if blokada else 'nie'}")
        if refs:
            print("\nodwolania bez cytatu w zrodle - [model - zweryfikuj]:")
            for r in refs:
                print(f"  {r['rodzaj']:<9} {r['odwolanie']}")
    return 1 if blokada else 0


if __name__ == "__main__":
    sys.exit(main())
