#!/usr/bin/env python3
"""Buduje plugins/grounding-prawo/skills z selection/selection.yaml.

Źródła: submoduły vendor/ (przypięte do commita) i own-skills/. Patche z selection/patches/
są nakładane na kopię, nigdy na vendor. Wynik jest generowany - nie edytuj go ręcznie,
zmieniaj selection.yaml, own-skills/ albo patche.
"""
import os, re, shutil, subprocess, sys, json
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEX = os.path.join(ROOT, "vendor/packs/LexMachina/Wersja rozwojowa rozpakowana")
AWE = os.path.join(ROOT, "vendor/packs/awesome-matematic-skills")
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
                if f.endswith(".md") and not any(x in p for x in SKIP_PARTS):
                    scrub_file(p, removed, stats)



# --- odwołania do skilli spoza pluginu: jedna reguła zamiast ręcznych poprawek ---------------
OUT_TAG = " (poza pluginem)"
HISTORY = re.compile(r"CHANGELOG|AUDIT-JOURNAL|HISTORIA|mapa_dzu|REGRESSION|NOTICE|THIRD_PARTY")
PROVENANCE = re.compile(r"Zast[eę]puje|Pochodzenie|nie ma ju[zż]|©|Źr[oó]d[lł]o:", re.I)


def out_of_plugin_re(sel):
    """Nazwy odrzuconych skilli (i skróty dr-NN), których nie ma w pluginie."""
    names = {d["name"] for d in sel["drop"]}
    names |= {n.split("-")[0] + "-" + n.split("-")[1] for n in names if re.match(r"dr-\d\d-", n)}
    names |= {"iura", "lexcache"}
    names -= {e["name"] for e in sel["keep"]}
    alt = "|".join(sorted(map(re.escape, names), key=len, reverse=True))
    return re.compile(r"(?<![\w/.-])(" + alt + r")(?![\w-])((?:/[\w./@§-]+)?)(?!" + re.escape(OUT_TAG) + ")")


def tag_out_of_plugin(sel):
    """Dopisuje '(poza pluginem)' do odwołań do skilli, których plugin nie zawiera - model widzi, że nie może ich użyć."""
    rx, n = out_of_plugin_re(sel), 0
    for e in sel["keep"]:
        if e.get("fold_into"):
            continue
        for root, _, fs in os.walk(os.path.join(SKILLS, e["name"])):
            for f in fs:
                p = os.path.join(root, f)
                if not f.endswith(".md") or HISTORY.search(p):
                    continue
                out, changed = [], False
                for ln in open(p, encoding="utf-8").read().split("\n"):
                    if not PROVENANCE.search(ln) and rx.search(ln):
                        ln, k = rx.subn(lambda m: m.group(0) + OUT_TAG, ln)
                        n += k; changed = True
                    out.append(ln)
                if changed:
                    open(p, "w", encoding="utf-8").write("\n".join(out))
    return n


PATH_REF = re.compile(r"`((?:references|modules|scripts|assets|workflows|shared)/[\w./@§-]+\.\w+)`(?! \(brak w pluginie\))")
MISSING_TAG = " (brak w pluginie)"


