from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import yaml

from .markdown_sanitize import render_document_body
from .models import OCRDocument


def build_frontmatter(source_path: Path, document: OCRDocument) -> dict[str, str]:
    return {
        "source_file": source_path.name,
        "converted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ocr_backend": document.provider,
    }


def render_with_frontmatter(source_path: Path, document: OCRDocument) -> str:
    body = render_document_body(document)
    frontmatter = build_frontmatter(source_path, document)
    yaml_block = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
    return f"---\n{yaml_block}\n---\n\n# {source_path.stem}\n\n{body}\n"
