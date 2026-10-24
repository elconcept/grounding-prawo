from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .document_metadata import extract_document_metadata
from .markdown_sanitize import render_document_body
from .models import OCRDocument


def document_plain_text(document: OCRDocument) -> str:
    return "\n".join(
        block.text for page in document.pages for block in page.blocks if block.text.strip()
    )


def build_frontmatter(source_path: Path, document: OCRDocument) -> dict[str, Any]:
    return {
        "source_file": source_path.name,
        "ocr_backend": document.provider,
        **extract_document_metadata(document),
    }


def render_with_frontmatter(source_path: Path, document: OCRDocument) -> str:
    body = render_document_body(document, document_name=source_path.name)
    frontmatter = build_frontmatter(source_path, document)
    yaml_block = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
    return f"---\n{yaml_block}\n---\n\n{body}\n"