def qualify_paths(sel):
    """Ścieżka bez nazwy skilla, której nie ma w skillu bieżącym: jeśli istnieje w dokładnie jednym innym - dopisz nazwę skilla;
    jeśli nigdzie - oznacz jawnie, że pliku nie ma w pluginie."""
    names = [d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d))]
    fixed = missing = 0
    for e in sel["keep"]:
        if e.get("fold_into"):
            continue
        base = os.path.join(SKILLS, e["name"])
        for root, _, fs in os.walk(base):
            for f in fs:
                p = os.path.join(root, f)
                if not f.endswith(".md") or HISTORY.search(p):
                    continue
                text = open(p, encoding="utf-8").read()

                def fix(m):
                    nonlocal fixed, missing
                    rel = m.group(1)
                    if rel.startswith("shared/"):
                        cands = [os.path.join(SKILLS, rel)]
                        ok = os.path.exists(cands[0])
                    else:
                        ok = os.path.exists(os.path.join(root, rel)) or os.path.exists(os.path.join(base, rel)) or os.path.exists(os.path.join(SKILLS, rel))
                    if ok:
                        return m.group(0)
                    owners = [n for n in names if os.path.exists(os.path.join(SKILLS, n, rel))]
                    if len(owners) == 1:
                        fixed += 1
                        return f"`{owners[0]}/{rel}`"
                    missing += 1
                    return m.group(0) + MISSING_TAG

                new = PATH_REF.sub(fix, text)
                if new != text:
                    open(p, "w", encoding="utf-8").write(new)
    return fixed, missing


def add_bridges(sel):
    """Dopisuje do każdego skilla sekcję MOST z selection/bridges.yaml: skąd wejście, gdzie wynik, co dalej."""
    bridges = yaml.safe_load(open(os.path.join(ROOT, "selection/bridges.yaml"), encoding="utf-8"))
    keep = {e["name"] for e in sel["keep"] if not e.get("fold_into")}
    errors = []
    for name in sorted(keep):
        if name in ("shared", "audyt-systemu-v4"):
            continue
        b = bridges["skills"].get(name) or (bridges["default_dr"] if name.startswith("dr-") else None)
        if not b:
            errors.append(f"bridges.yaml: brak mostu dla {name}")
            continue
        for d in b.get("dalej", []):
            if d not in keep:
                errors.append(f"bridges.yaml: {name} -> {d} (brak skilla w pluginie)")
        lines = ["", "", "## MOST - miejsce w przepływie grounding-prawo", "",
                 f"- **Wejście z:** {b['wejscie']}",
                 f"- **Wynik zapisz w:** {b['wynik']} (reguła: `shared/ARTEFAKTY-SPRAWY.md` - dopisuj do istniejących plików, nie twórz nowych raportów)",
                 "- **Następny krok:** " + ", ".join(f"`{d}`" for d in b.get("dalej", []))]
        if b.get("nie_dubluj"):
            lines.append(f"- **Nie dubluj:** {b['nie_dubluj']}")
        wiki = b.get("wiki") or bridges["wiki_etap"][b["etap"]]
        lines.append(f"- **Basic Memory (`legal`):** {wiki} (protokół: `shared/BASIC-MEMORY.md`)")
        lines.append("- **Mapa ścieżek:** `shared/SCIEZKI-PRACY.md` (router).")
        sm = os.path.join(SKILLS, name, "SKILL.md")
        text = open(sm, encoding="utf-8").read().rstrip("\n")
        open(sm, "w", encoding="utf-8").write(text + "\n".join(lines) + "\n")
    return errors


