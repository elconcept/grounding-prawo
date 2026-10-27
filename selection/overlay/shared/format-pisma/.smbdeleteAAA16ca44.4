#!/usr/bin/env python3
"""Cykl wersji pisma: jeden DOCX w legal/output, wersje Markdown w teczce (shared/ARTEFAKTY-SPRAWY.md).

    python3 -I wersja_pisma.py start   --docx legal/output/<plik>.docx --robocze <sprawa>/_robocze [--md <ostatnia>_vN.md]
    python3 -I wersja_pisma.py redline --baza <sprawa>/_robocze/<plik>_baza.docx --md <sprawa>/drafty/<pismo>/<plik>_vN.md \
                                       --output legal/output [--author "Imię Nazwisko"]
    python3 -I wersja_pisma.py nowe    --md <sprawa>/drafty/<pismo>/<plik>_v1.md --output legal/output
    python3 -I wersja_pisma.py sprawdz --output legal/output [--pismo <nazwa>]

start    - przyjmuje wszystkie zmiany śledzone w kopii roboczej (baza sesji), wypisuje jej tekst; z --md pokazuje różnice
           między ostatnią wersją MD a DOCX, czyli ręczne zmiany autora do przeniesienia do nowego snapshotu.
redline  - renderuje nową wersję MD, nakłada jej tekst na bazę jako zmiany śledzone (w:ins/w:del), sprawdza strukturę
           i zgodność po akceptacji, zapisuje <plik>_vN.docx w legal/output i usuwa poprzednie DOCX tego pisma.
nowe     - pierwsza wersja pisma: DOCX bez zmian śledzonych w legal/output (renderer, bez sidecara).
sprawdz  - bramka katalogu output: brak .md, najwyżej jeden DOCX na pismo. Kod wyjścia 1 = naruszenie.

Nazwa pisma to część nazwy pliku między prefiksem daty `rrrrMMdd_` a sufiksem `_vN`. Silnik: adeu (przypięty
w `redline-docx-pl`); zmienna ADEU nadpisuje polecenie (np. ADEU=adeu). Bez zmian śledzonych w wyniku etap jest
NIEZAKOŃCZONY, a poprzedni DOCX zostaje.
"""
import difflib, glob, json, os, re, shlex, shutil, subprocess, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_pismo  # noqa: E402

NAME = re.compile(r"^(?:\d{8}_)?(?P<pismo>.+?)(?:_v(?P<v>\d+))?(?:_\d{8})?$")


def adeu(*args, check=True):
    cmd = shlex.split(os.environ.get("ADEU", "")) or (
        ["uvx", "-q", "--from", "adeu==1.30.0", "adeu"] if shutil.which("uvx") else ["adeu"])
    r = subprocess.run(cmd + list(args), capture_output=True, text=True)
    if r.returncode and not check:
        return None
    if r.returncode:
        sys.exit(f"adeu {' '.join(args[:1])} nie przeszedł:\n{r.stdout[-2000:]}{r.stderr[-2000:]}")
    return r.stdout


def pismo(path):
    return NAME.match(os.path.splitext(os.path.basename(path))[0]).group("pismo")


def text(docx):
    with tempfile.TemporaryDirectory() as t:
        out = os.path.join(t, "x.md")
        adeu("extract", docx, "--page", "all", "-o", out)
        lines = open(out, encoding="utf-8").read().split("\n")
    return "\n".join(l for l in lines if not l.startswith("> **")).strip() + "\n"


def changes(docx):
    x = zipfile.ZipFile(docx).read("word/document.xml").decode("utf-8")
    return {k: len(re.findall(p, x)) for k, p in (("w:ins", r"<w:ins "), ("w:del", r"<w:del "), ("w:delText", r"<w:delText"))}


def plain(t):
    """Tekst bez znaczników wyróżnień (pogrubienie, podkreślenie, kursywa)."""
    return re.sub(r"\*\*|__|(?<![\w*])\*(?=\S)|(?<=\S)\*(?![\w*])", "", t)


