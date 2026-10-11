"""Adapter natywnych odpowiedzi konektorow MCP MateMatic -> wejscie klasyfikuj_odpowiedz().

Realizuje krok 4 z DOKUMENTACJA-WDROZENIOWA (sekcja 2): test_mcp_protocol.py zaklada
wejscie {"pozycje": [...]} / {"blad": "..."}, a konektory isap / saos / nsa / krs /
eu-sparql / eureka (przez mcp/gp-cache.mjs) zwracaja wynik tools/call:
    {"isError": bool, "structuredContent": {"citations": [...]} | {"error_code": "..."}}

Uzycie:
    python adapter_mcp_matematic.py --self-test      # 4 sciezki na prawdziwych odpowiedziach (przyklady/)
"""
import argparse
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_mcp_protocol import klasyfikuj_odpowiedz, wymaga_fallbacku_hardgate  # noqa: E402

ID_POLA = ("display_address", "case_number", "signature", "celex", "ecli", "krs", "eli", "title")
DATA_POLA = ("promulgation", "judgment_date", "publication_date", "issue_date", "odpis_date", "date")
NIEAKTUALNE = ("tekst_jednolity_nieaktualny", "tekst_ogloszony_istnieje_nowszy_jednolity")


def _status(c, sc):
    if sc.get("text_version") in NIEAKTUALNE:
        return "tekst_jednolity_nieaktualny"
    stan = c.get("in_force")
    if stan == "IN_FORCE":
        return "obowiazuje"
    if stan in ("NOT_IN_FORCE", "REPEALED", "EXPIRED"):
        return "uchylony"
    if stan:
        return "nieznany"
    return "nie_dotyczy"  # orzeczenie, podmiot KRS, interpretacja - bez statusu obowiazywania


def _norm(s):
    return " ".join(str(s).upper().split())


def z_odpowiedzi_mcp(wynik, sygnatura=None):
    """Wynik tools/call (result) -> {"pozycje": [...]} albo {"blad": "..."}.
    `sygnatura` (search_by_case): zostaw tylko dokladne trafienia - CBOSA dokleja
    orzeczenia powiazane (np. WSA z I instancji tej samej sprawy)."""
    sc = wynik.get("structuredContent") or {}
    if wynik.get("isError"):
        kod = sc.get("error_code") or "error"
        return {"pozycje": []} if kod == "not_found" else {"blad": kod}
    cyt = sc.get("citations") or []
    if sygnatura:
        cyt = [c for c in cyt if _norm(c.get("case_number") or c.get("signature") or "") == _norm(sygnatura)]
    pozycje, widziane = [], set()
    for c in cyt:
        ident = next((str(c[k]) for k in ID_POLA if c.get(k)), "")
        if ident in widziane:  # kilka dokumentow tej samej sprawy (wyrok + uzasadnienie)
            continue
        widziane.add(ident)
        pozycje.append({
            "identyfikator": ident,
            "tytul": c.get("title", ""),
            "status_obowiazywania": _status(c, sc),
            "data": next((c[k] for k in DATA_POLA if c.get(k)), ""),
            "url": c.get("url", ""),
        })
    return {"pozycje": pozycje}


def klasyfikuj_mcp(wynik, zrodlo, query_type="akt_prawny", sygnatura=None):
    return klasyfikuj_odpowiedz(z_odpowiedzi_mcp(wynik, sygnatura), zrodlo=zrodlo, query_type=query_type)


class TestPrawdziweKonektory(unittest.TestCase):
    """Cztery sciezki protokolu (FOUND / NOT_FOUND / AMBIGUOUS / ERROR) na odpowiedziach
    pobranych z prawdziwych konektorow (przyklady/mcp_matematic_odpowiedzi.json)."""

    def test_sciezki(self):
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "przyklady", "mcp_matematic_odpowiedzi.json")
        dane = json.load(open(p, encoding="utf-8"))
        widziane = set()
        for przypadek in dane["przypadki"]:
            with self.subTest(przypadek["opis"]):
                wynik = klasyfikuj_mcp(przypadek["wynik"], zrodlo=przypadek["serwer"],
                                       sygnatura=przypadek["argumenty"].get("caseNumber"))
                self.assertEqual(wynik["status"], przypadek["oczekiwany_status"])
                if wynik["status"] != "FOUND":
                    self.assertTrue(wymaga_fallbacku_hardgate(wynik))
                widziane.add(wynik["status"])
        self.assertEqual(widziane, {"FOUND", "NOT_FOUND", "AMBIGUOUS", "ERROR"})


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        r = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestPrawdziweKonektory))
        sys.exit(0 if r.wasSuccessful() else 1)
    ap.print_help()
