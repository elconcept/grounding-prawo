import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/'selection/overlay/shared/format-pisma'
sys.path.insert(0, str(SRC))
spec = importlib.util.spec_from_file_location('wersja_pisma', SRC/'wersja_pisma.py')
wersja_pisma = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wersja_pisma)


def test_text_reads_all_pages_and_drops_page_headers(monkeypatch):
    def fake_adeu(*args, check=True):
        assert args[:2] == ('extract', 'pismo.docx')
        assert args[args.index('--page') + 1] == 'all'
        out = Path(args[args.index('-o') + 1])
        out.write_text(
            '> **File Path:** /tmp/pismo.docx\n\n'
            '> **Page 1**\n\nStrona pierwsza\n\n'
            '> **Page 2**\n\nStrona druga\n\n'
            '> **Page 3**\n\nStrona trzecia\n',
            encoding='utf-8')
        return ''

    monkeypatch.setattr(wersja_pisma, 'adeu', fake_adeu)
    text = wersja_pisma.text('pismo.docx')

    assert 'Strona pierwsza' in text
    assert 'Strona druga' in text
    assert 'Strona trzecia' in text
    assert '> **' not in text
