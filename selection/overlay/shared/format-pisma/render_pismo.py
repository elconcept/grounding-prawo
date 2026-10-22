#!/usr/bin/env python3
"""Renderer pisma procesowego: źródło .md -> .docx.

DOCX jest artefaktem końcowym (użytkownik redaguje go w Wordzie, drukuje i podpisuje); źródło .md
zostaje w <sprawa>/drafty/<pismo>/, DOCX trafia do legal/output/ (bez sidecara). PDF nie powstaje.

Standard typograficzny: shared/FORMAT-PISMA.md. Tylko biblioteka standardowa. W pracy nad sprawą wołaj
wersja_pisma.py (nowe / start / redline / sprawdz), nie ten plik bezpośrednio: kolejna wersja pisma to redline
na istniejącym DOCX, nie nowy render (shared/ARTEFAKTY-SPRAWY.md).

Użycie:
    python3 -I render_pismo.py pismo.md [--out KATALOG] [--nadpisz]

Istniejącego .docx nie nadpisuje bez --nadpisz: mógł zostać już poprawiony ręcznie.

Źródło: blok metryki między liniami '---', potem treść.

    ---
    data: Kraków, dnia 15 października 2026 r.
    nadawca: Jan Kowalski
    nadawca_adres: ul. Przykładowa 1/2, 30-001 Kraków
    nadawca_kontakt: tel. 600 000 000, e-mail: jan.kowalski@example.pl
    adresat: Sąd Okręgowy w Krakowie
    adresat_jednostka: III Wydział Karny
    adresat_adres: ul. Przy Rondzie 7, 31-547 Kraków
    metryka: Sygn. akt | III Ko 1/26
    metryka: Wnioskodawca | Jan Kowalski
    tytul: PISMO
    podtytul: uzupełniające braki formalne wniosku
    podpis_rola: Za uczestnika - pełnomocnik      (opcjonalnie)
    podpis: Jan Kowalski
    zalacznik: Odpis pisma                         (powtarzalne, opcjonalne)
    ---

Klucze powtarzalne (adresat, adresat_jednostka, metryka, zalacznik) tworzą kolejne linie.
Blok adresata jest wyrównany do prawej: adresat 14 pt, adresat_jednostka (wydział, oddział,
podjednostka) 12 pt, adresat_adres 10 pt w jednej linii.
nadawca_kontakt jest obowiązkowy (art. 119 § 1 pkt 2 k.p.k./art. 126 k.p.c.): gdy nie znasz
telefonu ani e-maila, zapytaj użytkownika; wartość „nie posiadam” wpisuje się tylko na jego polecenie.

Treść:
    akapit                      - wyjustowany, Georgia 10 pt
    1. tekst / a) tekst         - punkt i podpunkt z wcięciem wiszącym
    (wcięcie 3 spacjami)        - kolejny akapit tego samego punktu
    # NAGŁÓWEK                  - wyśrodkowany, rozstrzelone wersaliki, bez pogrubienia
    ## Nagłówek                 - do lewej, rozstrzelone wersaliki, bez pogrubienia
    > cytat                     - wcięty z obu stron, 9,5 pt
    **teza**  __teza__  *tytuł* - pogrubienie / podkreślenie / kursywa (tylko w treści)
"""
import os, re, sys, zipfile
from xml.sax.saxutils import escape

FONT = "Georgia"            # zamienniki metryczne: Gelasio, Charter, DejaVu Serif
BODY = 20                   # półpunkty: 10 pt
NAME = 28                   # 14 pt - nazwa nadawcy i adresata
UNIT = 24                   # 12 pt - wydział, oddział, podjednostka adresata
QUOTE = 19                  # 9,5 pt
TITLE = 24                  # 12 pt
LINE = 300                  # interlinia 1,25
CM = 567                    # twips na centymetr
LABEL_TAB = int(3.5 * CM)   # kolumna wartości metryki
REPEATED = {"adresat", "adresat_jednostka", "metryka", "zalacznik"}
REQUIRED = ["data", "nadawca", "nadawca_adres", "nadawca_kontakt", "adresat", "adresat_adres", "tytul", "podpis"]


def parse(src):
    text = open(src, encoding="utf-8").read().replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        sys.exit("brak bloku metryki '---' na początku pliku")
    meta = {}
    for raw in m.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        k, _, v = raw.partition(":")
        k, v = k.strip(), v.strip()
        if k in REPEATED:
            meta.setdefault(k, []).append(v)
        else:
            meta[k] = v
    missing = [k for k in REQUIRED if not meta.get(k)]
    if missing:
        sys.exit("brak pól metryki: " + ", ".join(missing) +
                 "\n(nadawca_kontakt: zapytaj użytkownika o telefon i e-mail; nie zgaduj)")
    return meta, m.group(2)


