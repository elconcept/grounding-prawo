#!/usr/bin/env python3
"""lexcache - jeden wrapper na polskie i unijne zrodla prawa, z lokalnym cache.

Transport: curl (NIE urllib - w srodowiskach z inspekcja TLS urllib rzuca
CERTIFICATE_VERIFY_FAILED, curl przechodzi). Zaleznosci: tylko stdlib + curl,
opcjonalnie uvx dla krajowych ELI UE.

Cache: pliki .md z frontmatterem YAML, domyslnie ~/.claude/cache/lexcache/.
Frontmatter jest zgodny ze `shared/SCHEMAT-ODPOWIEDZI-MCP.md` (status /
query_type / source / identyfikator / status_obowiazywania / url) plus pola
ksiegowe cache (retrieved_at / expires_at / ttl_days / cache_key).

Uzycie:
    lexcache.py sources [--health]
    lexcache.py isap search --title "Kodeks cywilny" [--type Obwieszczenie]
    lexcache.py isap act DU/2018/1000
    lexcache.py isap text DU/2024/1568 --find "Art. 203."
    lexcache.py saos search --all "kara umowna" --court COMMON
    lexcache.py saos get 352475
    lexcache.py saos case "I ACa 772/13"
    lexcache.py cbosa search "RODO"
    lexcache.py eurlex celex 32016R0679
    lexcache.py eurlex sparql "SELECT ..."
    lexcache.py krs act 0000028860 [--rejestr P]
    lexcache.py nbp rate EUR [--date 2026-09-10]
    lexcache.py sudop nip 5250008195
    lexcache.py ceidg nip 5250008195          # wymaga LEXCACHE_CEIDG_KEY
    lexcache.py eli de tools                  # 9 krajowych ELI przez uvx
    lexcache.py eli de call search_acts '{"query":"BGB"}'

    lexcache.py find "kara umowna" [--source saos] [--field status_obowiazywania=obowiazuje]
    lexcache.py ls [--source isap] [--stale]
    lexcache.py purge --stale [--source isap]

Flagi globalne: --no-cache (pomin odczyt i zapis), --refresh (wymus pobranie),
--json (surowa odpowiedz zrodla na stdout), --ttl N (nadpisz TTL w dniach).
"""
import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import glob
import io
import subprocess
import sys
import time
import urllib.parse

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

UA = "lexcache/1.0 (+local legal-source wrapper)"

# ---------------------------------------------------------------------------
# Gdzie trzymamy dane. Wspolne repozytorium GROUNDING-PRAWO jest widoczne przez
# OneDrive (sync lokalny) i przez SMB. Kolejnosc kandydatow jest swiadoma:
# sprawdzamy KAZDY realnym zapisem I ODCZYTEM, bo `stat`/`touch` potrafia sie
# udac tam, gdzie `read` zwraca EIO (zaobserwowane na /Volumes/GROUNDING-PRAWO:
# 42 z 59 plikow ma poprawny rozmiar w stat, a dd czyta z nich 0 bajtow).
# ---------------------------------------------------------------------------
def _kandydaci():
    """(sciezka, wymaga_markera). Katalog biezacy, projekt Claude, katalog nad skillem
    i podpiety folder sesji Cowork licza sie tylko, gdy wygladaja na baze (maja CACHE/
    i INDEX/) - inaczej lexcache zakladalby CACHE/ tam, skad go akurat wywolano."""
    import glob
    h = os.path.expanduser("~")
    znane = []
    for od in ("OneDrive", "Library/CloudStorage/OneDrive-Personal",
               "Library/CloudStorage/OneDrive-Osobisty"):
        znane += [os.path.join(h, od, "LEGAL", "GROUNDING-PRAWO"), os.path.join(h, od, "GROUNDING-PRAWO")]
    znane += [r"E:\OneDrive\LEGAL\GROUNDING-PRAWO", "/mnt/e/OneDrive/LEGAL/GROUNDING-PRAWO",
              "/Volumes/GROUNDING-PRAWO"]
    z_markerem = [os.getcwd(), os.environ.get("CLAUDE_PROJECT_DIR"),
                  os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))]
    z_markerem += glob.glob("/sessions/*/mnt/*")
    return ([(os.environ.get("GROUNDING_ROOT"), False)] + [(c, True) for c in z_markerem]
            + [(c, False) for c in znane])


GROUNDING_KANDYDACI = _kandydaci()
LOKALNY_FALLBACK = os.path.expanduser("~/.claude/cache/lexcache")
KORPUS_KATALOGI = ["ORZECZENIA", "USTAWY", "OPRACOWANIA", "MAPY"]


def _probe_rw(d):
    """Czy da sie tu ZAPISAC i ODCZYTAC. Sam `isdir`/`touch` nie wystarcza."""
    try:
        os.makedirs(d, exist_ok=True)
        t = os.path.join(d, ".lexcache-probe")
        with open(t, "wb") as f:
            f.write(b"lexcache")
        with open(t, "rb") as f:
            ok = f.read() == b"lexcache"
        os.remove(t)
        return ok
    except Exception:
        return False


def _resolve():
    """Zwraca (grounding_root_lub_None, cache_dir, powod)."""
    forced = os.environ.get("LEXCACHE_DIR")
    if forced:
        d = os.path.expanduser(forced)
        return (None, d, "LEXCACHE_DIR wymuszone w srodowisku")
    for cand, marker in GROUNDING_KANDYDACI:
        if not cand:
            continue
        cand = os.path.expanduser(cand)
        if not os.path.isdir(cand):
            continue
        if marker and not (os.path.isdir(os.path.join(cand, "CACHE"))
                           and os.path.isdir(os.path.join(cand, "INDEX"))):
            continue
        c = os.path.join(cand, "CACHE")
        if _probe_rw(c):
            return (cand, c, "wspolne repozytorium: " + cand)
        sys.stderr.write("[lexcache] %s odpada - katalog istnieje, ale nie przechodzi "
                         "testu zapis+odczyt\n" % cand)
    return (None, LOKALNY_FALLBACK, "brak dostepnego GROUNDING-PRAWO - cache lokalny")


GROUNDING_ROOT, CACHE_DIR, CACHE_POWOD = _resolve()

# ---------------------------------------------------------------------------
# Rejestr zrodel. ttl w dniach; None = brak wygasania (nie stosowane).
# `normatyw` = czy zrodlo jest zrodlem prawa (vs rejestr faktyczny).
# ---------------------------------------------------------------------------
SOURCES = {
    "isap":   dict(nazwa="Sejm ELI - Dziennik Ustaw + Monitor Polski",
                   host="api.sejm.gov.pl/eli", normatyw=True, klucz=False,
                   ttl={"search": 7, "act": 30, "text": 90, "pdf": 90}, pii="low"),
    "saos":   dict(nazwa="SAOS - sady powszechne, SN, TK, KIO",
                   host="www.saos.org.pl/api", normatyw=True, klucz=False,
                   ttl={"search": 3, "get": 180, "case": 30}, pii="high"),
    "cbosa":  dict(nazwa="CBOSA - NSA + 16 WSA (orzeczenia spoza SAOS)",
                   host="orzeczenia.nsa.gov.pl", normatyw=True, klucz=False,
                   ttl={"search": 7}, pii="high"),
    "eurlex": dict(nazwa="EUR-Lex / CELLAR - prawo UE + TSUE",
                   host="publications.europa.eu", normatyw=True, klucz=False,
                   ttl={"celex": 30, "sparql": 14}, pii="low"),
    "krs":    dict(nazwa="KRS - Krajowy Rejestr Sadowy (Otwarte API)",
                   host="api-krs.ms.gov.pl", normatyw=False, klucz=False,
                   ttl={"act": 1, "full": 1}, pii="high"),
    "nbp":    dict(nazwa="NBP - kursy walut",
                   host="api.nbp.pl", normatyw=False, klucz=False,
                   ttl={"rate": 1}, pii="low"),
    "sudop":  dict(nazwa="SUDOP / UOKiK - pomoc publiczna",
                   host="api-sudop.uokik.gov.pl", normatyw=False, klucz=False,
                   ttl={"nip": 7}, pii="high"),
    "ceidg":  dict(nazwa="CEIDG - jednoosobowe dzialalnosci",
                   host="dane.biznes.gov.pl", normatyw=False, klucz=True,
                   ttl={"nip": 1}, pii="high"),
    "eli":    dict(nazwa="Krajowe ELI UE (de/at/es/fi/ie/nl/se/fr/lu) przez uvx",
                   host="uvx <cc>-eli-mcp", normatyw=True, klucz=False,
                   ttl={"tools": 30, "call": 14}, pii="low"),
}
ELI_KRAJE = ["de", "at", "es", "fi", "ie", "nl", "se", "fr", "lu"]


# ---------------------------------------------------------------------------
# HTTP przez curl
# ---------------------------------------------------------------------------
def http(url, params=None, accept="application/json", timeout=40, headers=None):
    cmd = ["curl", "-s", "-S", "--max-time", str(timeout), "-A", UA,
           "-H", "Accept: " + accept, "-w", "\n__HTTP__%{http_code}"]
    for k, v in (headers or {}).items():
        cmd += ["-H", "%s: %s" % (k, v)]
    if params:
        cmd.append("--get")
        for k, v in params:
            if v is None:
                continue
            cmd += ["--data-urlencode", "%s=%s" % (k, v)]
    cmd.append(url)
    p = subprocess.run(cmd, capture_output=True)
    body = p.stdout.decode("utf-8", "replace")
    code = 0
    m = re.search(r"__HTTP__(\d+)\s*$", body)
    if m:
        code = int(m.group(1))
        body = body[: m.start()]
    if p.returncode != 0 and not body:
        raise RuntimeError("curl: " + p.stderr.decode("utf-8", "replace").strip())
    return code, body


