#!/usr/bin/env python3
"""Martwe odwołania w zbudowanym pluginie: do skilli spoza pluginu i do nieistniejących plików.

Sprawdza plugins/grounding-prawo/skills. Skille odrzucone (selection.yaml: drop) i nazwy
znane z upstreamu, których nie ma w pluginie, są raportowane jako martwe odwołanie.
Użycie: python3 -I scripts/lint_refs.py [--summary]   (kod wyjścia 1 = są martwe odwołania)
"""
import collections, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "plugins/grounding-prawo/skills")
sel = yaml.safe_load(open(os.path.join(ROOT, "selection/selection.yaml"), encoding="utf-8"))
present = {d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d))}
dropped = {d["name"] for d in sel["drop"]} | {"iura", "lexcache", "dr-04", "dr-06", "dr-07", "dr-08", "dr-09", "dr-15"}
OUT_TAG = " (poza pluginem)"
PROVENANCE = re.compile(r"Zast[eę]puje|Pochodzenie|nie ma ju[zż]|©|Źr[oó]d[lł]o:", re.I)
SKILL_RE = re.compile(r"(?<![\w/.-])((?:dr-\d\d(?:-[a-z0-9-]+)?|[a-z0-9]+(?:-[a-z0-9]+)*-(?:pl|v\d+|v\d+-min90))|iura|lexcache|let-it-be)(?![\w-])((?:/[\w./@§-]+)?)(\s*\(poza pluginem\))?")
PATH_RE = re.compile(r"`((?:references|shared|scripts|assets|modules|templates|mcp-servers)/[\w./@-]+\.\w+)`(?! \(brak w pluginie\))")
FENCE = re.compile(r"```.*?```", re.S)
dead_skill, dead_path = collections.defaultdict(list), collections.defaultdict(list)
for skill in sorted(present):
    base = os.path.join(SKILLS, skill)
    for root, _, files in os.walk(base):
        if any(x in root for x in ("node_modules", "/tests", "/benchmark")):
            continue
        for f in files:
            if not f.endswith(".md") or re.search(r"CHANGELOG|AUDIT-JOURNAL|HISTORIA|mapa_dzu|REGRESSION|NOTICE|THIRD_PARTY", f):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, SKILLS)
            text = open(p, encoding="utf-8", errors="replace").read()
            for m in SKILL_RE.finditer(text):
                n = m.group(1)
                ls = text.rfind("\n", 0, m.start()) + 1
                if PROVENANCE.search(text[ls:text.find("\n", m.end()) if text.find("\n", m.end()) >= 0 else len(text)]):
                    continue
                if n in dropped and n not in present and not m.group(3):
                    dead_skill[n].append(rel)
            for m in PATH_RE.finditer(FENCE.sub("", text)):
                t = m.group(1)
                cands = [os.path.join(root, t), os.path.join(base, t), os.path.join(SKILLS, t),
                         os.path.join(SKILLS, "shared", t.split("/", 1)[-1]) if t.startswith("shared/") else ""]
                if not any(c and os.path.exists(c) for c in cands):
                    dead_path[t].append(rel)
total = sum(len(v) for v in dead_skill.values()) + sum(len(v) for v in dead_path.values())
if "--summary" in sys.argv:
    per = collections.Counter(r.split("/")[0] for d in (dead_skill, dead_path) for v in d.values() for r in v)
    print("per skill:", per.most_common(25))
    print("martwe skille:", {k: len(v) for k, v in sorted(dead_skill.items(), key=lambda x: -len(x[1]))})
    print("martwe ścieżki (unikalne):", len(dead_path), "wystąpień:", sum(len(v) for v in dead_path.values()))
else:
    for k, v in sorted(dead_skill.items()):
        print(f"SKILL {k}: " + ", ".join(sorted(set(v))[:6]) + (" ..." if len(set(v)) > 6 else ""))
    for k, v in sorted(dead_path.items()):
        print(f"PLIK  {k}: " + ", ".join(sorted(set(v))[:4]) + (" ..." if len(set(v)) > 4 else ""))
print("PASS: brak martwych odwołań" if not total else f"FAIL: {total} martwych odwołań")
sys.exit(1 if total else 0)
