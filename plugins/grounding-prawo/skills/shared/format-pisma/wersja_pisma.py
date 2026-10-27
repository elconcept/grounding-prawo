#!/usr/bin/env python3
"""Cykl pisma (shared/ARTEFAKTY-SPRAWY.md): JEDEN plik DOCX bez wersji w legal/output, snapshoty Markdown z wersją w teczce.

    python3 -I wersja_pisma.py start   --docx legal/output/<nazwa>.docx --drafty <sprawa>/drafty/<pismo> [--nazwa <nazwa>]
    python3 -I wersja_pisma.py redline --docx legal/output/<nazwa>.docx (--edits edits.json | --tekst nowa_wersja.md) \
                                       --author "Imię Nazwisko"
    python3 -I wersja_pisma.py nowe    --md <sprawa>/drafty/<pismo>/rrrrMMdd_hhmm_<nazwa>_v1.md --output legal/output
    python3 -I wersja_pisma.py sprawdz --output legal/output [--pismo <nazwa>]

start    - przyjmuje zmiany śledzone W TYM SAMYM pliku (komentarze zostają), ujednolica czcionkę runów i zapis list,
           a stan pisma zapisuje jako snapshot <drafty>/rrrrMMdd_hhmm_<nazwa>_vN.md (N = ostatnia wersja + 1).
redline  - nakłada zmiany sesji na TEN SAM plik jako zmiany śledzone (adeu apply: edits.json albo pełny tekst nowej
           wersji), nadaje wstawkom czcionkę otoczenia, sprawdza w:ins/w:del, puste akapity i pominięte edycje,
           dopiero potem podmienia plik. Nie tworzy nowych plików i niczego nie usuwa.
nowe     - pierwsza wersja pisma: render MD do legal/output/<nazwa>.docx (nazwa bez daty, godziny i _vN).
sprawdz  - bramka katalogu output: brak .md, nazwy DOCX bez daty i _vN, najwyżej jeden DOCX na pismo. Kod 1 = naruszenie.

Silnik: adeu przypięty w `redline-docx-pl`; zmienna ADEU nadpisuje polecenie (np. ADEU=adeu).
"""
import datetime, glob, json, os, re, shlex, shutil, subprocess, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_pismo  # noqa: E402

# rrrrMMdd_ albo rrrrMMdd_hhmm_ na początku, _vN na końcu
STAMP = re.compile(r"^\d{8}_(?:\d{4}_)?")
VER = re.compile(r"_v(\d+)$")
P_RE = r"<w:p[ >](?:(?!</w:p>).)*</w:p>"
R_RE = r"<w:r(?: [^>]*)?>(?:(?!</w:r>).)*</w:r>"


def adeu(*args, check=True):
    cmd = shlex.split(os.environ.get("ADEU", "")) or (
        ["uvx", "-q", "--from", "adeu==1.30.0", "adeu"] if shutil.which("uvx") else ["adeu"])
    r = subprocess.run(cmd + list(args), capture_output=True, text=True)
    if r.returncode and not check:
        return None
    if r.returncode:
        sys.exit(f"adeu {' '.join(args[:1])} nie przeszedł:\n{r.stdout[-2000:]}{r.stderr[-2000:]}")
    return r.stdout


def nazwa(path):
    """Nazwa pisma: bez katalogu, rozszerzenia, prefiksu daty (i godziny) oraz sufiksu _vN."""
    stem = os.path.splitext(os.path.basename(path))[0]
    return VER.sub("", STAMP.sub("", stem))


def text(docx):
    """Pełny tekst DOCX (wszystkie strony adeu), bez nagłówków stron i znaczników zmian."""
    with tempfile.TemporaryDirectory() as t:
        out = os.path.join(t, "x.md")
        adeu("extract", docx, "--page", "all", "--clean-view", "-o", out)
        lines = open(out, encoding="utf-8").read().split("\n")
    s = "\n".join(l for l in lines if not l.startswith("> **")).strip()
    s = re.sub(r"^---\n+", "", s)
    s = re.sub(r"\n+---\n+## Footnotes\n+---\n+## Endnotes\s*$", "", s)
    return s.strip() + "\n"


def xml(docx):
    return zipfile.ZipFile(docx).read("word/document.xml").decode("utf-8")