def fold(sel):
    """Skille z fold_into trafiają do modułów skilla nadrzędnego (modules/typy/) i do tabeli typów pism."""
    groups = {}
    for e in sel["keep"]:
        if e.get("fold_into"):
            groups.setdefault(e["fold_into"], []).append(e)
    for host, items in groups.items():
        hdir = os.path.join(SKILLS, host)
        tdir = os.path.join(hdir, "modules", "typy")
        rdir = os.path.join(hdir, "references")
        rows, refs = [], []
        for e in items:
            src = os.path.join(SKILLS, e["name"])
            body = re.sub(r"\A---\n.*?\n---\n", "", open(os.path.join(src, "SKILL.md"), encoding="utf-8").read(), flags=re.S)
            is_ref = e.get("as") == "reference"
            outdir = rdir if is_ref else tdir
            os.makedirs(outdir, exist_ok=True)
            # zasoby skilla leżą po scaleniu w <katalog>/<nazwa>-references itd.; ścieżki w treści muszą to odzwierciedlać
            body = re.sub(r"(?<![\w/.-])(references|assets|scripts)/", lambda m: f"{e['name']}-{m.group(1)}/", body)
            kind = "Referencja" if is_ref else "Typ pisma"
            hint = ("Czytaj jako metodykę uzupełniającą skilla `" + host + "`.") if is_ref else \
                f"Stosuj w W1/W2 jako wzorzec struktury i argumentacji dla tego typu pisma; bramki `{host}` obowiązują bez zmian."
            open(os.path.join(outdir, e["name"] + ".md"), "w", encoding="utf-8").write(
                f"# {kind}: {e['typ']}\n\n> Moduł scalony ze skilla `{e['name']}` (IURA). {hint}\n" + body)
            for sub in ("references", "assets", "scripts"):
                if os.path.isdir(os.path.join(src, sub)):
                    shutil.copytree(os.path.join(src, sub), os.path.join(outdir, e["name"] + "-" + sub), dirs_exist_ok=True)
            shutil.rmtree(src)
            (refs if is_ref else rows).append(
                f"| {e['typ']} | `{'references' if is_ref else 'modules/typy'}/{e['name']}.md` |")
        sm = os.path.join(hdir, "SKILL.md")
        t = open(sm, encoding="utf-8").read()
        if rows:
            block = "## TYPY PISM - MODUŁY SPECJALISTYCZNE\n\nGdy typ pisma jest znany, wczytaj odpowiedni moduł i użyj go jako wzorca struktury w W1/W2:\n\n| Typ pisma | Moduł |\n|---|---|\n" + "\n".join(rows) + "\n\n"
            marker = "## MODUŁY — MAPA WCZYTYWANIA"
            assert marker in t, "brak markera w " + host
            t = t.replace(marker, block + marker, 1)
        if refs:
            t = t.rstrip("\n") + "\n\n## REFERENCJE DOŁĄCZONE (IURA)\n\n| Temat | Plik |\n|---|---|\n" + "\n".join(refs) + "\n"
        open(sm, "w", encoding="utf-8").write(t)


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
    if entry.get("description_append"):  # dopisek do opisu upstreamu, bez utraty jego fraz wyzwalających
        portable["description"] = " ".join(str(portable["description"]).split()) + " " + entry["description_append"]
    if len(portable["description"]) > 1024:
        raise SystemExit(f"{entry['name']}: description ma {len(portable['description'])} znaków (limit 1024)")
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



# A single document skill owns OCR tools and the reusable contract library.
def bundle_documents():
    base = os.path.join(SKILLS, "odczyt-dokumentow")
    # the-ocr comes from its own repo (submodule, private): code and docs only - never .env/.secrets,
    # because this plugin is published from a public repository.
    the_ocr, tool = os.path.join(ROOT, "vendor/docs/the-ocr"), os.path.join(base, "tools/the-ocr")
    shutil.copytree(os.path.join(the_ocr, "src"), os.path.join(tool, "src"), ignore=IGNORE)
    for name in ("pyproject.toml", "README.md", "env.example"):
        shutil.copy(os.path.join(the_ocr, name), tool)
    upstream = os.path.join(AWE, "dokumenty/skills/doc-intel-contract-pl")
    target = os.path.join(base, "document_contract")
    os.makedirs(os.path.join(target, "scripts"), exist_ok=True)
    shutil.copytree(os.path.join(upstream, "contract"), os.path.join(target, "contract"))
    for name in ("contract.py", "evidence.py", "grounding_bridge.py", "split_packet.py"):
        shutil.copy(os.path.join(upstream, "scripts", name), os.path.join(target, "scripts", name))
    for name in ("LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md"):
        if os.path.isfile(os.path.join(upstream, name)):
            shutil.copy(os.path.join(upstream, name), target)
    schema_path = os.path.join(target, "contract/contract.schema.json")
    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)
    schema["properties"]["source"]["properties"]["engine"]["enum"] = [
        "datalab", "llamaparse", "azure", "google_vision", "rapidocr", "azure-di", "google-vision",
        "pymupdf", "markitdown", "text"]
    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)
        f.write("\n")


