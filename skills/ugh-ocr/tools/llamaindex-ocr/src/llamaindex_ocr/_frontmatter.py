"""Frontmatter YAML.

Bazowe pola (source_file/converted_at/converter/ocr_backend/ocr_used) sa
wspolne z markitdown-vision, dla spojnosci miedzy narzedziami. Dodatkowo
LlamaParse zwraca per-strone metadane (numer strony, pewnosc, notatki), ktore
warto zachowac -- to jedyne z dwoch narzedzi majace dostep do tych danych
(markitdown/Google Vision ich nie zwracaja), wiec byloby marnotrawstwem ich
nie zapisac.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def obj_to_plain(value: Any) -> Any:
    """Konwertuje odpowiedz SDK LlamaCloud (obiekty pydantic itp.) na
    zwykle typy Pythona (dict/list/str/...), zeby dalo sie je bezpiecznie
    przejrzec bez zaleznosci od konkretnej wersji SDK."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return [obj_to_plain(v) for v in value]
    if isinstance(value, dict):
        return {str(k): obj_to_plain(v) for k, v in value.items()}
    if hasattr(value, "model_dump"):
        try:
            return obj_to_plain(value.model_dump())
        except Exception:
            pass
    if hasattr(value, "dict"):
        try:
            return obj_to_plain(value.dict())
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        try:
            return obj_to_plain(vars(value))
        except Exception:
            pass
    return str(value)


def _compact(values: list[Any]) -> Any:
    cleaned = [v for v in values if v is not None and v != ""]
    if not cleaned:
        return None
    if len(values) == 1:
        return values[0]
    return values


def extract_page_metadata(raw_result: Any) -> dict[str, Any]:
    """Wyciaga per-strone metadane z surowej odpowiedzi LlamaCloud:
    liczbe stron, numery wydrukowane, pewnosc parsera, notatki."""
    plain = obj_to_plain(raw_result)
    metadata = plain.get("metadata") if isinstance(plain, dict) else None
    pages = metadata.get("pages") if isinstance(metadata, dict) else None

    if not isinstance(pages, list) or not pages:
        return {"pages_count": None, "page_numbers": None, "confidence": None, "notes": None}

    page_numbers, confidences, notes = [], [], []
    for p in pages:
        if not isinstance(p, dict):
            continue
        page_numbers.append(p.get("printed_page_number"))
        confidences.append(p.get("confidence"))
        notes.append(p.get("speaker_notes"))

    return {
        "pages_count": len(pages),
        "page_numbers": _compact(page_numbers),
        "confidence": _compact(confidences),
        "notes": _compact(notes),
    }


def build_frontmatter(
    source_path: Path,
    *,
    tier: str,
    raw_result: Any = None,
) -> dict[str, Any]:
    frontmatter: dict[str, Any] = {
        "source_file": source_path.name,
        "converted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "converter": "llamaindex-ocr",
        "ocr_backend": "llamaparse",
        "ocr_used": True,
        "tier": tier,
    }
    if raw_result is not None:
        frontmatter.update(extract_page_metadata(raw_result))
    return frontmatter


def render_with_frontmatter(
    source_path: Path,
    markdown: str,
    *,
    tier: str,
    raw_result: Any = None,
) -> str:
    frontmatter = build_frontmatter(source_path, tier=tier, raw_result=raw_result)
    yaml_block = yaml.safe_dump(
        frontmatter, allow_unicode=True, sort_keys=False
    ).strip()
    body = markdown.strip()
    return f"---\n{yaml_block}\n---\n\n{body}\n"
