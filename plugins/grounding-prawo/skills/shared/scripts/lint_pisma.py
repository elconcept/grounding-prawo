#!/usr/bin/env python3
"""Mechaniczna kontrola stylu i formy pisma (shared/BRAMKA-REDAKCJI.md, STYLE.md).

Sprawdza tekst DOCX (po przyjęciu zmian) albo Markdown. Błąd blokuje wydanie pisma; uwaga idzie do recenzji.

    python3 lint_pisma.py <pismo.docx|pismo.md|-> [--json] [--limit-slow N]

Błędy:
  E1  myślnik „—” w tekście,
  E2  półpauza albo łącznik ze spacjami jako znak interpunkcyjny w zdaniu („ – ”, „ - ”);
      w zakresach bez spacji („k. 8–9”, „2025–2026”) zostaje,
  E3  pozostałości Markdown w DOCX (nagłówek „#”, „**”, „__”, „~~”, „`”),
  E4  placeholdery („⬛”, „[UZUPEŁNIJ”, „[DO ”, „[do uzupełnienia”, „TODO”, „XXX”),
  E5  zdanie dłuższe niż limit słów (domyślnie 35; tekst w cudzysłowie „…” się nie liczy),
  E6  dwukropek w środku zdania, po którym zdanie biegnie dalej małą literą
      (dwukropek przed wyliczeniem, cytatem, liczbą i w metryce pisma zostaje).
  Punkt petitum zaczynający się rzeczownikiem odczasownikowym („zakazanie”, „zasądzenie”) nie podlega E5 ani U2.
Uwagi:
  U1  zdanie od 26 słów do limitu: do przejrzenia, czy nie rozbić,
  U2  punkt wyliczenia bez orzeczenia w pierwszych słowach (podejrzenie równoważnika zdania).
Kod wyjścia: 0 bez błędów, 1 są błędy.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pismo_tekst import tekst  # noqa: E402

L = "a-ząćęłńóśźż"
U = "A-ZĄĆĘŁŃÓŚŹŻ"
CYTAT = re.compile(r"„[^”]*”|»[^«]*«")
ZDANIE = re.compile(rf"(?<=[.!?…])\s+(?=[{U}„(\d])")
METRYKA = re.compile(r"^\s*(Sygn\.|Sygnatura|Dotyczy|Załącznik|Załączniki|Adresat|Nadawca|Do|Od|Strona|Wnioskodawca|"
                     r"Pokrzywdzony|Pokrzywdzona|Zawiadamiający|Zawiadamiająca|Skarżący|Skarżąca|Powód|Powódka|Pozwany|"
                     r"Pozwana|Pozwani|Uczestnik|Data|Miejsce|PESEL|tel|e-mail|AE|ePUAP|Wartość)\b[^:]{0,40}:", re.I)
PLACEHOLDER = re.compile(r"⬛|\[UZUPEŁNIJ|\[DO |\[do uzupełnienia|\bTODO\b|\bXXX\b")
MARKDOWN = re.compile(r"^\s*#{1,6}\s|\*\*|__|~~|`")
# czasowniki osobowe i formy orzeczenia, które zwykle otwierają pełne zdanie w punkcie
ORZECZENIE = re.compile(rf"\b([{L}]+(ł|ła|ło|li|ły|łem|łam|liśmy|łyśmy|my|cie|ję|uje|ują|am|em|ę|ią|ał|ił|ył|"
                        rf"ała|iła|yła|eli|ali|ili|yli|ano|ono|to|no|wa|wi|ma|mi|ci|ni|si|zi|ży|je|ie)|jest|są|był|"
                        rf"była|było|byli|były|nie|ma|mają|wnoszę|wnosimy|żądam|żądamy|zarzucam|zarzucamy|uważam|"
                        rf"proszę|prosimy|zawiadamiam|domagam|składam|wskazuję|podnoszę)\b", re.I)


def dlugosc(zdanie):
    return len(re.findall(rf"[{L}{U}0-9]+", CYTAT.sub(" ", zdanie)))


def sprawdz(t, limit=35):
    bledy, uwagi = [], []
    akapity = [a for a in t.split("\n")]
    for nr, ak in enumerate(akapity, 1):
        s = ak.strip()
        if not s:
            continue
        frag = lambda m: s[max(0, m.start() - 30):m.end() + 30]  # noqa: E731
        bez_cyt = CYTAT.sub(lambda m: " " * len(m.group(0)), s)
        for m in re.finditer("—", bez_cyt):
            bledy.append(("E1", nr, frag(m)))
        for m in re.finditer(rf"(?<=[{L}{U}0-9,.;)”])\s[–-]\s(?=[{L}{U}„(0-9])", bez_cyt):
            przed = bez_cyt[:m.start()]
            if re.search(r"\d{4} r\.$", przed) and re.match(rf"\s[–-]\s[{U}]", bez_cyt[m.start():]):
                continue  # urzędowy tytuł aktu: „ustawa z dnia … 1964 r. – Kodeks cywilny”
            if re.fullmatch(r"\s*(Z|ZS|Zał\.|Załącznik)?\s?[A-Z]{0,3}\d+[a-z]?", przed):
                continue  # etykieta załącznika na liście: „Z3 – wydruk …”
            bledy.append(("E2", nr, frag(m)))
        for m in MARKDOWN.finditer(s):
            bledy.append(("E3", nr, frag(m)))
        for m in PLACEHOLDER.finditer(s):
            bledy.append(("E4", nr, frag(m)))
        if not METRYKA.match(s):
            z_cyt = CYTAT.sub(lambda m: "Q" * len(m.group(0)), s)  # cytat po dwukropku to dozwolony cytat
            for m in re.finditer(rf":\s+(?=[{L}])", z_cyt):
                bledy.append(("E6", nr, frag(m)))
        # Punkt petitum („1. zakazanie…”, „nakazanie…”, „zasądzenie…”) to formuła żądania po „wnoszę o”;
        # sąd przenosi ją do sentencji jako jedno zdanie, więc nie podlega limitowi długości ani testowi U2.
        petitum = bool(re.match(rf"^\d+\.\s+[{L}]+(anie|enie|cie)\b", s))
        for z in ([] if petitum else ZDANIE.split(s)):
            n = dlugosc(z)
            if n > limit:
                bledy.append(("E5", nr, f"{n} słów: {z[:90]}…"))
            elif n > 25:
                uwagi.append(("U1", nr, f"{n} słów: {z[:90]}…"))
        m = re.match(r"^(\d+\.|[a-z]\)|[-•])\s+(.*)", s)
        if m and not petitum:
            pocz = " ".join(m.group(2).split()[:8])
            if not ORZECZENIE.search(pocz) and len(m.group(2).split()) > 2 and not m.group(2).isupper():
                uwagi.append(("U2", nr, pocz))
    return bledy, uwagi


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    limit = int(args[args.index("--limit-slow") + 1]) if "--limit-slow" in args else 35
    bledy, uwagi = sprawdz(tekst(args[0]), limit)
    if "--json" in args:
        print(json.dumps({"bledy": bledy, "uwagi": uwagi}, ensure_ascii=False))
    else:
        for kod, nr, f in bledy:
            print(f"BŁĄD {kod} akapit {nr}: {f}")
        for kod, nr, f in uwagi:
            print(f"uwaga {kod} akapit {nr}: {f}")
        print(f"— błędów: {len(bledy)}, uwag: {len(uwagi)}")
    sys.exit(1 if bledy else 0)


if __name__ == "__main__":
    main()
