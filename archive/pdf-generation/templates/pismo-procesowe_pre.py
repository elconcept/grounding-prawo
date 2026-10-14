"""Preprocessing dla szablonu pismo-procesowe: rozbija klucz frontmatteru
`odbiorca` (string lub lista stringow, kazdy string = nazwa+adres rozdzielone
przecinkami) na znormalizowane zmienne, ktore szablon LaTeX potrafi
wyrenderowac bez zadnej logiki parsowania stringow (ktorej jezyk szablonow
pandoc nie ma wcale).

Wejscie (frontmatter):
    odbiorca: "Sad Rejonowy dla Warszawy-Srodmiescia, I Wydzial Cywilny, ul. Marszalkowska 82, 00-517 Warszawa"
lub:
    odbiorca:
      - "Sad Rejonowy ..., ul. ..., 00-517 Warszawa"
      - "Prokuratura Rejonowa ..., ul. ..., 00-001 Warszawa"

Wyjscie (wstrzykniete do frontmatteru, oryginalny klucz `odbiorca` usuniety):
    odbiorca_glowny_nazwa: "..."
    odbiorca_glowny_adres: ["...", "..."]
    odbiorca_dw:                      # tylko gdy odbiorca byla lista >1 elementu
      - nazwa: "..."
        adres: ["...", "..."]

Brak klucza `odbiorca` w ogole = brak zmiany, plik przechodzi bez modyfikacji
(to poprawna sytuacja, np. oswiadczenie bez konkretnego adresata).
"""
import re
import tempfile
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", re.DOTALL)
TOP_KEY_RE = re.compile(r"^odbiorca:[ \t]*(.*)$")
LIST_ITEM_RE = re.compile(r"^[ \t]+-[ \t]+(.*)$")


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def _yaml_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _split_entry(raw: str) -> list[str]:
    parts = [p.strip() for p in _strip_quotes(raw).split(",")]
    return [p for p in parts if p]


def _extract_odbiorca(frontmatter: str) -> tuple[str, list[list[str]]]:
    lines = frontmatter.splitlines()
    for i, line in enumerate(lines):
        m = TOP_KEY_RE.match(line)
        if not m:
            continue
        inline_val = m.group(1).strip()
        if inline_val:
            remaining = lines[:i] + lines[i + 1:]
            return "\n".join(remaining), [_split_entry(inline_val)]
        # blok listy w kolejnych liniach
        j = i + 1
        raw_items = []
        while j < len(lines) and LIST_ITEM_RE.match(lines[j]):
            raw_items.append(LIST_ITEM_RE.match(lines[j]).group(1))
            j += 1
        remaining = lines[:i] + lines[j:]
        entries = [_split_entry(item) for item in raw_items]
        return "\n".join(remaining), entries
    return frontmatter, []


def _build_injected_yaml(entries: list[list[str]]) -> str:
    glowny, dw = entries[0], entries[1:]
    out = []
    out.append(f"odbiorca_glowny_nazwa: {_yaml_quote(glowny[0])}")
    if len(glowny) > 1:
        out.append("odbiorca_glowny_adres:")
        for line in glowny[1:]:
            out.append(f"  - {_yaml_quote(line)}")
    else:
        out.append("odbiorca_glowny_adres: []")
    if dw:
        out.append("odbiorca_dw:")
        for entry in dw:
            out.append(f"  - nazwa: {_yaml_quote(entry[0])}")
            if len(entry) > 1:
                out.append("    adres:")
                for line in entry[1:]:
                    out.append(f"      - {_yaml_quote(line)}")
            else:
                out.append("    adres: []")
    return "\n".join(out)


# `#` (H1) w tresci ma byc CALKOWICIE zignorowany (tytul pochodzi z
# frontmatteru). Usuwamy linie H1 juz na poziomie markdown (nie w LaTeX) --
# tak, zeby pandoc nigdy nie wygenerowal \section, co unika konfliktu
# renderowania \section z titlesec/hyperref w szablonie.
H1_LINE_RE = re.compile(r"^#(?!#)[ \t]+.*$", re.MULTILINE)


def _strip_h1_headings(body: str) -> tuple[str, bool]:
    new_body, n = H1_LINE_RE.subn("", body)
    return new_body, n > 0


def preprocess(input_path: Path) -> Path:
    text = input_path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return input_path  # brak frontmatteru -- nic do zrobienia
    frontmatter, body = m.group(1), m.group(2)

    remaining_frontmatter, entries = _extract_odbiorca(frontmatter)
    new_body, h1_stripped = _strip_h1_headings(body)

    if not entries and not h1_stripped:
        return input_path  # nic do zmiany -- poprawna sytuacja

    if entries:
        injected = _build_injected_yaml(entries)
        new_frontmatter = remaining_frontmatter.rstrip("\n") + "\n" + injected
    else:
        new_frontmatter = remaining_frontmatter
    new_text = f"---\n{new_frontmatter}\n---\n{new_body}"

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", prefix="pismo-procesowe-pre-",
        delete=False, encoding="utf-8",
    )
    tmp.write(new_text)
    tmp.close()
    return Path(tmp.name)
