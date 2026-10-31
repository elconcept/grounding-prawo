#!/usr/bin/env python3
"""Przeszukiwalna baza ustaw z komentarzem - lokalnie, SQLite FTS5, bez zależności spoza biblioteki standardowej.

Źródła (submoduły repo grounding-prawo, lista w .gitmodules):
- vendor/law-git/<kodeks> - kodeksy i Konstytucja „git as law”: tekst jednolity jako punkt kontrolny, potem jeden
  commit na każdą nowelizację w dacie wejścia w życie; gałąź main = stan prawny na dzień ostatniej naniesionej zmiany.
  Z tych repozytoriów pochodzi brzmienie kodeksów (pole `zrodlo: git-as-law`, `stan_na`, `ostatnia_zmiana`).
- vendor/law/<ustawa> - komentarz do każdego artykułu (sekcja „Brzmienie przepisu” i komentarz) według tekstu
  jednolitego z 00-wprowadzenie.md. Dla ustaw spoza law-git brzmienie pochodzi stąd (`zrodlo: komentarz`).

    python ustawy.py buduj [--law DIR] [--law-git DIR] [--db PLIK]   # indeks ze wszystkich repozytoriów
    python ustawy.py akty                                 # lista aktów, skróty, podstawa tekstu
    python ustawy.py art kk 148 [--komentarz]
    python ustawy.py szukaj "obrona konieczna" [--akt kk] [--zakres przepisy|komentarze] [--limit 10]
    python ustawy.py cytat kpk 168a "dowodu nie można uznać"   # czy fragment stoi w brzmieniu artykułu

Stan brzmienia podaje pole `uwaga`: dla git-as-law data ostatniej naniesionej nowelizacji, dla komentarza tekst
jednolity, na którym oparto opracowanie. Komentarz jest opracowaniem, nie źródłem prawa: cytuj go jako komentarz.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LAW = os.environ.get("USTAWY_LAW_DIR") or os.path.normpath(os.path.join(HERE, "../../../vendor/law"))
DEFAULT_LAW_GIT = os.environ.get("USTAWY_LAW_GIT_DIR") or os.path.normpath(os.path.join(HERE, "../../../vendor/law-git"))
# repozytorium git-as-law -> identyfikator aktu (nazwa repozytorium komentarza)
GIT_ACT = {"konstytucja-rp": "konstytucja-rzeczypospolitej-polskiej"}
AMEND = re.compile(r"^(\d{4}-\d{2}-\d{2}) \u2014 (\S+?):?\s(.*)$")
CHECKPOINT = re.compile(r"^Punkt kontrolny \u2014 tekst jednolity (.+)$")
ART_LINE = re.compile(r"^Art\.\s+(\d+[a-z]*(?:\[\d+\])?)\.\s*(.*)$")
DEFAULT_DB = os.environ.get("USTAWY_DB") or os.path.join(os.getcwd(), "ustawy.sqlite")

# skróty -> katalog aktu (nazwa repozytorium)
ALIASES = {
    "kc": "kodeks-cywilny", "kk": "kodeks-karny", "kpa": "kodeks-postepowania-administracyjnego",
    "kpc": "kodeks-postepowania-cywilnego", "kpk": "kodeks-postepowania-karnego",
    "kpw": "kodeks-postepowania-w-sprawach-o-wykroczenia", "kpsw": "kodeks-postepowania-w-sprawach-o-wykroczenia",
    "kro": "kodeks-rodzinny-i-opiekunczy", "kw": "kodeks-wykroczen",
    "konstytucja": "konstytucja-rzeczypospolitej-polskiej", "krp": "konstytucja-rzeczypospolitej-polskiej",
    "ppsa": "prawo-o-postepowaniu-przed-sadami-administracyjnymi", "pusa": "prawo-o-ustroju-sadow-administracyjnych",
    "usp": "prawo-o-ustroju-sadow-powszechnych", "pusp": "prawo-o-ustroju-sadow-powszechnych",
    "usn": "o-sadzie-najwyzszym", "pop": "prawo-o-prokuraturze", "pa": "prawo-o-adwokaturze",
    "urp": "o-radcach-prawnych", "uksc": "o-kosztach-sadowych-w-sprawach-cywilnych",
    "uops": "odpowiedzialnosci-podmiotow-zbiorowych-za-czyny-zabronione-pod-grozba-kary",
    "uokik": "o-ochronie-konkurencji-i-konsumentow", "uokk": "o-ochronie-konkurencji-i-konsumentow",
    "upk": "o-prawach-konsumenta", "uopl": "o-ochronie-praw-lokatorow",
    "udui": "o-dzialalnosci-ubezpieczeniowej-i-reasekuracyjnej", "uodo": "o-ochronie-danych-osobowych",
    "uozp": "o-ochronie-zdrowia-psychicznego", "uoozp": "o-ochronie-zdrowia-psychicznego",
    "upp": "o-prawach-pacjenta-i-rzeczniku-praw-pacjenta", "udl": "o-dzialalnosci-leczniczej",
    "uzl": "o-zawodach-lekarza-i-lekarza-dentysty", "pf": "prawo-farmaceutyczne",
    "uswiadczeniach": "o-swiadczeniach-opieki-zdrowotnej-finansowanych-ze-srodkow-publicznych",
    "uop": "o-policji", "ustawa-o-policji": "o-policji", "udip": "o-dostepie-do-informacji-publicznej",
    "ukrs": "o-krajowym-rejestrze-sadowym", "uos": "o-oplacie-skarbowej", "usd": "o-podatku-od-spadkow-i-darowizn",
    "ups": "o-pomocy-spolecznej", "upps": "o-pomocy-spolecznej", "uppd": "o-przeciwdzialaniu-przemocy-domowej",
    "prd": "prawo-o-ruchu-drogowym",
    "kks": "kodeks-karny-skarbowy", "kkw": "kodeks-karny-wykonawczy", "km": "kodeks-morski",
    "kp": "kodeks-pracy", "ksh": "kodeks-spolek-handlowych", "kwyb": "kodeks-wyborczy",
}
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
CHAPTER = re.compile(r"\d+-rozdzial\.md$")


def fold(s: str) -> str:
    """Wielkość liter i diakrytyki bez znaczenia; FTS5 remove_diacritics nie składa litery ł."""
    s = s.lower().replace("ł", "l")
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))


def norm_art(a: str) -> str:
    """'117¹', '117^1', '117[1]', '117(1)' -> '117^1'; '43 bb' -> '43bb'; 'art. 148' -> '148'."""
    a = a.strip().lower()
    a = re.sub(r"^art\.?\s*", "", a).rstrip(".")
    m = re.match(r"^(\d+)\s*([a-z]*)\s*([a-z]*)\s*(?:\[(\d+)\]|\^(\d+)|\((\d+)\)|([⁰¹²³⁴⁵⁶⁷⁸⁹]+))?$", a)
    if not m:
        return a.replace(" ", "")
    base = m.group(1) + m.group(2) + m.group(3)
    sup = m.group(4) or m.group(5) or m.group(6) or (m.group(7) or "").translate(SUP)
    return base + ("^" + sup if sup else "")


def resolve_act(name: str) -> str:
    n = fold(name.strip()).replace(".", "").replace(" ", "-")
    return ALIASES.get(n, n)


def parse_commentary(text: str):
    """Rozdział komentarza -> [(art, jednostka, brzmienie, komentarz)]."""
    out, unit = [], ""
    parts = re.split(r"^(#{3,4} .+?)\s*$", text, flags=re.M)
    art = None
    for chunk in parts:
        if chunk.startswith("#### "):
            unit = chunk[5:].strip()
            continue
        if chunk.startswith("### "):
            m = re.match(r"### Art\.\s*(.+)$", chunk)
            art = norm_art(m.group(1)) if m else None
            continue
        if not art:
            continue
        quote, rest, in_q = [], [], False
        for ln in chunk.split("\n"):
            if ln.strip().startswith("**Brzmienie przepisu"):
                in_q = True
                continue
            if in_q and (ln.startswith(">") or (not ln.strip() and not rest and quote)):
                quote.append(ln[1:].strip() if ln.startswith(">") else "")
                continue
            if ln.strip() or rest:
                in_q = False if ln.strip() else in_q
                rest.append(ln)
        out.append((art, unit, "\n".join(quote).strip(), "\n".join(rest).strip()))
        art = None
    return out


def act_meta(path: str, name: str) -> dict:
    """Tytuł, podstawa tekstu (tekst jednolity) i ELI z 00-wprowadzenie.md / README.md."""
    meta = {"tytul": name, "tekst_jednolity": None, "eli": None}
    for fn in ("00-wprowadzenie.md", "README.md", "INDEX.md"):
        p = os.path.join(path, fn)
        if not os.path.isfile(p):
            continue
        t = open(p, encoding="utf-8").read()
        if meta["tytul"] == name:
            first = t.split("\n", 1)[0].lstrip("# ").strip()
            first = re.sub(r"^INDEX\s*\u2014\s*", "", first)
            meta["tytul"] = re.sub(r"^Komentarz do (ustawy|Konstytucji)",
                                   lambda m: "Ustawa" if m.group(1) == "ustawy" else "Konstytucja", first)
        m = re.search(r"tekst jednolity[^\n]*?(Dz\.\s?U\.\s*\d{4}\s*poz\.\s*\d+)", t)
        if m and not meta["tekst_jednolity"]:
            meta["tekst_jednolity"] = re.sub(r"\s+", " ", m.group(1))
        m = re.search(r"api\.sejm\.gov\.pl/eli/acts/([A-Z]+/\d{4}/\d+)", t)
        if m and not meta["eli"]:
            meta["eli"] = m.group(1)
    return meta


def git_date(repo: str) -> str:
    try:
        return subprocess.run(["git", "-C", repo, "log", "-1", "--format=%cs"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def git_law_meta(repo: str) -> dict:
    """Stan repozytorium git-as-law: ostatnia naniesiona nowelizacja i ostatni punkt kontrolny (tekst jednolity)."""
    try:
        log = subprocess.run(["git", "-C", repo, "log", "--format=%s"], capture_output=True, text=True,
                             check=True).stdout.splitlines()
    except (subprocess.CalledProcessError, FileNotFoundError):
        log = []
    meta = {"stan_na": None, "ostatnia_zmiana": None, "tekst_jednolity": None}
    for subj in log:
        m = AMEND.match(subj)
        if m and not meta["stan_na"]:
            meta["stan_na"], meta["ostatnia_zmiana"] = m.group(1), f"{m.group(2)}: {m.group(3)}"
        c = CHECKPOINT.match(subj)
        if c and not meta["tekst_jednolity"]:
            meta["tekst_jednolity"] = c.group(1).strip()
        if meta["stan_na"] and meta["tekst_jednolity"]:
            break
    return meta


def parse_git_law(text: str):
    """Plik kodeksu git-as-law -> [(art, jednostka, brzmienie)]; jednostka = ostatni nagłówek rozdziału."""
    out, unit, art, buf = [], "", None, []

    def flush():
        if art:
            out.append((art, unit, "\n\n".join(p for p in "\n".join(buf).split("\n\n") if p.strip()).strip()))

    for ln in text.split("\n"):
        if ln.startswith("## "):
            flush(); art, buf = None, []
            unit = ln[3:].strip()
            continue
        m = ART_LINE.match(ln)
        if m:
            flush()
            art, buf = norm_art(m.group(1)), [ln]
            continue
        if art is not None:
            buf.append(ln)
    flush()
    return out


def build_git(con, law_git: str) -> tuple[int, int]:
    acts = arts = 0
    if not os.path.isdir(law_git):
        return 0, 0
    for d in sorted(os.listdir(law_git)):
        p = os.path.join(law_git, d)
        files = sorted(f for f in os.listdir(p) if f.endswith(".md") and f.upper() != "README.MD") if os.path.isdir(p) else []
        if len(files) != 1:
            continue
        akt = GIT_ACT.get(d, d)
        gm = git_law_meta(p)
        text = open(os.path.join(p, files[0]), encoding="utf-8").read()
        head = text.split("\n", 1)[0].lstrip("# ").strip()
        if not con.execute("SELECT 1 FROM akty WHERE akt=?", (akt,)).fetchone():
            con.execute("INSERT INTO akty (akt, tytul) VALUES (?, ?)", (akt, head))
        con.execute("UPDATE akty SET zrodlo='git-as-law', stan_na=?, ostatnia_zmiana=?, tekst_jednolity=?, "
                    "opracowanie=? WHERE akt=?", (gm["stan_na"], gm["ostatnia_zmiana"],
                                                  gm["tekst_jednolity"] or head, git_date(p), akt))
        acts += 1
        for art, unit, quote in parse_git_law(text):
            old = con.execute("SELECT komentarz FROM artykuly WHERE akt=? AND art=?", (akt, art)).fetchone()
            con.execute("INSERT OR REPLACE INTO artykuly VALUES (?,?,?,?,?,?)",
                        (akt, art, unit, quote, old["komentarz"] if old else "", f"{d}/{files[0]}"))
            arts += 0 if old else 1
    return acts, arts


def build(law: str, db: str, law_git: str = DEFAULT_LAW_GIT) -> int:
    tmp = db + ".tmp"
    if os.path.exists(tmp):
        os.remove(tmp)
    con = sqlite3.connect(tmp)
    con.executescript("""
        CREATE TABLE akty (akt TEXT PRIMARY KEY, tytul TEXT, tekst_jednolity TEXT, eli TEXT, opracowanie TEXT,
                           zrodlo TEXT DEFAULT 'komentarz', stan_na TEXT, ostatnia_zmiana TEXT);
        CREATE TABLE artykuly (akt TEXT, art TEXT, jednostka TEXT, brzmienie TEXT, komentarz TEXT, plik TEXT,
                               PRIMARY KEY (akt, art));
        CREATE VIRTUAL TABLE fts USING fts5(akt UNINDEXED, art UNINDEXED, rodzaj UNINDEXED, zlozony, tokenize='unicode61');
    """)
    acts = arts = 0
    for d in sorted(os.listdir(law)):
        p = os.path.join(law, d)
        if not os.path.isdir(p):
            continue
        chapters = sorted(f for f in os.listdir(p) if CHAPTER.match(f))
        if not chapters:
            continue
        m = act_meta(p, d)
        con.execute("INSERT INTO akty (akt, tytul, tekst_jednolity, eli, opracowanie) VALUES (?,?,?,?,?)",
                    (d, m["tytul"], m["tekst_jednolity"], m["eli"], git_date(p)))
        acts += 1
        for fn in chapters:
            for art, unit, quote, comm in parse_commentary(open(os.path.join(p, fn), encoding="utf-8").read()):
                cur = con.execute("INSERT OR IGNORE INTO artykuly VALUES (?,?,?,?,?,?)",
                                  (d, art, unit, quote, comm, f"{d}/{fn}"))
                if cur.rowcount:
                    arts += 1
                    con.execute("INSERT INTO fts VALUES (?,?,?,?)", (d, art, "komentarz", fold(comm)))
    con.row_factory = sqlite3.Row
    gacts, garts = build_git(con, law_git)
    arts += garts
    # indeks przepisów po złożeniu obu źródeł (brzmienie git-as-law zastępuje brzmienie z komentarza)
    for r in con.execute("SELECT akt, art, brzmienie FROM artykuly").fetchall():
        con.execute("INSERT INTO fts VALUES (?,?,?,?)", (r["akt"], r["art"], "przepis", fold(r["brzmienie"])))
    con.commit()
    acts = con.execute("SELECT count(*) FROM akty").fetchone()[0]
    con.close()
    if acts == 0 or arts == 0:
        os.remove(tmp)
        print(f"BŁĄD: pusty indeks (akty {acts}, artykuły {arts}) - sprawdź {law}", file=sys.stderr)
        return 20
    os.replace(tmp, db)
    print(f"indeks: {acts} aktów ({gacts} z brzmieniem git-as-law), {arts} artykułów -> {db}")
    return 0


class Baza:
    def __init__(self, db: str = DEFAULT_DB):
        if not os.path.exists(db):
            raise FileNotFoundError(f"brak indeksu {db} - uruchom: python ustawy.py buduj")
        self.con = sqlite3.connect(db, check_same_thread=False)
        self.con.row_factory = sqlite3.Row

    def akty(self) -> list[dict]:
        skroty = {}
        for k, v in ALIASES.items():
            skroty.setdefault(v, []).append(k)
        rows = self.con.execute("SELECT a.*, (SELECT count(*) FROM artykuly WHERE akt=a.akt) n_art FROM akty a ORDER BY akt")
        return [dict(r, skroty=skroty.get(r["akt"], [])) for r in rows]

    def artykul(self, akt: str, art: str, komentarz: bool = False) -> dict:
        akt, art = resolve_act(akt), norm_art(art)
        meta = self.con.execute("SELECT * FROM akty WHERE akt=?", (akt,)).fetchone()
        if not meta:
            return {"status": "OUT_OF_SCOPE", "akt": akt, "powod": "akt spoza bazy; brzmienie z ELI (api.sejm.gov.pl)"}
        out = {"akt": akt, "art": art, "tytul": meta["tytul"], "tekst_jednolity": meta["tekst_jednolity"],
               "eli": meta["eli"], "zrodlo": meta["zrodlo"], "stan_na": meta["stan_na"],
               "ostatnia_zmiana": meta["ostatnia_zmiana"]}
        r = self.con.execute("SELECT * FROM artykuly WHERE akt=? AND art=?", (akt, art)).fetchone()
        if not r:
            return dict(out, status="NOT_FOUND", powod=f"brak art. {art} w bazie aktu {akt}")
        out.update(status="FOUND", jednostka=r["jednostka"], tekst=r["brzmienie"], plik=r["plik"], uwaga=uwaga(meta))
        if komentarz:
            out["komentarz"] = r["komentarz"]
        return out

    def akt_po_eli(self, eli: str, offset: int = 0, limit: int = 5000,
                   art: str | None = None) -> dict:
        """Bezpośredni read-only odczyt polskiego korpusu po ELI.

        Wewnętrzny endpoint resolvera; NIE jest wyszukiwarką. Obsługuje tylko
        dokładne identyfikatory publikacji. Nie odpowiada pełnemu plikowi Dz.U.
        (brak załączników), zatem świadomie raportuje dokument_pelny=False.
        """
        if not re.fullmatch(r"(DU|MP)/\d{4}/\d{1,5}", eli, re.I):
            return {"status": "INVALID_ELI", "eli": eli}
        if type(offset) is not int or offset < 0 or type(limit) is not int or limit < 1 or limit > 20000:
            return {"status": "INVALID_RANGE", "offset": offset, "limit": limit}
        meta = self.con.execute("SELECT * FROM akty WHERE UPPER(eli)=UPPER(?)", (eli,)).fetchone()
        if not meta:
            return {"status": "OUT_OF_SCOPE", "eli": eli,
                    "powod": "Dokładny tekst tej publikacji nie występuje w lokalnej bazie USTAWY"}
        if art:
            numer = norm_art(art)
            rows = self.con.execute(
                "SELECT art, brzmienie FROM artykuly WHERE akt=? AND art=?",
                (meta["akt"], numer),
            ).fetchall()
        else:
            rows = self.con.execute(
                "SELECT art, brzmienie FROM artykuly WHERE akt=? ORDER BY rowid",
                (meta["akt"],),
            ).fetchall()
        if not rows:
            return {"status": "NOT_FOUND", "eli": eli, "art": art,
                    "powod": "Brak artykułu w lokalnym korpusie"}
        tekst = "\n\n".join(str(r["brzmienie"] or "").strip()
                          for r in rows if str(r["brzmienie"] or "").strip())
        total = len(tekst)
        frag = tekst[offset:offset + limit]
        next_offset = offset + len(frag)
        more = next_offset < total
        return {"status": "FOUND", "eli": meta["eli"], "akt": meta["akt"],
                "tytul": meta["tytul"], "tekst_jednolity": meta["tekst_jednolity"],
                "stan_na": meta["stan_na"], "zrodlo": meta["zrodlo"],
                "art": art, "tekst": frag,
                "totalLength": total, "returnedLength": len(frag),
                "offset": offset, "hasMore": more,
                "nextOffset": next_offset if more else None,
                "dokument_pelny": False, "kompletnosc": "zaindeksowane_artykuły",
                "uwaga": "Lokalna baza USTAWY nie gwarantuje pełnego oryginalnego Dz.U. "
                         "z załącznikami i późniejszymi zmianami. " + uwaga(meta)}

    def szukaj(self, q: str, akt: str | None = None, zakres: str | None = None, limit: int = 10) -> list[dict]:
        words = [w for w in re.findall(r"\w+", fold(q)) if w]
        if not words:
            return []
        # odmiana: dla słów od 6 liter ucinamy 2 znaki końcówki i szukamy prefiksu
        stems = [w[:-2] if len(w) >= 6 else w for w in words]
        terms = ['"' + s + '"' + ("*" if len(w) >= 4 else "") for s, w in zip(stems, words)]
        sql = "SELECT akt, art, rodzaj, bm25(fts) s FROM fts WHERE fts MATCH ?"
        args: list = [" ".join(terms)]
        if akt:
            sql += " AND akt=?"; args.append(resolve_act(akt))
        if zakres in ("przepisy", "komentarze"):
            sql += " AND rodzaj=?"; args.append("przepis" if zakres == "przepisy" else "komentarz")
        sql += " ORDER BY s LIMIT ?"; args.append(int(limit))
        out = []
        for r in self.con.execute(sql, args):
            t = self.con.execute("SELECT brzmienie, komentarz FROM artykuly WHERE akt=? AND art=?", (r["akt"], r["art"])).fetchone()
            text = (t["brzmienie"] if r["rodzaj"] == "przepis" else t["komentarz"]) if t else ""
            out.append({"akt": r["akt"], "art": r["art"], "rodzaj": r["rodzaj"], "fragment": snippet(text, stems)})
        return out

    def cytat(self, akt: str, art: str, fragment: str) -> dict:
        a = self.artykul(akt, art)
        if a.get("status") != "FOUND":
            return dict(a, wynik="NOT_CHECKED")
        hay, needle = squash(a["tekst"]), squash(fragment)
        ok = bool(needle) and needle in hay
        return {"wynik": "FOUND" if ok else "NOT_FOUND", "akt": a["akt"], "art": a["art"],
                "tekst_jednolity": a["tekst_jednolity"], "eli": a["eli"], "tekst": a["tekst"],
                "uwaga": a["uwaga"] if ok else "fragment nie występuje dosłownie w brzmieniu artykułu"}


def uwaga(meta) -> str:
    if meta["zrodlo"] == "git-as-law":
        return (f"brzmienie obowiązujące według repozytorium git-as-law: tekst jednolity {meta['tekst_jednolity']} "
                f"z naniesionymi nowelizacjami, ostatnia w dniu {meta['stan_na']} ({meta['ostatnia_zmiana']}). "
                f"Cytuj jako stan na {meta['stan_na']}; nowelizację albo nowy tekst jednolity wchodzący w życie po tej "
                "dacie sprawdź w isap_search_acts.")
    return (f"brzmienie z komentarza opartego na tekście jednolitym {meta['tekst_jednolity']}; nowelizacje wchodzące "
            "w życie po tym tekście jednolitym sprawdź w isap_search_acts (pole eli).")


def squash(s: str) -> str:
    s = s.replace(" ", " ").replace("„", '"').replace("”", '"').replace("“", '"')
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def snippet(text: str, stems: list[str], width: int = 220) -> str:
    f = fold(text)
    pos = min((f.find(s) for s in stems if s in f), default=0)
    start = max(0, pos - width // 3)
    s = text[start:start + width].replace("\n", " ")
    return ("…" if start else "") + s + ("…" if start + width < len(text) else "")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--law", default=DEFAULT_LAW)
    ap.add_argument("--law-git", default=DEFAULT_LAW_GIT)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("buduj")
    sub.add_parser("akty")
    p = sub.add_parser("art"); p.add_argument("akt"); p.add_argument("nr"); p.add_argument("--komentarz", action="store_true")
    p = sub.add_parser("szukaj"); p.add_argument("q"); p.add_argument("--akt"); p.add_argument("--zakres", choices=["przepisy", "komentarze"]); p.add_argument("--limit", type=int, default=10)
    p = sub.add_parser("cytat"); p.add_argument("akt"); p.add_argument("nr"); p.add_argument("fragment")
    a = ap.parse_args(argv)
    if a.cmd == "buduj":
        return build(a.law, a.db, a.law_git)
    b = Baza(a.db)
    res = {"akty": lambda: b.akty(),
           "art": lambda: b.artykul(a.akt, a.nr, a.komentarz),
           "szukaj": lambda: b.szukaj(a.q, a.akt, a.zakres, a.limit),
           "cytat": lambda: b.cytat(a.akt, a.nr, a.fragment)}[a.cmd]()
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