# ---------- runy ----------
def rpr(size=BODY, b=False, u=False, i=False, spacing=0):
    x = f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}" w:eastAsia="{FONT}"/>'
    if b: x += "<w:b/><w:bCs/>"
    if i: x += "<w:i/><w:iCs/>"
    if u: x += '<w:u w:val="single"/>'
    if spacing: x += f'<w:spacing w:val="{spacing}"/>'
    x += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    return f"<w:rPr>{x}</w:rPr>"


def run(text, **kw):
    parts = text.split("\t")
    out = []
    for n, p in enumerate(parts):
        if n: out.append(f"<w:r>{rpr(**kw)}<w:tab/></w:r>")
        if p: out.append(f'<w:r>{rpr(**kw)}<w:t xml:space="preserve">{escape(p)}</w:t></w:r>')
    return "".join(out)


TOKEN = re.compile(r"(\*\*|__|\*)")


def inline(text, size=BODY, stats=None):
    """**pogrubienie**, __podkreślenie__, *kursywa*; znaczniki mogą się zagnieżdżać."""
    b = u = i = False
    out = []
    for piece in TOKEN.split(text):
        if piece == "**": b = not b; stats is not None and b and stats.append("b"); continue
        if piece == "__": u = not u; stats is not None and u and stats.append("u"); continue
        if piece == "*": i = not i; continue
        if piece: out.append(run(piece, size=size, b=b, u=u, i=i))
    if b or u or i:
        sys.exit(f"niezamknięty znacznik formatowania w: {text[:80]}")
    return "".join(out)


def para(content, jc="both", ind="", before=0, after=120, tabs="", keep=False, line=LINE):
    ppr = f'<w:spacing w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="auto"/>'
    if tabs: ppr = f"<w:tabs>{tabs}</w:tabs>" + ppr
    if ind: ppr += ind
    if keep: ppr = "<w:keepNext/>" + ppr
    ppr += f'<w:jc w:val="{jc}"/>'
    return f"<w:p><w:pPr>{ppr}</w:pPr>{content}</w:p>"


def tab(pos):
    return f'<w:tab w:val="left" w:pos="{pos}"/>'


# ---------- dokument ----------
def header(meta):
    x = [para(run(meta["data"]), jc="right", after=240)]
    x.append(para(run(meta["nadawca"], size=NAME), jc="left", after=0, line=240))
    x.append(para(run(meta["nadawca_adres"]), jc="left", after=0))
    x.append(para(run(meta["nadawca_kontakt"]), jc="left", after=360))
    for line in meta["adresat"]:
        x.append(para(run(line, size=NAME), jc="right", after=0, line=240))
    for line in meta.get("adresat_jednostka", []):
        x.append(para(run(line, size=UNIT), jc="right", after=0, line=240))
    x.append(para(run(meta["adresat_adres"]), jc="right", after=360))
    for row in meta.get("metryka", []):
        label, _, val = row.partition("|")
        x.append(para(run(f"{label.strip()}:\t{val.strip()}"), jc="left", tabs=tab(LABEL_TAB), after=60))
    x.append(para(run(meta["tytul"].upper(), size=TITLE, spacing=60), jc="center", before=360,
                  after=60 if meta.get("podtytul") else 360, keep=True))
    if meta.get("podtytul"):
        x.append(para(run(meta["podtytul"]), jc="center", after=360, keep=True))
    return x


