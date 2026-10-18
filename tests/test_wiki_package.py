"""Marketplace users receive wiki procedures without the repository README."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/grounding-prawo/skills'


def test_wiki_rules_are_bundled_and_reachable():
    for name in ('WIKI.md', 'BASIC-MEMORY.md'):
        assert (SKILLS / 'shared' / name).read_bytes() == (
            ROOT / 'selection/overlay/shared' / name
        ).read_bytes()
    for name in ('ingest-wiki', 'wiki-basic-memory', 'prawny-router-v3'):
        text = (SKILLS / name / 'SKILL.md').read_text()
        assert 'shared/BASIC-MEMORY.md' in text
    assert 'shared/WIKI.md' in (SKILLS / 'shared/BASIC-MEMORY.md').read_text()
    ingest = (SKILLS / 'ingest-wiki/SKILL.md').read_text()
    assert 'inspect_page' in ingest and 'verify_page' in ingest
    assert 'wiki-basic-memory' in (SKILLS / 'shared/SCIEZKI-PRACY.md').read_text()
