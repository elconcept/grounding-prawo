"""Inherited instructions must preserve the owner's complete-document workflow."""

import collections
import tempfile
import unittest
from pathlib import Path

from scripts.build import scrub_file


class DocumentPolicyTests(unittest.TestCase):
    def scrub(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'SKILL.md'
            path.write_text(text, encoding='utf-8')
            scrub_file(str(path), [], collections.Counter())
            return path.read_text(encoding='utf-8')

    def test_confidentiality_gate_removed_without_losing_signature_checks(self):
        result = self.scrub(
            '## Ochrona danych\n\n'
            '- **Próg poufności** - przy wątpliwości nie przekazuj.\n'
            '- **Metadane przy wysyłce** - wyczyść autora.\n'
            '- Sprawdź integralność podpisu PDF.\n'
        )
        self.assertNotIn('Próg poufności', result)
        self.assertNotIn('wyczyść autora', result)
        self.assertIn('Sprawdź integralność podpisu PDF.', result)

    def test_connector_guidance_survives_removing_inherited_gate(self):
        result = self.scrub(
            'Konektory SAOS i KRS. Dane sprawy objęte tajemnicą lub wrażliwe - '
            'oceń osobno, czy w ogóle wnosić je do narzędzia; przy wątpliwości nie przekazuj.\n'
        )
        self.assertIn('Konektory SAOS i KRS.', result)
        self.assertNotIn('nie przekazuj', result)

    def test_owner_policy_and_document_identifiers_preserved(self):
        text = (
            '## KONFIGURACJA PLUGINU\n\n'
            'Bez anonimizacji. Zachowaj PESEL: 00000000000 i dane medyczne.\n'
        )
        self.assertEqual(self.scrub(text), text)


if __name__ == '__main__':
    unittest.main()
