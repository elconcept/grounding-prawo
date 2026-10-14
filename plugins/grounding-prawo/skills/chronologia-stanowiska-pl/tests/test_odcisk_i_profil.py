"""Odcisk akt, "nieocenione" i profil do sadu (v0.2.0).

Pomysly (nie kod) z oceny GSkuza/AI-Legal-SkillsPL, legal-abduction, 2026-10-10:
- wynik jest powiazany z wersja tekstu akt, na ktorej powstal; zmiana akt po budowie
  nie przechodzi po cichu,
- brak oceny to nie "nic nie ma": pole nieobecne = nieocenione, pusta lista = sprawdzono,
- dwa profile: roboczy oznacza watpliwosci, profil "sad" je blokuje.
"""
import json
import shutil
import sys
from pathlib import Path

TU = Path(__file__).parent
sys.path.insert(0, str(TU.parent / "scripts"))
import bramka_lokatorow as b  # noqa: E402

AKTA = TU / "fixtures" / "akta-tekst"


def _wczytaj(nazwa):
    return json.loads((TU / "fixtures" / nazwa).read_text(encoding="utf-8"))


def _uruchom(tmp_path, dane, akta=AKTA, *extra):
    p = tmp_path / "wynik.json"
    p.write_text(json.dumps(dane, ensure_ascii=False), encoding="utf-8")
    return b.main([str(p), str(akta), *extra]), p


def _raport(p):
    return p.with_suffix(".bramka.md").read_text(encoding="utf-8")


def _kopia_akt(tmp_path):
    kat = tmp_path / "akta"
    shutil.copytree(AKTA, kat)
    return kat


# --- odcisk akt ---

def test_odcisk_liczony_z_tekstu_niezalezny_od_konca_linii(tmp_path):
    kat = _kopia_akt(tmp_path)
    p = kat / "pozew.txt"
    lf = b.odcisk_akt(kat)["pozew"]
    p.write_bytes(p.read_text(encoding="utf-8").replace("\n", "\r\n").encode("utf-8"))
    assert b.odcisk_akt(kat)["pozew"] == lf


def test_fixture_ma_zgodny_odcisk_ok(tmp_path):
    rc, p = _uruchom(tmp_path, _wczytaj("chronologia.json"))
    assert rc == b.OK, _raport(p)


def test_brak_odcisku_uwagi_w_profilu_roboczym(tmp_path):
    d = _wczytaj("chronologia.json"); d.pop("akta_odcisk")
    rc, p = _uruchom(tmp_path, d)
    assert rc == b.UWAGI and "OD01" in _raport(p)


def test_raport_podaje_odcisk_do_wpisania(tmp_path):
    d = _wczytaj("chronologia.json"); d.pop("akta_odcisk")
    _, p = _uruchom(tmp_path, d)
    assert b.odcisk_akt(AKTA)["pozew"] in _raport(p)


def test_akta_zmienione_po_budowie_uwagi(tmp_path):
    # cytaty nadal stoja na swoich stronach - zmienil sie inny fragment tekstu (np. ponowny OCR)
    kat = _kopia_akt(tmp_path)
    p = kat / "korespondencja.txt"
    p.write_text(p.read_text(encoding="utf-8") + "\nDopisek po ponownym OCR.\n", encoding="utf-8")
    rc, raport_p = _uruchom(tmp_path, _wczytaj("chronologia.json"), kat)
    raport = _raport(raport_p)
    assert rc == b.UWAGI and "OD02" in raport and "korespondencja" in raport


def test_plik_akt_uzyty_a_nieobjety_odciskiem_uwagi(tmp_path):
    d = _wczytaj("chronologia.json"); d["akta_odcisk"].pop("umowa")
    rc, p = _uruchom(tmp_path, d)
    assert rc == b.UWAGI and "OD03" in _raport(p)


def test_odcisk_zlego_ksztaltu_blokada(tmp_path):
    d = _wczytaj("chronologia.json"); d["akta_odcisk"] = "abc"
    rc, p = _uruchom(tmp_path, d)
    assert rc == b.BLOKADA and "OD04" in _raport(p)


# --- nieocenione != pusto ---

def test_pusta_lista_dowodow_przeciw_to_ocena_ok(tmp_path):
    d = _wczytaj("zestawienie.json")
    assert d["elementy"][0]["dowody_przeciw"] == []
    rc, p = _uruchom(tmp_path, d)
    assert rc == b.OK, _raport(p)


def test_brak_pola_dowody_przeciw_to_nieocenione_uwagi(tmp_path):
    d = _wczytaj("zestawienie.json"); d["elementy"][0].pop("dowody_przeciw")
    rc, p = _uruchom(tmp_path, d)
    raport = _raport(p)
    assert rc == b.UWAGI and "NA01" in raport and "dowody_przeciw" in raport


# --- profil do sadu ---

def test_profil_sad_czyste_ok(tmp_path):
    rc, p = _uruchom(tmp_path, _wczytaj("zestawienie.json"), AKTA, "--profil", "sad")
    assert rc == b.OK, _raport(p)


def test_profil_sad_brak_odcisku_blokada(tmp_path):
    d = _wczytaj("chronologia.json"); d.pop("akta_odcisk")
    rc, p = _uruchom(tmp_path, d, AKTA, "--profil", "sad")
    assert rc == b.BLOKADA and "OD01" in _raport(p)


def test_profil_sad_zmienione_akta_blokada(tmp_path):
    kat = _kopia_akt(tmp_path)
    p = kat / "umowa.txt"
    p.write_text(p.read_text(encoding="utf-8") + "\nAneks.\n", encoding="utf-8")
    rc, raport_p = _uruchom(tmp_path, _wczytaj("chronologia.json"), kat, "--profil", "sad")
    assert rc == b.BLOKADA and "OD02" in _raport(raport_p)


def test_profil_sad_nieocenione_blokada(tmp_path):
    d = _wczytaj("zestawienie.json"); d["elementy"][0].pop("dowody_przeciw")
    rc, p = _uruchom(tmp_path, d, AKTA, "--profil", "sad")
    assert rc == b.BLOKADA and "NA01" in _raport(p)


def test_profil_sad_fakt_spoza_akt_blokada(tmp_path):
    d = _wczytaj("chronologia.json"); d["wpisy"][0]["pochodzenie"] = "uzytkownik"
    rc, p = _uruchom(tmp_path, d, AKTA, "--profil", "sad")
    assert rc == b.BLOKADA and "ZR12" in _raport(p)


def test_profil_sad_nie_zmienia_wpisu_w_porzadku(tmp_path):
    # kontrola pozytywna profilu: zaostrza tylko wskazane kody, nie wszystko
    d = _wczytaj("chronologia.json")
    rc, _ = _uruchom(tmp_path, d, AKTA, "--profil", "sad")
    assert rc == b.OK


def test_nieznany_profil_odrzucony_a_znany_przyjety(tmp_path):
    import pytest
    # bez tej polowy test przechodzil przed v0.2.0, bo argparse odrzucal KAZDA nieznana flage
    rc, _ = _uruchom(tmp_path, _wczytaj("chronologia.json"), AKTA, "--profil", "robocza")
    assert rc == b.OK
    with pytest.raises(SystemExit):
        _uruchom(tmp_path, _wczytaj("chronologia.json"), AKTA, "--profil", "luzny")
