#!/usr/bin/env python3
"""Przeszukiwalna baza ustaw z komentarzem - lokalnie, SQLite FTS5, bez zależności spoza biblioteki standardowej.

Źródła (submoduły repo grounding-prawo):
  vendor/law/<kodeks>/            git-as-law: aktualny tekst jednolity, jeden commit = jedna nowelizacja
                                  w dacie wejścia w życie (historia brzmień przez git)
  vendor/law/komentarze/<ustawa>/ komentarz do każdego artykułu (rozdziały *-rozdzial.md)

    python ustawy.py buduj [--law DIR] [--db PLIK]       # indeks z obu źródeł
    python ustawy.py akty                                 # lista aktów, skróty, stan tekstu
    python ustawy.py art kk 148 [--komentarz] [--na-dzien 2024-05-01]
    python ustawy.py szukaj "obrona konieczna" [--akt kk] [--zakres przepisy|komentarze] [--limit 10]
    python ustawy.py cytat kpk 168a "dowodu nie można uznać"   # czy fragment stoi w brzmieniu artykułu

Brzmienie przepisu pochodzi z tekstu git-as-law (stan: data ostatniego commitu). Gdy akt nie ma tekstu
git-as-law, brzmienie pochodzi z komentarza i jest oznaczone `zrodlo=komentarz` z datą opracowania;
takie brzmienie wymaga potwierdzenia w ELI (api.sejm.gov.pl) przed cytatem w piśmie.
Komentarz jest opracowaniem, nie źródłem prawa: cytuj go jako komentarz, a nie jako treść przepisu.
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
DEFAULT_DB = os.environ.get("USTAWY_DB") or os.path.join(os.getcwd(), "ustawy.sqlite")

# skróty -> katalog aktu; katalog git-as-law i katalog komentarza mogą się różnić
ALIASES = {
    "kc": "kodeks-cywilny", "kk": "kodeks-karny", "kks": "kodeks-karny-skarbowy", "kkw": "kodeks-karny-wykonawczy",
    "km": "kodeks-morski", "kpa": "kodeks-postepowania-administracyjnego", "kpc": "kodeks-postepowania-cywilnego",
    "kpk": "kodeks-postepowania-karnego", "kpw": "kodeks-postepowania-w-sprawach-o-wykroczenia", "kp": "kodeks-pracy",
    "kro": "kodeks-rodzinny-i-opiekunczy", "ksh": "kodeks-spolek-handlowych", "kw": "kodeks-wykroczen",
    "kodeks-wyborczy": "kodeks-wyborczy", "konstytucja": "konstytucja-rp", "krp": "konstytucja-rp",
    "uodo": "o-ochronie-danych-osobowych", "uozp": "o-ochronie-zdrowia-psychicznego",
    "uoozp": "o-ochronie-zdrowia-psychicznego", "upp": "o-prawach-pacjenta-i-rzeczniku-praw-pacjenta",
    "udl": "o-dzialalnosci-leczniczej", "ustawa-o-policji": "o-policji", "udip": "o-dostepie-do-informacji-publicznej",
    "prd": "prawo-o-ruchu-drogowym", "pusp": "prawo-o-ustroju-sadow-powszechnych", "pop": "prawo-o-prokuraturze",
    "upps": "o-pomocy-spolecznej", "uppd": "o-przeciwdzialaniu-przemocy-domowej",
}
COMMENTARY_DIR = {"konstytucja-rp": "konstytucja-rzeczypospolitej-polskiej"}
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
ART_LINE = re.compile(r"^Art\.\s+(\d+[a-z]*(?:\s+[a-z]{1,3})?(?:\[\d+\]|[⁰¹²³⁴⁵⁶⁷⁸⁹]+)?)\.(?=\s|$)")


def fold(s: str) -> str:
    """Wielkość liter i diakrytyki bez znaczenia; FTS5 remove_diacritics nie składa litery ł."""
    s = s.lower().replace("ł", "l")
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))


def norm_art(a: str) -> str:
    """'117[1]', '117¹', '117^1', '117(1)' -> '117^1'; '43 bb' -> '43bb'; 'art. 148' -> '148'."""
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


def law_file(d: str) -> str | None:
    for f in sorted(os.listdir(d)):
        if f.endswith(".md") and f.lower() not in ("readme.md", "license.md"):
            return os.path.join(d, f)
    return None


def parse_law(text: str):
    """Tekst git-as-law -> [(art, jednostka, tekst)]. Artykuł trwa do następnego 'Art.' albo nagłówka."""
    out, heads, cur, unit = [], [], None, ""
    for ln in text.split("\n"):
        if ln.startswith("#"):
            if cur:
                out.append(cur); cur = None
            title = ln.lstrip("#").strip()
            if ln.startswith("# "):
                continue
            if re.match(r"(?i)(rozdział|dział|część|księga|tytuł|oddział)\b", title):
                heads = [title]
            else:
                heads = (heads + [title])[-2:]
            unit = " / ".join(heads)
            continue
        m = ART_LINE.match(ln)
        if m:
            if cur:
                out.append(cur)
            cur = [norm_art(m.group(1)), unit, ln.rstrip()]
            continue
        if cur is not None:
            cur[2] += "\n" + ln.rstrip()
    if cur:
        out.append(cur)
    return [(a, u, t.strip()) for a, u, t in out]


def parse_commentary(text: str):
    """Rozdział komentarza -> [(art, brzmienie, komentarz)]."""
    out = []
    parts = re.split(r"^### Art\.\s*(.+?)\s*$", text, flags=re.M)
    for i in range(1, len(parts) - 1, 2):
        art, body = norm_art(parts[i]), parts[i + 1]
        body = re.split(r"^#{1,4} ", body, maxsplit=1, flags=re.M)[0]
        quote, rest, in_q = [], [], False
        for ln in body.split("\n"):
            if ln.strip().startswith("**Brzmienie przepisu"):
                in_q = True
                continue
            if in_q and (ln.startswith(">") or (not ln.strip() and not rest and quote)):
                quote.append(ln[1:].strip() if ln.startswith(">") else "")
                continue
            if ln.strip() or rest:
                in_q = False if ln.strip() else in_q
                rest.append(ln)
        out.append((art, "\n".join(quote).strip(), "\n".join(rest).strip()))
    return out


def git(repo: str, *args: str) -> str:
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout.strip()


def build(law: str, db: str) -> int:
    tmp = db + ".tmp"
    if os.path.exists(tmp):
        os.remove(tmp)
    con = sqlite3.connect(tmp)
    con.executescript("""
        CREATE TABLE akty (akt TEXT PRIMARY KEY, tytul TEXT, tekst_jednolity TEXT, stan_na TEXT, commit_sha TEXT,
                           zrodlo_tekstu TEXT, komentarz TEXT, komentarz_stan TEXT);
        CREATE TABLE artykuly (akt TEXT, art TEXT, jednostka TEXT, tekst TEXT, zrodlo TEXT, PRIMARY KEY (akt, art));
        CREATE TABLE komentarze (akt TEXT, art TEXT, brzmienie TEXT, komentarz TEXT, plik TEXT);
        CREATE VIRTUAL TABLE fts USING fts5(akt UNINDEXED, art UNINDEXED, rodzaj UNINDEXED, zlozony, tokenize='unicode61');
    """)
    acts = 0
    for d in sorted(os.listdir(law)):
        p = os.path.join(law, d)
        if d == "komentarze" or not os.path.isdir(p):
            continue
        f = law_file(p)
        if not f:
            continue
        text = open(f, encoding="utf-8").read()
        first = text.split("\n", 1)[0].lstrip("# ").strip()
        try:
            sha, date = git(p, "log", "-1", "--format=%H %cs").split()
        except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
            sha, date = "", ""
        readme = os.path.join(p, "README.md")
        title = d
        if os.path.isfile(readme):
            title = re.split(r"\s+\u2014\s+|\s+-\s+", open(readme, encoding="utf-8").readline().lstrip("# ").strip())[0]
        con.execute("INSERT INTO akty VALUES (?,?,?,?,?,?,?,?)", (d, title, first, date, sha, "git-as-law", None, None))
        for art, unit, body in parse_law(text):
            con.execute("INSERT OR IGNORE INTO artykuly VALUES (?,?,?,?,?)", (d, art, unit, body, "git-as-law"))
            con.execute("INSERT INTO fts VALUES (?,?,?,?)", (d, art, "przepis", fold(body)))
        acts += 1
    kroot = os.path.join(law, "komentarze")
    rev = {v: k for k, v in COMMENTARY_DIR.items()}
    for d in sorted(os.listdir(kroot)) if os.path.isdir(kroot) else []:
        p = os.path.join(kroot, d)
        if not os.path.isdir(p):
            continue
        akt = rev.get(d, d)
        idx = os.path.join(p, "INDEX.md")
        title = open(idx, encoding="utf-8").readline().lstrip("# ").replace("INDEX \u2014 ", "").strip() if os.path.isfile(idx) else d
        title = re.sub(r"^Komentarz do (ustawy|Konstytucji)", lambda m: "Ustawa" if m.group(1) == "ustawy" else "Konstytucja", title)
        try:
            kdate = git(p, "log", "-1", "--format=%cs")
        except (subprocess.CalledProcessError, FileNotFoundError):
            kdate = ""
        row = con.execute("SELECT akt FROM akty WHERE akt=?", (akt,)).fetchone()
        if row:
            con.execute("UPDATE akty SET tytul=?, komentarz=?, komentarz_stan=? WHERE akt=?", (title, d, kdate, akt))
        else:
            con.execute("INSERT INTO akty VALUES (?,?,?,?,?,?,?,?)", (akt, title, None, kdate, None, "komentarz", d, kdate))
            acts += 1
        for fn in sorted(os.listdir(p)):
            if not re.match(r"\d+-rozdzial\.md$", fn):
                continue
            for art, quote, comm in parse_commentary(open(os.path.join(p, fn), encoding="utf-8").read()):
                con.execute("INSERT INTO komentarze VALUES (?,?,?,?,?)", (akt, art, quote, comm, f"{d}/{fn}"))
                con.execute("INSERT INTO fts VALUES (?,?,?,?)", (akt, art, "komentarz", fold(comm)))
                if not row and quote:  # akt bez git-as-law: brzmienie z komentarza, oznaczone
                    con.execute("INSERT OR IGNORE INTO artykuly VALUES (?,?,?,?,?)", (akt, art, "", quote, "komentarz"))
                    con.execute("INSERT INTO fts VALUES (?,?,?,?)", (akt, art, "przepis", fold(quote)))
    n_art = con.execute("SELECT count(*) FROM artykuly").fetchone()[0]
    n_kom = con.execute("SELECT count(*) FROM komentarze").fetchone()[0]
    con.commit()
    con.close()
    if acts == 0 or n_art == 0:
        os.remove(tmp)
        print(f"BŁĄD: pusty indeks (akty {acts}, artykuły {n_art}) - sprawdź {law}", file=sys.stderr)
        return 20
    os.replace(tmp, db)
    print(f"indeks: {acts} aktów, {n_art} artykułów, {n_kom} komentarzy -> {db}")
    return 0


class Baza:
    def __init__(self, db: str = DEFAULT_DB, law: str = DEFAULT_LAW):
        if not os.path.exists(db):
            raise FileNotFoundError(f"brak indeksu {db} - uruchom: python ustawy.py buduj")
        self.con = sqlite3.connect(db, check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self.law = law

    def akty(self) -> list[dict]:
        rows = self.con.execute("SELECT a.*, (SELECT count(*) FROM artykuly WHERE akt=a.akt) n_art, "
                                "(SELECT count(*) FROM komentarze WHERE akt=a.akt) n_kom FROM akty a ORDER BY akt")
        skroty = {}
        for k, v in ALIASES.items():
            skroty.setdefault(v, []).append(k)
        return [dict(r, skroty=skroty.get(r["akt"], [])) for r in rows]

    def _meta(self, akt: str) -> dict | None:
        r = self.con.execute("SELECT * FROM akty WHERE akt=?", (akt,)).fetchone()
        return dict(r) if r else None

    def artykul(self, akt: str, art: str, komentarz: bool = False, na_dzien: str | None = None) -> dict:
        akt, art = resolve_act(akt), norm_art(art)
        meta = self._meta(akt)
        if not meta:
            return {"status": "OUT_OF_SCOPE", "akt": akt, "powod": "akt spoza korpusu; sprawdź ELI api.sejm.gov.pl"}
        out = {"akt": akt, "art": art, "tytul": meta["tytul"], "tekst_jednolity": meta["tekst_jednolity"]}
        if na_dzien:
            out.update(self._wersja(akt, art, na_dzien))
        else:
            r = self.con.execute("SELECT * FROM artykuly WHERE akt=? AND art=?", (akt, art)).fetchone()
            if not r:
                return dict(out, status="NOT_FOUND", powod=f"brak art. {art} w {akt}")
            out.update(status="FOUND", jednostka=r["jednostka"], tekst=r["tekst"], zrodlo=r["zrodlo"],
                       stan_na=meta["stan_na"], commit=meta["commit_sha"])
            if r["zrodlo"] == "komentarz":
                out["uwaga"] = "brzmienie z komentarza (stan opracowania); potwierdź w ELI przed cytatem"
        if komentarz:
            ks = self.con.execute("SELECT komentarz, plik FROM komentarze WHERE akt=? AND art=?", (akt, art)).fetchall()
            out["komentarz"] = [{"tekst": k["komentarz"], "plik": k["plik"]} for k in ks] or None
        return out

    def _wersja(self, akt: str, art: str, na_dzien: str) -> dict:
        repo = os.path.join(self.law, akt)
        f = law_file(repo) if os.path.isdir(repo) else None
        if not f:
            return {"status": "NOT_CHECKED", "powod": "brak historii git-as-law dla tego aktu"}
        try:
            if git(repo, "rev-parse", "--is-shallow-repository") == "true":
                return {"status": "NOT_CHECKED", "powod": "płytki klon bez historii nowelizacji; pobierz historię: "
                        f"git -C {repo} fetch --unshallow"}
            sha = git(repo, "rev-list", "-1", f"--before={na_dzien} 23:59:59", "HEAD")
            if not sha:
                return {"status": "NOT_FOUND", "powod": f"brak wersji obowiązującej {na_dzien} w historii repo"}
            when = git(repo, "log", "-1", "--format=%cs %s", sha)
            text = git(repo, "show", f"{sha}:{os.path.relpath(f, repo)}")
        except subprocess.CalledProcessError as exc:
            return {"status": "NOT_CHECKED", "powod": "historia niedostępna (płytki klon?): " + exc.stderr.strip()[:200]}
        for a, unit, body in parse_law(text):
            if a == art:
                return {"status": "FOUND", "na_dzien": na_dzien, "wersja": when, "commit": sha, "jednostka": unit,
                        "tekst": body, "zrodlo": "git-as-law"}
        return {"status": "NOT_FOUND", "na_dzien": na_dzien, "wersja": when, "powod": "artykułu nie było w tej wersji"}

    def szukaj(self, q: str, akt: str | None = None, zakres: str | None = None, limit: int = 10) -> list[dict]:
        words = [w for w in re.findall(r"\w+", fold(q)) if w]
        if not words:
            return []
        # odmiana: dla słów od 6 liter ucinamy 2 znaki końcówki i szukamy prefiksu
        terms = ['"' + (w[:-2] if len(w) >= 6 else w) + '"' + ("*" if len(w) >= 4 else "") for w in words]
        sql = "SELECT akt, art, rodzaj, bm25(fts) s FROM fts WHERE fts MATCH ?"
        args: list = [" ".join(terms)]
        if akt:
            sql += " AND akt=?"; args.append(resolve_act(akt))
        if zakres in ("przepisy", "komentarze"):
            sql += " AND rodzaj=?"; args.append("przepis" if zakres == "przepisy" else "komentarz")
        sql += " ORDER BY s LIMIT ?"; args.append(int(limit))
        out = []
        for r in self.con.execute(sql, args):
            if r["rodzaj"] == "przepis":
                t = self.con.execute("SELECT tekst FROM artykuly WHERE akt=? AND art=?", (r["akt"], r["art"])).fetchone()
            else:
                t = self.con.execute("SELECT komentarz tekst FROM komentarze WHERE akt=? AND art=?", (r["akt"], r["art"])).fetchone()
            text = t["tekst"] if t else ""
            out.append({"akt": r["akt"], "art": r["art"], "rodzaj": r["rodzaj"], "fragment": snippet(text, words)})
        return out

    def cytat(self, akt: str, art: str, fragment: str, na_dzien: str | None = None) -> dict:
        a = self.artykul(akt, art, na_dzien=na_dzien)
        if a.get("status") != "FOUND":
            return dict(a, wynik="NOT_CHECKED")
        hay, needle = squash(a["tekst"]), squash(fragment)
        ok = bool(needle) and needle in hay
        return {"wynik": "FOUND" if ok else "NOT_FOUND", "akt": a["akt"], "art": a["art"], "zrodlo": a.get("zrodlo"),
                "stan_na": a.get("stan_na") or a.get("wersja"), "tekst": a["tekst"],
                "uwaga": a.get("uwaga") or ("fragment nie występuje dosłownie w brzmieniu artykułu" if not ok else None)}


def squash(s: str) -> str:
    s = s.replace("\u00a0", " ").replace("\u201e", '"').replace("\u201d", '"').replace("\u201c", '"').replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def snippet(text: str, words: list[str], width: int = 220) -> str:
    f = fold(text)
    pos = min((f.find(w[:-2] if len(w) >= 6 else w) for w in words if (w[:-2] if len(w) >= 6 else w) in f), default=0)
    start = max(0, pos - width // 3)
    s = text[start:start + width].replace("\n", " ")
    return ("…" if start else "") + s + ("…" if start + width < len(text) else "")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--law", default=DEFAULT_LAW)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("buduj")
    sub.add_parser("akty")
    p = sub.add_parser("art"); p.add_argument("akt"); p.add_argument("nr"); p.add_argument("--komentarz", action="store_true"); p.add_argument("--na-dzien")
    p = sub.add_parser("szukaj"); p.add_argument("q"); p.add_argument("--akt"); p.add_argument("--zakres", choices=["przepisy", "komentarze"]); p.add_argument("--limit", type=int, default=10)
    p = sub.add_parser("cytat"); p.add_argument("akt"); p.add_argument("nr"); p.add_argument("fragment"); p.add_argument("--na-dzien")
    a = ap.parse_args(argv)
    if a.cmd == "buduj":
        return build(a.law, a.db)
    b = Baza(a.db, a.law)
    res = {"akty": lambda: b.akty(),
           "art": lambda: b.artykul(a.akt, a.nr, a.komentarz, a.na_dzien),
           "szukaj": lambda: b.szukaj(a.q, a.akt, a.zakres, a.limit),
           "cytat": lambda: b.cytat(a.akt, a.nr, a.fragment, a.na_dzien)}[a.cmd]()
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
