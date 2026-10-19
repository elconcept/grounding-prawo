#!/usr/bin/env python3
"""Publish canonical plugin rules into a legal worktree; preserve local instructions."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- grounding-prawo:begin -->'
END = '<!-- grounding-prawo:end -->'
BLOCK = f'''{START}
## Kanoniczne reguły praktyki prawnej

Przed pracą przeczytaj `.agents/grounding-prawo/shared/ZASADY-PLUGINU.md`.
Przed redakcją pisma przeczytaj `.agents/grounding-prawo/shared/STYLE.md`.
Przed zapisem plików przeczytaj `.agents/grounding-prawo/shared/ARTEFAKTY-SPRAWY.md`.
Ścieżki `shared/` w tych dokumentach oznaczają `.agents/grounding-prawo/shared/`;
pozostałe skille pochodzą z zainstalowanego pluginu grounding-prawo.
Reguły źródeł, stylu i wersjonowania są kanoniczne w grounding-prawo; nie duplikuj ich lokalnie.
Ten blok oraz `.agents/grounding-prawo/` aktualizuje CI grounding-prawo.
{END}
'''
LEGACY_CLAUDE = 'Kopie najnowszego pisma w `output/` obejmują wszystkie formaty, w tym `.md` i `.docx`.\n'
LEGACY_AGENTS = '''13. Nowa wersja draftu albo nowy draft → kopia w `output/`, poprzednie wersje w folderze sprawy.
    Przy aktualizacji usuwasz kopię poprzedniej wersji z `output/` i wstawiasz nową (wyjątek od
    zasady 5 „niczego nie usuwaj”, wyłącznie dla `output/`), po sprawdzeniu `cmp`, że usuwana wersja
    jest w `sprawy/<sprawa>/drafty/`. W `output/` zawsze dokładnie jedna, najnowsza wersja każdego pisma.
'''


def update_pointer(text):
    if text.count(START) != text.count(END) or text.count(START) > 1:
        raise ValueError('Nieprawidłowe znaczniki grounding-prawo')
    if START in text:
        a, b = text.index(START), text.index(END)
        if b < a:
            raise ValueError('Odwrócone znaczniki grounding-prawo')
        return text[:a] + BLOCK.rstrip('\n') + text[b + len(END):]
    return text.rstrip() + '\n\n' + BLOCK


def sync(source, target):
    source, target = Path(source), Path(target)
    for name in ('ZASADY-PLUGINU.md', 'STYLE.md', 'ARTEFAKTY-SPRAWY.md'):
        if not (source / name).is_file():
            raise ValueError(f'Brak reguł: {name}')
    if not (target / 'AGENTS.md').is_file():
        raise ValueError('Cel musi być istniejącym projektem legal z AGENTS.md')
    managed = target / '.agents/grounding-prawo'
    for p in (target / '.agents', managed, target / 'AGENTS.md', target / 'CLAUDE.md'):
        if p.is_symlink():
            raise ValueError(f'Cel nie może być dowiązaniem: {p}')
    updates = {}
    for name in ('AGENTS.md', 'CLAUDE.md'):
        path = target / name
        text = path.read_text() if path.exists() else ''
        text = text.replace(LEGACY_CLAUDE, '').replace(LEGACY_AGENTS,
            '13. Publikacja i historia pism: `.agents/grounding-prawo/shared/ARTEFAKTY-SPRAWY.md`.\n'
            '    To wyjątek od zasady 5 dla zastępowanego DOCX pisma w `output/`,\n'
            '    po zapisaniu snapshotu MD zgodnie z regułą kanoniczną.\n')
        updates[path] = update_pointer(text)
    # Build and validate the entire payload before touching the destination.
    with tempfile.TemporaryDirectory() as temp:
        staged = Path(temp) / 'shared'
        shutil.copytree(source, staged, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '@eaDir'))
        hashes = {str(p.relative_to(staged)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(staged.rglob('*')) if p.is_file()}
        managed.mkdir(parents=True, exist_ok=True)
        old = managed / 'shared'
        if old.is_symlink():
            raise ValueError('Katalog shared nie może być dowiązaniem')
        # Only this generated subtree is owned by the synchronizer; no case files are touched.
        old.mkdir(exist_ok=True)
        for rel in hashes:
            dest = old / rel
            if dest.is_symlink() or any(p.is_symlink() for p in dest.parents if p != old.parent):
                raise ValueError(f'Dowiązanie w katalogu zarządzanym: {dest}')
        for rel in hashes:
            dest = old / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=dest.parent, delete=False) as tmp:
                tmp.write((staged / rel).read_bytes())
                temp_path = Path(tmp.name)
            temp_path.chmod(0o644)
            temp_path.replace(dest)
        # Remove stale generated files only after all replacement files have been written.
        for dest in old.rglob('*'):
            if dest.is_file() and str(dest.relative_to(old)) not in hashes:
                dest.unlink()
        manifest = managed / 'manifest.json'
        manifest.write_text(json.dumps(hashes, ensure_ascii=False, indent=2) + '\n')
    for path, text in updates.items():
        path.write_text(text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=Path, help='worktree projektu legal')
    parser.add_argument('--source', type=Path, default=ROOT / 'plugins/grounding-prawo/skills/shared')
    args = parser.parse_args()
    sync(args.source, args.target)
