#!/usr/bin/env python3
"""Cykl pisma (shared/ARTEFAKTY-SPRAWY.md): folder pisma legal/output/<nazwa>/ z kolejnymi wersjami DOCX
<nazwa>_v1.docx, <nazwa>_v2.docx, ... Bez zmian śledzonych: każda zmiana pisma to nowy plik z wyższym _vN.

    python3 -I wersja_pisma.py nowe      --md <sprawa>/drafty/<pismo>/rrrrMMdd_hhmm_<nazwa>_v1.md --output legal/output
    python3 -I wersja_pisma.py nastepna  --pismo legal/output/<nazwa> [--drafty <sprawa>/drafty/<pismo>]
    python3 -I wersja_pisma.py zmien     --docx legal/output/<nazwa>/<nazwa>_vN.docx (--edits edits.json | --tekst nowa.md)
    python3 -I wersja_pisma.py akceptuj  --docx <plik.docx>
    python3 -I wersja_pisma.py najnowsza --pismo legal/output/<nazwa>
    python3 -I wersja_pisma.py sprawdz   --output legal/output [--pismo <nazwa>]

nowe      - pierwsza wersja pisma: render MD do legal/output/<nazwa>/<nazwa>_v1.docx.
nastepna  - kopia najnowszej wersji jako <nazwa>_v(N+1).docx: przyjmuje w kopii zmiany śledzone (komentarze zostają),
            ujednolica czcionkę runów i zapis list; poprzednie wersje zostają bez zmian. Opcjonalnie snapshot MD.
            Kopia zachowuje ręczne zmiany autora w Wordzie; nie renderuj kolejnej wersji od nowa z MD.
zmien     - nakłada zmiany sesji (adeu apply: edits.json albo pełny tekst nowej wersji) na NAJNOWSZĄ wersję i od razu
            je przyjmuje: wynik bez zmian śledzonych. Sprawdza pominięte edycje, puste akapity i (przy --tekst) tekst.
akceptuj  - przyjmuje zmiany śledzone w pliku (porządki starych redline'ów), komentarze zostają.
najnowsza - wypisuje ścieżkę najnowszej wersji pisma.
sprawdz   - bramka katalogu output: nic luzem w korzeniu, w folderze pisma DOCX <nazwa>_vN.docx, bez .md (poza _*.md),
            najnowsza wersja bez zmian śledzonych, załączniki z _ZALACZNIKI.md obecne w folderze (załącznik DOCX dozwolony,
            gdy jest w spisie). Kod 1 = naruszenie.

Silnik: adeu przypięty w `redline-docx-pl`; zmienna ADEU nadpisuje polecenie (np. ADEU=adeu).
"""
import datetime, glob, os, re, shlex, shutil, subprocess, sys, tempfile, unicodedata, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# rrrrMMdd_ albo rrrrMMdd_hhmm_ na początku, _vN na końcu
STAMP = re.compile(r"^\d{8}_(?:\d{4}_)?")
VER = re.compile(r"_v(\d+)$")
P_RE = r"<w:p[ >](?:(?!</w:p>).)*</w:p>"
R_RE = r"<w:r(?: [^>]*)?>(?:(?!</w:r>).)*</w:r>"
POMIJANE = ("_", ".")  # katalogi i pliki pomocnicze w output/


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


def wersja(path):
    m = VER.search(os.path.splitext(os.path.basename(path))[0])
    return int(m.group(1)) if m else 0


def wersje(folder):
    """Wersje DOCX pisma w folderze: [(N, ścieżka)] rosnąco; plik bez _vN (stary układ) ma N = 0."""
    nm = os.path.basename(os.path.normpath(folder))
    out = []
    for p in glob.glob(os.path.join(folder, "*.docx")):
        b = os.path.basename(p)
        if b.startswith(("~$", ".")):
            continue
        stem = os.path.splitext(b)[0]
        if stem == nm or (VER.search(stem) and VER.sub("", stem) == nm):
            out.append((wersja(p), p))
    return sorted(out)


def najnowsza_wersja(folder):
    w = wersje(folder)
    return w[-1][1] if w else None


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
    return {k: len(re.findall(p, x)) for k, p in (
        ("w:ins", r"<w:ins "), ("w:del", r"<w:del "), ("w:delText", r"<w:delText"),
        ("formatowanie", r"<w:(?:rPr|pPr|sectPr|tblPr|trPr|tcPr)Change "), ("komentarze", r"<w:commentReference"))}


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
    x = re.sub(r"<w:(moveFromRangeStart|moveFromRangeEnd|moveToRangeStart|moveToRangeEnd) [^>]*/>", "", x)
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


