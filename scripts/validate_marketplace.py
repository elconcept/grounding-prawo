#!/usr/bin/env python3
"""Validate the distributable package, not just the marketplace JSON.

This does not test authenticated Claude/Cowork or ChatGPT server-side sync.
"""
import json
from pathlib import Path
import re
import sys
import yaml


# humanizer-pl zachowuje mechanikę upstreamu: jego frontmatter zawiera pola
# spoza minimalnego zestawu Agent Skills (wersja, atrybucja).
VERBATIM_UPSTREAM = {'humanizer-pl'}
UPSTREAM_FIELDS = {'version', 'attribution', 'compatibility', 'data-residency',
                   'requires-human-approval', 'pii-egress'}


def validate(root):
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)
    def read_json(path):
        return json.loads(path.read_text(encoding="utf-8"))
    try:
        claude = read_json(root / ".claude-plugin/marketplace.json")
        codex = read_json(root / ".agents/plugins/marketplace.json")
        check(claude['name'] == codex['name'], 'Marketplace names differ')
        check(len(claude['plugins']) == 1 and len(codex['plugins']) == 2, 'Expected original Claude plugin and two Codex marketplace entries')
        cp = claude['plugins'][0]
        op = next((item for item in codex['plugins'] if item['name'] == cp['name']), None)
        check(op is not None, 'Original plugin missing from Codex marketplace')
        if op is None:
            return errors
        check(cp['source'] == op['source']['path'], 'Plugin source paths differ')
        plugin = (root / cp['source']).resolve()
        check(plugin.is_relative_to(root.resolve()), 'Plugin escapes repository')
        cm = read_json(plugin / '.claude-plugin/plugin.json')
        om = read_json(plugin / '.codex-plugin/plugin.json')
        check(cm['name'] == om['name'] == cp['name'] == op['name'] == plugin.name, 'Plugin names differ')
        check('version' not in cm, 'Claude manifest must not pin version (SHA commita steruje aktualizacjami)')
        check(bool(re.fullmatch(r'\d+\.\d+\.\d+', om['version'])), 'Expected release semver in Codex manifest')
        for key in ('displayName', 'shortDescription', 'longDescription', 'developerName'):
            check(isinstance(om['interface'].get(key), str) and bool(om['interface'][key]), f'Missing interface.{key}')
        check(bool(om['interface'].get('defaultPrompt')), 'Missing defaultPrompt')
        check(isinstance(om['interface'].get('capabilities'), list), 'Missing capabilities')
        check(om.get('mcpServers') == './.mcp.json', 'MCP companion file not declared')
        read_json(plugin / '.mcp.json')
        skills = list((plugin / 'skills').glob('*/SKILL.md'))
        selected = yaml.safe_load((root / 'selection/selection.yaml').read_text())
        import importlib.util
        spec = importlib.util.spec_from_file_location("marketplace_build", root / "scripts/build.py")
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        for entry in selected['keep']:
            check((Path(builder.source(entry)) / 'SKILL.md').is_file(), f"Missing source: {entry['name']}")
        expected = {e['name'] for e in selected['keep'] if not e.get('fold_into') and not e.get('merge_into')}
        for e in selected['keep']:
            if e.get('merge_into'):
                check((plugin / 'skills' / e['merge_into'] / 'modules' / e['name'] / 'MODULE.md').is_file(),
                      f"{e['name']}: brak modułu w {e['merge_into']}/modules/")
        check({p.parent.name for p in skills} == expected, 'Built skill set differs from selection')
        for path in skills:
            label = path.parent.name
            text = path.read_text(encoding='utf-8')
            match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
            check(match is not None, f'{label}: missing frontmatter')
            if not match:
                continue
            fm = yaml.safe_load(match[1])
            check(fm.get('name') == label and len(label) <= 64 and bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', label)), f'{label}: invalid name')
            desc = fm.get('description')
            check(isinstance(desc, str) and 0 < len(desc) <= 1024 and '<' not in desc and '>' not in desc, f'{label}: invalid description')
            check(not set(fm) - {'name', 'description', 'license', 'allowed-tools', 'metadata'} - (UPSTREAM_FIELDS if label in VERBATIM_UPSTREAM else set()),
                  f'{label}: nonportable frontmatter (including invocation blockers)')
            meta = fm.get('metadata', {})
            check(isinstance(meta, dict) and all(isinstance(v, str) for v in meta.values()), f'{label}: metadata values must be strings')
            dependencies = json.loads(meta.get('dependencies', '{}'))
            for dep in dependencies.get('requires', []):
                check(dep in expected, f'{label}: missing dependency {dep}')
            for nested in ('.claude-plugin', '.codex-plugin'):
                check(not (path.parent / nested).exists(), f'{label}: nested plugin manifest')
            agent = path.parent / 'agents/openai.yaml'
            if agent.exists():
                data = yaml.safe_load(agent.read_text())
                check(not set(data.get('policy', {})) - {'allow_implicit_invocation'}, f'{label}: unsupported agent policy')
                for field in ('icon_small', 'icon_large'):
                    asset = data.get('interface', {}).get(field)
                    if asset:
                        check((path.parent / asset).is_file(), f'{label}: missing {field}')
        # Dedicated CHAT package is independently versioned; do not replace the Claude build.
        chat_entry = next((item for item in codex['plugins'] if item['name'] == 'lexmachina-chat'), None)
        check(chat_entry is not None, 'Missing dedicated lexmachina-chat marketplace entry')
        if chat_entry is not None:
            check(chat_entry['source']['source'] == 'local', 'CHAT entry must use local packaged source')
            chat = (root / chat_entry['source']['path']).resolve()
            check(chat.is_relative_to(root.resolve()), 'CHAT plugin escapes repository')
            chat_manifest = read_json(chat / 'plugin.json')
            chat_compat = read_json(chat / '.codex-plugin/plugin.json')
            chat_source = read_json(chat / 'SOURCE-RELEASE.json')
            check(chat_manifest.get('$schema') == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'CHAT: invalid portable manifest')
            check(chat_manifest['name'] == chat_compat['name'] == chat_entry['name'], 'CHAT: names differ')
            check(chat_manifest['version'] == chat_compat['version'], 'CHAT: versions differ')
            check(bool(re.fullmatch(r'\d+\.\d+\.\d+', chat_manifest['version'])), 'CHAT: invalid semver')
            check(not (chat / 'mcp.json').exists() and not (chat / '.mcp.json').exists(), 'CHAT: must not require MCP')
            expected_chat = set(chat_source['skills'])
            actual_chat = {f.parent.name for f in (chat / 'skills').glob('*/SKILL.md')}
            check(actual_chat == expected_chat, 'CHAT: skill inventory differs from source manifest')
            for f in (chat / 'skills').glob('*/SKILL.md'):
                match = re.match(r'\A---\n(.*?)\n---\n', f.read_text(encoding='utf-8'), re.S)
                check(match is not None, f'CHAT: missing frontmatter {f.parent.name}')
                if match:
                    data = yaml.safe_load(match[1])
                    check(data.get('name') == f.parent.name and bool(data.get('description')), f'CHAT: wrong name/description {f.parent.name}')
            for f in chat.rglob('*'):
                check(not f.is_symlink(), f'CHAT: symlink {f}')
        for path in plugin.rglob('*'):
            check(not path.is_symlink(), f'Symlink in package: {path}')
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        errors.append(str(exc))
    return errors


if __name__ == '__main__':
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print('\n'.join('ERROR: ' + e for e in errors))
        sys.exit(1)
    print('PASS: marketplace, manifests, all selected skills, dependencies and assets')
