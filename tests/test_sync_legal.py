import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('sync_legal', Path(__file__).parents[1] / 'scripts/sync_legal.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class SyncTests(unittest.TestCase):
    def test_preserves_local_content_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, target = root / 'source', root / 'legal'
            source.mkdir(); target.mkdir()
            for name in ('ZASADY-PLUGINU.md', 'STYLE.md', 'ARTEFAKTY-SPRAWY.md'):
                (source / name).write_text(name)
            (target / 'AGENTS.md').write_text('Lokalne zasady\n' + sync.LEGACY_AGENTS)
            (target / 'CLAUDE.md').write_text('@AGENTS.md\n' + sync.LEGACY_CLAUDE)
            (target / 'output').mkdir()
            (target / 'output/pismo.md').write_text('dane użytkownika')
            sync.sync(source, target)
            first = {str(p.relative_to(target)): p.read_bytes() for p in target.rglob('*') if p.is_file()}
            sync.sync(source, target)
            self.assertEqual(first, {str(p.relative_to(target)): p.read_bytes() for p in target.rglob('*') if p.is_file()})
            self.assertIn('Lokalne zasady', (target / 'AGENTS.md').read_text())
            self.assertNotIn('wszystkie formaty', (target / 'CLAUDE.md').read_text())
            self.assertEqual((target / 'output/pismo.md').read_text(), 'dane użytkownika')
            (source / 'STYLE.md').write_text('nowy styl')
            sync.sync(source, target)
            self.assertEqual((target / '.agents/grounding-prawo/shared/STYLE.md').read_text(), 'nowy styl')

    def test_bad_markers_fail_before_writing(self):
        for text in (sync.START, sync.END, sync.END + sync.START, sync.START + sync.END + sync.START + sync.END):
            with self.assertRaises(ValueError):
                sync.update_pointer(text)

    def test_missing_source_does_not_touch_target(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'AGENTS.md').write_text('zachowaj')
            with self.assertRaises(ValueError):
                sync.sync(root / 'missing', root)
            self.assertEqual((root / 'AGENTS.md').read_text(), 'zachowaj')