def accept_file(docx):
    """Przyjmuje zmiany śledzone w pliku; zwraca liczniki sprzed przyjęcia."""
    before = changes(docx)
    if before["w:ins"] or before["w:del"] or before["formatowanie"]:
        x = accept_xml(xml(docx))
        if x is None:
            tmp = docx + ".acc.docx"
            adeu("accept-all", docx, "-o", tmp)
            os.replace(tmp, docx)
            print("UWAGA: usunięty znacznik akapitu z tekstem - przyjęto przez adeu accept-all (komentarze utracone)")
        else:
            rewrite(docx, lambda _: x)
    return before


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


def guard_latest(docx):
    folder = os.path.dirname(os.path.abspath(docx))
    if os.path.basename(folder) != nazwa(docx):
        sys.exit(f"{docx}: pismo leży w legal/output/<nazwa>/<nazwa>_vN.docx (ARTEFAKTY-SPRAWY)")
    last = najnowsza_wersja(folder)
    if os.path.abspath(last) != os.path.abspath(docx):
        sys.exit(f"{docx}: to nie jest najnowsza wersja ({os.path.basename(last)}); zmiany wchodzą tylko do najnowszej")
    if lock_of(docx) and "--mimo-blokady" not in sys.argv:
        sys.exit(f"{docx} jest otwarty w Wordzie; poproś autora o zamknięcie pliku albo użyj --mimo-blokady")


# ---------- polecenia ----------
def nowe():
    import render_pismo  # noqa: E402
    md, out = arg("--md"), arg("--output")
    nm = nazwa(md)
    folder = os.path.join(out, nm)
    if wersje(folder):
        sys.exit(f"{folder} ma już wersje pisma: kolejna wersja to `nastepna` (+ `zmien`)")
    os.makedirs(folder, exist_ok=True)
    cel = os.path.join(folder, f"{nm}_v1.docx")
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


