"""Per-page OCR candidate export. The caller/model is the sole reviewer."""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import pymupdf

from .config import all_providers
from .providers import canonical_provider_name
from .visual.scale_a4 import fit_pdf_to_a4, is_already_a4

PRIMARY = ("google_vision", "azure")
FALLBACK = ("datalab", "llamaparse")


def number_of_pages(source: Path) -> int:
    if source.suffix.lower() != ".pdf" or not source.is_file():
        raise ValueError("Only an existing PDF is accepted")
    with pymupdf.open(source) as pdf:
        if pdf.needs_pass or len(pdf) < 1:
            raise ValueError("Locked or empty PDF")
        return len(pdf)


def capture_page(source: Path, *, page: int | None = None,
                 provider_name: str | None = None, output: Path | None = None):
    source = Path(source)
    total = number_of_pages(source)
    if page is None and total != 1:
        raise ValueError(f"{total} pages: --page N is mandatory; model reviews each page")
    page = page or 1
    if not 1 <= page <= total:
        raise ValueError(f"Page out of bounds: 1..{total}")
    providers = {p.name: p for p in all_providers()}
    options = [canonical_provider_name(provider_name)] if provider_name else list(PRIMARY)
    if any(name not in PRIMARY + FALLBACK for name in options):
        raise ValueError("Allowed OCR providers: google_vision, azure, datalab, llamaparse")
    provider = next((providers[n] for n in options if providers[n].is_available()[0]), None)
    if provider is None:
        raise ValueError("No configured OCR provider available; no automatic fallback")
    with tempfile.TemporaryDirectory(prefix="ocr-page-") as work:
        one = Path(work) / "one.pdf"
        with pymupdf.open(source) as original, pymupdf.open() as isolated:
            isolated.insert_pdf(original, from_page=page - 1, to_page=page - 1)
            isolated.save(one)
        candidate = provider.recognize(one)
    if not candidate.ok or candidate.document is None or len(candidate.document.pages) != 1:
        raise ValueError(f"OCR failed: {candidate.error or 'empty or invalid result'}")
    target = Path(output) if output else (
        source.with_suffix(".md") if total == 1 else
        source.with_name(f"{source.stem}.page-{page:04d}.{provider.name}.candidate.md")
    )
    if target.suffix.lower() != ".md":
        raise ValueError("Output must be .md")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8", newline="\n") as dst:
        dst.write(f"==< {source.name} (Page {page}/{total}) >==\n")
        dst.write(candidate.document.text.strip() + "\n")
    return target, provider.name, page, total


def make_a4_copy(source: Path, output: Path | None = None) -> Path:
    source = Path(source)
    number_of_pages(source)
    target = Path(output) if output else source.with_name(f"{source.stem}_a4.pdf")
    if target.resolve() == source.resolve() or target.exists():
        raise ValueError("Never overwrite original or an existing output PDF")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ocr-a4-") as tmp:
        staged = Path(tmp) / "a4.pdf"
        if is_already_a4(source):
            shutil.copyfile(source, staged)
        else:
            fit_pdf_to_a4(source, staged)
        with staged.open("rb") as src, target.open("xb") as dst:
            shutil.copyfileobj(src, dst)
    return target