def changes(docx):
    x = xml(docx)
    return {k: len(re.findall(p, x)) for k, p in (("w:ins", r"<w:ins "), ("w:del", r"<w:del "),
                                                  ("w:delText", r"<w:delText"), ("komentarze", r"<w:commentReference"))}


def rewrite(docx, fn):
    """Podmienia word/document.xml przez fn(xml) w miejscu (przez plik tymczasowy obok)."""
    tmp = docx + ".tmp"
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == "word/document.xml":
                data = fn(data.decode("utf-8")).encode("utf-8")
            zout.writestr(it, data)
    os.replace(tmp, docx)


# ---------- operacje na XML ----------
def accept_xml(x):
    """Przyjęcie zmian śledzonych z zachowaniem komentarzy. Akapit z usuniętym znacznikiem i tekstem -> None."""
    x = re.sub(r"<w:(del|moveFrom) (?:[^>/]|/(?!>))*>.*?</w:\1>", "", x, flags=re.S)
    x = re.sub(r"<w:(ins|moveTo) (?:[^>/]|/(?!>))*>(.*?)</w:\1>", r"\2", x, flags=re.S)
    x = re.sub(r"<w:(ins|moveTo|moveFrom) [^>]*/>", "", x)
    x = re.sub(r"<w:(rPrChange|pPrChange|sectPrChange|tblPrChange|trPrChange|tcPrChange) (?:[^>/]|/(?!>))*>.*?</w:\1>",
               "", x, flags=re.S)
    bad = []

    def mark(m):
        p = m.group(0)
        if not re.search(r"<w:pPr>.*?<w:del [^>]*/>.*?</w:pPr>", p, re.S):
            return p
        if "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)).strip():
            bad.append(p)
            return p
        return ""
    x = re.sub(P_RE, mark, x, flags=re.S)
    return None if bad else x


def unify_fonts(x):
    """Run z tekstem bez w:rFonts dostaje czcionkę i rozmiar z sąsiedniego runu akapitu albo z rPr akapitu
    (wstawka na początku akapitu nie dziedziczy formatowania i spada do domyślnej czcionki dokumentu)."""
    def fix_p(m):
        p = m.group(0)
        runs = list(re.finditer(R_RE, p, flags=re.S))
        ref = None
        for r in runs:
            rp = re.search(r"<w:rPr>(.*?)</w:rPr>", r.group(0), re.S)
            if rp and "<w:rFonts" in rp.group(1) and "CommentReference" not in rp.group(1):
                ref = rp.group(1)
                break
        if ref is None:
            pp = re.search(r"<w:pPr>(?:(?!</w:pPr>).)*?<w:rPr>(.*?)</w:rPr>", p, re.S)
            if pp and "<w:rFonts" in pp.group(1):
                ref = pp.group(1)
        if ref is None:
            return p
        base = "".join(re.findall(r"<w:rFonts[^>]*/>|<w:sz [^>]*/>|<w:szCs [^>]*/>", ref))
        out = []
        for r in runs:
            s = r.group(0)
            if "<w:t" not in s or "CommentReference" in s:
                continue
            rp = re.search(r"<w:rPr>(.*?)</w:rPr>", s, re.S)
            if rp and "<w:rFonts" in rp.group(1):
                continue
            if rp:
                inner = re.sub(r"<w:sz [^>]*/>|<w:szCs [^>]*/>", "", rp.group(1))
                new = s.replace(rp.group(0), "<w:rPr>" + base + inner + "</w:rPr>", 1)
            else:
                new = re.sub(r"^(<w:r(?: [^>]*)?>)", lambda mm: mm.group(1) + "<w:rPr>" + base + "</w:rPr>", s, count=1)
            out.append((r.start(), r.end(), new))
        for a, b, new in reversed(out):
            p = p[:a] + new + p[b:]
        return p
    return re.sub(P_RE, fix_p, x, flags=re.S)


