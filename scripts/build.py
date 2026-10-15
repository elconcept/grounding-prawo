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



# --- czyszczenie: anonimizacja, zakaz chmury, odwołania do skilli spoza pluginu ---------------
LIST_ITEM = re.compile(r"^\s*([-*]|\d+\.)\s")
POLICY = re.compile(r"let-it-be|tajemnica-preflight|(?<!\w)(pseudo)?anonimiz\w*|zero-egress|\bchmur\w*", re.I)
POLICY_DIRECTIVE = re.compile(r"przed|przez|zanim|oczy[sś][cć]|wysy[lł]k|obowi[aą]z|zawsze|zakaz|nie wysy|wymag|pseudonimizuj|anonimizuj|let-it-be|tajemnica-preflight", re.I)
SKIP_PARTS = ("KROK0A-anonimizer.md", "references/SELF-CHECK.md", "CHANGELOG", "/audyt-systemu-v4/", "/benchmark/", "/tests/", "NOTICE", "THIRD_PARTY")


def blocks(lines):
    """Dzieli markdown na bloki: akapit albo pojedyncza pozycja listy/wiersz tabeli."""
    out, cur = [], []
    for ln in lines:
        if not ln.strip():
            if cur: out.append(cur); cur = []
            out.append([ln]); continue
        if cur and (LIST_ITEM.match(ln) or ln.lstrip().startswith("|") or cur[0].lstrip().startswith("|") or ln.startswith("#")):
            out.append(cur); cur = []
        cur.append(ln)
    if cur: out.append(cur)
    return out


def scrub_file(path, removed, stats):
    text = open(path, encoding="utf-8").read()
    fm = re.match(r"---\n.*?\n---\n", text, re.S)
    head, body = (text[: fm.end()], text[fm.end():]) if fm else ("", text)
    if head:  # frontmatter: tylko wycinamy nazwy z list
        for n in ("let-it-be", "tajemnica-preflight-pl") + tuple(removed):
            head = re.sub(r",\s*" + re.escape(n) + r"(?![\w-])|(?<![\w-])" + re.escape(n) + r"\s*,\s*", "", head)
            head = re.sub(r"^\s*-\s*" + re.escape(n) + r"\s*\n", "", head, flags=re.M)
    rm_re = re.compile(r"(?<![\w-])(" + "|".join(re.escape(n) for n in removed) + r")(?![\w-])") if removed else None
    kept = []
    in_code = False
    protected = False  # sekcje dopisane patchami (KONFIGURACJA PLUGINU, WYJĄTEK) nie podlegają czyszczeniu
    for b in blocks(body.split("\n")):
        s = "\n".join(b)
        if b[0].startswith("## "):
            protected = b[0].startswith(("## KONFIGURACJA PLUGINU", "## WYJĄTEK: ZAWIADOMIENIE"))
        if any(l.startswith("```") for l in b):
            in_code = not in_code if sum(l.startswith("```") for l in b) == 1 else in_code
        drop = None
        if not in_code and s.strip() and not protected:
            if POLICY.search(s) and POLICY_DIRECTIVE.search(s) and re.search(r"let-it-be|tajemnica-preflight|pseudonimiz|(?<!\w)anonimiz|chmur", s, re.I):
                drop = "polityka"
            elif rm_re and rm_re.search(s) and (b[0].lstrip().startswith("|") or LIST_ITEM.match(b[0])):
                drop = "odwolanie"
        if drop:
            stats[drop] += 1
        else:
            kept.append(s)
    open(path, "w", encoding="utf-8").write(head + "\n".join(kept))


def scrub(sel, stats):
    removed = [d["name"] for d in sel["drop"]]
    for e in sel["keep"]:
        if e.get("fold_into"):
            continue
        for root, _, fs in os.walk(os.path.join(SKILLS, e["name"])):
            for f in fs:
                p = os.path.join(root, f)
                if f.endswith(".md") and not any(x in p for x in SKIP_PARTS) and not (e["name"] == "profil-postepowan-wlasnych"):
                    scrub_file(p, removed, stats)



