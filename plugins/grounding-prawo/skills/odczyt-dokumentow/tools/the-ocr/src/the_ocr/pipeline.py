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
from .models import OCRDocument
from .pdf.searchable_pdf import build_document_searchable_pdf
from .pdf.source_pdf import image_to_a4_pdf, strip_invisible_text
from .providers.base import OCRProvider
from .visual.scale_a4 import fit_pdf_to_a4, is_already_a4


SUPPORTED_SUFFIXES = {".pdf", ".jpg", ".jpeg", ".png"}

ARCHIVE_DIR_ENV_VAR = "THE_OCR_ARCHIVE_DIR"


def resolve_archive_dir(archive_dir: Path | str | None = None) -> Path:
    """Katalog archiwum: parametr/CLI > zmienna THE_OCR_ARCHIVE_DIR > ~/archive."""
    if archive_dir is not None:
        return Path(archive_dir)
    configured = os.environ.get(ARCHIVE_DIR_ENV_VAR, "").strip()
    if configured:
        return Path(configured)
    return Path.home() / "archive"


@dataclass
class PipelineResult:
    chain_result: ChainResult
    archive_path: Path | None = None
    pdf_path: Path | None = None
    markdown_path: Path | None = None
    json_path: Path | None = None
    wanted_markdown: bool = False
    wanted_json: bool = False

    @property
    def ok(self) -> bool:
        return (
            self.chain_result.ok
            and self.pdf_path is not None
            and (self.markdown_path is not None or not self.wanted_markdown)
            and (self.json_path is not None or not self.wanted_json)
        )


def run_pipeline(
    input_path: Path,
    providers: list[OCRProvider],
    *,
    force: str | None = None,
    output: Path | str | None = None,
    markdown: bool = False,
    json_output: bool = False,
    archive: bool = False,
    archive_dir: Path | str | None = None,
    a4: bool = True,
    layer: str = "auto",
) -> PipelineResult:
    """OCR (Datalab -> LlamaParse -> Azure -> Google Vision) -> wierny przeszukiwalny PDF.

    Domyslnie powstaje tylko PDF: dla PDF w miejscu wejscia, dla obrazu obok
    (<stem>.pdf, obraz zostaje). Opcjonalnie: `output` (inna sciezka PDF),
    `markdown`/`json_output` (pliki obok PDF), `archive` lub `archive_dir`
    (kopia oryginalu przed OCR; przy archiwizacji obraz wejsciowy jest
    usuwany po sukcesie). Strony sa domyslnie dopasowywane do A4
    (`a4=False` zachowuje geometrie). `layer` to tryb OCRmyPDF dla warstwy:
    `auto` (domyslnie) = `redo` (oryginalna tresc stron bez rasteryzacji),
    a dla PDF z formularzem AcroForm `skip`; `force` rasteryzuje strony.
    """
    input_path = Path(input_path)
    suffix = input_path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(f"unsupported input type '{suffix}'; expected PDF, JPG, JPEG, or PNG")
    if not input_path.is_file():
        raise ValueError(f"input is not a file: {input_path}")

    output_pdf = Path(output) if output is not None else input_path.with_suffix(".pdf")
    output_md = output_pdf.with_suffix(".md")
    output_json = output_pdf.with_suffix(".json")
    archive_path = None
    if archive or archive_dir is not None:
        archive_path = _archive_input(input_path, resolve_archive_dir(archive_dir))
    result = PipelineResult(
        chain_result=ChainResult(result=None),
        archive_path=archive_path,
        wanted_markdown=markdown,
        wanted_json=json_output,
    )
    if output is None and suffix != ".pdf" and output_pdf.exists():
        kept = f"; input preserved as {archive_path}" if archive_path else ""
        raise ValueError(f"refusing to overwrite existing output PDF: {output_pdf}{kept}")
    source = archive_path or input_path
    temps: list[Path] = []
    try:
        prepared_pdf = _temporary_path(input_path.parent, ".prepared.pdf")
        temps.append(prepared_pdf)
        prepare_pdf(source, prepared_pdf, a4=a4)

        chain_result = run_chain(prepared_pdf, providers, force=force)
        result.chain_result = chain_result
        if not chain_result.ok:
            return result

        document = replace(
            chain_result.result.document,
            doc_id=input_path.stem,
            source_name=input_path.name,
        )
        document.validate()
        chain_result.result.document = document
        chain_result.result.text = document.text

        pdf_tmp = _temporary_path(input_path.parent, ".pdf.tmp")
        temps.append(pdf_tmp)
        build_document_searchable_pdf(prepared_pdf, pdf_tmp, document, mode=resolve_layer(layer, prepared_pdf))
        validate_searchable_pdf(pdf_tmp, document)
        _fsync_file(pdf_tmp)
        pairs: list[tuple[Path, Path]] = []
        if json_output:
            json_tmp = _temporary_path(input_path.parent, ".json.tmp")
            temps.append(json_tmp)
            _write_text_durable(json_tmp, json.dumps(document.to_dict(), ensure_ascii=False, indent=2) + "\n")
            pairs.append((json_tmp, output_json))
        if markdown:
            md_tmp = _temporary_path(input_path.parent, ".md.tmp")
            temps.append(md_tmp)
            _write_text_durable(md_tmp, render_with_frontmatter(input_path, document))
            pairs.append((md_tmp, output_md))
        pairs.append((pdf_tmp, output_pdf))

        output_pdf.parent.mkdir(parents=True, exist_ok=True)
        _publish_outputs(tuple(pairs), temps)
        result.pdf_path = output_pdf
        result.json_path = output_json if json_output else None
        result.markdown_path = output_md if markdown else None

        if suffix != ".pdf" and archive_path is not None and output is None:
            input_path.unlink()
        return result
    finally:
        for path in temps:
            path.unlink(missing_ok=True)


