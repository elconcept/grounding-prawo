#!/usr/bin/env python3
"""Buduje plugins/grounding-prawo/skills z selection/selection.yaml.

Źródła: submoduły vendor/ (przypięte do commita) i own-skills/. Patche z selection/patches/
są nakładane na kopię, nigdy na vendor. Wynik jest generowany - nie edytuj go ręcznie,
zmieniaj selection.yaml, own-skills/ albo patche.
"""
import os, re, shutil, subprocess, sys, json
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEX = os.path.join(ROOT, "vendor/LexMachina/Wersja rozwojowa rozpakowana")
AWE = os.path.join(ROOT, "vendor/awesome-matematic-skills-pl")
PLUGIN = os.path.join(ROOT, "plugins/grounding-prawo")
SKILLS = os.path.join(PLUGIN, "skills")
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "node_modules", ".git", ".DS_Store", "@eaDir")


def source(entry):
    n, f = entry["name"], entry["from"]
    if f == "lex":
        return os.path.join(LEX, n)
    if f.startswith("awe:"):
        return os.path.join(AWE, f[4:], "skills", n)
    if f == "own":
        return os.path.join(ROOT, "own-skills", n)
    if f.startswith("vendor:"):
        return os.path.join(ROOT, "vendor", f[7:])
    raise SystemExit(f"nieznane źródło {f} dla {n}")


def frontmatter(path):
    t = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", t, re.S)
    return (yaml.safe_load(m.group(1)) if m else None), t, m


def main():
    sel = yaml.safe_load(open(os.path.join(ROOT, "selection/selection.yaml"), encoding="utf-8"))
    if os.path.isdir(SKILLS):
        shutil.rmtree(SKILLS)
    os.makedirs(SKILLS)
    for e in sel["keep"]:
        src = source(e)
        if not os.path.isfile(os.path.join(src, "SKILL.md")):
            raise SystemExit(f"brak SKILL.md: {src}")
        shutil.copytree(src, os.path.join(SKILLS, e["name"]), ignore=IGNORE)

    pdir = os.path.join(ROOT, "selection/patches")
    for p in sorted(os.listdir(pdir)) if os.path.isdir(pdir) else []:
        if p.endswith(".patch"):
            r = subprocess.run(["patch", "-p1", "-s", "-d", SKILLS, "-i", os.path.join(pdir, p)],
                               capture_output=True, text=True)
            if r.returncode:
                raise SystemExit(f"patch {p} nie przeszedł:\n{r.stdout}{r.stderr}")
            print("patch", p)

    errors = []
    for e in sel["keep"]:
        sm = os.path.join(SKILLS, e["name"], "SKILL.md")
        fm, t, m = frontmatter(sm)
        if not fm or fm.get("name") != e["name"] or not fm.get("description"):
            errors.append(f"{e['name']}: frontmatter name/description niezgodne (name={fm and fm.get('name')})")
            continue
        if e.get("internal"):
            if "disable-model-invocation" not in fm:
                t = t[: m.end(1)] + "\ndisable-model-invocation: true" + t[m.end(1):]
                open(sm, "w", encoding="utf-8").write(t)
        for dep in ((fm.get("dependencies") or {}).get("requires") or []):
            if not os.path.isdir(os.path.join(SKILLS, dep)):
                errors.append(f"{e['name']}: requires {dep}, którego nie ma w pluginie")

    plugin = {
        "name": "grounding-prawo",
        "description": "Prawo polskie z weryfikacją źródeł: silnik LexMachina (router, DR-01…16), kontrola pism (MateMatic), skille własne do spraw karnych, medycznych i RODO.",
        "version": sel.get("version", "0.1.0"),
        "author": {"name": "elconcept"},
    }
    os.makedirs(os.path.join(PLUGIN, ".claude-plugin"), exist_ok=True)
    json.dump(plugin, open(os.path.join(PLUGIN, ".claude-plugin/plugin.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    # adapter Codex: ten sam katalog pluginu, osobny manifest
    os.makedirs(os.path.join(PLUGIN, ".codex-plugin"), exist_ok=True)
    codex = dict(plugin, skills="./skills/", interface={"displayName": "Grounding Prawo", "category": "Legal"})
    json.dump(codex, open(os.path.join(PLUGIN, ".codex-plugin/plugin.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.makedirs(os.path.join(ROOT, ".agents/plugins"), exist_ok=True)
    json.dump({"name": "grounding-prawo", "interface": {"displayName": "Grounding Prawo"},
               "plugins": [{"name": "grounding-prawo", "source": {"source": "local", "path": "./plugins/grounding-prawo"},
                            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "category": "Legal"}]},
              open(os.path.join(ROOT, ".agents/plugins/marketplace.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"zbudowano {len(sel['keep'])} skilli, błędów: {len(errors)}")
    for x in errors:
        print("  BŁĄD", x)
    sys.exit(1 if errors else 0)


main()