def http_json(url, params=None, **kw):
    code, body = http(url, params, **kw)
    try:
        return code, json.loads(body)
    except json.JSONDecodeError:
        return code, {"_raw": body}


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
def _now():
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0)


def cache_key(source, op, args):
    canon = json.dumps([source, op, args], sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(canon.encode("utf-8")).hexdigest()[:16]


def cache_path(source, key):
    return os.path.join(CACHE_DIR, source, key + ".md")


def _yaml_scalar(v):
    if v is None:
        return '""'
    s = str(v).replace("\r", " ").replace("\n", " ").strip()
    if s == "":
        return '""'
    if re.search(r'[:#\-\[\]{}"\'&*!|>%@`]', s) or s.lower() in ("true", "false", "null"):
        return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return s


def write_cache(source, key, meta, body):
    p = cache_path(source, key)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    lines = ["---"]
    for k, v in meta.items():
        if isinstance(v, list):
            # flow-style: parser frontmatteru czyta linia-po-linii, wiec forma
            # blokowa gubilaby cale listy przy odczycie (i przy `find`).
            lines.append("%s: [%s]" % (k, ", ".join(_yaml_scalar(x) for x in v)))
        else:
            lines.append("%s: %s" % (k, _yaml_scalar(v)))
    lines += ["---", ""]
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + body.rstrip() + "\n")
    return p


def parse_frontmatter(path):
    meta, body_at = {}, 0
    try:
        with open(path, encoding="utf-8") as f:
            txt = f.read()
    except OSError:
        return {}, ""
    if not txt.startswith("---\n"):
        return {}, txt
    end = txt.find("\n---\n", 4)
    if end < 0:
        return {}, txt
    for line in txt[4:end].split("\n"):
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            v = m.group(2).strip()
            if len(v) > 1 and v[0] == '"' and v[-1] == '"':
                v = v[1:-1].replace('\\"', '"')
            meta[m.group(1)] = v
    body_at = end + 5
    return meta, txt[body_at:]


def is_stale(meta):
    exp = meta.get("expires_at")
    if not exp:
        return False
    try:
        d = _dt.datetime.fromisoformat(exp.replace("Z", "+00:00"))
    except ValueError:
        return False
    return d < _now()


def read_cache(source, key):
    p = cache_path(source, key)
    if not os.path.exists(p):
        return None
    meta, body = parse_frontmatter(p)
    return {"meta": meta, "body": body, "path": p}


# ---------------------------------------------------------------------------
# Normalizacja -> frontmatter (SCHEMAT-ODPOWIEDZI-MCP + kontrakt citations)
# ---------------------------------------------------------------------------
def base_meta(source, op, query, ttl_days, extra=None):
    now = _now()
    m = {
        "status": "FOUND",
        "query_type": "inne",
        "source": source,
        "tool": "%s.%s" % (source, op),
        "query": query,
        "identyfikator": "",
        "tytul": "",
        "status_obowiazywania": "nieznany",
        "data": "",
        "url": "",
        "retrieved_at": now.isoformat().replace("+00:00", "Z"),
        "expires_at": (now + _dt.timedelta(days=ttl_days)).isoformat().replace("+00:00", "Z"),
        "ttl_days": ttl_days,
        "confidence": "deterministic",
        "pii_risk": SOURCES[source]["pii"],
        "cache_key": "",
    }
    m.update(extra or {})
    return m


ISAP_STATUS = {
    "obowiązujący": "obowiazuje", "akt posiada tekst jednolity": "obowiazuje",
    "uchylony": "uchylony", "wygaśnięcie aktu": "uchylony",
}


def norm_isap(op, data, meta):
    meta["query_type"] = "akt_prawny"
    if isinstance(data, dict) and data.get("_error"):
        meta["status"] = "ERROR"
        meta["error_code"] = data["_error"]
        meta["eli"] = data.get("ELI", "")
        meta["identyfikator"] = data.get("ELI", "")
        if data.get("pdf_lokalnie"):
            meta["pdf_lokalnie"] = data["pdf_lokalnie"]
        if op == "pdf":
            # nawet przy bledzie niesiemy werdykt o wersji tekstu - SKILL.md
            # obiecuje, ze `text_version` jest zawsze obecne przy `isap pdf`
            meta["zrodlo_tekstu"] = "pdf"
            meta["text_version"] = data.get("text_version") or "nieznana"
            if data.get("uzyj_zamiast"):
                meta["uzyj_zamiast"] = data["uzyj_zamiast"]
        if data["_error"] == "text_unavailable_use_pdf":
            meta["tytul"] = "tresc tylko w PDF - HTML niedostepny"
            meta["pdf_url"] = ("https://api.sejm.gov.pl/eli/acts/%s/text.pdf"
                               % data.get("ELI", "").strip("/"))
            meta["uwaga"] = ("uzyj `isap pdf <ELI> --find \"Art. N.\"` - wyciagnie tresc "
                             "wprost z PDF obowiazujacego tekstu jednolitego")
        else:
            meta["tytul"] = "brak frazy w tekscie aktu"
        if data.get("alternatywy"):
            meta["teksty_jednolite"] = data["alternatywy"]
        return meta
    if op == "search":
        items = data.get("items", []) if isinstance(data, dict) else []
        meta["status"] = "FOUND" if items else "NOT_FOUND"
        meta["identyfikator"] = "%d trafien" % (data.get("totalCount") or len(items))
        meta["eli_list"] = [i.get("ELI", "") for i in items[:20]]
        if items:
            meta["tytul"] = items[0].get("title", "")[:200]
    else:
        if data.get("zrodlo_tekstu") == "pdf":
            tv = data.get("text_version") or "nieznana"
            meta["zrodlo_tekstu"] = "pdf"
            meta["text_version"] = tv
            meta["pdf_lokalnie"] = data.get("pdf_lokalnie", "")
            meta["tytul"] = (data.get("title") or "")[:300]
            meta["data"] = data.get("promulgation") or ""
            meta["in_force"] = data.get("inForce") or ""
            if tv == "tekst_jednolity":
                meta["status_obowiazywania"] = ISAP_STATUS.get(
                    (data.get("status") or "").strip().lower(), "nieznany")
                meta["uwaga"] = ("tresc z PDF tekstu jednolitego - zweryfikuj fragment "
                                 "wzrokowo przed cytowaniem doslownym w pismie")
            else:
                # Brzmienie pierwotne aktu bazowego NIE moze wygladac na aktualne.
                meta["status"] = "AMBIGUOUS"
                meta["status_obowiazywania"] = "nieznany"
                meta["uwaga"] = (data.get("_ostrzezenie")
                                 or "to nie jest tekst jednolity - brzmienie moze byc nieaktualne")
                if data.get("uzyj_zamiast"):
                    meta["uzyj_zamiast"] = data["uzyj_zamiast"]
        eli = data.get("ELI") or ""
        meta["identyfikator"] = eli
        meta["eli"] = eli
        meta["tytul"] = (data.get("title") or "")[:300]
        meta["data"] = data.get("promulgation") or data.get("announcementDate") or ""
        meta["in_force"] = data.get("inForce") or ""
        meta["typ_aktu"] = data.get("type") or ""
        meta["status_obowiazywania"] = ISAP_STATUS.get(
            (data.get("status") or "").strip().lower(), "nieznany")
        meta["ma_html"] = data.get("textHTML")
        meta["ma_pdf"] = data.get("textPDF")
        refs = (data.get("references") or {})
        for k, v in refs.items():
            if "tek" in k.lower() and "jednolit" in k.lower():
                ids = [e.get("id") or (e.get("act") or {}).get("ELI") for e in v]
                meta["teksty_jednolite"] = [x for x in ids if x][:12]
                break
        if eli:
            meta["url"] = "https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=" + eli
        if meta.get("status") == "AMBIGUOUS":
            # PDF aktu bazowego: sam akt obowiazuje, ale TO BRZMIENIE juz nie.
            # Enum ze SCHEMAT-ODPOWIEDZI-MCP, ktory blokuje bramke MCP-VERIFIED.
            meta["status_obowiazywania"] = "tekst_jednolity_nieaktualny"
        else:
            meta["status"] = "FOUND" if eli else "NOT_FOUND"
    return meta


def norm_saos(op, data, meta):
    meta["query_type"] = "orzeczenie"
    if op in ("search", "case"):
        items = data.get("items", []) if isinstance(data, dict) else []
        meta["status"] = "FOUND" if items else "NOT_FOUND"
        meta["identyfikator"] = "%d trafien na stronie" % len(items)
        sygn, ids = [], []
        for i in items[:20]:
            cc = i.get("courtCases") or [{}]
            sygn.append(cc[0].get("caseNumber", ""))
            ids.append(str(i.get("id", "")))
        meta["sygnatury"] = [s for s in sygn if s]
        meta["saos_ids"] = ids
        if items:
            meta["data"] = items[0].get("judgmentDate", "")
            meta["court_type"] = items[0].get("courtType", "")
    else:
        d = data.get("data", data) if isinstance(data, dict) else {}
        cc = (d.get("courtCases") or [{}])[0]
        meta["identyfikator"] = cc.get("caseNumber", "")
        meta["sygnatura"] = cc.get("caseNumber", "")
        meta["saos_id"] = d.get("id", "")
        meta["data"] = d.get("judgmentDate", "")
        meta["court_type"] = d.get("courtType", "")
        meta["judgment_type"] = d.get("judgmentType", "")
        meta["url"] = "https://www.saos.org.pl/judgments/%s" % d.get("id", "")
        meta["tytul"] = "%s - %s" % (meta["identyfikator"], meta["court_type"])
        meta["status"] = "FOUND" if d.get("id") else "NOT_FOUND"
        meta["uwaga_ocr"] = "daty w SAOS bywaja znieksztalcone przez OCR - zweryfikuj w zrodle"
    return meta


