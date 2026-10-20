"""Marketplace users receive wiki procedures without the repository README."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/grounding-prawo/skills'


def test_wiki_rules_are_bundled_and_reachable():
    for name in ('WIKI.md', 'BASIC-MEMORY.md'):
        assert (SKILLS / 'shared' / name).read_bytes() == (
            ROOT / 'selection/overlay/shared' / name
        ).read_bytes()
    for name in ('wiki-basic-memory', 'prawny-router-v3'):
        text = (SKILLS / name / 'SKILL.md').read_text()
        assert 'shared/BASIC-MEMORY.md' in text
    assert 'shared/WIKI.md' in (SKILLS / 'shared/BASIC-MEMORY.md').read_text()
    # ingest-wiki jest modułem skilla wiki-basic-memory (merge_into), nie osobnym skillem
    assert not (SKILLS / 'ingest-wiki').exists()
    ingest = (SKILLS / 'wiki-basic-memory/modules/ingest-wiki/MODULE.md').read_text()
    assert 'modules/ingest-wiki/MODULE.md' in (SKILLS / 'wiki-basic-memory/SKILL.md').read_text()
    assert 'the-ocr-ingest-page' in ingest and 'R2' in ingest
    assert 'wiki-basic-memory' in (SKILLS / 'shared/SCIEZKI-PRACY.md').read_text()