def edits(old, new):
    """Zmiany akapitów jako edycje JSON adeu na czystym tekście (zapas, gdy przesunęły się wyróżnienia)."""
    a = [plain(p) for p in old.split("\n\n") if p.strip()]
    b = [plain(p) for p in new.split("\n\n") if p.strip()]
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace" and i2 - i1 == j2 - j1:
            out += [{"type": "modify", "target_text": x, "new_text": y} for x, y in zip(a[i1:i2], b[j1:j2])]
        elif tag in ("replace", "delete"):
            out.append({"type": "modify", "target_text": a[i1], "new_text": "\n\n".join(b[j1:j2])})
            out += [{"type": "modify", "target_text": x, "new_text": ""} for x in a[i1 + 1:i2]]
        elif i1:
            out.append({"type": "modify", "target_text": a[i1 - 1], "new_text": a[i1 - 1] + "\n\n" + "\n\n".join(b[j1:j2])})
        else:
            out.append({"type": "modify", "target_text": a[0], "new_text": "\n\n".join(b[j1:j2]) + "\n\n" + a[0]})
    return out


def render(md, out_dir):
    """Renderuje MD do out_dir (renderer odmawia nadpisania, więc najpierw czyści cel)."""
    target = os.path.join(out_dir, os.path.splitext(os.path.basename(md))[0] + ".docx")
    if os.path.exists(target):
        os.remove(target)
    argv, stdout = sys.argv, sys.stdout
    sys.argv, sys.stdout = ["render_pismo.py", md, "--out", out_dir], open(os.devnull, "w")
    try:
        render_pismo.main()
    finally:
        sys.stdout.close()
        sys.argv, sys.stdout = argv, stdout
    return target


def arg(name, required=True):
    a = sys.argv
    if name in a and a.index(name) + 1 < len(a):
        return a[a.index(name) + 1]
    if required:
        sys.exit(f"brak {name}\n\n{__doc__}")
    return None


def start():
    docx, rob = arg("--docx"), arg("--robocze")
    os.makedirs(rob, exist_ok=True)
    baza = os.path.join(rob, os.path.splitext(os.path.basename(docx))[0] + "_baza.docx")
    before = changes(docx)
    adeu("accept-all", docx, "-o", baza)
    t = text(baza)
    open(baza[:-5] + ".txt", "w", encoding="utf-8").write(t)
    print(f"baza sesji: {baza} (przyjęto zmiany: w:ins {before['w:ins']}, w:del {before['w:del']})")
    md = arg("--md", required=False)
    if md:
        with tempfile.TemporaryDirectory() as tmp:
            prev = text(render(md, tmp))
        diff = list(difflib.unified_diff(prev.split("\n"), t.split("\n"), md, baza, lineterm="", n=1))
        print("różnice ostatniej wersji MD względem DOCX (zmiany autora do snapshotu):" if diff else
              "DOCX odpowiada ostatniej wersji MD: snapshot = kopia tej wersji z kolejnym numerem")
        print("\n".join(diff))