def nastepna():
    folder = arg("--pismo").rstrip("/")
    w = wersje(folder)
    if not w:
        sys.exit(f"{folder}: brak wersji pisma (<nazwa>_vN.docx)")
    src = w[-1][1]
    if lock_of(src) and "--mimo-blokady" not in sys.argv:
        sys.exit(f"{src} jest otwarty w Wordzie; poproś autora o zamknięcie pliku albo użyj --mimo-blokady")
    nm = os.path.basename(folder)
    n = max(w[-1][0], 0) + 1
    cel = os.path.join(folder, f"{nm}_v{n}.docx")
    shutil.copyfile(src, cel)
    before = accept_file(cel)
    rewrite(cel, lambda s: list_space(unify_fonts(s)))
    drafty = arg("--drafty", required=False)
    snap = ""
    if drafty:
        os.makedirs(drafty, exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        snap = os.path.join(drafty, f"{stamp}_{nm}_v{n}.md")
        open(snap, "w", encoding="utf-8").write(text(cel))
    print(f"{cel} (z {os.path.basename(src)}; przyjęto w:ins {before['w:ins']}, w:del {before['w:del']}, "
          f"formatowanie {before['formatowanie']}; komentarze {changes(cel)['komentarze']})" + (f"; snapshot: {snap}" if snap else ""))


def zmien():
    docx = arg("--docx")
    guard_latest(docx)
    edits, tekst = arg("--edits", required=False), arg("--tekst", required=False)
    if bool(edits) == bool(tekst):
        sys.exit("podaj dokładnie jedno: --edits edits.json albo --tekst nowa_wersja.md")
    if changes(docx)["w:ins"] or changes(docx)["w:del"]:
        sys.exit("plik ma nieprzyjęte zmiany śledzone: utwórz wersję przez `nastepna`")
    if wersja(docx) <= 1 and len(wersje(os.path.dirname(os.path.abspath(docx)))) <= 1 and "--v1" not in sys.argv:
        sys.exit("zmiany wchodzą do nowej wersji: najpierw `nastepna` (świadoma poprawka v1: --v1)")
    empty0 = empty_paras(xml(docx))
    with tempfile.TemporaryDirectory() as tmp:
        wynik = os.path.join(tmp, "wynik.docx")
        log = adeu("apply", docx, edits or tekst, "-o", wynik, "--author", "wersja_pisma")
        m = re.search(r"Edits: (\d+) applied, (\d+) skipped", log or "")
        if m and int(m.group(2)):
            sys.exit(f"NIEZAKOŃCZONY: adeu pominął {m.group(2)} edycji (target_text nie pasuje); plik bez zmian\n{log[-1500:]}")
        rewrite(wynik, unify_fonts)
        c = changes(wynik)
        if not (c["w:ins"] or c["w:del"]):
            sys.exit(f"NIEZAKOŃCZONY: brak zmian do naniesienia ({c}); plik bez zmian")
        accept_file(wynik)
        x = xml(wynik)
        if empty_paras(x) > empty0:
            sys.exit(f"NIEZAKOŃCZONY: przybyło pustych akapitów ({empty0} -> {empty_paras(x)}); plik bez zmian")
        if tekst and text(wynik).split() != open(tekst, encoding="utf-8").read().split():
            sys.exit("NIEZAKOŃCZONY: tekst DOCX różni się od nowej wersji; plik bez zmian")
        shutil.copyfile(wynik, docx + ".tmp")
        os.replace(docx + ".tmp", docx)
    print(f"{docx}: naniesiono i przyjęto w:ins {c['w:ins']}, w:del {c['w:del']}; plik bez zmian śledzonych")


def akceptuj():
    docx = arg("--docx")
    before = accept_file(docx)
    print(f"{docx}: przyjęto w:ins {before['w:ins']}, w:del {before['w:del']}, formatowanie {before['formatowanie']}; "
          f"komentarze {changes(docx)['komentarze']}")


def najnowsza():
    p = najnowsza_wersja(arg("--pismo").rstrip("/"))
    if not p:
        sys.exit("brak wersji pisma")
    print(p)


def zalaczniki(folder, wymienione=None):
    """Pliki wskazane w _ZALACZNIKI.md (`nazwa` w backtickach przed „(źródło”) i ich obecność w folderze."""
    p = os.path.join(folder, "_ZALACZNIKI.md")
    if not os.path.exists(p):
        return None, []
    braki = []
    if wymienione is not None:
        for line in open(p, encoding="utf-8"):
            m = re.match(r"\s*\d+\.\s.*?—\s*`([^`]+)`", line)
            if m:
                wymienione.add(unicodedata.normalize("NFC", m.group(1)))
    obecne = {unicodedata.normalize("NFC", f) for f in os.listdir(folder)}
    for line in open(p, encoding="utf-8"):
        m = re.match(r"\s*\d+\.\s.*?—\s*`([^`]+)`", line)
        if m and unicodedata.normalize("NFC", m.group(1)) not in obecne:
            braki.append(m.group(1))
        elif re.search(r"BRAK W UDZIALE|NIE ZNALEZIONO", line):
            braki.append(line.strip())
    return True, braki


def sprawdz():
    out, only = arg("--output"), arg("--pismo", required=False)
    bad, n = [], 0
    for p in sorted(glob.glob(os.path.join(out, "*"))):
        b = os.path.basename(p)
        if b.startswith(POMIJANE) or b.startswith("~$"):
            continue
        if only and b != only:
            continue
        if not os.path.isdir(p):
            bad.append(f"plik luzem w output (miejsce: output/<nazwa>/): {b}")
            continue
        w = wersje(p)
        if not w:
            bad.append(f"{b}/: brak DOCX pisma <nazwa>_vN.docx")
            continue
        n += 1
        wymienione = set()
        jest, braki = zalaczniki(p, wymienione)
        for f in os.listdir(p):
            if f.startswith((".", "~$", "_")):
                continue
            stem, ext = os.path.splitext(f)
            if ext.lower() == ".md":
                bad.append(f"{b}/{f}: MD w folderze pisma (miejsce: drafty/<pismo>/ w teczce)")
            elif ext.lower() == ".docx" and stem != b and not (VER.search(stem) and VER.sub("", stem) == b) \
                    and unicodedata.normalize("NFC", f) not in wymienione:
                bad.append(f"{b}/{f}: DOCX o nazwie innej niż {b}_vN.docx")
        if [k for k, _ in w if k == 0]:
            bad.append(f"{b}/{b}.docx: wersja bez _vN (stary układ): nadaj numer wersji")
        c = changes(w[-1][1])
        if c["w:ins"] or c["w:del"]:
            bad.append(f"{os.path.basename(w[-1][1])}: najnowsza wersja ma zmiany śledzone (w:ins {c['w:ins']}, w:del {c['w:del']})")
        if jest is None:
            bad.append(f"{b}/: brak _ZALACZNIKI.md (spis załączników; „brak załączników”, gdy pismo ich nie ma)")
        for z in braki:
            bad.append(f"{b}/: brak załącznika {z}")
    print("\n".join(bad) if bad else f"PASS: {n} pism, każde w folderze z wersjami _vN i załącznikami")
    sys.exit(1 if bad else 0)


def redline_wycofany():
    sys.exit("`redline` i `start` są wycofane (4.11.2026): kolejna wersja to `nastepna`, zmiany to `zmien` (ARTEFAKTY-SPRAWY)")


if __name__ == "__main__":
    cmds = {"nowe": nowe, "nastepna": nastepna, "zmien": zmien, "akceptuj": akceptuj, "najnowsza": najnowsza,
            "sprawdz": sprawdz, "redline": redline_wycofany, "start": redline_wycofany}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmds[sys.argv.pop(1)]()