def fold(sel):
    """Skille z fold_into trafiają do modułów skilla nadrzędnego (modules/typy/) i do tabeli typów pism."""
    groups = {}
    for e in sel["keep"]:
        if e.get("fold_into"):
            groups.setdefault(e["fold_into"], []).append(e)
    for host, items in groups.items():
        hdir = os.path.join(SKILLS, host)
        tdir = os.path.join(hdir, "modules", "typy")
        os.makedirs(tdir, exist_ok=True)
        rows = []
        for e in items:
            src = os.path.join(SKILLS, e["name"])
            body = re.sub(r"\A---\n.*?\n---\n", "", open(os.path.join(src, "SKILL.md"), encoding="utf-8").read(), flags=re.S)
            open(os.path.join(tdir, e["name"] + ".md"), "w", encoding="utf-8").write(
                f"# Typ pisma: {e['typ']}\n\n> Moduł scalony ze skilla `{e['name']}` (IURA). Stosuj w W1/W2 jako wzorzec struktury i argumentacji dla tego typu pisma; bramki `{host}` obowiązują bez zmian.\n" + body)
            for sub in ("references", "assets", "scripts"):
                if os.path.isdir(os.path.join(src, sub)):
                    shutil.copytree(os.path.join(src, sub), os.path.join(tdir, e["name"] + "-" + sub), dirs_exist_ok=True)
            shutil.rmtree(src)
            rows.append(f"| {e['typ']} | `modules/typy/{e['name']}.md` |")
        sm = os.path.join(hdir, "SKILL.md")
        t = open(sm, encoding="utf-8").read()
        block = "## TYPY PISM - MODUŁY SPECJALISTYCZNE\n\nGdy typ pisma jest znany, wczytaj odpowiedni moduł i użyj go jako wzorca struktury w W1/W2:\n\n| Typ pisma | Moduł |\n|---|---|\n" + "\n".join(rows) + "\n\n"
        marker = "## MODUŁY — MAPA WCZYTYWANIA"
        assert marker in t, "brak markera w " + host
        open(sm, "w", encoding="utf-8").write(t.replace(marker, block + marker, 1))


def normalize_skill(sm, entry):
    """Emit portable skill metadata; preserve upstream annotations as strings."""
    fm, text, match = frontmatter(sm)
    allowed = {"name", "description", "license", "allowed-tools", "metadata"}
    metadata = fm.get("metadata") or {}
    metadata = {k: v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
                for k, v in metadata.items()}
    for key, value in fm.items():
        if key not in allowed and key not in {"disable-model-invocation", "disable_model_invocation"}:
            metadata[key] = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    portable = {k: v for k, v in fm.items() if k in allowed and k != "metadata"}
    if entry.get("description"):
        portable["description"] = entry["description"]
    if metadata:
        portable["metadata"] = metadata
    open(sm, "w", encoding="utf-8").write(
        "---\n" + yaml.safe_dump(portable, allow_unicode=True, sort_keys=False, width=1000)
        + "---\n" + text[match.end():])
    agent = os.path.join(os.path.dirname(sm), "agents/openai.yaml")
    if os.path.isfile(agent):
        data = yaml.safe_load(open(agent, encoding="utf-8"))
        if "policy" in data:
            data["policy"].pop("products", None)
        with open(agent, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=1000)
    # These are manifests of upstream standalone plugins, not components of this plugin.
    for name in (".claude-plugin", ".codex-plugin"):
        shutil.rmtree(os.path.join(os.path.dirname(sm), name), ignore_errors=True)


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

    fold(sel)
    import collections
    stats = collections.Counter()
    scrub(sel, stats)
    print("czyszczenie:", dict(stats))
    errors = []
    for e in [x for x in sel["keep"] if not x.get("fold_into")]:
        sm = os.path.join(SKILLS, e["name"], "SKILL.md")
        fm, t, m = frontmatter(sm)
        if not fm or fm.get("name") != e["name"] or not fm.get("description"):
            errors.append(f"{e['name']}: frontmatter name/description niezgodne (name={fm and fm.get('name')})")
            continue
        for dep in ((fm.get("dependencies") or {}).get("requires") or []):
            if not os.path.isdir(os.path.join(SKILLS, dep)):
                errors.append(f"{e['name']}: requires {dep}, którego nie ma w pluginie")
        normalize_skill(sm, e)

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
    codex = dict(plugin, skills="./skills/", mcpServers="./.mcp.json", interface={
        "displayName": "Grounding Prawo", "category": "Legal",
        "shortDescription": "Prawo polskie: analiza spraw, źródła i kontrola pism",
        "longDescription": plugin["description"], "developerName": "elconcept",
        "defaultPrompt": ["Przeanalizuj moją sprawę prawną i wskaż źródła wymagające weryfikacji."],
        "capabilities": []})
    json.dump(codex, open(os.path.join(PLUGIN, ".codex-plugin/plugin.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.makedirs(os.path.join(ROOT, ".agents/plugins"), exist_ok=True)
    json.dump({"name": "grounding-prawo", "interface": {"displayName": "Grounding Prawo"},
               "plugins": [{"name": "grounding-prawo", "source": {"source": "local", "path": "./plugins/grounding-prawo"},
                            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "category": "Legal"}]},
              open(os.path.join(ROOT, ".agents/plugins/marketplace.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    shutil.copy(os.path.join(ROOT, ".mcp.json"), os.path.join(PLUGIN, ".mcp.json"))  # jedyny konektor: portal MCP
    print(f"zbudowano {sum(not e.get('fold_into') for e in sel['keep'])} skilli, błędów: {len(errors)}")
    for x in errors:
        print("  BŁĄD", x)
    sys.exit(1 if errors else 0)


main()