def redline():
    baza, md, out = arg("--baza"), arg("--md"), arg("--output")
    meta, _ = render_pismo.parse(md)
    author = arg("--author", required=False) or meta.get("podpis") or meta.get("nadawca")
    if not author:
        sys.exit("podaj --author (autor zmian śledzonych); nie zostawiaj nazwy konta systemowego")
    with tempfile.TemporaryDirectory() as tmp:
        nowy = text(render(md, tmp))
        txt = os.path.join(tmp, "nowy.md")
        open(txt, "w", encoding="utf-8").write(nowy)
        wynik = os.path.join(tmp, os.path.splitext(os.path.basename(md))[0] + "_redline.docx")
        tryb = "tekst"
        if adeu("apply", baza, txt, "-o", wynik, "--author", author, check=False) is None:
            tryb = "akapity"
            ej = os.path.join(tmp, "edits.json")
            json.dump(edits(text(baza), nowy), open(ej, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            adeu("apply", baza, ej, "-o", wynik, "--author", author)
        c = changes(wynik)
        if not (c["w:ins"] or c["w:del"]):
            sys.exit(f"NIEZAKOŃCZONY: wynik bez zmian śledzonych ({c}); poprzedni DOCX zostaje. "
                     "Jeśli tekst się nie zmienił, nowa wersja nie jest potrzebna.")
        if c["w:del"] and not c["w:delText"]:
            sys.exit(f"NIEZAKOŃCZONY: usunięcia poza w:delText ({c}); poprzedni DOCX zostaje")
        acc = os.path.join(tmp, "akcept.docx")
        adeu("accept-all", wynik, "-o", acc)
        po, cel_txt = text(acc), nowy
        if tryb == "akapity":
            po, cel_txt = plain(po), plain(nowy)
        if po.split() != cel_txt.split():
            sys.exit("NIEZAKOŃCZONY: po akceptacji zmian tekst DOCX różni się od nowej wersji MD; poprzedni DOCX zostaje")
        cel = os.path.join(out, os.path.splitext(os.path.basename(md))[0] + ".docx")
        shutil.copyfile(wynik, cel)
    if changes(cel) != c:
        sys.exit(f"NIEZAKOŃCZONY: kopia {cel} różni się od zweryfikowanego wyniku")
    usun = [p for p in glob.glob(os.path.join(out, "*")) if os.path.abspath(p) != os.path.abspath(cel)
            and pismo(p) == pismo(cel) and os.path.splitext(p)[1].lower() in (".docx", ".md")]
    for p in usun:
        os.remove(p)
    print(f"{cel}: w:ins {c['w:ins']}, w:del {c['w:del']}, autor „{author}”; usunięte poprzednie: "
          + (", ".join(os.path.basename(p) for p in usun) or "brak"))
    if tryb == "akapity":
        print("UWAGA: zmiany naniesione akapitami na czystym tekście; zmiany samych wyróżnień (pogrubienie, "
              "podkreślenie) nie są w DOCX - nanieś je w Wordzie albo zgłoś autorowi.")


def nowe():
    md, out = arg("--md"), arg("--output")
    os.makedirs(out, exist_ok=True)
    cel = os.path.join(out, os.path.splitext(os.path.basename(md))[0] + ".docx")
    inne = [p for p in glob.glob(os.path.join(out, "*.docx")) if pismo(p) == pismo(cel)]
    if inne:
        sys.exit(f"pismo ma już DOCX w output ({', '.join(map(os.path.basename, inne))}): użyj start + redline")
    print(render(md, out))


def sprawdz():
    out, only = arg("--output"), arg("--pismo", required=False)
    groups, bad = {}, []
    for p in sorted(glob.glob(os.path.join(out, "*"))):
        ext = os.path.splitext(p)[1].lower()
        if os.path.isdir(p) or os.path.basename(p).startswith((".", "~$")):
            continue
        if only and pismo(p) != only:
            continue
        if ext == ".md":
            bad.append(f"MD w output (miejsce: drafty/<pismo>/ w teczce): {os.path.basename(p)}")
        elif ext == ".docx":
            groups.setdefault(pismo(p), []).append(os.path.basename(p))
    for k, v in groups.items():
        if len(v) > 1:
            bad.append(f"{len(v)} DOCX pisma „{k}” (dozwolony jeden): {', '.join(v)}")
    print("\n".join(bad) if bad else f"PASS: {sum(map(len, groups.values()))} DOCX, każde pismo raz, bez MD")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    cmds = {"start": start, "redline": redline, "nowe": nowe, "sprawdz": sprawdz}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmds[sys.argv.pop(1)]()
