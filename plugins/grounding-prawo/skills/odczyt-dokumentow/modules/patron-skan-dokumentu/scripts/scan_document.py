#!/usr/bin/env python3
"""Skan bezpieczenstwa dokumentu wejsciowego przed czytaniem go przez model (stdlib, offline).

Port z Patrona (MateMatic Solutions, AGPL-3.0): backend/src/lib/input-security/detectors/
  adversarial-pl.ts  - prompt injection / jailbreak PL i EN, context stuffing
  steganography.ts   - znaki zerowej szerokosci, /Launch /JavaScript /EmbeddedFile w PDF
  obfuscation.ts     - homoglify (mieszanie pism w slowie), base64, znaki bidi
Poprawka wzgledem Patrona: akronimy jailbreak (DAN, STAN, AIM, DUDE) tylko wielkimi
literami i z kontekstem ("DAN mode", "DAN prompt") - w Patronie wzorzec z flaga "i"
lapie polskie "stan" ("Stan faktyczny"), a naglowki pism bywaja wersalikami.

  scan_document.py PLIK [PLIK...] [--json]

Werdykt: BLOKADA (critical) / PRZEGLAD (high) / OSTRZEZENIE (medium) / INFO (low) / CZYSTY.
Kod wyjscia: 2 = BLOKADA, 1 = PRZEGLAD, 0 = pozostale.
"""
import argparse
import base64
import json
import re
import subprocess
import sys
import zipfile
from html import unescape
from pathlib import Path

SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3, "critical": 4}
VERDICT = {0: "CZYSTY", 1: "INFO", 2: "OSTRZEZENIE", 3: "PRZEGLAD", 4: "BLOKADA"}

I = re.I
SIGNALS = [
    ("prompt-injection-pl", "high",
     re.compile(r"(?<!\w)(?:zignoruj|pomi[nń]|zapomnij|odrzu[cć])\s+(?:wszystkie\s+)?(?:poprzednie|powy[zż]sze|"
                r"wcze[sś]niejsze|dotychczasowe)\s+(?:instrukcje|polecenia|wytyczne|ustalenia|zasady)", I),
     "Proba nadpisania instrukcji systemowych."),
    ("prompt-injection-pl-newrole", "high",
     re.compile(r"(?<!\w)(?:dzia[lł]aj\s+(?:jako|jak)|udawaj,?\s+[zż]e\s+jeste[sś]|wciel\s+si[eę]\s+w)(?!\w)", I),
     "Proba przejecia roli modelu."),
    ("prompt-injection-pl-reveal", "high",
     re.compile(r"(?<!\w)(?:ujawnij|poka[zż]|wypisz|wy[sś]wietl|zdrad[zź])\s+(?:sw[oó]j\s+)?(?:prompt\s+systemowy|"
                r"instrukcje\s+systemowe|polecenie\s+systemowe|konfiguracj[eę]|ustawienia\s+systemowe)", I),
     "Proba wydobycia promptu systemowego."),
    ("jailbreak-pl-mode", "high",
     re.compile(r"(?<!\w)(?:tryb\s+(?:dewelopera|deweloperski|bez\s+ogranicze[nń]|nieocenzurowany|swobodny)|"
                r"bez\s+(?:filtr[oó]w|cenzury|ogranicze[nń])|pomi[nń]\s+(?:zabezpieczenia|filtry|"
                r"zasady\s+bezpiecze[nń]stwa))(?!\w)", I),
     "Polska proba jailbreak."),
    ("prompt-injection-en", "high",
     re.compile(r"\b(?:ignore|disregard|forget)\s+(?:all\s+)?(?:previous|above|prior|earlier)\s+"
                r"(?:instructions|prompts|commands|rules)", I),
     "Override instrukcji (EN)."),
    ("prompt-injection-en-marker", "medium",
     re.compile(r"\[(?:SYSTEM|ADMIN|INST|/INST)\]|<\|(?:system|im_start|im_end)\|>|###\s*system", I),
     "Wstrzykniety znacznik roli - proba sfalszowania struktury rozmowy."),
    ("jailbreak-en-known", "high",
     re.compile(r"\b(?:DAN|STAN|DUDE|AIM)\b(?=\s+(?:mode|prompt|jailbreak))|(?i:do\s+anything\s+now|"
                r"developer\s+mode|jailbreak)"),
     "Znana technika jailbreak (EN)."),
]
ZERO_WIDTH = "​‌‍﻿⁠᠎"
BIDI_RE = re.compile("[‪-‮⁦-⁩]")
CONFUSABLE = set("аеорсухіјѕАВЕКМНОРСТХІЈοανριкΑΒΕΖΗΙΚΜΝΟΡΤΧ")
LATIN = re.compile(r"[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]")
B64_RE = re.compile(r"\b([A-Za-z0-9+/]{60,}={0,2})\b")


