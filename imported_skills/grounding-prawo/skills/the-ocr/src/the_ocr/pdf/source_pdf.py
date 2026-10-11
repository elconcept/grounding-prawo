from __future__ import annotations

from pathlib import Path

import pikepdf
import pymupdf
from PIL import Image, ImageOps

from ..visual.scale_a4 import A4_HEIGHT_PT, A4_WIDTH_PT


_TEXT_SHOWING_OPERATORS = {"Tj", "TJ", "'", '"'}


def strip_invisible_text(src: Path, dst: Path) -> None:
    """Remove hidden OCR text (`Tr 3`) while retaining visible page content."""
    with pikepdf.open(src) as pdf:
        visited: dict[tuple[int, int], int] = {}
        for page in pdf.pages:
            _strip_container(pdf, page, _inherited_resources(page.obj), visited, inherited_render_mode=0)
        pdf.save(
            dst,
            compress_streams=True,
            object_stream_mode=pikepdf.ObjectStreamMode.generate,
        )


def _strip_container(
    pdf: pikepdf.Pdf,
    container,
    resources,
    visited: dict[tuple[int, int], int],
    *,
    inherited_render_mode: int,
) -> None:
    try:
        instructions = list(pikepdf.parse_content_stream(container))
    except (pikepdf.PdfError, TypeError):
        return
    render_mode = inherited_render_mode
    stack: list[int] = []
    kept = []
    for instruction in instructions:
        operator = str(instruction.operator)
        if operator == "q":
            stack.append(render_mode)
        elif operator == "Q" and stack:
            render_mode = stack.pop()
        elif operator == "Tr" and instruction.operands:
            render_mode = int(instruction.operands[0])
        elif operator == "Do" and instruction.operands:
            xobjects = (resources or {}).get("/XObject", {})
            xobject = xobjects.get(instruction.operands[0])
            if xobject is not None and xobject.get("/Subtype") == "/Form":
                visit_key = xobject.objgen
                previous_mode = visited.get(visit_key)
                if previous_mode is not None and previous_mode != render_mode:
                    raise ValueError("shared Form XObject is used with both visible and hidden text modes")
                if previous_mode is None:
                    visited[visit_key] = render_mode
                    _strip_container(
                        pdf,
                        xobject,
                        xobject.get("/Resources") or resources,
                        visited,
                        inherited_render_mode=render_mode,
                    )
        if not (operator in _TEXT_SHOWING_OPERATORS and render_mode == 3):
            kept.append(instruction)
    stream = pikepdf.unparse_content_stream(kept)
    if hasattr(container, "Contents"):
        container.Contents = pdf.make_stream(stream)
    else:
        container.write(stream)


def _inherited_resources(page_object):
    current = page_object
    while current is not None:
        resources = current.get("/Resources")
        if resources is not None:
            return resources
        current = current.get("/Parent")
    return None

def image_to_a4_pdf(src: Path, dst: Path) -> None:
    """Place an image on A4 without enhancement, binarization, or resampling."""
    image_source = src
    rotated: Path | None = None
    with Image.open(src) as image:
        orientation = image.getexif().get(274, 1)
        if orientation != 1:
            transposed = ImageOps.exif_transpose(image)
            width, height = transposed.size
            rotated = dst.with_suffix(".oriented.png")
            transposed.save(rotated, format="PNG")
            image_source = rotated
        else:
            width, height = image.size

    landscape = width > height
    page_width, page_height = (A4_HEIGHT_PT, A4_WIDTH_PT) if landscape else (A4_WIDTH_PT, A4_HEIGHT_PT)
    scale = min(page_width / width, page_height / height)
    draw_width, draw_height = width * scale, height * scale
    rect = pymupdf.Rect(
        (page_width - draw_width) / 2,
        (page_height - draw_height) / 2,
        (page_width + draw_width) / 2,
        (page_height + draw_height) / 2,
    )
    document = pymupdf.open()
    try:
        page = document.new_page(width=page_width, height=page_height)
        page.insert_image(rect, filename=str(image_source), keep_proportion=True)
        document.save(dst, garbage=4, deflate=True)
    finally:
        document.close()
        if rotated is not None:
            rotated.unlink(missing_ok=True)