def list_space(x):
    """„N.<tab>tekst” -> „N. tekst”: bez tabulatora i wcięcia wiszącego, numer w rozmiarze tekstu."""
    def fix_p(m):
        p = m.group(0)
        if "</w:pPr>" not in p:
            return p
        head, rest = p.split("</w:pPr>", 1)
        t = "".join(a if a else "\t" for a, _ in re.findall(r"<w:t[^>]*>([^<]*)</w:t>|(<w:tab/>)", rest))
        mm = re.match(r"^\s*(\d+\.|[a-z]\))\s*\t", t)
        if not mm:
            return p
        head = re.sub(r"<w:tabs>.*?</w:tabs>", "", head, flags=re.S)
        head = re.sub(r'\s*w:hanging="\d+"', "", head)
        rest = rest.replace("<w:tab/>", "", 1)
        rest = re.sub(r'<w:t(?: [^>]*)?>' + re.escape(mm.group(1)) + r'\s*</w:t>',
                      f'<w:t xml:space="preserve">{mm.group(1)} </w:t>', rest, count=1)
        rest = re.sub(r'(<w:t xml:space="preserve">' + re.escape(mm.group(1)) + r' </w:t></w:r>)'
                      r'(<w:r(?: [^>]*)?>(?:<w:rPr>(?:(?!</w:rPr>).)*</w:rPr>)?<w:t xml:space="preserve"> </w:t></w:r>)',
                      r"\1", rest, count=1, flags=re.S)

        def num_size(r):
            s = r.group(0)
            if re.search(r"<w:t[^>]*>" + re.escape(mm.group(1)) + r" </w:t>", s):
                s = re.sub(r'<w:sz w:val="\d+"/>|<w:szCs w:val="\d+"/>', "", s)
            return s
        rest = re.sub(R_RE, num_size, rest, count=0, flags=re.S)
        return head + "</w:pPr>" + rest
    return re.sub(P_RE, fix_p, x, flags=re.S)


