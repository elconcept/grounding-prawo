"""Deterministic JSON -> Markdown rendering.

Priority is information and logical structure, not pretty Markdown. The
renderer therefore reads `block.markdown` (the structure the provider
actually recognised) instead of the flattened `block.text`, and only
normalises it: headings to `##`/`###`/`####`, lists to `-`/`N.`, form label/value pairs
to `Label: value`, tables either to field lines (label/value forms) or to a
syntactically valid Markdown table (real data tables).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser

from .models import BBox, OCRBlock, OCRDocument


SPECIAL_TAGS = {"handnote", "signature", "stamp", "footer", "header", "logo", "photo", "graphic"}
_TAG_ALIASES = {
    "odręczne": "handnote",
    "odreczne": "handnote",
    "podpis": "signature",
    "pieczęć": "stamp",
    "pieczec": "stamp",
    "stopka": "footer",
    "nagłówek": "header",
    "naglowek": "header",
    "zdjęcie": "photo",
    "zdjecie": "photo",
    "rysunek": "graphic",
    "diagram": "graphic",
}
_RE_SPECIAL = re.compile(r"\*?\[\*?([^\]:*]+)\*?(?::\s*([^]]*))?]\*?", re.IGNORECASE)

HEADING_TYPES = {"title"}
TABLE_TYPES = {"table"}
LIST_TYPES = {"list"}

_LETTER = r"[^\W\d_]"
# A cell or block that is only a form label: one line, ends with a colon.
_LABEL_RE = re.compile(r"^([^\n:]{1,100}?)\s*:$")
_LIST_ITEM_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<marker>[-+*•]|\d{1,3}[.)])[ \t]+(?P<body>.+)$")
_SEPARATOR_RE = re.compile(r"[\s|:+]*(?:[-=]{3,}[\s|:+]*)+")
_SOURCE_BULLET_RE = re.compile(r"^(?:\\\*|[*•·●▪])[ \t]+")

# Semantic list detection thresholds. Deliberately strict: a wrong split
# invents structure, and inventing structure is worse than leaving prose.
_LIST_MAX_BLOCK_CHARS = 250
_LIST_MAX_ITEM_CHARS = 60
_LIST_MAX_ITEM_WORDS = 6
_LIST_MIN_ITEMS = 2


class _HTMLText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"br", "p", "div", "li", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self.parts.append("\n" if tag not in {"td", "th"} else " | ")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self.parts.append("\n")


_IMAGE_RE = re.compile(r"!\[([^\]]*)]\([^)]*\)")
_LINK_RE = re.compile(r"(?<!!)\[([^\]\n]+)]\((https?://[^)\s]+|[^)\s]+)\)")
_AUTOLINK_RE = re.compile(r"<((?:https?|mailto|ftp)://[^\s<>]+|mailto:[^\s<>]+|[^\s<>@]+@[^\s<>@]+)>")


def sanitize_markdown(text: str) -> str:
    """Normalize provider Markdown while preserving the project's special tags."""
    placeholders: list[str] = []

    def hold(value: str) -> str:
        token = f"\x00TAG{len(placeholders)}\x00"
        placeholders.append(value)
        return token

    def preserve_link(match: re.Match[str]) -> str:
        label, target = match.group(1).strip(), match.group(2).strip()
        if not target.lower().startswith(("http://", "https://", "mailto:", "ftp://")):
            return label
        return f"{label} {hold(f'<{target}>')}" if label else hold(f"<{target}>")

    # An autolink is not an HTML tag, but html.parser cannot tell the
    # difference and silently drops it, which loses the URL entirely.
    text = _IMAGE_RE.sub(lambda match: match.group(1), text)
    text = _LINK_RE.sub(preserve_link, text)
    text = _AUTOLINK_RE.sub(lambda match: hold(f"<{match.group(1)}>"), text)

    def preserve_tag(match: re.Match[str]) -> str:
        label = match.group(1).strip().lower()
        label = _TAG_ALIASES.get(label, label)
        if label not in SPECIAL_TAGS:
            return match.group(0)
        value = (match.group(2) or "illegible").strip()
        return hold(f"*[{label}: {value}]*")

    text = _RE_SPECIAL.sub(preserve_tag, text)
    parser = _HTMLText()
    parser.feed(text)
    text = "".join(parser.parts)
    text = re.sub(r"^\s*[+*]\s+", "- ", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*([^*\n]+)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"__([^_\n]+)__", r"\1", text)
    text = re.sub(r"(?<![\w_])_([^_\n]+)_(?![\w_])", r"\1", text)
    # Provider H1/H2/H3 carry relative logical hierarchy. In our output
    # H2 is the highest level; preserve depth without ever emitting H1.
    text = re.sub(
        r"^(#{1,6})[ \t]+",
        lambda match: "#" * min(4, len(match.group(1)) + 1) + " ",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(r"(?<![<(])(https?://[^\s<>()]+)", _wrap_url, text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    for index, tag in enumerate(placeholders):
        text = text.replace(f"\x00TAG{index}\x00", tag)
    return text


def _inline(text: str) -> str:
    """Collapse a fragment to a single line (table cells, tag values)."""
    return re.sub(r"\s*\n\s*", " ", text).strip()


@dataclass(frozen=True)
class _Element:
    kind: str  # special | heading | table | list | label | field | text
    text: str
    bbox: BBox | None


def render_document_body(document: OCRDocument, *, document_name: str | None = None) -> str:
    """Render each page as a self-contained, explicitly delimited section."""
    name = document_name or document.source_name or document.doc_id
    total_pages = len(document.pages)
    pages: list[str] = []
    for page in document.pages:
        elements = _merge_form_fields([_block_element(block) for block in page.blocks])
        parts: list[str] = [f"==< {name}> (Page {page.number}/{total_pages}) >=="]
        for element in elements:
            content = element.text
            if element.kind == "text":
                content = _semantic_list(content) or content
            if content:
                parts.append(content)
        parts.append("---")
        pages.append("\n\n".join(parts))
    return "\n\n".join(pages).strip()


def _block_element(block: OCRBlock) -> _Element:
    raw = (block.markdown or "").strip() or (block.text or "").strip()
    block_type = block.block_type

    if block_type in SPECIAL_TAGS:
        value = _special_value(block_type, raw) or "illegible"
        return _Element("special", f"*[{block_type}: {value}]*", block.bbox)

    if block_type == "strikethrough":
        body = sanitize_markdown(raw)
        return _Element("text", f"~~{body}~~" if body else "", block.bbox)

    if block_type in HEADING_TYPES:
        body = sanitize_markdown(re.sub(r"^\s*#{1,6}\s*", "", raw)).rstrip(" :;,.!?")
        return _Element("heading", f"## {body}" if body else "", block.bbox)

    if block_type in TABLE_TYPES:
        return _Element("table", render_table(raw, block.text), block.bbox)

    if block_type in LIST_TYPES:
        return _Element("list", render_list(raw, block.text), block.bbox)

    body = sanitize_markdown(raw)
    label = _bare_label(body)
    if label is not None:
        return _Element("label", f"{label}:", block.bbox)
    return _Element("text", body, block.bbox)


# --- form fields -----------------------------------------------------------

def _bare_label(text: str) -> str | None:
    """`Label:` on its own -- a form field whose value sits in another block."""
    match = _LABEL_RE.match(text.strip())
    if match is None:
        return None
    label = match.group(1).strip()
    if not label or len(label.split()) > 12:
        return None
    if not re.search(_LETTER, label):
        return None
    return label


def _is_field_value(text: str) -> bool:
    value = text.strip()
    if not value or "\n" in value or len(value) > 200:
        return False
    if value.endswith(":"):
        return False
    return not value.startswith(("-", "#", "*[", "~~", "|", ">"))


def _fields_adjacent(label: BBox | None, value: BBox | None) -> bool:
    """Geometry check when both blocks are positioned.

    Without bboxes the provider's reading order is the only signal, and it is
    the signal the label/value split comes from, so pairing stays allowed.
    """
    if label is None or value is None:
        return True
    lx0, ly0, lx1, ly1 = label
    vx0, vy0, vx1, vy1 = value
    height = ly1 - ly0
    if height > 0 and (min(ly1, vy1) - max(ly0, vy0)) / height > 0.3:
        if vx0 >= lx0 - 0.01 and -0.02 <= vx0 - lx1 <= 0.15:
            return True
    width = lx1 - lx0
    if width > 0 and (min(lx1, vx1) - max(lx0, vx0)) / width > 0.3:
        if -0.005 <= vy0 - ly1 <= 0.05:
            return True
    return False


def _merge_form_fields(elements: list[_Element]) -> list[_Element]:
    merged: list[_Element] = []
    index = 0
    while index < len(elements):
        element = elements[index]
        following = elements[index + 1] if index + 1 < len(elements) else None
        if (
            element.kind == "label"
            and following is not None
            and following.kind == "text"
            and _is_field_value(following.text)
            and _fields_adjacent(element.bbox, following.bbox)
        ):
            merged.append(_Element("field", f"{element.text} {following.text.strip()}", element.bbox))
            index += 2
            continue
        merged.append(element)
        index += 1
    return merged


# --- tables ----------------------------------------------------------------

def render_table(markdown: str, fallback: str) -> str:
    rows = _parse_table_rows(markdown)
    rows = _strip_empty_edge_rows(rows)
    if not rows:
        return sanitize_markdown(fallback)
    if max(len(row) for row in rows) == 1:
        items = [row[0] for row in rows if row and row[0]]
        return "\n".join(f"- {item}" for item in items)
    if _is_form_table(rows):
        return _table_as_fields(rows)
    return _table_as_markdown(rows)


def _parse_table_rows(markdown: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in markdown.splitlines():
        line = line.strip()
        if "|" not in line:
            continue
        if _SEPARATOR_RE.fullmatch(line):
            continue
        rows.append([_cell_text(cell) for cell in _split_row(line)])
    return rows


def _split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [part.replace("\\|", "|") for part in re.split(r"(?<!\\)\|", line)]


def _cell_text(raw: str) -> str:
    return _inline(sanitize_markdown(raw))


def _strip_empty_edge_rows(rows: list[list[str]]) -> list[list[str]]:
    while rows and not any(cell for cell in rows[0]):
        rows = rows[1:]
    while rows and not any(cell for cell in rows[-1]):
        rows = rows[:-1]
    return rows


def _is_form_table(rows: list[list[str]]) -> bool:
    cells = [cell for row in rows for cell in row if cell]
    if not cells:
        return False
    labels = sum(1 for cell in cells if _LABEL_RE.match(cell))
    return labels / len(cells) >= 0.3


def _table_as_fields(rows: list[list[str]]) -> str:
    entries: list[str] = []
    for row in rows:
        index = 0
        while index < len(row):
            cell = row[index]
            if not cell:
                index += 1
                continue
            match = _LABEL_RE.match(cell)
            if match is None:
                entries.append(cell)
                index += 1
                continue
            label = match.group(1).strip()
            value = row[index + 1] if index + 1 < len(row) else ""
            if value and _LABEL_RE.match(value) is None:
                entries.append(f"{label}: {value}")
                index += 2
            else:
                entries.append(f"{label}:")
                index += 1
    return "\n\n".join(entries)


def _table_as_markdown(rows: list[list[str]]) -> str:
    width = max(len(row) for row in rows)
    normalized = [
        [cell.replace("|", "\\|") for cell in row] + [""] * (width - len(row))
        for row in rows
    ]
    header, body = normalized[0], normalized[1:]
    if not body:
        return "\n\n".join(cell for cell in header if cell)
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(" --- " for _ in header) + "|"]
    lines.extend("| " + " | ".join(row) + " |" for row in body)
    return "\n".join(lines)


# --- lists -----------------------------------------------------------------

def render_list(markdown: str, fallback: str) -> str:
    lines: list[str] = []
    for raw in markdown.splitlines():
        match = _LIST_ITEM_RE.match(raw)
        if match is None:
            continuation = sanitize_markdown(raw)
            if continuation and lines:
                lines[-1] = f"{lines[-1]} {continuation}"
            elif continuation:
                lines.append(f"- {continuation}")
            continue
        depth = min(len(match.group("indent").expandtabs(4)) // 2, 4)
        marker = match.group("marker")
        body = sanitize_markdown(_SOURCE_BULLET_RE.sub("", match.group("body")))
        if not body:
            continue
        prefix = marker if marker[:1].isdigit() else "-"
        lines.append("  " * depth + f"{prefix} {body}")
    if lines:
        return "\n".join(lines)
    parts = [sanitize_markdown(part) for part in re.split(r"\n+|;\s+", fallback) if part.strip()]
    parts = [part for part in parts if part]
    return "\n".join(f"- {part}" for part in parts)


# --- semantic lists --------------------------------------------------------

def _semantic_list(text: str) -> str | None:
    """Split an enumeration that is a list in all but punctuation.

    Applied only when every guard holds, so prose is never chopped up:
    one line, no sentence punctuation, no colons, short items, each item
    carrying a real word and no year/parenthetical reference.
    """
    value = text.strip()
    if not value or "\n" in value or len(value) > _LIST_MAX_BLOCK_CHARS:
        return None
    if value.startswith(("-", "#", "*[", "~~", "|", ">")):
        return None
    if ":" in value:
        return None
    body = value.rstrip(";,. ")
    if re.search(r"[.!?]", body):
        return None
    separator = ";" if ";" in body else ","
    if separator not in body:
        return None
    items = [item.strip() for item in body.split(separator)]
    if len(items) < _LIST_MIN_ITEMS:
        return None
    for item in items:
        if not item or len(item) > _LIST_MAX_ITEM_CHARS:
            return None
        if len(item.split()) > _LIST_MAX_ITEM_WORDS:
            return None
        if not re.search(_LETTER + "{3}", item):
            return None
        if re.search(r"[()\[\]/]|\d{4}", item):
            return None
    return "\n".join(f"- {item}" for item in items)


# --- special tags ----------------------------------------------------------

def _unwrap_special(match: re.Match[str]) -> str:
    label = _TAG_ALIASES.get(match.group(1).strip().lower(), match.group(1).strip().lower())
    if label not in SPECIAL_TAGS:
        return match.group(0)  # a bracket that is not one of our tags stays put
    return (match.group(2) or "").strip()


def _special_value(block_type: str, text: str) -> str:
    """Inner value of a `*[type: value]*` block, without repeating the type."""
    value = _inline(sanitize_markdown(_RE_SPECIAL.sub(_unwrap_special, text)))
    prefixes = [block_type] + [alias for alias, target in _TAG_ALIASES.items() if target == block_type]
    for prefix in prefixes:
        value = re.sub(rf"^{re.escape(prefix)}\s*:\s*", "", value, flags=re.IGNORECASE)
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1].strip()
    return _dedupe_repeat(value)


def _dedupe_repeat(value: str) -> str:
    """Providers repeat an image's alt text as its caption; keep it once."""
    words = value.split()
    half = len(words) // 2
    if half and words[:half] == words[half:]:
        return " ".join(words[:half])
    return value


def _wrap_url(match: re.Match[str]) -> str:
    value = match.group(1)
    trailing = ""
    while value and value[-1] in ".,;:!?":
        trailing = value[-1] + trailing
        value = value[:-1]
    return f"<{value}>{trailing}"


# Compatibility names for callers outside the CLI. They now delegate to the
# single sanitizer instead of maintaining three subtly different passes.
def extract_bold_flags(text: str) -> tuple[str, list[str]]:
    return re.sub(r"\*\*([^*\n]+)\*\*", r"\1", text), []


def strip_italic_label_markup(text: str) -> str:
    return sanitize_markdown(text)


def sanitize_markdown_formatting(text: str) -> str:
    return sanitize_markdown(text)