def migrate_document_references():
    for root, _, files in os.walk(SKILLS):
        for name in files:
            if not name.endswith((".md", ".mjs", ".json", ".yaml")):
                continue
            path = os.path.join(root, name)
            # Do not rewrite tool identity or contract implementation provenance.
            if "/odczyt-dokumentow/tools/" in path or "/document_contract/" in path:
                continue
            text = open(path, encoding="utf-8").read()
            text = text.replace('"doc-intel-contract-pl", "contract"', '"odczyt-dokumentow", "document_contract", "contract"')
            text = text.replace("doc-intel-contract-pl/", "odczyt-dokumentow/document_contract/")
            for old, new in (("doc-intel-contract-pl", "odczyt-dokumentow"),
                             ("akta-przeszukiwalne-pl", "odczyt-dokumentow"),
                             ("the-ocr", "odczyt-dokumentow"),
                             ("prowadnik-grounding-prawo", "prawny-router-v3")):
                # New skill legitimately names its internal OCR tool.
                if old == "the-ocr" and "/odczyt-dokumentow/" in path:
                    continue
                text = text.replace(old, new)
            open(path, "w", encoding="utf-8").write(text)


def add_session_protocol():
    for name in os.listdir(SKILLS):
        path = os.path.join(SKILLS, name, "SKILL.md")
        if not os.path.isfile(path) or name in ("shared", "audyt-systemu-v4"):
            continue
        text = open(path, encoding="utf-8").read()
        fm = re.match(r"---\n.*?\n---\n", text, re.S)
        directive = ("\n## Pamięć sesji — przed pracą i przed odpowiedzią końcową\n\n"
            "Przeczytaj `shared/BASIC-MEMORY.md` i `shared/ZASADY-PLUGINU.md`. "
            "Na wejściu odczytaj kontekst sprawy z projektu `legal`; przed odpowiedzią końcową "
            "zapisz lub zaktualizuj recap tej sesji w projekcie `main` i sprawdź odczytem zapis. "
            "Nowe dokumenty i ustalenia zapisuj w `legal` po każdym zakończonym etapie. "
            "Podaj status pamięci i identyfikator notatki; nie zgłaszaj zapisu bez potwierdzenia MCP.\n")
        if name == "prawny-router-v3":
            directive += "\nNajpierw wybierz cel według `shared/SCIEZKI-PRACY.md`; to jedyny punkt wejścia pluginu.\n"
        open(path, "w", encoding="utf-8").write(text[:fm.end()] + directive + text[fm.end():])



