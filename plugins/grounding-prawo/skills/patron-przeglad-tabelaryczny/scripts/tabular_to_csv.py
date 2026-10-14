#!/usr/bin/env python3
"""Sklada wyniki przegladu tabelarycznego (JSONL) w tabele CSV lub Markdown.

Kazdy plik JSONL = jeden dokument; kazda linia = jedna komorka:
  {"document": "umowa1.pdf", "column_index": 0, "column": "Strony",
   "summary": "...", "flag": "green|grey|yellow|red", "reasoning": "..."}

  tabular_to_csv.py wyniki/*.jsonl -o przeglad.csv
  tabular_to_csv.py wyniki/*.jsonl --markdown -o przeglad.md
  tabular_to_csv.py wyniki/*.jsonl --columns kolumny.json --with-reasoning --plain -o przeglad.csv
--columns: lista {"index", "name"} (np. "kolumny" z szablonu) - ustala kolejnosc.
--plain:   usuwa znaczniki cytatow [[page:N||quote:...]] z komorek.
CSV zapisywany jako UTF-8 z BOM (Excel otwiera polskie znaki poprawnie).
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

CITE_RE = re.compile(r"\s*\[\[page:[^|\]]+\|\|quote:.+?\]\]", re.S)
FLAG_PL = {"green": "zielona", "yellow": "żółta", "red": "czerwona", "grey": "szara"}


def load(files) -> tuple:
    rows, cols = {}, {}
    for f in files:
        for n, line in enumerate(Path(f).read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                c = json.loads(line)
            except json.JSONDecodeError:
                print(f"pominieto {f}:{n} - niepoprawny JSON", file=sys.stderr)
                continue
            doc = c.get("document") or Path(f).stem
            idx = int(c.get("column_index", 0))
            cols.setdefault(idx, c.get("column") or f"Kolumna {idx}")
            rows.setdefault(doc, {})[idx] = c
    return rows, cols


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("-o", "--output", default="-")
    ap.add_argument("--columns", help="JSON z lista kolumn {index, name}")
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--with-reasoning", action="store_true")
    ap.add_argument("--plain", action="store_true", help="usun znaczniki cytatow z komorek")
    a = ap.parse_args(argv)

    rows, cols = load(a.files)
    if a.columns:
        spec = json.loads(Path(a.columns).read_text(encoding="utf-8"))
        spec = spec.get("kolumny", spec) if isinstance(spec, dict) else spec
        cols = {int(c["index"]): c["name"] for c in spec}
    order = sorted(cols)

    header = ["Dokument"]
    for i in order:
        header += [cols[i], f"{cols[i]} [flaga]"] + ([f"{cols[i]} [uzasadnienie]"] if a.with_reasoning else [])
    table = []
    for doc in sorted(rows):
        line = [doc]
        for i in order:
            c = rows[doc].get(i, {})
            val = c.get("summary", "")
            if a.plain:
                val = CITE_RE.sub("", val).strip()
            line += [val, FLAG_PL.get(c.get("flag", ""), c.get("flag", ""))]
            if a.with_reasoning:
                line.append(c.get("reasoning", ""))
        table.append(line)

    out = sys.stdout if a.output == "-" else open(a.output, "w", encoding="utf-8-sig" if not a.markdown else "utf-8", newline="")
    if a.markdown:
        esc = lambda s: str(s).replace("|", "\\|").replace("\n", "<br>")
        out.write("| " + " | ".join(map(esc, header)) + " |\n")
        out.write("|" + "---|" * len(header) + "\n")
        for line in table:
            out.write("| " + " | ".join(map(esc, line)) + " |\n")
    else:
        w = csv.writer(out)
        w.writerow(header)
        w.writerows(table)
    if out is not sys.stdout:
        out.close()
        print(f"{len(table)} dokumentow x {len(order)} kolumn -> {a.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
