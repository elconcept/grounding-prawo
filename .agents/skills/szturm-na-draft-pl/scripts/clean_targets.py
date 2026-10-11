#!/usr/bin/env python3
"""Bramka przed `adeu apply` (E7 szturmu): czysci target_text/new_text z markdownu
i sprawdza, czy kazdy target wystepuje w dokumencie DOKLADNIE raz.

Dlaczego to osobny krok:
- adeu dopasowuje tekst Worda, a markdown traktuje doslownie. Target z `**` albo `<u>`
  nie trafi albo - gorzej - trafi i wstawi do pisma gwiazdki jako tekst (zmierzone 28.09).
- adeu waliduje pakiet atomowo: jedna nietrafiona albo niejednoznaczna edycja odrzuca
  CALY pakiet. Lepiej wiedziec, ktora, zanim sie go wysle.
- adeu liczy wystapienia jako podciag, nie slowo ("obraz" trafia tez w "obrazie").
  Ten skrypt liczy tak samo.

Wejscie: edits.json (lista obiektow modify; dodatkowe pola sa usuwane z wyjscia)
         + <nazwa>.clean.md z extract_all_pages.sh (baza porownania).
Wyjscie: edits.adeu.json - tylko type, target_text, new_text, comment (+ match_mode, jesli byl).

Uzycie:
  python3 clean_targets.py edits.json --md run/pismo.clean.md -o run/edits.adeu.json [--json]

Exit: 0 = wszystkie edycje jednoznaczne, 1 = sa edycje do poprawy (wyjscie zapisane tylko
dla poprawnych, z --tylko-poprawne), 2 = blad wejscia.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

POLA_ADEU = ("type", "target_text", "new_text", "comment", "match_mode")
RE_CRITIC = re.compile(r"\{--(.*?)--\}|\{\+\+(.*?)\+\+\}|\{~~(.*?)~>(.*?)~~\}|\{>>.*?<<\}|\{==(.*?)==\}", re.S)


def _critic_clean(m: re.Match) -> str:
    # wersja "przyjeta": usuniete znika, wstawione zostaje, zamiana -> nowe, komentarz znika
    if m.group(1) is not None:
        return ""
    if m.group(2) is not None:
        return m.group(2)
    if m.group(4) is not None:
        return m.group(4)
    return m.group(5) or ""


def bez_markdownu(t: str) -> str:
    """Tekst tak, jak widzi go adeu w Wordzie: bez znacznikow formatowania markdown."""
    t = RE_CRITIC.sub(_critic_clean, t)
    t = re.sub(r"</?u>", "", t)
    t = re.sub(r"(?m)^\s{0,3}#{1,6}\s+", "", t)
    t = re.sub(r"(?m)^>\s?", "", t)
    t = t.replace("**", "").replace("__", "")
    t = re.sub(r"(?<![\w*])\*(?=\S)|(?<=\S)\*(?![\w*])", "", t)
    t = re.sub(r"(?<![\w_])_(?=\S)|(?<=\S)_(?![\w_])", "", t)
    t = t.replace("\\", "")
    return t


def plain_doc(md: str) -> str:
    return "\n".join(bez_markdownu(l) for l in md.splitlines())


def konteksty(doc: str, target: str, n: int = 3) -> list[str]:
    out, i = [], doc.find(target)
    while i >= 0 and len(out) < n:
        out.append("…" + doc[max(0, i - 40):i + len(target) + 40].replace("\n", " ⏎ ") + "…")
        i = doc.find(target, i + 1)
    return out


def sprawdz(edits: list[dict], doc: str) -> list[dict]:
    wyniki = []
    for nr, e in enumerate(edits, 1):
        w = {"nr": nr, "id": e.get("id"), "ok": False, "problemy": []}
        if e.get("type", "modify") != "modify":
            w["ok"] = True
            w["edit"] = {k: e[k] for k in e if k in POLA_ADEU or k in ("target_id", "text", "cells")}
            wyniki.append(w)
            continue
        tgt_raw, new_raw = e.get("target_text", ""), e.get("new_text", "")
        tgt, new = bez_markdownu(tgt_raw).strip(), bez_markdownu(new_raw).strip()
        if tgt != tgt_raw.strip():
            w["problemy"].append("target oczyszczony z markdownu")
        if new != new_raw.strip():
            w["problemy"].append("new_text oczyszczony z markdownu (formatowanie nowego tekstu nie przejdzie)")
        if not tgt:
            w["problemy"].append("BLAD: pusty target_text")
        elif "\n" in tgt:
            w["problemy"].append("BLAD: target obejmuje wiecej niz jeden akapit - podziel edycje")
        elif " | " in tgt:
            w["problemy"].append("BLAD: target przechodzi przez komorki tabeli - edytuj komorke osobno")
        else:
            ile = doc.count(tgt)
            w["wystapien"] = ile
            tryb = e.get("match_mode", "strict")
            if ile == 0:
                w["problemy"].append("BLAD: target nie wystepuje w dokumencie")
            elif ile > 1 and tryb == "strict":
                w["problemy"].append(f"BLAD: target niejednoznaczny ({ile} wystapien) - dodaj kontekst")
                w["konteksty"] = konteksty(doc, tgt)
            else:
                w["ok"] = True
        if re.match(r"^\d+[.)]\s", tgt):
            w["problemy"].append("uwaga: target zaczyna sie numerem listy - jezeli numeracja jest automatyczna, nie ma jej w tekscie Worda")
        if tgt == new:
            w["ok"] = False
            w["problemy"].append("BLAD: new_text identyczny z target_text po oczyszczeniu")
        w["edit"] = {"type": "modify", "target_text": tgt, "new_text": new,
                     **({"comment": e["comment"]} if e.get("comment") else {}),
                     **({"match_mode": e["match_mode"]} if e.get("match_mode") else {})}
        wyniki.append(w)
    return wyniki


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("edits", type=Path)
    ap.add_argument("--md", type=Path, required=True, help="<nazwa>.clean.md z extract_all_pages.sh")
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("--tylko-poprawne", action="store_true", help="zapisz wyjscie z samych poprawnych edycji")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        edits = json.loads(a.edits.read_text(encoding="utf-8"))
        doc = plain_doc(a.md.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"BLAD wejscia: {e}", file=sys.stderr)
        return 2
    if isinstance(edits, dict):
        edits = edits.get("edits", [])
    wyniki = sprawdz(edits, doc)
    zle = [w for w in wyniki if not w["ok"]]
    if a.output and (not zle or a.tylko_poprawne):
        a.output.write_text(json.dumps([w["edit"] for w in wyniki if w["ok"]], ensure_ascii=False, indent=2),
                            encoding="utf-8")
    if a.json:
        print(json.dumps(wyniki, ensure_ascii=False, indent=2))
    else:
        for w in wyniki:
            znak = "OK " if w["ok"] else "ZLE"
            print(f"[{znak}] #{w['nr']}{' ' + w['id'] if w.get('id') else ''}: "
                  f"{w['edit'].get('target_text', '')[:70]!r} " + "; ".join(w["problemy"]))
            for k in w.get("konteksty", []):
                print(f"        {k}")
        print(f"edycji {len(wyniki)} | poprawnych {len(wyniki) - len(zle)} | do poprawy {len(zle)}"
              + (f" | zapisano {a.output}" if a.output and (not zle or a.tylko_poprawne) else ""))
    return 1 if zle else 0


if __name__ == "__main__":
    sys.exit(main())
