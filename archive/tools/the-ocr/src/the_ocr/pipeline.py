from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path

import pymupdf
import pikepdf

from .chain import ChainResult, run_chain
from .frontmatter import render_with_frontmatter
from .models import OCRDocument, sha256_file
from .pdf.text_layer import build_document_searchable_pdf
from .pdf.source_pdf import image_to_a4_pdf, strip_invisible_text
from .providers.base import OCRProvider
from .visual.scale_a4 import fit_pdf_to_a4, is_already_a4


SUPPORTED_SUFFIXES = {".pdf", ".jpg", ".jpeg", ".png"}


@dataclass
class PipelineResult:
    chain_result: ChainResult
    archive_path: Path
    pdf_path: Path | None = None
    markdown_path: Path | None = None
    json_path: Path | None = None

    @property
    def ok(self) -> bool:
        return self.chain_result.ok and all((self.pdf_path, self.markdown_path, self.json_path))


def run_pipeline(input_path: Path, providers: list[OCRProvider], *, force: str | None = None) -> PipelineResult:
    """Archive input, OCR through Datalab -> LlamaParse, publish PDF/MD/JSON."""
    input_path = Path(input_path)
    suffix = input_path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(f"unsupported input type '{suffix}'; expected PDF, JPG, JPEG, or PNG")
    if not input_path.is_file():
        raise ValueError(f"input is not a file: {input_path}")

    output_pdf = input_path.with_suffix(".pdf")
    output_md = input_path.with_suffix(".md")
    output_json = input_path.with_suffix(".json")
    archive_path = _archive_input(input_path)
    result = PipelineResult(chain_result=ChainResult(result=None), archive_path=archive_path)
    if suffix != ".pdf" and output_pdf.exists():
        raise ValueError(f"refusing to overwrite existing output PDF: {output_pdf}; input preserved as {archive_path}")
    temps: list[Path] = []
    try:
        prepared_pdf = _temporary_path(input_path.parent, ".prepared.pdf")
        temps.append(prepared_pdf)
        _prepare_pdf(archive_path, prepared_pdf)

        chain_result = run_chain(prepared_pdf, providers, force=force)
        result.chain_result = chain_result
        if not chain_result.ok:
            return result

        document = replace(
            chain_result.result.document,
            source_name=input_path.name,
            source_sha256=sha256_file(archive_path),
        )
        document.validate()
        chain_result.result.document = document
        chain_result.result.text = document.text

        json_tmp = _temporary_path(input_path.parent, ".json.tmp")
        md_tmp = _temporary_path(input_path.parent, ".md.tmp")
        pdf_tmp = _temporary_path(input_path.parent, ".pdf.tmp")
        temps.extend((json_tmp, md_tmp, pdf_tmp))

        _write_text_durable(json_tmp, json.dumps(document.to_dict(), ensure_ascii=False, indent=2) + "\n")
        _write_text_durable(md_tmp, render_with_frontmatter(input_path, document))
        build_document_searchable_pdf(prepared_pdf, pdf_tmp, document)
        _validate_searchable_pdf(pdf_tmp, document)
        _fsync_file(pdf_tmp)

        _publish_outputs(((json_tmp, output_json), (md_tmp, output_md), (pdf_tmp, output_pdf)), temps)
        result.json_path = output_json
        result.markdown_path = output_md
        result.pdf_path = output_pdf

        if suffix != ".pdf":
            input_path.unlink()
        _remove_legacy_outputs(input_path)
        return result
    finally:
        for path in temps:
            path.unlink(missing_ok=True)


def process_input(input_path: Path, providers: list[OCRProvider], **kwargs) -> PipelineResult:
    return run_pipeline(input_path, providers, **kwargs)


def _prepare_pdf(archive_path: Path, destination: Path) -> None:
    if archive_path.suffix.lower() != ".pdf":
        image_to_a4_pdf(archive_path, destination)
        return

    clean = destination.with_suffix(".clean.pdf")
    try:
        strip_invisible_text(archive_path, clean)
        if is_already_a4(clean) or _requires_original_geometry(clean):
            clean.replace(destination)
        else:
            fit_pdf_to_a4(clean, destination)
    finally:
        clean.unlink(missing_ok=True)