def process_input(input_path: Path, providers: list[OCRProvider], **kwargs) -> PipelineResult:
    return run_pipeline(input_path, providers, **kwargs)


def resolve_layer(layer: str, pdf_path: Path) -> str:
    """`auto` -> `redo`, chyba ze PDF ma formularz (OCRmyPDF odmawia redo) -> `skip`."""
    if layer != "auto":
        return layer
    with pikepdf.open(pdf_path) as pdf:
        return "skip" if "/AcroForm" in pdf.Root else "redo"


def prepare_pdf(source: Path, destination: Path, *, a4: bool = True) -> None:
    """Obraz trafia na strone A4; PDF traci stara niewidzialna warstwe tekstu
    i jest dopasowywany do A4, chyba ze a4=False (geometria bez zmian)."""
    if source.suffix.lower() != ".pdf":
        image_to_a4_pdf(source, destination)
        return

    clean = destination.with_suffix(".clean.pdf")
    try:
        strip_invisible_text(source, clean)
        if not a4 or is_already_a4(clean) or _requires_original_geometry(clean):
            clean.replace(destination)
        else:
            fit_pdf_to_a4(clean, destination)
    finally:
        clean.unlink(missing_ok=True)


def _archive_input(input_path: Path, archive_dir: Path) -> Path:
    _ensure_writable_dir(archive_dir)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate = archive_dir / f"{input_path.stem}_{stamp}{input_path.suffix.lower()}"
    counter = 2
    while candidate.exists():
        candidate = archive_dir / f"{input_path.stem}_{stamp}-{counter}{input_path.suffix.lower()}"
        counter += 1
    _durable_copy(input_path, candidate)
    return candidate


def _ensure_writable_dir(directory: Path) -> None:
    """Proba zapisu przed OCR: brak dostepu = czytelny blad, OCR sie nie zaczyna."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        probe = directory / ".the-ocr-write-test"
        with probe.open("wb") as handle:
            handle.write(b"ok")
            handle.flush()
            os.fsync(handle.fileno())
        probe.unlink()
    except OSError as exc:
        raise OSError(f"archive directory is not writable: {directory} ({exc})") from exc


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


def validate_searchable_pdf(path: Path, document: OCRDocument) -> None:
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


def _requires_original_geometry(path: Path) -> bool:
    """Avoid an unsafe A4 transform for rotated pages or internal links.

    Every value read here comes from an untrusted PDF, so nothing is assumed
    to have the type the specification prescribes: /Rotate may not be a
    number, /Annots may not be an array, an annotation or its /A action may
    not be a dictionary. A malformed object must not raise -- when the
    structure cannot be understood, the page keeps its original geometry.
    """
    with pikepdf.open(path) as pdf:
        for page in pdf.pages:
            if _rotated(page.obj.get("/Rotate")):
                return True
            annotations = page.obj.get("/Annots")
            if not isinstance(annotations, pikepdf.Array):
                if annotations is not None:
                    return True
                continue
            for annotation in annotations:
                if not isinstance(annotation, pikepdf.Dictionary):
                    return True
                if "/Dest" in annotation:
                    return True
                action = annotation.get("/A")
                if action is None:
                    continue
                if not isinstance(action, pikepdf.Dictionary):
                    return True
                if str(action.get("/S", "")) == "/GoTo":
                    return True
    return False


def _rotated(value: object) -> bool:
    if value is None:
        return False
    try:
        return int(value) % 360 != 0
    except (TypeError, ValueError):
        return True
