#!/usr/bin/env python3
"""Independent offline validation of the dedicated ChatGPT CHAT marketplace plugin."""
import json
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "plugins" / "lexmachina-chat"


def main() -> int:
    errors = []

    def check(value, why):
        if not value:
            errors.append(why)

    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    claude = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    chat_entries = [x for x in marketplace["plugins"] if x["name"] == "lexmachina-chat"]
    check(len(chat_entries) == 1, "exactly one lexmachina-chat entry")
    check([x["name"] for x in claude["plugins"]] == ["grounding-prawo"], "Claude entry was changed")
    if not chat_entries:
        print("\n".join(errors))
        return 1
    check(chat_entries[0]["source"]["path"] == "./plugins/lexmachina-chat", "invalid market source")
    manifest = json.loads((PKG / "plugin.json").read_text())
    legacy = json.loads((PKG / ".codex-plugin/plugin.json").read_text())
    source = json.loads((PKG / "SOURCE-RELEASE.json").read_text())
    check(manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", "invalid schema")
    check(manifest["name"] == legacy["name"] == "lexmachina-chat", "plugin identity")
    check(manifest["version"] == legacy["version"] == "1.0.0", "version mismatch")
    check(source["source_release_id"] == "pluginrel_6afdb8ff27688191aa4ce96949c98dfa", "source release")
    check(bool(re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])), "invalid semver")
    check(manifest["extensions"]["com.openai"]["interface"]["defaultPrompt"] ==
          "Uruchom Akta i Dowody i pomóż mi z moim zadaniem.", "defaultPrompt changed")
    check(not (PKG / "mcp.json").exists() and not (PKG / ".mcp.json").exists(), "unexpected root MCP dependency")
    expected = set(source["skills"])
    actual = {f.parent.name for f in (PKG / "skills").glob("*/SKILL.md")}
    check(actual == expected, "missing or extra skills: " + repr(sorted(actual ^ expected)))
    for name in sorted(expected):
        f = PKG / "skills" / name / "SKILL.md"
        check(f.exists(), "missing SKILL: " + name)
        if not f.exists():
            continue
        content = f.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
        check(match is not None, "missing YAML frontmatter: " + name)
        if not match:
            continue
        data = yaml.safe_load(match[1])
        check(isinstance(data, dict) and data.get("name") == name and
              isinstance(data.get("description"), str) and bool(data["description"]),
              "invalid name/description: " + name)
    for name in ["prawny-router-v3", "prawo-polskie-v2", "przewodnik-prawny-v2",
                 "analizator-umow-v1", "raport-sytuacyjny-v2", "raport-klienta-v1", "audyt-systemu-v4"]:
        check((PKG / "skills" / name / "references/CHAT-RUNTIME.md").exists(),
              "missing CHAT adapter: " + name)
    check((PKG / "skills/prawo-polskie-v2/ROUTING-MAP.md").exists(), "missing original DR routing")
    check((PKG / "skills/raport-sytuacyjny-v2/assets/widget-raport-sytuacyjny.html").exists(),
          "missing situation widget")
    check((PKG / "skills/raport-klienta-v1/assets/widget-raport-klienta.html").exists(),
          "missing client widget")
    for f in PKG.rglob("*"):
        check(not f.is_symlink(), "symlink: " + str(f.relative_to(ROOT)))
    if errors:
        print("\n".join("FAIL: " + e for e in errors))
        return 1
    print(f"PASS: LexMachina CHAT {manifest['version']}, {len(expected)} skills, manifests, adapters, no root MCP")
    return 0


if __name__ == "__main__":
    sys.exit(main())
