"""lens_runner.py z atrapami `claude` i `codex`: zapis ustaleń z proweniencją, stop bez zastępstwa,
odrzucenie w synteza.py pliku ustaleń, którego nie wytworzył wykonawca.

  python3 -m unittest discover -s own-skills/szturm-na-draft-pl/tests -p 'test_lens_runner.py'
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SZ = Path(__file__).resolve().parent.parent / "scripts"

USTALENIE = [{"dokument": "PISMO", "kotwica": "pismo.clean.nl.txt:3", "klasa": "LOGIKA", "waga": "🟠",
              "naprawa": "DECYZJA_AUTORA", "komentarz": "teza nie na pierwszej stronie"}]

ATRAPA = r'''#!/usr/bin/env python3
import json, os, sys
if "--version" in sys.argv:
    print("atrapa 1.0"); sys.exit(0)
prompt = sys.stdin.read()
open(os.environ["ATRAPA_LOG"], "a").write(json.dumps({"argv": sys.argv, "len": len(prompt),
    "akta": "TAJNE_AKTA" in prompt}) + "\n")
tryb = os.environ.get("ATRAPA_TRYB", "ok")
tekst = {"ok": json.dumps(USTALENIE), "zly": "Wszystko OK, brak uwag.", "pusty": "[]"}[tryb]
if os.path.basename(sys.argv[0]) == "claude":
    print(json.dumps({"result": tekst, "is_error": False, "modelUsage": {"claude-sonnet-x": {}, "claude-haiku-x": {}}}))
else:
    open(sys.argv[sys.argv.index("-o") + 1], "w").write(tekst)
'''.replace("USTALENIE", repr(USTALENIE))


class LensRunner(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = Path(self.tmp.name)
        self.bin = t / "bin"
        self.bin.mkdir()
        for n in ("claude", "codex"):
            (self.bin / n).write_text(ATRAPA)
            (self.bin / n).chmod(0o755)
        skill = t / "skill"
        (skill / "modules" / "sedzia").mkdir(parents=True)
        (skill / "modules" / "sedzia" / "MODULE.md").write_text("# Sędzia\nCzytaj na zimno.")
        (skill / "modules" / "sub").mkdir(parents=True)
        (skill / "modules" / "sub" / "MODULE.md").write_text("# Subsumpcja")
        self.cfg = skill / "cfg.json"
        self.cfg.write_text(json.dumps({
            "providers": {"claude": {"command": "claude", "model": "sonnet"},
                          "codex": {"command": "codex", "model": "gpt-6.1-sol", "reasoning_effort": "high"}},
            "lenses": {"sedzia": {"providers": ["claude"], "izolacja": "zimna", "mandat": ["modules/sedzia/MODULE.md"]},
                       "sub": {"providers": ["codex", "claude"], "izolacja": "material", "mandat": ["modules/sub/MODULE.md"]}},
            "skroty": {}}))
        self.skill = skill
        self.run = t / "RUN"
        self.run.mkdir()
        (self.run / "pismo.clean.nl.txt").write_text("1\tPISMO\n2\t\n3\tTeza.\n")
        (self.run / "akta.md").write_text("TAJNE_AKTA protokół")
        self.log = t / "log.jsonl"

    def tearDown(self):
        self.tmp.cleanup()

    def uruchom(self, *lens, tryb="ok"):
        env = dict(os.environ, PATH=f"{self.bin}:{os.environ['PATH']}", ATRAPA_TRYB=tryb, ATRAPA_LOG=str(self.log))
        args = [sys.executable, str(SZ / "lens_runner.py"), "--run", str(self.run), "--draft",
                str(self.run / "pismo.clean.nl.txt"), "--teza", "T", "--material", str(self.run / "akta.md"),
                "--skill-dir", str(self.skill), "--config", str(self.cfg)]
        for x in lens:
            args += ["--lens", x]
        return subprocess.run(args, env=env, capture_output=True, text=True)

    def wywolania(self):
        return [json.loads(x) for x in self.log.read_text().splitlines()]

    def test_ok_proweniencja_i_synteza(self):
        r = self.uruchom("sedzia", "sub")
        self.assertEqual(r.returncode, 0, r.stderr)
        pliki = sorted(p.name for p in (self.run / "ustalenia").iterdir())
        self.assertEqual(pliki, ["11_sedzia.json", "12_sub__claude.json", "12_sub__codex.json"])
        u = json.loads((self.run / "ustalenia" / "11_sedzia.json").read_text())
        self.assertEqual(u[0]["soczewka"], "sedzia")
        self.assertEqual(u[0]["kotwica"], "pismo.clean.md:3")
        self.assertEqual(u[0]["_proweniencja"]["model_uzyty"], "claude-sonnet-x")
        mf = json.loads((self.run / "soczewki" / "manifest.json").read_text())
        self.assertEqual(len(mf["przebiegi"]), 3)
        # izolacja: soczewka zimna nie dostaje akt, materiałowa dostaje
        w = self.wywolania()
        self.assertIn(False, [x["akta"] for x in w])
        self.assertIn(True, [x["akta"] for x in w])
        codex = next(x for x in w if x["argv"][0].endswith("codex"))
        self.assertIn("--ignore-user-config", codex["argv"])
        self.assertIn("read-only", codex["argv"])
        s = subprocess.run([sys.executable, str(SZ / "synteza.py"), str(self.run / "ustalenia"),
                            "-o", str(self.run / "out")], capture_output=True, text=True)
        self.assertNotEqual(s.returncode, 3, s.stderr)

    def test_zla_odpowiedz_stop_bez_pliku(self):
        r = self.uruchom("sedzia", tryb="zly")
        self.assertEqual(r.returncode, 2)
        self.assertFalse((self.run / "ustalenia" / "11_sedzia.json").exists())
        self.assertTrue((self.run / "soczewki" / "bledy" / "11_sedzia.json").exists())
        self.assertEqual(len(self.wywolania()), 2)  # jedna próba naprawy u tego samego wykonawcy

    def test_synteza_odrzuca_ustalenia_koordynatora(self):
        self.assertEqual(self.uruchom("sedzia").returncode, 0)
        (self.run / "ustalenia" / "20_atak.json").write_text(json.dumps(
            [dict(USTALENIE[0], soczewka="atak-przeciwnika-pl")]))
        s = subprocess.run([sys.executable, str(SZ / "synteza.py"), str(self.run / "ustalenia"),
                            "-o", str(self.run / "out")], capture_output=True, text=True)
        self.assertEqual(s.returncode, 3)
        self.assertIn("20_atak.json", s.stderr)
        # zmiana pliku wykonawcy po fakcie też odpada
        (self.run / "ustalenia" / "20_atak.json").unlink()
        f = self.run / "ustalenia" / "11_sedzia.json"
        f.write_text(f.read_text().replace("🟠", "🟢"))
        s = subprocess.run([sys.executable, str(SZ / "synteza.py"), str(self.run / "ustalenia"),
                            "-o", str(self.run / "out")], capture_output=True, text=True)
        self.assertEqual(s.returncode, 3)

    def test_e1_bez_manifestu(self):
        (self.run / "ustalenia").mkdir()
        (self.run / "ustalenia" / "01_e1.json").write_text(json.dumps(
            [dict(USTALENIE[0], soczewka="citation-grounding-pl", klasa="CYTAT")]))
        s = subprocess.run([sys.executable, str(SZ / "synteza.py"), str(self.run / "ustalenia"),
                            "-o", str(self.run / "out")], capture_output=True, text=True)
        self.assertNotEqual(s.returncode, 3, s.stderr)

    def test_brak_cli(self):
        env = dict(os.environ, PATH="/nonexistent")
        r = subprocess.run([sys.executable, str(SZ / "lens_runner.py"), "--run", str(self.run), "--draft",
                            str(self.run / "pismo.clean.nl.txt"), "--skill-dir", str(self.skill),
                            "--config", str(self.cfg), "--lens", "sedzia"], env=env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("nie może", r.stderr)


if __name__ == "__main__":
    unittest.main()