def generate_skill_index(sel):
    """Generate the canonical, human-usable skill inventory from selection."""
    out = [
        "# Indeks kanonicznych skilli grounding-prawo",
        "",
        "Plik generowany automatycznie przez \`scripts/build.py\` z \`selection/selection.yaml\`.",
        "Nie edytuj go ręcznie. \`why\` to krótkie uzasadnienie/charakterystyka wyboru.",
        "",
        "| Skill | Rola / krótki opis | Źródło | Tryb |",
        "|---|---|---|---|",
    ]
    count = 0
    folded = []
    for entry in sel["keep"]:
        name = entry["name"]
        if entry.get("fold_into"):
            folded.append(entry)
            continue
        path = os.path.join(SKILLS, name, "SKILL.md")
        fm, _, _ = frontmatter(path)
        description = (entry.get("why") or (fm or {}).get("description") or "brak opisu").strip()
        description = re.sub(r"\\s+", " ", description).replace("|", "\\|")
        desc_limit = 190
        if len(description) > desc_limit:
            description = description[:desc_limit].rsplit(" ", 1)[0] + "…"
        role = "wewnętrzny" if entry.get("internal") else "wywoływany"
        out.append(
            f"| [\\`{name}\\`](../{name}/SKILL.md) | {description} | "
            f"\\`{entry['from']}\\` | {role} |"
        )
        count += 1
    out.insert(5, f"**Skille dostępne:** {count}. Dołączone typy i moduły: {len(folded)}.\\n")
    if folded:
        out.extend(["", "## Moduły włączone do innych skilli", "", "| Moduł | Skill nadrzędny | Opis |", "|---|---|---|"])
        for e in folded:
            why = str(e.get("why") or e.get("typ") or "").replace("|", "\\|")
            out.append(f"| \`{e['name']}\` | \`{e['fold_into']}\` | {why} |")
    path = os.path.join(SKILLS, "shared", "INDEKS-SKILLI.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write("\\n".join(out).replace("\\\`", "`") + "\\n")



def main():
    sel = yaml.safe_load(open(os.path.join(ROOT, "selection/selection.yaml"), encoding="utf-8"))
    missing = [source(e) for e in sel["keep"] if not os.path.isfile(os.path.join(source(e), "SKILL.md"))]
    if missing:
        raise SystemExit("Brak źródeł (istniejący plugin zachowany): " + ", ".join(missing))
    if os.path.isdir(SKILLS):
        shutil.rmtree(SKILLS)
    os.makedirs(SKILLS)
    for e in sel["keep"]:
        src = source(e)
        if not os.path.isfile(os.path.join(src, "SKILL.md")):
            raise SystemExit(f"brak SKILL.md: {src}")
        shutil.copytree(src, os.path.join(SKILLS, e["name"]), ignore=IGNORE)

    overlay = os.path.join(ROOT, "selection/overlay")  # pliki dopisane do pluginu (np. shared/ARTEFAKTY-SPRAWY.md)
    if os.path.isdir(overlay):
        shutil.copytree(overlay, SKILLS, dirs_exist_ok=True)

    pdir = os.path.join(ROOT, "selection/patches")
    for p in sorted(os.listdir(pdir)) if os.path.isdir(pdir) else []:
        if p.endswith(".patch"):
            # -E: plik usunięty patchem znika także w BSD patch (macOS zostawia pusty plik)
            r = subprocess.run(["patch", "-p1", "-s", "-E", "-d", SKILLS, "-i", os.path.join(pdir, p)],
                               capture_output=True, text=True)
            if r.returncode:
                raise SystemExit(f"patch {p} nie przeszedł:\n{r.stdout}{r.stderr}")
            print("patch", p)

    fold(sel)
    bundle_documents()
    migrate_document_references()
    import collections
    stats = collections.Counter()
    scrub(sel, stats)
    print("czyszczenie:", dict(stats))
    print("odwołania poza pluginem oznaczone:", tag_out_of_plugin(sel))
    print("ścieżki zakwalifikowane / brakujące oznaczone:", qualify_paths(sel))
    errors = add_bridges(sel)
    add_session_protocol()
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

    generate_skill_index(sel)

    plugin = {
        "name": "grounding-prawo",
        "description": "Prawo polskie z weryfikacją źródeł: silnik LexMachina (router, DR-01…16), kontrola pism (MateMatic), skille własne do spraw karnych, medycznych i RODO.",
        "author": {"name": "elconcept"},
    }
    os.makedirs(os.path.join(PLUGIN, ".claude-plugin"), exist_ok=True)
    json.dump(plugin, open(os.path.join(PLUGIN, ".claude-plugin/plugin.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    # adapter Codex: ten sam katalog pluginu, osobny manifest
    os.makedirs(os.path.join(PLUGIN, ".codex-plugin"), exist_ok=True)
    # Claude Code bez pola version używa SHA commita, więc każda zmiana na main dociera do klientów;
    # przypięte "version" blokowało aktualizacje (cache kluczowany wersją).
    codex = dict(plugin, version=sel.get("version", "0.1.0"), skills="./skills/", mcpServers="./.mcp.json", interface={
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


if __name__ == "__main__":
    main()