def clip(s: str, n: int = 120) -> str:
    return s if len(s) <= n else s[:n] + "..."


def scan_text(text: str) -> list:
    f = []
    for technique, sev, rx, impact in SIGNALS:
        hits = rx.findall(text)
        if hits:
            first = rx.search(text).group(0)
            f.append({"technika": technique, "waga": sev, "pewnosc": min(80 + len(hits) * 5, 98),
                      "dowod": clip(first), "skutek": impact})
    sentences = [s.strip() for s in re.split(r"[.!?\n]+", text) if len(s.strip()) > 10]
    if len(sentences) >= 100:
        rep = 1 - len({s.lower() for s in sentences}) / len(sentences)
        if rep > 0.3:
            f.append({"technika": "context-stuffing", "waga": "medium", "pewnosc": 75,
                      "dowod": f"{len(sentences)} zdan, {rep:.0%} powtorzen",
                      "skutek": "Proba przepelnienia okna kontekstu i ukrycia tresci."})
    zw = sum(text.count(c) for c in ZERO_WIDTH)
    if zw:
        f.append({"technika": "zero-width-chars", "waga": "high" if zw > 8 else "medium",
                  "pewnosc": min(50 + zw * 5, 95), "dowod": f"{zw} znakow zerowej szerokosci",
                  "skutek": "Ukryta tresc lub polecenie zakodowane znakami niewidocznymi."})
    bidi = len(BIDI_RE.findall(text))
    if bidi:
        f.append({"technika": "bidi-control-chars", "waga": "high", "pewnosc": 85,
                  "dowod": f"{bidi} znakow sterujacych kierunkiem",
                  "skutek": "Tekst widziany przez czlowieka rozni sie od tego, ktory czyta model."})
    suspect = [w for w in text.split() if len(w) >= 2 and LATIN.search(w) and any(c in CONFUSABLE for c in w)]
    if suspect:
        f.append({"technika": "homoglyph-mixed-script", "waga": "high" if len(suspect) > 3 else "medium",
                  "pewnosc": min(60 + len(suspect) * 10, 95),
                  "dowod": f'{len(suspect)} slow z mieszanym pismem, np. "{suspect[0][:30]}"',
                  "skutek": "Lacinka zmieszana z cyrylica/greka - omijanie filtrow."})
    m = B64_RE.search(text)
    if m:
        try:
            decoded = base64.b64decode(m.group(1) + "===", validate=False).decode("utf-8")
            if len(decoded) > 10 and re.search(r"[a-zA-Ząćęłńóśźż]{4,}", decoded):
                f.append({"technika": "base64-readable", "waga": "medium", "pewnosc": 65,
                          "dowod": f"ciag base64 dlugosci {len(m.group(1))}: {clip(decoded, 80)!r}",
                          "skutek": "Zakodowana tresc dekoduje sie do czytelnego tekstu."})
        except (ValueError, UnicodeDecodeError):
            pass
    return f


