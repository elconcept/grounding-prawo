from __future__ import annotations

import re
from html.parser import HTMLParser

from .models import OCRDocument


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


def sanitize_markdown(text: str) -> str:
    """Normalize provider Markdown while preserving the project's special tags."""
    placeholders: list[str] = []

    def preserve_tag(match: re.Match[str]) -> str:
        label = match.group(1).strip().lower()
        label = _TAG_ALIASES.get(label, label)
        if label not in SPECIAL_TAGS:
            return match.group(0)
        value = (match.group(2) or "illegible").strip()
        token = f"\x00TAG{len(placeholders)}\x00"
        placeholders.append(f"*[{label}: {value}]*")
        return token

    text = _RE_SPECIAL.sub(preserve_tag, text)
    parser = _HTMLText()
    parser.feed(text)
    text = "".join(parser.parts)
    text = re.sub(r"^\s*[+*]\s+", "- ", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*([^*\n]+)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"__([^_\n]+)__", r"\1", text)
    text = re.sub(r"(?<![\w_])_([^_\n]+)_(?![\w_])", r"\1", text)
    text = re.sub(r"^#\s+", "## ", text, flags=re.MULTILINE)
    text = re.sub(r"(?<![<(])(https?://[^\s<>()]+)", _wrap_url, text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    for index, tag in enumerate(placeholders):
        text = text.replace(f"\x00TAG{index}\x00", tag)
    return text


def render_document_body(document: OCRDocument) -> str:
    pages: list[str] = []
    for page in document.pages:
        blocks: list[str] = [f"## Page {page.number}"]
        for block in page.blocks:
            content = block.text.strip()
            if block.block_type in SPECIAL_TAGS:
                content = f"*[{block.block_type}: {_special_value(block.text) or 'illegible'}]*"
            elif block.block_type == "strikethrough" and content:
                content = f"~~{block.text.strip()}~~"
            elif block.block_type in {"title", "heading", "sectionheader"} and content:
                content = f"### {content.rstrip(' :;,.!?')}"
            elif block.block_type == "table":
                content = _table_as_list(block.markdown, block.text)
            elif block.block_type in {"list", "listitem"}:
                content = _list_as_dashes(block.markdown, block.text)
            content = sanitize_markdown(content)
            if content:
                blocks.append(content)
        pages.append("\n\n".join(blocks))
    return "\n\n".join(page for page in pages if page).strip()


def _table_as_list(markdown: str, fallback: str) -> str:
    rows = []
    for line in markdown.splitlines():
        if "|" not in line or re.fullmatch(r"[\s|:=-]+", line):
            continue
        cells = [sanitize_markdown(cell.strip()) for cell in line.strip().strip("|").split("|")]
        if any(cells):
            rows.append(cells)
    if not rows:
        value = sanitize_markdown(fallback)
        return f"- Table row 1: {value}" if value else ""
    has_headers = len(rows) > 1
    headers = rows[0] if has_headers else []
    data_rows = rows[1:] if has_headers else rows
    rendered = []
    for index, row in enumerate(data_rows, start=1):
        pairs = []
        for cell_index, value in enumerate(row):
            label = headers[cell_index] if cell_index < len(headers) and headers[cell_index] else f"column {cell_index + 1}"
            if value:
                pairs.append(f"{label}: {value}")
        if pairs:
            rendered.append(f"- Table row {index}: " + "; ".join(pairs))
    return "\n".join(rendered)


def _list_as_dashes(markdown: str, fallback: str) -> str:
    items = []
    for line in markdown.splitlines():
        match = re.match(r"^\s*(?:[-+*]|\d+[.)])\s+(.+)$", line)
        if match:
            items.append(sanitize_markdown(match.group(1)))
    if not items and fallback.strip():
        items = [sanitize_markdown(part) for part in re.split(r"\n+|;\s+", fallback) if part.strip()]
    return "\n".join(f"- {item}" for item in items if item)


def _special_value(text: str) -> str:
    value = re.sub(r"\*?\[\*?[^\]:*]+\*?\s*:\s*([^]]+)]\*?", r"\1", text).strip()
    return sanitize_markdown(value)


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
