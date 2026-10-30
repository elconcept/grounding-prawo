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


def test_nazwa_bez_daty_godziny_i_wersji():
    n = wersja_pisma.nazwa
    assert n('drafty/20261024_1233_wniosek_o_sprostowanie_protokolu_v15.md') == 'wniosek_o_sprostowanie_protokolu'
    assert n('drafty/20261024_wniosek_v3.md') == 'wniosek'
    assert n('output/II_W_1342_26_wniosek.docx') == 'II_W_1342_26_wniosek'


W = '<w:p><w:pPr><w:rPr><w:rFonts w:ascii="Georgia"/><w:sz w:val="20"/></w:rPr></w:pPr>{}</w:p>'


def test_wstawka_dostaje_czcionke_otoczenia():
    x = W.format('<w:ins w:id="1" w:author="A"><w:r><w:t>Nowe zdanie. </w:t></w:r></w:ins>'
                 '<w:r><w:rPr><w:rFonts w:ascii="Georgia"/><w:sz w:val="20"/></w:rPr><w:t>Stare.</w:t></w:r>')
    y = wersja_pisma.unify_fonts(x)
    assert y.count('<w:rFonts w:ascii="Georgia"/>') == 3


def test_lista_numer_spacja_bez_tabulatora():
    x = ('<w:p><w:pPr><w:tabs><w:tab w:val="left" w:pos="567"/></w:tabs><w:ind w:left="567" w:hanging="567"/></w:pPr>'
         '<w:r><w:rPr><w:sz w:val="24"/></w:rPr><w:t>2.</w:t></w:r><w:r><w:tab/><w:t>tekst</w:t></w:r></w:p>')
    y = wersja_pisma.list_space(x)
    assert '<w:tab/>' not in y and 'hanging' not in y and '<w:tabs>' not in y
    assert '>2. </w:t>' in y and 'w:val="24"' not in y


def test_akceptacja_zachowuje_komentarze():
    x = ('<w:p><w:r><w:t>A</w:t></w:r><w:del w:id="2" w:author="A"><w:r><w:delText>B</w:delText></w:r></w:del>'
         '<w:ins w:id="3" w:author="A"><w:r><w:t>C</w:t></w:r></w:ins>'
         '<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="9"/></w:r></w:p>')
    y = wersja_pisma.accept_xml(x)
    assert 'B' not in y and '>C<' in y and 'commentReference w:id="9"' in y and '<w:ins' not in y


def _adeu_dostepny():
    import shutil
    return bool(shutil.which('uvx') or shutil.which('adeu'))


def test_redline_dlugiego_docx_na_prawdziwym_adeu(tmp_path, monkeypatch):
    """DOCX dłuższy niż jedna syntetyczna strona adeu: text() bez banerów stron, redline --tekst przechodzi."""
    import pytest
    docx = pytest.importorskip('docx')
    if not _adeu_dostepny():
        pytest.skip('brak uvx/adeu')
    pismo = tmp_path/'pismo.docx'
    d = docx.Document()
    for i in range(400):
        d.add_paragraph(f'Akapit {i}: ' + 'tekst pisma procesowego ' * 8)
    d.save(pismo)

    s = wersja_pisma.text(str(pismo))
    assert 'Akapit 0:' in s and 'Akapit 399:' in s
    assert 'Page 1 of' not in s and 'Continues on page' not in s

    nowa = tmp_path/'nowa.md'
    nowa.write_text(s.replace('Akapit 399:', 'Akapit ostatni:'), encoding='utf-8')
    monkeypatch.setattr(sys, 'argv', ['wersja_pisma.py', 'redline', '--docx', str(pismo),
                                      '--tekst', str(nowa), '--author', 'Test'])
    wersja_pisma.redline()
    c = wersja_pisma.changes(str(pismo))
    assert c['w:ins'] and c['w:del']