def _pusto(data):
    if not data:
        return True
    if isinstance(data, dict):
        if "_raw" in data and not str(data["_raw"]).strip():
            return True
        if data.get("error"):
            return False
        if not any(v for k, v in data.items() if not k.startswith("_")):
            return "_raw" not in data
    return False


def norm_generic(op, data, meta, qtype="inne", http_code=200):
    meta["query_type"] = qtype
    meta["http"] = http_code
    if http_code >= 400 or (isinstance(data, dict) and data.get("error")):
        meta["status"] = "ERROR"
        err = (data or {}).get("error") if isinstance(data, dict) else None
        if isinstance(err, dict):
            meta["tytul"] = str(err.get("error-reason") or err.get("error-result") or "")[:200]
    elif _pusto(data):
        meta["status"] = "NOT_FOUND"
        meta["tytul"] = "brak wynikow dla tego zapytania"
    else:
        meta["status"] = "FOUND"
    return meta


# ---------------------------------------------------------------------------
# Adaptery zrodel: zwracaja (raw_obj_or_text, meta_patch_fn, url, op_ttl_key)
# ---------------------------------------------------------------------------
def fetch_isap(op, a):
    B = "https://api.sejm.gov.pl/eli"
    if op == "search":
        params = [("title", a.title), ("publisher", a.publisher), ("type", a.type),
                  ("limit", a.limit)]
        if a.year:
            params.append(("year", a.year))
        if a.in_force:
            params.append(("inForce", "1"))
        code, d = http_json(B + "/acts/search", params)
        return d, norm_isap, B + "/acts/search", "search"
    if op == "act":
        code, d = http_json("%s/acts/%s" % (B, a.eli.strip("/")))
        return d, norm_isap, "%s/acts/%s" % (B, a.eli), "act"
    if op == "text":
        url = "%s/acts/%s/text.html" % (B, a.eli.strip("/"))
        code, html = http(url, accept="text/html", timeout=90)
        if code != 200 or not html.strip():
            alt = []
            try:
                _, meta_act = http_json("%s/acts/%s" % (B, a.eli.strip("/")))
                refs = meta_act.get("references") or {}
                baza = []
                for k, v in refs.items():
                    kl = k.lower()
                    ids = [e.get("id") or (e.get("act") or {}).get("ELI") for e in v]
                    ids = [x for x in ids if x]
                    if kl.startswith("inf. o tek"):
                        alt = ids[:10]
                    elif "tekst jednolity dla aktu" in kl:
                        baza = ids[:1]
                if not alt and baza:
                    _, m2 = http_json("%s/acts/%s" % (B, baza[0]))
                    for k, v in (m2.get("references") or {}).items():
                        if k.lower().startswith("inf. o tek"):
                            ids = [e.get("id") or (e.get("act") or {}).get("ELI") for e in v]
                            alt = [x for x in ids if x][:10]
                            break
            except Exception:
                pass
            return ({"_error": "text_unavailable_use_pdf", "ELI": a.eli, "http": code,
                     "pdf": "%s/acts/%s/text.pdf" % (B, a.eli.strip("/")),
                     "alternatywy": alt,
                     "wskazowka": "sprobuj kolejnego tekstu jednolitego z listy - pierwszy "
                                  "z wersja HTML zwroci tresc (bedzie NIEAKTUALNY, podaj date)"},
                    norm_isap, url, "text")
        plain = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", html, flags=re.I)
        plain = re.sub(r"<[^>]+>", " ", plain)
        plain = (plain.replace("&nbsp;", " ").replace("&amp;", "&")
                 .replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"'))
        plain = re.sub(r"\s+", " ", plain).strip()
        if a.find:
            i = plain.find(a.find)
            if i < 0:
                return ({"_error": "not_found", "szukane": a.find, "ELI": a.eli},
                        norm_isap, url, "text")
            plain = plain[max(0, i - 200): i + 4000]
        return ({"ELI": a.eli, "text": plain, "len": len(plain)}, norm_isap, url, "text")
    if op == "pdf":
        eli = a.eli.strip("/")
        url = "%s/acts/%s/text.pdf" % (B, eli)
        pdf_dir = os.path.join(CACHE_DIR, "isap", "_pdf")
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_p = os.path.join(pdf_dir, eli.replace("/", "_") + ".pdf")
        # PDF lezy obok wpisu .md, ale ma wlasne zycie: purge kasuje .md i bez
        # tego testu osierocony plik serwowalby sie w nieskonczonosc jako swiezy.
        swiezy = (os.path.exists(pdf_p) and os.path.getsize(pdf_p) >= 1000
                  and (time.time() - os.path.getmtime(pdf_p))
                  < SOURCES["isap"]["ttl"]["pdf"] * 86400)
        if getattr(a, "refresh", False) or not swiezy:
            # pobieramy do pliku tymczasowego i podmieniamy dopiero po walidacji,
            # zeby urwane pobranie nie zatrulo cache na 90 dni
            tmp_p = pdf_p + ".part"
            r = subprocess.run(["curl", "-sSL", "--max-time", "300", "--retry", "2",
                                "-A", UA, "-o", tmp_p, url], capture_output=True)
            ok = r.returncode == 0 and os.path.exists(tmp_p) and os.path.getsize(tmp_p) > 1000
            if ok:
                with open(tmp_p, "rb") as f:
                    ok = f.read(5).startswith(b"%PDF")
            if not ok:
                detal = (r.stderr.decode("utf-8", "replace")[:200] or
                         "pobrano %s B, to nie jest PDF"
                         % (os.path.getsize(tmp_p) if os.path.exists(tmp_p) else 0))
                if os.path.exists(tmp_p):
                    os.remove(tmp_p)
                return ({"_error": "upstream_error", "ELI": a.eli, "detal": detal,
                         "pdf_url": url}, norm_isap, url, "pdf")
            os.replace(tmp_p, pdf_p)
        if not shutil.which("mutool"):
            return ({"_error": "brak_mutool", "ELI": a.eli, "pdf_lokalnie": pdf_p,
                     "wskazowka": "zainstaluj mupdf-tools (mutool) albo przeczytaj "
                                  "pobrany PDF natywnym Read / skillem mac-ocr"},
                    norm_isap, url, "pdf")
        r = subprocess.run(["mutool", "draw", "-F", "txt", "-o", "-", pdf_p],
                           capture_output=True, timeout=240)
        txt = r.stdout.decode("utf-8", "replace")
        txt = re.sub(r"\s+", " ", txt).strip()
        # PDF-y ISAP lamia wyrazy myslnikiem na koncu wiersza
        txt = re.sub(r"([a-ząćęłńóśźż])-\s+([a-ząćęłńóśźż])", r"\1\2", txt)
        if not txt:
            return ({"_error": "brak_warstwy_tekstu", "ELI": a.eli, "pdf_lokalnie": pdf_p,
                     "wskazowka": "PDF bez warstwy tekstu - uzyj OCR (skill mac-ocr)"},
                    norm_isap, url, "pdf")
        out = {"ELI": a.eli, "zrodlo_tekstu": "pdf", "pdf_lokalnie": pdf_p,
               "pdf_url": url, "len": len(txt)}
        try:                       # tytul, status i WERSJA TEKSTU z metadanych aktu
            _, ma = http_json("%s/acts/%s" % (B, eli))
            out["title"] = ma.get("title")
            out["status"] = ma.get("status")
            out["inForce"] = ma.get("inForce")
            out["promulgation"] = ma.get("promulgation")
            # Kluczowe rozroznienie: PDF aktu BAZOWEGO to brzmienie PIERWOTNE,
            # a nie tekst jednolity. Odroznia je klucz w `references`.
            jest_tj, nowsze = False, []
            for k, v in (ma.get("references") or {}).items():
                kl = k.lower()
                if "tekst jednolity dla aktu" in kl:
                    jest_tj = True
                elif kl.startswith("inf. o tek"):
                    nowsze = [e.get("id") or (e.get("act") or {}).get("ELI") for e in v]
                    nowsze = [x for x in nowsze if x][:10]
            if jest_tj:
                out["text_version"] = "tekst_jednolity"
            elif nowsze:
                out["text_version"] = "tekst_ogloszony_istnieje_nowszy_jednolity"
                out["uzyj_zamiast"] = nowsze
                out["_ostrzezenie"] = (
                    "To PDF aktu BAZOWEGO - brzmienie PIERWOTNE z dnia ogloszenia, "
                    "NIE stan na dzis. Powtorz z najnowszym tekstem jednolitym: "
                    "isap pdf %s" % nowsze[0])
            else:
                out["text_version"] = "tekst_ogloszony"
        except Exception:
            out["text_version"] = "nieznana"
        if a.find:
            i = txt.find(a.find)
            if i < 0:
                out["_error"] = "not_found"
                out["szukane"] = a.find
                out["wskazowka"] = ("sprawdz pisownie z polskimi znakami i kropke po numerze; "
                                    "artykuly z indeksem gornym wychodza z PDF jako "
                                    "\"Art. 205[1]\", a nie \"Art. 205\u00b9\"")
            else:
                out["text"] = txt[max(0, i - 200): i + 4000]
        else:
            out["text"] = txt[:12000]
            out["uciety"] = len(txt) > 12000
        return out, norm_isap, url, "pdf"
    raise SystemExit("isap: nieznana operacja " + op)


def fetch_saos(op, a):
    B = "https://www.saos.org.pl/api"
    if op in ("search", "case"):
        params = [("pageSize", a.size), ("pageNumber", a.page)]
        if op == "case":
            params.append(("caseNumber", a.case))
        else:
            for k, v in (("all", a.all), ("caseNumber", a.case), ("courtType", a.court),
                         ("judgeName", a.judge), ("legalBase", a.legalbase),
                         ("referencedRegulation", a.regulation),
                         ("judgmentDateFrom", a.date_from), ("judgmentDateTo", a.date_to)):
                if v:
                    params.append((k, v))
        code, d = http_json(B + "/search/judgments", params)
        return d, norm_saos, B + "/search/judgments", op
    if op == "get":
        code, d = http_json("%s/judgments/%s" % (B, a.id))
        return d, norm_saos, "https://www.saos.org.pl/judgments/%s" % a.id, "get"
    raise SystemExit("saos: nieznana operacja " + op)


def fetch_cbosa(op, a):
    url = "https://orzeczenia.nsa.gov.pl/cbo/find"
    code, html = http(url, [("p", "1"), ("btnSubmit", "Szukaj"), ("word", a.query)],
                      accept="text/html", timeout=60)
    plain = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", html, flags=re.I)
    links = re.findall(r'href="(/doc/[A-F0-9]+)"[^>]*>([^<]{3,120})<', plain)
    txt = re.sub(r"<[^>]+>", " ", plain)
    txt = re.sub(r"\s+", " ", txt).strip()

    def norm(op_, data, meta):
        meta["query_type"] = "orzeczenie"
        meta["status"] = "FOUND" if links else "NOT_FOUND"
        meta["identyfikator"] = "%d linkow do orzeczen" % len(links)
        meta["sygnatury"] = [t.strip() for _, t in links[:20]]
        meta["url"] = "https://orzeczenia.nsa.gov.pl/cbo/find?word=" + urllib.parse.quote(a.query)
        meta["uwaga"] = "CBOSA nie ma REST API - to scrape HTML; po serii zapytan pojawia sie captcha"
        return meta
    return ({"http": code, "linki": ["https://orzeczenia.nsa.gov.pl" + h for h, _ in links],
             "tekst": txt[:6000]}, norm, url, "search")


def fetch_eurlex(op, a):
    EP = "https://publications.europa.eu/webapi/rdf/sparql"
    if op == "celex":
        q = ("PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> "
             "SELECT ?work ?date ?title WHERE { ?work cdm:resource_legal_id_celex ?c . "
             "FILTER(str(?c)='%s') OPTIONAL{?work cdm:work_date_document ?date} "
             "OPTIONAL{?e cdm:expression_belongs_to_work ?work; "
             "cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/%s>; "
             "cdm:expression_title ?title} } LIMIT 5"
             % (a.celex.replace("'", ""), (a.lang or "POL").upper()))
    else:
        q = a.query
    code, d = http_json(EP, [("query", q), ("format", "application/sparql-results+json")],
                        accept="application/sparql-results+json", timeout=90)

    def norm(op_, data, meta):
        meta["query_type"] = "akt_prawny"
        b = (((data or {}).get("results") or {}).get("bindings") or [])
        meta["status"] = "FOUND" if b else "NOT_FOUND"
        meta["identyfikator"] = getattr(a, "celex", "") or "SPARQL"
        if getattr(a, "celex", ""):
            meta["celex"] = a.celex
            meta["url"] = "https://eur-lex.europa.eu/legal-content/PL/TXT/?uri=CELEX:" + a.celex
        if b:
            meta["tytul"] = (b[0].get("title", {}) or {}).get("value", "")[:300]
            meta["data"] = (b[0].get("date", {}) or {}).get("value", "")
        return meta
    return d, norm, EP, op


def fetch_krs(op, a):
    kind = "OdpisPelny" if op == "full" else "OdpisAktualny"
    krs = a.krs.zfill(10)
    url = "https://api-krs.ms.gov.pl/api/krs/%s/%s" % (kind, krs)
    code, d = http_json(url, [("rejestr", a.rejestr), ("format", "json")], timeout=60)

    def norm(op_, data, meta):
        meta["query_type"] = "podmiot"
        o = (data or {}).get("odpis") or {}
        nag = o.get("naglowekA") or {}
        dane = ((o.get("dane") or {}).get("dzial1") or {}).get("danePodmiotu") or {}
        meta["status"] = "FOUND" if nag else "NOT_FOUND"
        meta["identyfikator"] = "KRS " + (nag.get("numerKRS") or krs)
        meta["krs"] = nag.get("numerKRS") or krs
        meta["tytul"] = (dane.get("nazwa") or "")[:200]
        meta["data"] = nag.get("stanZDnia") or ""
        meta["rejestr"] = nag.get("rejestr") or a.rejestr
        meta["url"] = "https://prs.ms.gov.pl/krs/podglad-informacji-aktualnej"
        meta["uwaga"] = "odpis to snapshot - cytuj z data stanu"
        return meta
    return d, norm, url, op


def fetch_nbp(op, a):
    seg = a.date or ""
    url = "https://api.nbp.pl/api/exchangerates/rates/a/%s/%s" % (a.code.lower(), seg)
    code, d = http_json(url.rstrip("/"), [("format", "json")], timeout=30)

    def norm(op_, data, meta):
        r = ((data or {}).get("rates") or [{}])[0]
        meta["query_type"] = "kurs"
        meta["status"] = "FOUND" if r.get("mid") is not None else "NOT_FOUND"
        meta["identyfikator"] = "%s %s" % (a.code.upper(), r.get("effectiveDate", ""))
        meta["tytul"] = "%s = %s PLN" % (a.code.upper(), r.get("mid", ""))
        meta["data"] = r.get("effectiveDate", "")
        meta["url"] = "https://api.nbp.pl/"
        return meta
    return d, norm, url, "rate"


def fetch_sudop(op, a):
    url = "https://api-sudop.uokik.gov.pl/sudop-api/api/przypadki-pomocy"
    code, d = http_json(url, [("nip-beneficjenta", a.nip)], timeout=60)
    return (d, (lambda o, dd, m, c=code: norm_generic(o, dd, m, "pomoc_publiczna", c)),
            url, "nip")


def fetch_ceidg(op, a):
    key = os.environ.get("LEXCACHE_CEIDG_KEY")
    if not key:
        raise SystemExit("ceidg: brak klucza API - ustaw LEXCACHE_CEIDG_KEY "
                         "(bezplatny wniosek na dane.biznes.gov.pl)")
    url = "https://dane.biznes.gov.pl/api/ceidg/v2/firmy"
    code, d = http_json(url, [("nip", a.nip)],
                        headers={"Authorization": "Bearer " + key}, timeout=60)
    return d, (lambda o, dd, m, c=code: norm_generic(o, dd, m, "podmiot", c)), url, "nip"


def fetch_eli(op, a):
    if not shutil.which("uvx"):
        raise SystemExit("eli: brak uvx w PATH (zainstaluj uv: https://docs.astral.sh/uv/)")
    if a.country not in ELI_KRAJE:
        raise SystemExit("eli: kraj musi byc jednym z: " + ", ".join(ELI_KRAJE))
    pkg = "%s-eli-mcp" % a.country
    msgs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize",
             "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                        "clientInfo": {"name": "lexcache", "version": "1.0"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"}]
    if op == "tools":
        msgs.append({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    else:
        try:
            args = json.loads(a.args or "{}")
        except json.JSONDecodeError as e:
            raise SystemExit("eli: --args musi byc poprawnym JSON-em: %s" % e)
        msgs.append({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                     "params": {"name": a.tool, "arguments": args}})
    proc = subprocess.Popen(["uvx", pkg], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err_tail = None, ""
    try:
        # Serwery FastMCP koncza sie, gdy stdin zostanie zamkniete zanim
        # przetworza kolejke - dlatego piszemy po jednej wiadomosci i
        # czekamy na odpowiedz, trzymajac potok otwarty.
        for m in msgs:
            proc.stdin.write((json.dumps(m) + "\n").encode("utf-8"))
            proc.stdin.flush()
            if "id" not in m:
                continue
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                line = line.decode("utf-8", "replace").strip()
                if not line:
                    continue
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if o.get("id") == m["id"]:
                    if m["id"] == 2:
                        out = o
                    break
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
        try:
            err_tail = proc.stderr.read().decode("utf-8", "replace")[-400:]
        except Exception:
            err_tail = ""
    if out is None:
        raise SystemExit("eli/%s: brak odpowiedzi. stderr: %s" % (pkg, err_tail))
    d = out.get("result", out)

    def norm(op_, data, meta):
        meta["query_type"] = "akt_prawny"
        meta["status"] = "ERROR" if out.get("error") else "FOUND"
        meta["identyfikator"] = "%s/%s" % (a.country, op if op == "tools" else a.tool)
        meta["jurysdykcja"] = a.country.upper()
        meta["pakiet"] = pkg
        if a.country == "fr":
            meta["uwaga"] = "fr-eli wymaga darmowych danych dostepowych PISTE"
        return meta
    return d, norm, "uvx " + pkg, op


FETCHERS = {"isap": fetch_isap, "saos": fetch_saos, "cbosa": fetch_cbosa,
            "eurlex": fetch_eurlex, "krs": fetch_krs, "nbp": fetch_nbp,
            "sudop": fetch_sudop, "ceidg": fetch_ceidg, "eli": fetch_eli}


# ---------------------------------------------------------------------------
# Rdzen: pobierz z cache lub ze zrodla
# ---------------------------------------------------------------------------
def run_fetch(source, op, a):
    ident = {k: v for k, v in vars(a).items()
             if k not in ("func", "source", "op", "no_cache", "refresh", "json", "ttl")}
    key = cache_key(source, op, ident)
    hit = None if (a.no_cache or a.refresh) else read_cache(source, key)

    if hit:
        stale = is_stale(hit["meta"])
        if stale:
            print("[UWAGA] wpis w cache WYGASL (expires_at=%s). Uzyj --refresh po swieze dane."
                  % hit["meta"].get("expires_at"), file=sys.stderr)
        print("[cache] %s" % hit["path"], file=sys.stderr)
        if a.json:
            m = re.search(r"```json\n([\s\S]*?)\n```", hit["body"])
            sys.stdout.write(m.group(1) if m else hit["body"])
        else:
            sys.stdout.write(hit["body"])
        return 0 if not stale else 3

    data, normfn, url, ttlkey = FETCHERS[source](op, a)
    ttl = a.ttl if a.ttl is not None else SOURCES[source]["ttl"].get(ttlkey, 7)
    if isinstance(data, dict) and data.get("_error") and a.ttl is None:
        ttl = 1          # bledu nie trzymamy dlugo - zrodlo moze wrocic
    meta = base_meta(source, op, json.dumps(ident, ensure_ascii=False, sort_keys=True), ttl)
    meta["cache_key"] = key
    meta = normfn(op, data, meta)
    if meta.get("status") == "ERROR" and a.ttl is None and ttl > 1:
        ttl = 1                      # bledu zrodla nie trzymamy dlugo
        meta["ttl_days"] = 1
        meta["expires_at"] = (_now() + _dt.timedelta(days=1)) \
            .isoformat().replace("+00:00", "Z")
    if not meta.get("url"):
        meta["url"] = url

    if isinstance(data, str):
        body = data
    else:
        body = "```json\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n```\n"

    if a.json:
        sys.stdout.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write("# %s\n\n" % (meta.get("tytul") or meta.get("identyfikator") or op))
        sys.stdout.write("status=%s  zrodlo=%s  url=%s\n\n" % (meta["status"], source, meta["url"]))
        sys.stdout.write(body)

    if not a.no_cache:
        p = write_cache(source, key, meta, body)
        print("[zapisano] %s (TTL %sd)" % (p, ttl), file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# Operacje na cache
# ---------------------------------------------------------------------------
def iter_cache(source=None, korpus=True):
    """Pliki cache, a domyslnie takze recznie kurowany korpus GROUNDING-PRAWO."""
    roots = [os.path.join(CACHE_DIR, source) if source else CACHE_DIR]
    if korpus and GROUNDING_ROOT and not source:
        roots += [os.path.join(GROUNDING_ROOT, k) for k in KORPUS_KATALOGI]
    for root in roots:
        for dirpath, _, files in os.walk(root):
            for fn in sorted(files):
                if fn.endswith(".md"):
                    yield os.path.join(dirpath, fn)


def _fts_path():
    # Indeks poza folderem synchronizowanym: SQLite na OneDrive/SMB to proszenie sie
    # o konflikty miedzy hostami. Plik mozna w kazdej chwili skasowac - odbuduje sie.
    tag = hashlib.sha1(os.path.abspath(CACHE_DIR).encode("utf-8")).hexdigest()[:10]
    return os.path.join(os.path.expanduser("~/.cache/lexcache"), "fts-%s.sqlite" % tag)


def fts_sync(files, pelny):
    """G2: indeks SQLite FTS5 (korpus + cache), aktualizowany przyrostowo po mtime."""
    import sqlite3
    p = _fts_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    db = sqlite3.connect(p)
    db.execute("CREATE TABLE IF NOT EXISTS pliki(path TEXT PRIMARY KEY, mtime REAL)")
    db.execute("CREATE VIRTUAL TABLE IF NOT EXISTS fts USING fts5(path UNINDEXED, meta, body, "
               "tokenize='unicode61 remove_diacritics 2')")
    known = dict(db.execute("SELECT path, mtime FROM pliki"))
    seen = set()
    for f in files:
        seen.add(f)
        try:
            m = os.path.getmtime(f)
        except OSError:
            continue
        if known.get(f) == m:
            continue
        meta, body = parse_frontmatter(f)
        db.execute("DELETE FROM fts WHERE path=?", (f,))
        db.execute("INSERT INTO fts(path, meta, body) VALUES (?,?,?)",
                   (f, " ".join("%s %s" % kv for kv in meta.items()), body))
        db.execute("INSERT OR REPLACE INTO pliki VALUES (?,?)", (f, m))
    if pelny:
        for f in set(known) - seen:
            db.execute("DELETE FROM fts WHERE path=?", (f,))
            db.execute("DELETE FROM pliki WHERE path=?", (f,))
    db.commit()
    return db


def cmd_find(a):
    needle = a.query.lower()
    filters = dict(kv.split("=", 1) for kv in (a.field or []))
    files = list(iter_cache(a.source, korpus=not a.bez_korpusu))
    kandydaci = None
    tokens = re.findall(r"\w+", needle)
    if tokens and not a.bez_fts:
        try:
            db = fts_sync(files, pelny=not a.source and not a.bez_korpusu)
            q = " AND ".join('"%s"*' % t for t in tokens)
            kandydaci = {r[0] for r in db.execute("SELECT path FROM fts WHERE fts MATCH ?", (q,))}
        except Exception as e:   # brak FTS5 w tej kompilacji SQLite itp.
            print("[lexcache] FTS niedostepne (%s) - przeszukiwanie liniowe" % e, file=sys.stderr)
    n = 0
    for p in files:
        if kandydaci is not None and p not in kandydaci:
            continue
        meta, body = parse_frontmatter(p)
        if not meta:
            continue
        if any(meta.get(k, "").lower() != v.lower() for k, v in filters.items()):
            continue
        blob = (" ".join("%s %s" % (k, v) for k, v in meta.items())
                + ("" if a.meta_only else " " + body)).lower()
        if needle and needle not in blob:
            continue
        n += 1
        flag = " [WYGASLY]" if is_stale(meta) else ""
        print("%s%s\n    %s | %s | %s\n    %s" % (
            meta.get("identyfikator") or "?", flag,
            meta.get("source", "?"), meta.get("data", "-"),
            (meta.get("tytul") or "")[:90], p))
    print("\n%d trafien | cache: %s%s" % (
        n, CACHE_DIR,
        "" if a.bez_korpusu or not GROUNDING_ROOT else " + korpus: " + GROUNDING_ROOT),
        file=sys.stderr)
    return 0


def cmd_ls(a):
    rows = []
    for p in iter_cache(a.source, korpus=not a.bez_korpusu):
        meta, _ = parse_frontmatter(p)
        if not meta:
            continue
        st = is_stale(meta)
        if a.stale and not st:
            continue
        rows.append((meta.get("origin", "cache")[:6], meta.get("source", "?"), meta.get("tool", "?"),
                     meta.get("identyfikator", "")[:44],
                     (meta.get("retrieved_at") or meta.get("znormalizowano") or "")[:10],
                     "WYGASLY" if st else "swiezy", p))
    for r in sorted(rows):
        print("%-6s %-7s %-18s %-40s %s  %-7s  %s" % r)
    print("\n%d wpisow | cache: %s%s" % (
        len(rows), CACHE_DIR,
        "" if a.bez_korpusu or not GROUNDING_ROOT else " + korpus: " + GROUNDING_ROOT),
        file=sys.stderr)
    return 0


def _gp_refresh_script():
    here = os.path.dirname(os.path.abspath(__file__))
    for c in (os.path.join(GROUNDING_ROOT or "", "mcp", "gp-refresh.mjs"),
              os.path.join(here, "..", "..", "..", "..", "mcp", "gp-refresh.mjs"),   # repozytorium
              os.path.join(here, "..", "..", "..", "mcp", "gp-refresh.mjs")):       # plugin
        if os.path.isfile(c):
            return os.path.abspath(c)
    return None


def cmd_refresh(a):
    """G4: odswiez wygasle wpisy lexcache, powtarzajac zapisane zapytanie (pole `query`)."""
    import time
    rows = []
    for p in iter_cache(a.source, korpus=False):
        meta, _ = parse_frontmatter(p)
        if not meta or meta.get("origin") in ("korpus", "mcp-cache"):
            continue
        if a.all or is_stale(meta):
            rows.append((p, meta))
    if a.limit:
        rows = rows[:a.limit]
    ok = err = 0
    for p, meta in rows:
        src, _, op = meta.get("tool", "").partition(".")
        try:
            ident = json.loads(meta.get("query") or "{}")
        except ValueError:
            continue
        if src not in FETCHERS or not op or not isinstance(ident, dict):
            continue
        print("%s %s.%s %s" % ("[dry-run]" if a.dry_run else "[odswiezam]", src, op,
                               meta.get("identyfikator") or ident), file=sys.stderr)
        if a.dry_run:
            continue
        ns = argparse.Namespace(**ident, func=None, source=src, op=op, no_cache=False,
                                refresh=True, json=False, ttl=None)
        real, sys.stdout = sys.stdout, open(os.devnull, "w")
        try:
            rc = run_fetch(src, op, ns)
        except Exception as e:
            rc = 4
            print("  blad: %s" % e, file=sys.stderr)
        finally:
            sys.stdout.close()
            sys.stdout = real
        ok += rc == 0
        err += rc != 0
        time.sleep(a.pauza)
    print("lexcache: %d odswiezonych, %d bledow (kandydatow: %d)" % (ok, err, len(rows)), file=sys.stderr)
    if a.mcp:
        s = _gp_refresh_script()
        if not s:
            print("[lexcache] brak mcp/gp-refresh.mjs - pomijam wpisy konektorow MCP", file=sys.stderr)
        else:
            env = dict(os.environ, GROUNDING_ROOT=GROUNDING_ROOT or "")
            cmd = ["node", s] + (["--all"] if a.all else []) + (["--limit", str(a.limit)] if a.limit else [])
            cmd += ["--dry-run"] if a.dry_run else []
            subprocess.run(cmd, env=env)
    return 0 if not err else 1


def cmd_harvest(a):
    """G3: zapelnianie wsadowe. Kazda pozycja to ogon polecenia lexcache (np. `isap act DU/2018/1000`)."""
    import glob, shlex, time
    jobs = []
    if a.z_map:
        skills = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        seen = set()
        for f in sorted(glob.glob(os.path.join(skills, "*", "MAPA-AKTOW.md"))):
            with open(f, encoding="utf-8", errors="replace") as fh:
                for y, poz in re.findall(r"Dz\.\s?U\.\s?(\d{4})\s?poz\.\s?(\d+)", fh.read()):
                    eli = "DU/%s/%s" % (y, poz)
                    if eli not in seen:
                        seen.add(eli)
                        jobs.append(["isap", "act", eli])
    if a.plik:
        with open(a.plik, encoding="utf-8") as fh:
            jobs += [shlex.split(l) for l in fh if l.strip() and not l.lstrip().startswith("#")]
    if a.limit:
        jobs = jobs[:a.limit]
    trafione = pobrane = bledy = 0
    for argv in jobs:
        if a.dry_run:
            print("[dry-run] lexcache %s" % " ".join(argv))
            continue
        r = subprocess.run([sys.executable, os.path.abspath(__file__)] + argv,
                           capture_output=True, text=True, timeout=240)
        if "[cache]" in r.stderr:
            trafione += 1
            continue
        if r.returncode == 0:
            pobrane += 1
        else:
            bledy += 1
            print("[blad] %s: %s" % (" ".join(argv), r.stderr.strip()[-160:]), file=sys.stderr)
        time.sleep(a.pauza)
    print("harvest: %d pozycji | juz w bazie %d | pobrane %d | bledy %d"
          % (len(jobs), trafione, pobrane, bledy), file=sys.stderr)
    return 0 if not bledy else 1


def cmd_purge(a):
    n = 0
    for p in iter_cache(a.source, korpus=False):   # purge NIGDY nie rusza korpusu
        meta, _ = parse_frontmatter(p)
        if a.all or is_stale(meta) or (a.errors and meta.get("status") == "ERROR"):
            os.remove(p)
            n += 1
    # Zalaczniki binarne (PDF-y ISAP) nie sa wpisami .md, wiec iter_cache ich nie
    # widzi - bez tego przebiegu zostawaly na dysku na zawsze.
    npdf = 0
    if a.source in (None, "isap"):
        pdf_dir = os.path.join(CACHE_DIR, "isap", "_pdf")
        prog = SOURCES["isap"]["ttl"]["pdf"] * 86400
        for fn in sorted(os.listdir(pdf_dir)) if os.path.isdir(pdf_dir) else []:
            fp = os.path.join(pdf_dir, fn)
            if a.all or (time.time() - os.path.getmtime(fp)) > prog:
                os.remove(fp)
                npdf += 1
    print("usunieto %d wpisow, %d PDF-ow" % (n, npdf), file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# KORPUS - recznie zebrane dokumenty w GROUNDING-PRAWO (ORZECZENIA / USTAWY /
# OPRACOWANIA / MAPY). Normalizacja frontmatteru i indeks.
# ---------------------------------------------------------------------------
MIESIACE = {"stycznia": 1, "lutego": 2, "marca": 3, "kwietnia": 4, "maja": 5,
            "czerwca": 6, "lipca": 7, "sierpnia": 8, "wrzesnia": 9, "września": 9,
            "pazdziernika": 10, "października": 10, "listopada": 11, "grudnia": 12}

# Izby i wydzialy Sadu Najwyzszego wg symbolu sygnatury.
SN_SYMBOLE = ["CSKP", "CSPK", "CSK", "CKN", "CZP", "CZ", "KZP", "KK", "UK",
              "PK", "UZ", "PZ", "KO", "KS", "NP"]


def _iso_date(s):
    s = s.strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", s)
    if m:
        return s
    m = re.match(r"^(\d{1,2})\s+([a-ząćęłńóśźż]+)\s+(\d{4})$", s, re.I)
    if m and m.group(2).lower() in MIESIACE:
        return "%s-%02d-%02d" % (m.group(3), MIESIACE[m.group(2).lower()], int(m.group(1)))
    return ""


def _klasyfikuj(sygn, nazwa_pliku, tekst):
    """(source, court_type, sad) - z jawnym 'nieznany' zamiast zgadywania."""
    s = (sygn or "").upper()
    # Numer skargi do ETPC: same cyfry i dwucyfrowy rok, bez symbolu izby.
    if re.match(r"^\d{3,6}[/_-]\d{2}$", s):
        return "echr", "", "Europejski Trybunał Praw Człowieka"
    if "OSK" in s or "OSD" in s or re.search(r"\bSA/\w", s):
        return "cbosa", "", "sąd administracyjny (NSA/WSA)"
    if "AKA" in s or "ACA" in s or re.search(r"_SA_", nazwa_pliku, re.I):
        m = re.search(r"[Ss]ąd Apelacyjny w ([A-ZŁŚŻŹĆÓĘĄŃ][\wąćęłńóśźż]+)", tekst or "")
        return "saos", "COMMON", ("Sąd Apelacyjny w " + m.group(1)) if m else "sąd powszechny"
    for sym in SN_SYMBOLE:
        if re.search(r"\b%s\b" % sym, s):
            return "saos", "SUPREME", "Sąd Najwyższy"
    if re.match(r"^(WA|SD|WO|WK)\b", s):
        return "saos", "SUPREME", "Sąd Najwyższy (Izba Wojskowa / dyscyplinarna)"
    return "nieznane", "", ""


def _parsuj_orzeczenie(path):
    txt = io.open(path, encoding="utf-8", errors="replace").read()
    body = txt
    if txt.startswith("---\n"):                  # juz znormalizowany
        e = txt.find("\n---\n", 4)
        if e > 0:
            body = txt[e + 5:]
    linie = [l.strip() for l in body.split("\n")[:14] if l.strip()]
    baza = os.path.basename(path)
    meta = {"sygnatura": "", "data": "", "typ": "", "sad": ""}

    # ksztalt 3: "- sąd: X" / "- data: Y" / "- typ: Z"
    for l in linie:
        m = re.match(r"^-\s*(sąd|sad|data|typ|źródło|zrodlo|url)\s*:\s*(.+)$", l, re.I)
        if m:
            k = m.group(1).lower().replace("ą", "a").replace("ó", "o").replace("ź", "z")
            v = m.group(2).strip()
            if k == "sad":
                # eksporty bywaja z enumem SAOS zamiast nazwy sadu
                meta["sad"] = {"SUPREME": "Sąd Najwyższy",
                               "COMMON": "sąd powszechny",
                               "CONSTITUTIONAL_TRIBUNAL": "Trybunał Konstytucyjny",
                               "NATIONAL_APPEAL_CHAMBER": "Krajowa Izba Odwoławcza"
                               }.get(v.strip().upper(), v)
            elif k == "data":
                meta["data"] = _iso_date(v) or v
            elif k == "typ":
                meta["typ"] = v
    # ksztalt 4: eksport BOS
    for l in linie:
        m = re.match(r"^Data orzeczenia:\s*(.+)$", l)
        if m:
            meta["data"] = _iso_date(m.group(1))
        m = re.match(r"^Rodzaj organu orzekającego:\s*(.+)$", l)
        if m and not meta["sad"]:
            meta["sad"] = m.group(1).strip()

    # sygnatura: z naglowka H1, z linii "goliej" sygnatury, albo z nazwy pliku
    kandydaci = []
    for l in linie[:6]:
        l2 = re.sub(r"^#+\s*", "", l)
        l2 = re.sub(r"^Orzeczenie Sądowe\s*", "", l2).strip()
        m = re.search(r"sygn\.?\s*(?:akt)?\s*([IVX]+\s+[A-Za-zĄĆĘŁŃÓŚŹŻ]+\s*\d+/\d+)", l2)
        if m:
            kandydaci.append(m.group(1))
        if re.match(r"^[IVX]+\s+[A-Za-zĄĆĘŁŃÓŚŹŻ]{1,5}\s*\d+/\d+$", l2) or \
           re.match(r"^\d{3,6}/\d{2}$", l2) or \
           re.match(r"^(WA|SD|WO|WK)\s*\d+/\d+$", l2):
            kandydaci.append(l2)
    if kandydaci:
        meta["sygnatura"] = kandydaci[0]
    else:                                        # z nazwy pliku: _ -> spacja, - -> /
        n = re.sub(r"\.md$", "", baza)
        n = re.sub(r"_SA_\w+$", "", n)
        n = n.replace("_", " ").strip()
        n = re.sub(r"\s*-\s*(\d{2})$", r"/\1", n)
        meta["sygnatura"] = n

    if not meta["data"]:
        for l in linie[:8]:
            d = _iso_date(l)
            if d:
                meta["data"] = d
                break
    if not meta["typ"]:
        low = body[:2000].lower()
        for slowo, typ in (("postanowienie", "POSTANOWIENIE"), ("uchwała", "UCHWALA"),
                           ("wyrok", "WYROK")):
            if slowo in low:
                meta["typ"] = typ
                break
    src, ct, sad = _klasyfikuj(meta["sygnatura"], baza, body)
    if not meta["sad"]:
        meta["sad"] = sad
    meta["source"] = src
    meta["court_type"] = ct
    return meta, txt, body


def _parsuj_ustawe(path):
    """Tekst ujednolicony w .docx - wyciagamy metryke Dz.U. i wersje."""
    meta = {"tytul": "", "dziennik": "", "eli": "", "wersja_od": "", "status_aktu": ""}
    try:
        import zipfile
        z = zipfile.ZipFile(path)
        x = z.read("word/document.xml").decode("utf-8", "replace")
        t = re.sub(r"<[^>]+>", " ", x)
        t = re.sub(r"\s+", " ", t)[:1500]
    except Exception:
        return meta, ""
    m = re.search(r"Dz\.U\.(\d{4})\.(\d+)", t)
    if m:
        meta["dziennik"] = "Dz.U. %s poz. %s" % (m.group(1), m.group(2))
        meta["eli"] = "DU/%s/%s" % (m.group(1), m.group(2))
    m = re.search(r"(Akt obowiązujący|Akt utracił moc|Akt oczekujący)", t)
    if m:
        meta["status_aktu"] = m.group(1)
    m = re.search(r"Wersja od:\s*([^ ]+ [^ ]+ \d{4})", t)
    if m:
        meta["wersja_od"] = _iso_date(m.group(1)) or m.group(1)
    meta["tytul"] = re.sub(r"\.md\.docx$|\.docx$", "", os.path.basename(path)).replace("_", " ")
    return meta, t


def _korpus_root():
    if not GROUNDING_ROOT:
        sys.exit("[lexcache] nie znaleziono repozytorium GROUNDING-PRAWO "
                 "(sprawdz OneDrive lub ustaw GROUNDING_ROOT)")
    return GROUNDING_ROOT


def _duplikat_bez_rozszerzenia(f):
    """Plik bez rozszerzenia, ktory jest kopia 1:1 swojego rodzenstwa .md."""
    if os.path.splitext(f)[1]:
        return False
    blizniak = f + ".md"
    if not os.path.exists(blizniak):
        return False
    # Porownujemy TRESC po odjeciu frontmatteru - inaczej detekcja przestaje
    # dzialac zaraz po tym, jak znormalizujemy rodzenstwo .md.
    try:
        def tresc(x):
            t = io.open(x, encoding="utf-8", errors="replace").read()
            if t.startswith("---\n"):
                e = t.find("\n---\n", 4)
                if e > 0:
                    t = t[e + 5:]
            return t.strip()
        return tresc(f) == tresc(blizniak)
    except Exception:
        return False


def cmd_korpus_normalize(a):
    root = _korpus_root()
    kat = os.path.join(root, "ORZECZENIA")
    zmian = pomin = dupli = 0
    duplikaty = []
    for f in sorted(glob.glob(kat + "/*")):
        if not os.path.isfile(f):
            continue
        if _duplikat_bez_rozszerzenia(f):
            dupli += 1
            duplikaty.append(os.path.basename(f))
            continue
        meta, txt, body = _parsuj_orzeczenie(f)
        if txt.startswith("---\n") and not a.force:
            pomin += 1
            continue
        fm = {
            "status": "FOUND",
            "query_type": "orzeczenie",
            "origin": "korpus",
            "source": meta["source"],
            "tool": "korpus.orzeczenia",
            "identyfikator": meta["sygnatura"],
            "sygnatura": meta["sygnatura"],
            "tytul": ("%s - %s" % (meta["sygnatura"], meta["sad"])).strip(" -"),
            "sad": meta["sad"],
            "court_type": meta["court_type"],
            "typ_orzeczenia": meta["typ"],
            "data": meta["data"],
            "status_obowiazywania": "nieznany",
            "url": "",
            "plik": os.path.basename(f),
            "confidence": "reczna_kuracja",
            "pii_risk": "high",
            "znormalizowano": _now().isoformat().replace("+00:00", "Z"),
        }
        if a.dry_run:
            print("%-34s %-16s %-10s %s" % (fm["plik"], fm["sygnatura"],
                                            fm["data"] or "-", fm["source"]))
            zmian += 1
            continue
        linie = ["---"]
        for k, v in fm.items():
            linie.append("%s: %s" % (k, _yaml_scalar(v)))
        linie += ["---", ""]
        io.open(f, "w", encoding="utf-8").write("\n".join(linie) + body.lstrip("\n"))
        zmian += 1
    print("znormalizowano: %d | pominieto (juz z frontmatterem): %d | "
          "duplikaty bez rozszerzenia: %d" % (zmian, pomin, dupli), file=sys.stderr)
    if duplikaty:
        print("[do decyzji uzytkownika] kopie 1:1 plikow .md, nietkniete:\n  %s"
              % "\n  ".join(duplikaty), file=sys.stderr)
    return 0


def cmd_korpus_index(a):
    root = _korpus_root()
    wpisy = []
    for f in sorted(glob.glob(os.path.join(root, "ORZECZENIA", "*"))):
        if not os.path.isfile(f) or _duplikat_bez_rozszerzenia(f):
            continue
        m, _ = parse_frontmatter(f)
        if not m:
            m, _, _ = (lambda t: ({"sygnatura": t[0]["sygnatura"], "data": t[0]["data"],
                                   "sad": t[0]["sad"], "source": t[0]["source"],
                                   "typ_orzeczenia": t[0]["typ"]}, None, None))(
                _parsuj_orzeczenie(f))
        m["plik"] = os.path.relpath(f, root)
        m["kategoria"] = "ORZECZENIA"
        wpisy.append(m)
    for f in sorted(glob.glob(os.path.join(root, "USTAWY", "*.docx"))):
        m, _ = _parsuj_ustawe(f)
        if os.path.getsize(f) == 0 or not m.get("dziennik"):
            m["problem"] = ("plik pusty (0 B)" if os.path.getsize(f) == 0
                            else "nie udalo sie odczytac metryki Dz.U.")
        m.update({"plik": os.path.relpath(f, root), "kategoria": "USTAWY",
                  "origin": "korpus", "source": "isap-lokalny", "query_type": "akt_prawny",
                  "identyfikator": m.get("eli") or m.get("dziennik", ""),
                  "data": m.get("wersja_od", "")})
        wpisy.append(m)
    for kat in ("OPRACOWANIA", "MAPY"):
        for f in sorted(glob.glob(os.path.join(root, kat, "*"))):
            if not os.path.isfile(f):
                continue
            wpisy.append({"plik": os.path.relpath(f, root), "kategoria": kat,
                          "origin": "korpus", "source": "opracowanie",
                          "query_type": "opracowanie",
                          "tytul": os.path.splitext(os.path.basename(f))[0],
                          "identyfikator": os.path.basename(f), "data": ""})

    idx_dir = os.path.join(root, "INDEX")
    os.makedirs(idx_dir, exist_ok=True)
    with io.open(os.path.join(idx_dir, "index.jsonl"), "w", encoding="utf-8") as fh:
        for w in wpisy:
            fh.write(json.dumps(w, ensure_ascii=False) + "\n")

    lin = ["---", "name: INDEX-GROUNDING-PRAWO",
           "description: Indeks wspolnego repozytorium zrodel prawa (korpus + cache lexcache).",
           "wygenerowano: " + _now().isoformat().replace("+00:00", "Z"),
           "pozycji: %d" % len(wpisy), "---", "",
           "# GROUNDING-PRAWO - indeks", "",
           "Generowany przez `lexcache korpus index`. Nie edytuj recznie.", ""]
    for kat in ("ORZECZENIA", "USTAWY", "OPRACOWANIA", "MAPY"):
        grupa = [w for w in wpisy if w.get("kategoria") == kat]
        if not grupa:
            continue
        lin += ["## %s (%d)" % (kat, len(grupa)), ""]
        if kat == "ORZECZENIA":
            lin += ["| Sygnatura | Data | Sąd | Źródło | Plik |", "|---|---|---|---|---|"]
            for w in sorted(grupa, key=lambda x: (x.get("data") or "", x.get("sygnatura") or "")):
                lin.append("| %s | %s | %s | %s | `%s` |" % (
                    w.get("sygnatura", "") or w.get("identyfikator", ""), w.get("data", "") or "—",
                    w.get("sad", "") or "—", w.get("source", ""), w["plik"]))
        elif kat == "USTAWY":
            lin += ["| Akt | Dz.U. | ELI | Wersja od | Status | Plik |", "|---|---|---|---|---|---|"]
            for w in sorted(grupa, key=lambda x: x.get("tytul", "")):
                lin.append("| %s | %s | %s | %s | %s | `%s` |" % (
                    w.get("tytul", "") or "**?**", w.get("dziennik", "") or "—",
                    w.get("eli", "") or "—", w.get("wersja_od", "") or "—",
                    w.get("status_aktu", "") or ("⚠️ " + w["problem"] if w.get("problem") else "—"),
                    w["plik"]))
        else:
            for w in sorted(grupa, key=lambda x: x.get("tytul", "")):
                lin.append("- %s — `%s`" % (w.get("tytul", ""), w["plik"]))
        lin.append("")
    io.open(os.path.join(idx_dir, "INDEX.md"), "w", encoding="utf-8").write("\n".join(lin) + "\n")
    print("indeks: %d pozycji -> %s" % (len(wpisy), idx_dir), file=sys.stderr)
    return 0


def cmd_migrate(a):
    zrodlo = os.path.expanduser(a.z or LOKALNY_FALLBACK)
    if os.path.abspath(zrodlo) == os.path.abspath(CACHE_DIR):
        print("zrodlo i cel to ten sam katalog - nic do zrobienia", file=sys.stderr)
        return 0
    n = 0
    for dirpath, _, files in os.walk(zrodlo):
        for fn in files:
            src = os.path.join(dirpath, fn)
            rel = os.path.relpath(src, zrodlo)
            dst = os.path.join(CACHE_DIR, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if a.dry_run:
                print("%s -> %s" % (rel, dst))
            else:
                shutil.copy2(src, dst)
            n += 1
    print("przeniesiono %d plikow do %s%s" % (n, CACHE_DIR,
          " (proba, nic nie zapisano)" if a.dry_run else ""), file=sys.stderr)
    if not a.dry_run and a.usun_zrodlo:
        shutil.rmtree(zrodlo, ignore_errors=True)
        print("usunieto stary cache: " + zrodlo, file=sys.stderr)
    return 0


def cmd_sources(a):
    print("repozytorium: %s" % (GROUNDING_ROOT or "— (brak, cache lokalny)"))
    print("cache:        %s" % CACHE_DIR)
    print("powod:        %s\n" % CACHE_POWOD)
    for k, v in SOURCES.items():
        typ = "normatyw" if v["normatyw"] else "rejestr "
        klucz = "KLUCZ API" if v["klucz"] else "otwarte  "
        line = "%-7s %s  %s  pii=%-4s  %s" % (k, typ, klucz, v["pii"], v["nazwa"])
        if a.health:
            try:
                code, _ = http("https://" + v["host"].split("/")[0], accept="*/*", timeout=12) \
                    if not v["host"].startswith("uvx") else (200 if shutil.which("uvx") else 0, "")
            except Exception:
                code = 0
            line += "   [%s]" % ("ok" if code else "brak")
        print(line)
    print("\nkrajowe ELI UE: " + ", ".join(ELI_KRAJE) + "  (fr wymaga danych PISTE)")
    return 0


# ---------------------------------------------------------------------------
def main():
    # Flagi globalne dubluja sie na kazdym liściu, zeby dzialaly w obu
    # pozycjach: `lexcache --refresh isap act X` i `lexcache isap act X --refresh`.
    glob = argparse.ArgumentParser(add_help=False)
    glob.add_argument("--no-cache", action="store_true")
    glob.add_argument("--refresh", action="store_true")
    glob.add_argument("--json", action="store_true")
    glob.add_argument("--ttl", type=int, default=None, help="nadpisz TTL w dniach")

    ap = argparse.ArgumentParser(prog="lexcache", description=__doc__,
                                 parents=[glob],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="source", required=True)
    _add = sub.add_parser
    sub.add_parser = lambda name, **kw: _add(
        name, parents=list(kw.pop("parents", [])) + [glob], **kw)

    def fetcher(src, op, p):
        p.set_defaults(func=lambda a, s=src, o=op: run_fetch(s, o, a))

    # isap
    def leaf(parent):
        s2 = parent.add_subparsers(dest="op", required=True)
        _a = s2.add_parser
        s2.add_parser = lambda name, **kw: _a(
            name, parents=list(kw.pop("parents", [])) + [glob], **kw)
        return s2

    s = leaf(sub.add_parser("isap"))
    p = s.add_parser("search"); p.add_argument("--title"); p.add_argument("--publisher", default="DU")
    p.add_argument("--type"); p.add_argument("--year"); p.add_argument("--limit", default="10")
    p.add_argument("--in-force", action="store_true"); fetcher("isap", "search", p)
    p = s.add_parser("act"); p.add_argument("eli"); fetcher("isap", "act", p)
    p = s.add_parser("text"); p.add_argument("eli"); p.add_argument("--find")
    fetcher("isap", "text", p)
    p = s.add_parser("pdf"); p.add_argument("eli"); p.add_argument("--find")
    fetcher("isap", "pdf", p)

    # saos
    s = leaf(sub.add_parser("saos"))
    p = s.add_parser("search")
    for f in ("--all", "--case", "--court", "--judge", "--legalbase", "--regulation",
              "--date-from", "--date-to"):
        p.add_argument(f)
    p.add_argument("--size", default="10"); p.add_argument("--page", default="0")
    fetcher("saos", "search", p)
    p = s.add_parser("case"); p.add_argument("case"); p.add_argument("--size", default="10")
    p.add_argument("--page", default="0"); fetcher("saos", "case", p)
    p = s.add_parser("get"); p.add_argument("id"); fetcher("saos", "get", p)

    # cbosa
    s = leaf(sub.add_parser("cbosa"))
    p = s.add_parser("search"); p.add_argument("query"); fetcher("cbosa", "search", p)

    # eurlex
    s = leaf(sub.add_parser("eurlex"))
    p = s.add_parser("celex"); p.add_argument("celex"); p.add_argument("--lang", default="POL")
    fetcher("eurlex", "celex", p)
    p = s.add_parser("sparql"); p.add_argument("query"); fetcher("eurlex", "sparql", p)

    # krs / nbp / sudop / ceidg
    s = leaf(sub.add_parser("krs"))
    for op in ("act", "full"):
        p = s.add_parser(op); p.add_argument("krs"); p.add_argument("--rejestr", default="P")
        fetcher("krs", op, p)
    s = leaf(sub.add_parser("nbp"))
    p = s.add_parser("rate"); p.add_argument("code"); p.add_argument("--date", default="")
    fetcher("nbp", "rate", p)
    s = leaf(sub.add_parser("sudop"))
    p = s.add_parser("nip"); p.add_argument("nip"); fetcher("sudop", "nip", p)
    s = leaf(sub.add_parser("ceidg"))
    p = s.add_parser("nip"); p.add_argument("nip"); fetcher("ceidg", "nip", p)

    # eli (uvx)
    s = sub.add_parser("eli"); s.add_argument("country")
    s2 = leaf(s)
    p = s2.add_parser("tools"); fetcher("eli", "tools", p)
    p = s2.add_parser("call"); p.add_argument("tool"); p.add_argument("--args", default="{}")
    fetcher("eli", "call", p)

    # cache
    p = sub.add_parser("find"); p.add_argument("query", nargs="?", default="")
    p.add_argument("--source"); p.add_argument("--field", action="append")
    p.add_argument("--meta-only", action="store_true")
    p.add_argument("--bez-korpusu", action="store_true", help="tylko cache, pomin GROUNDING-PRAWO")
    p.add_argument("--bez-fts", action="store_true", help="przeszukiwanie liniowe zamiast indeksu FTS5")
    p.set_defaults(func=cmd_find)
    p = sub.add_parser("refresh", help="odswiez wygasle wpisy (G4)")
    p.add_argument("--source"); p.add_argument("--all", action="store_true", help="takze niewygasle")
    p.add_argument("--limit", type=int, default=0); p.add_argument("--dry-run", action="store_true")
    p.add_argument("--pauza", type=float, default=0.5, help="sekundy miedzy zapytaniami")
    p.add_argument("--mcp", action="store_true", help="odswiez tez wpisy konektorow MCP (mcp/gp-refresh.mjs)")
    p.set_defaults(func=cmd_refresh)
    p = sub.add_parser("harvest", help="zapelnianie wsadowe bazy (G3)")
    p.add_argument("--z-map", action="store_true", help="akty z MAPA-AKTOW.md modulow DR -> isap act")
    p.add_argument("--plik", help="lista: jedna linia = ogon polecenia lexcache")
    p.add_argument("--limit", type=int, default=0); p.add_argument("--dry-run", action="store_true")
    p.add_argument("--pauza", type=float, default=0.5)
    p.set_defaults(func=cmd_harvest)
    p = sub.add_parser("ls"); p.add_argument("--source"); p.add_argument("--stale", action="store_true")
    p.add_argument("--bez-korpusu", action="store_true")
    p.set_defaults(func=cmd_ls)
    p = sub.add_parser("purge"); p.add_argument("--source"); p.add_argument("--all", action="store_true")
    p.add_argument("--stale", action="store_true")
    p.add_argument("--errors", action="store_true", help="usun wpisy ze statusem ERROR")
    p.set_defaults(func=cmd_purge)
    p = sub.add_parser("sources"); p.add_argument("--health", action="store_true")
    p.set_defaults(func=cmd_sources)

    # korpus (GROUNDING-PRAWO)
    sk = leaf(sub.add_parser("korpus"))
    q = sk.add_parser("normalize")
    q.add_argument("--dry-run", action="store_true", help="pokaz, nic nie zapisuj")
    q.add_argument("--force", action="store_true", help="przepisz tez pliki z frontmatterem")
    q.set_defaults(func=cmd_korpus_normalize)
    q = sk.add_parser("index"); q.set_defaults(func=cmd_korpus_index)

    p = sub.add_parser("migrate")
    p.add_argument("--z", help="katalog zrodlowy (domyslnie stary cache lokalny)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--usun-zrodlo", action="store_true")
    p.set_defaults(func=cmd_migrate)

    a = ap.parse_args()
    for f in ("no_cache", "refresh", "json", "ttl"):
        if not hasattr(a, f):
            setattr(a, f, None)
    try:
        return a.func(a)
    except subprocess.TimeoutExpired:
        print("[ERROR] timeout zrodla", file=sys.stderr)
        return 4
    except RuntimeError as e:
        print("[ERROR] %s" % e, file=sys.stderr)
        return 4


if __name__ == "__main__":
    sys.exit(main())