def scan_pdf_bytes(raw: bytes) -> list:
    head = raw.decode("latin-1")
    f = []
    has_launch = "/Launch" in head
    has_js = "/JavaScript" in head or re.search(r"/JS[\s/(<]", head) is not None
    if has_launch:
        f.append({"technika": "pdf-launch-action", "waga": "critical", "pewnosc": 92,
                  "dowod": "PDF zawiera /Launch", "skutek": "Uruchamia zewnetrzny program przy otwarciu."})
    if has_js:
        f.append({"technika": "pdf-javascript", "waga": "critical", "pewnosc": 92,
                  "dowod": "PDF zawiera /JavaScript|/JS", "skutek": "PDF wykonuje JavaScript."})
    if ("/OpenAction" in head or "/AA" in head) and not (has_launch or has_js):
        f.append({"technika": "pdf-auto-navigation", "waga": "low", "pewnosc": 40,
                  "dowod": "/OpenAction|/AA bez kodu", "skutek": "Typowo nieszkodliwa nawigacja - odnotowane."})
    if "/EmbeddedFile" in head:
        f.append({"technika": "pdf-embedded-file", "waga": "high", "pewnosc": 80,
                  "dowod": "PDF zawiera /EmbeddedFile", "skutek": "Osadzony plik - mozliwy nosnik ukrytej tresci."})
    if "/OCProperties" in head:
        f.append({"technika": "pdf-hidden-layers", "waga": "medium", "pewnosc": 60,
                  "dowod": "warstwy opcjonalne /OCProperties", "skutek": "Ukryte warstwy moga zawierac tresc."})
    return f


def extract_text(p: Path, notes: list) -> str:
    s = p.suffix.lower()
    if s == ".docx":
        with zipfile.ZipFile(p) as z:
            xml = z.read("word/document.xml").decode("utf-8", errors="replace")
        return unescape(re.sub(r"<[^>]+>", "", re.sub(r"</w:p>", "\n", xml)))
    if s == ".pdf" and p.with_suffix(".md").exists():
        notes.append(f"tresc sprawdzona z {p.with_suffix('.md').name} (OCR obok PDF)")
        return p.with_suffix(".md").read_text(encoding="utf-8", errors="replace")
    if s == ".pdf":
        try:
            return subprocess.run(["pdftotext", str(p), "-"], check=True, capture_output=True, text=True).stdout
        except (FileNotFoundError, subprocess.CalledProcessError):
            notes.append("brak pdftotext - sprawdzono tylko strukture PDF, bez tresci")
            return ""
    return p.read_text(encoding="utf-8", errors="replace")


def scan_file(path: str) -> dict:
    p = Path(path)
    notes: list = []
    findings = scan_text(extract_text(p, notes))
    if p.suffix.lower() == ".pdf" or p.read_bytes()[:4] == b"%PDF":
        findings += scan_pdf_bytes(p.read_bytes())
        notes.append("strumienie skompresowane PDF nie sa rozpakowywane - /JS w object streams moze umknac")
    rank = max((SEVERITY_RANK[x["waga"]] for x in findings), default=0)
    return {"plik": str(p), "werdykt": VERDICT[rank], "ustalenia": findings, "uwagi": notes}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    reports = [scan_file(f) for f in a.files]
    if a.json:
        print(json.dumps(reports, ensure_ascii=False, indent=2))
    else:
        for r in reports:
            print(f"{r['werdykt']:<12} {r['plik']}")
            for x in r["ustalenia"]:
                print(f"    [{x['waga']}] {x['technika']}: {x['dowod']} - {x['skutek']}")
            for n in r["uwagi"]:
                print(f"    (uwaga: {n})")
    worst = max((list(VERDICT.values()).index(r["werdykt"]) for r in reports), default=0)
    return 2 if worst == 4 else 1 if worst == 3 else 0


if __name__ == "__main__":
    sys.exit(main())