def empty_paras(x):
    return sum(1 for p in re.findall(P_RE, x, flags=re.S)
               if not "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)).strip())


def lock_of(docx):
    """Plik blokady Worda: „~$” + nazwa bez dwóch pierwszych znaków."""
    d, b = os.path.split(docx)
    lock = os.path.join(d, "~$" + b[2:])
    return [lock] if os.path.exists(lock) else []


def arg(name, required=True):
    a = sys.argv
    if name in a and a.index(name) + 1 < len(a):
        return a[a.index(name) + 1]
    if required:
        sys.exit(f"brak {name}\n\n{__doc__}")
    return None


def guard(docx):
    if nazwa(docx) != os.path.splitext(os.path.basename(docx))[0]:
        sys.exit(f"{docx}: plik pisma w output ma nazwę bez daty i bez _vN (ARTEFAKTY-SPRAWY); zmień nazwę przez mv")
    if lock_of(docx) and "--mimo-blokady" not in sys.argv:
        sys.exit(f"{docx} jest otwarty w Wordzie ({', '.join(map(os.path.basename, lock_of(docx)))}); "
                 "poproś autora o zamknięcie pliku albo użyj --mimo-blokady")


# ---------- polecenia ----------
def start():
    docx, drafty = arg("--docx"), arg("--drafty")
    guard(docx)
    os.makedirs(drafty, exist_ok=True)
    before = changes(docx)
    if before["w:ins"] or before["w:del"]:
        x = accept_xml(xml(docx))
        if x is None:
            tmp = docx + ".acc.docx"
            adeu("accept-all", docx, "-o", tmp)
            os.replace(tmp, docx)
            print("UWAGA: usunięty znacznik akapitu z tekstem - przyjęto przez adeu accept-all (komentarze utracone)")
        else:
            rewrite(docx, lambda _: x)
    rewrite(docx, lambda s: list_space(unify_fonts(s)))
    ver = [int(m.group(1)) for p in glob.glob(os.path.join(drafty, "*.md"))
           if (m := VER.search(os.path.splitext(p)[0]))]
    n = max(ver, default=0) + 1
    nm = arg("--nazwa", required=False)
    if not nm:
        prev = sorted((p for p in glob.glob(os.path.join(drafty, "*_v*.md")) if VER.search(os.path.splitext(p)[0])),
                      key=lambda p: int(VER.search(os.path.splitext(p)[0]).group(1)))
        nm = nazwa(prev[-1]) if prev else nazwa(docx)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    snap = os.path.join(drafty, f"{stamp}_{nm}_v{n}.md")
    open(snap, "w", encoding="utf-8").write(text(docx))
    print(f"przyjęto zmiany w {docx} (w:ins {before['w:ins']}, w:del {before['w:del']}; "
          f"komentarze {changes(docx)['komentarze']}); snapshot: {snap}")


def redline():
    docx = arg("--docx")
    guard(docx)
    author = arg("--author")
    edits, tekst = arg("--edits", required=False), arg("--tekst", required=False)
    if bool(edits) == bool(tekst):
        sys.exit("podaj dokładnie jedno: --edits edits.json albo --tekst nowa_wersja.md")
    if changes(docx)["w:ins"] or changes(docx)["w:del"]:
        sys.exit("plik ma nieprzyjęte zmiany śledzone: najpierw `start`")
    empty0 = empty_paras(xml(docx))
    with tempfile.TemporaryDirectory() as tmp:
        wynik = os.path.join(tmp, "redline.docx")
        log = adeu("apply", docx, edits or tekst, "-o", wynik, "--author", author)
        m = re.search(r"Edits: (\d+) applied, (\d+) skipped", log or "")
        if m and int(m.group(2)):
            sys.exit(f"NIEZAKOŃCZONY: adeu pominął {m.group(2)} edycji (target_text nie pasuje); plik bez zmian\n{log[-1500:]}")
        rewrite(wynik, unify_fonts)
        c = changes(wynik)
        if not (c["w:ins"] or c["w:del"]):
            sys.exit(f"NIEZAKOŃCZONY: wynik bez zmian śledzonych ({c}); plik bez zmian")
        if c["w:del"] and not c["w:delText"]:
            sys.exit(f"NIEZAKOŃCZONY: usunięcia poza w:delText ({c}); plik bez zmian")
        x = accept_xml(xml(wynik))
        if x is not None and empty_paras(x) > empty0:
            sys.exit(f"NIEZAKOŃCZONY: po akceptacji przybyło pustych akapitów ({empty0} -> {empty_paras(x)}); plik bez zmian")
        if tekst:
            acc = os.path.join(tmp, "akcept.docx")
            adeu("accept-all", wynik, "-o", acc)
            if text(acc).split() != open(tekst, encoding="utf-8").read().split():
                sys.exit("NIEZAKOŃCZONY: po akceptacji tekst DOCX różni się od nowej wersji; plik bez zmian")
        shutil.copyfile(wynik, docx + ".tmp")
        os.replace(docx + ".tmp", docx)
    print(f"{docx}: w:ins {c['w:ins']}, w:del {c['w:del']}, komentarze {c['komentarze']}, autor „{author}”")


def nowe():
    md, out = arg("--md"), arg("--output")
    os.makedirs(out, exist_ok=True)
    cel = os.path.join(out, nazwa(md) + ".docx")
    if os.path.exists(cel):
        sys.exit(f"{cel} już istnieje: kolejna wersja to `start` + `redline` na tym pliku")
    with tempfile.TemporaryDirectory() as tmp:
        argv, stdout = sys.argv, sys.stdout
        sys.argv, sys.stdout = ["render_pismo.py", md, "--out", tmp], open(os.devnull, "w")
        try:
            render_pismo.main()
        finally:
            sys.stdout.close()
            sys.argv, sys.stdout = argv, stdout
        shutil.copyfile(os.path.join(tmp, os.path.splitext(os.path.basename(md))[0] + ".docx"), cel)
    print(cel)


def sprawdz():
    out, only = arg("--output"), arg("--pismo", required=False)
    groups, bad = {}, []
    for p in sorted(glob.glob(os.path.join(out, "*"))):
        b = os.path.basename(p)
        ext = os.path.splitext(p)[1].lower()
        if os.path.isdir(p) or b.startswith((".", "~$", "_")):
            continue
        if only and nazwa(p) != only:
            continue
        if ext == ".md":
            bad.append(f"MD w output (miejsce: drafty/<pismo>/ w teczce): {b}")
        elif ext == ".docx":
            if nazwa(p) != os.path.splitext(b)[0]:
                bad.append(f"DOCX z datą lub _vN w nazwie (plik pisma jest bez wersji): {b}")
            groups.setdefault(nazwa(p), []).append(b)
    for k, v in groups.items():
        if len(v) > 1:
            bad.append(f"{len(v)} DOCX pisma „{k}” (dozwolony jeden): {', '.join(v)}")
    print("\n".join(bad) if bad else f"PASS: {sum(map(len, groups.values()))} DOCX, każde pismo raz, bez wersji w nazwie")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    cmds = {"start": start, "redline": redline, "nowe": nowe, "sprawdz": sprawdz}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmds[sys.argv.pop(1)]()