def _archive_input(input_path: Path) -> Path:
    archive_dir = input_path.parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate = archive_dir / f"{input_path.stem}_{stamp}{input_path.suffix.lower()}"
    counter = 2
    while candidate.exists():
        candidate = archive_dir / f"{input_path.stem}_{stamp}-{counter}{input_path.suffix.lower()}"
        counter += 1
    _durable_copy(input_path, candidate)
    if sha256_file(input_path) != sha256_file(candidate):
        raise RuntimeError("archive copy checksum mismatch")
    return candidate


def _durable_copy(source: Path, destination: Path) -> None:
    with source.open("rb") as src, destination.open("wb") as dst:
        shutil.copyfileobj(src, dst)
        dst.flush()
        os.fsync(dst.fileno())


def _temporary_path(parent: Path, suffix: str) -> Path:
    descriptor, name = tempfile.mkstemp(prefix="the-ocr-", suffix=suffix)
    os.close(descriptor)
    return Path(name)


def _write_text_durable(path: Path, value: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(value)
        handle.flush()
        os.fsync(handle.fileno())


def _fsync_file(path: Path) -> None:
    with path.open("r+b") as handle:
        os.fsync(handle.fileno())


def _validate_searchable_pdf(path: Path, document: OCRDocument) -> None:
    with pymupdf.open(path) as pdf:
        if len(pdf) != len(document.pages):
            raise RuntimeError("generated PDF page count differs from OCR document")
        extracted = "".join(page.get_text() for page in pdf).strip()
        if not extracted:
            raise RuntimeError("generated PDF has no extractable OCR text")
        expected_tokens = {
            token.casefold()
            for page in document.pages
            for block in page.blocks
            for token in re.findall(r"\w{3,}", block.text, flags=re.UNICODE)
        }
        extracted_folded = extracted.casefold()
        found = sum(token in extracted_folded for token in expected_tokens)
        if expected_tokens and found / len(expected_tokens) < 0.8:
            raise RuntimeError("generated PDF is missing too much OCR text")


def _publish_outputs(pairs: tuple[tuple[Path, Path], ...], temps: list[Path]) -> None:
    backups: dict[Path, Path] = {}
    published: list[Path] = []
    try:
        for _, destination in pairs:
            if destination.exists():
                backup = _temporary_path(destination.parent, f".{destination.suffix.lstrip('.')}.rollback")
                temps.append(backup)
                _durable_copy(destination, backup)
                backups[destination] = backup
        for temporary, destination in pairs:
            _replace_or_copy(temporary, destination)
            published.append(destination)
    except Exception:
        for destination in reversed(published):
            backup = backups.get(destination)
            if backup is not None and backup.exists():
                _replace_or_copy(backup, destination)
            else:
                destination.unlink(missing_ok=True)
        raise


def _replace_or_copy(source: Path, destination: Path) -> None:
    try:
        source.replace(destination)
    except OSError:
        _durable_copy(source, destination)


def _remove_legacy_outputs(input_path: Path) -> None:
    for suffix in (".searchable.pdf", ".a4.pdf", ".contract.json"):
        legacy = input_path.with_name(input_path.stem + suffix)
        if legacy != input_path:
            legacy.unlink(missing_ok=True)


def _requires_original_geometry(path: Path) -> bool:
    """Avoid an unsafe A4 transform for rotated pages or internal links."""
    with pikepdf.open(path) as pdf:
        for page in pdf.pages:
            if int(page.obj.get("/Rotate", 0)) % 360:
                return True
            for annotation in page.obj.get("/Annots", []):
                if "/Dest" in annotation:
                    return True
                action = annotation.get("/A")
                if action is not None and action.get("/S") == "/GoTo":
                    return True
    return False