def body(text, stats):
    x = []
    blocks = re.split(r"\n\s*\n", text.strip())
    for blk in blocks:
        raw = blk.rstrip()
        flat = " ".join(l.strip() for l in raw.splitlines())
        if raw.startswith("# "):
            x.append(para(run(flat[2:].upper(), size=BODY + 2, spacing=40), jc="center", before=240, after=180, keep=True))
        elif raw.startswith("## "):
            x.append(para(run(flat[3:].upper(), spacing=30), jc="left", before=200, after=120, keep=True))
        elif raw.startswith(">"):
            q = " ".join(l.lstrip("> ").strip() for l in raw.splitlines())
            x.append(para(inline(q, QUOTE, stats), ind=f'<w:ind w:left="{CM}" w:right="{CM}"/>'))
        elif m := re.match(r"(\d+\.)\s+(.*)", flat, re.S):
            x.append(para(run(m.group(1) + "\t") + inline(m.group(2), stats=stats), tabs=tab(CM),
                          ind=f'<w:ind w:left="{CM}" w:hanging="{CM}"/>'))
        elif m := re.match(r"([a-z]\))\s+(.*)", flat, re.S):
            x.append(para(run(m.group(1) + "\t") + inline(m.group(2), stats=stats), tabs=tab(2 * CM),
                          ind=f'<w:ind w:left="{2 * CM}" w:hanging="{CM}"/>'))
        elif raw.startswith("   "):
            x.append(para(inline(flat, stats=stats), ind=f'<w:ind w:left="{CM}"/>'))
        else:
            x.append(para(inline(flat, stats=stats)))
    return x


def footer_sig(meta):
    x = []
    if meta.get("podpis_rola"):
        x.append(para(run(meta["podpis_rola"]), jc="right", before=480, after=0, keep=True))
    x.append(para(run("……………………………………"), jc="right", before=0 if meta.get("podpis_rola") else 720, after=0, keep=True))
    x.append(para(run(meta["podpis"]), jc="right", after=360))
    if meta.get("zalacznik"):
        x.append(para(run("Załączniki:"), jc="left", after=0, keep=True))
        for n, z in enumerate(meta["zalacznik"], 1):
            x.append(para(run(f"{n}.\t{z}"), jc="left", tabs=tab(CM // 2 + 113),
                          ind=f'<w:ind w:left="{CM // 2 + 113}" w:hanging="{CM // 2 + 113}"/>', after=0))
    return x


NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')


def document(paragraphs):
    sect = (f'<w:sectPr><w:footerReference w:type="default" r:id="rIdF"/>'
            f'<w:pgSz w:w="11906" w:h="16838"/>'
            f'<w:pgMar w:top="{2 * CM}" w:right="{2 * CM}" w:bottom="{2 * CM}" w:left="{int(2.5 * CM)}" '
            f'w:header="708" w:footer="567" w:gutter="0"/></w:sectPr>')
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>{"".join(paragraphs)}{sect}</w:body></w:document>'


def footer():
    fld = (f'<w:r>{rpr(size=16)}<w:fldChar w:fldCharType="begin"/></w:r>'
           f'<w:r>{rpr(size=16)}<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
           f'<w:r>{rpr(size=16)}<w:fldChar w:fldCharType="separate"/></w:r>'
           f'<w:r>{rpr(size=16)}<w:t>1</w:t></w:r>'
           f'<w:r>{rpr(size=16)}<w:fldChar w:fldCharType="end"/></w:r>')
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {NS}><w:p><w:pPr><w:jc w:val="right"/></w:pPr>{fld}</w:p></w:ftr>'


STYLES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault>{rpr()}</w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="{LINE}" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:pPr><w:widowControl/></w:pPr></w:style>
</w:styles>'''

CT = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>'''

DOC_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rIdS" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rIdF" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
</Relationships>'''


def core(title, author):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/">'
            f'<dc:title>{escape(title)}</dc:title><dc:creator>{escape(author)}</dc:creator></cp:coreProperties>')


def lint(stats, text):
    words = len(re.findall(r"\w+", text))
    limit = max(1, words // 250)
    if len(stats) > limit:
        print(f"UWAGA: {len(stats)} wyróżnień (pogrubienie/podkreślenie) na {words} słów; "
              f"limit FORMAT-PISMA to ok. {limit}. Zostaw tylko uchybienie organu lub kluczowy zarzut.", file=sys.stderr)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    src = args[0]
    out = args[args.index("--out") + 1] if "--out" in args else os.path.dirname(os.path.abspath(src))
    meta, text = parse(src)
    stats = []
    paragraphs = header(meta) + body(text, stats) + footer_sig(meta)
    lint(stats, text)
    base = os.path.splitext(os.path.basename(src))[0]
    docx = os.path.join(out, base + ".docx")
    if os.path.exists(docx) and "--nadpisz" not in args:
        sys.exit(f"{docx} już istnieje (mógł być redagowany ręcznie); użyj --nadpisz albo zmień nazwę źródła")
    with zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CT)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/document.xml", document(paragraphs))
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/footer1.xml", footer())
        z.writestr("docProps/core.xml", core(meta["tytul"], meta["podpis"]))
    print(docx)


if __name__ == "__main__":
    main()
