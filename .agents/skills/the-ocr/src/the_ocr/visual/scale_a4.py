from __future__ import annotations

from pathlib import Path

import pikepdf

# Same constants used across every prior implementation of this math in this
# codebase's history (scale-to-a4/app.py, fix_scan_v5.fit_pdf_to_a4_vector,
# SearchablePDFRenderer.swift) -- 210mm x 297mm in PDF points (72/inch).
A4_WIDTH_PT = 595.275590551
A4_HEIGHT_PT = 841.88976378

# Chromium's page.pdf(format="A4") and any already-A4 scan land within a
# fraction of a point of the canonical size, never past it -- this is not a
# "close enough for print" fudge factor, it only absorbs float round-trip
# noise through PDF's own text-based number formatting.
_A4_TOLERANCE_PT = 1.0


def is_already_a4(path: Path) -> bool:
    """True if every page's own mediabox already matches canonical A4
    (portrait or landscape) within `_A4_TOLERANCE_PT`. `fit_pdf_to_a4`
    would be a pure identity transform on such a file -- the caller
    should skip calling it entirely rather than pay the Form-XObject-
    wrapping cost (which also nests fonts inside that Form XObject's own
    /Resources, confirmed to confuse at least one third-party layout-
    analysis text extractor) for zero actual change."""
    with pikepdf.open(path) as pdf:
        for page in pdf.pages:
            mediabox = page.mediabox
            w = float(mediabox[2]) - float(mediabox[0])
            h = float(mediabox[3]) - float(mediabox[1])
            portrait = abs(w - A4_WIDTH_PT) <= _A4_TOLERANCE_PT and abs(h - A4_HEIGHT_PT) <= _A4_TOLERANCE_PT
            landscape = abs(w - A4_HEIGHT_PT) <= _A4_TOLERANCE_PT and abs(h - A4_WIDTH_PT) <= _A4_TOLERANCE_PT
            if not (portrait or landscape):
                return False
    return True


def _transform_rect(rect, mediabox, scale: float, x0: float, y0: float) -> pikepdf.Array:
    """Map a Rect (widget /Rect, in the source page's own coordinate space)
    through the same scale-and-center transform used to place that page's
    content on the destination canvas."""
    mb_x0, mb_y0 = float(mediabox[0]), float(mediabox[1])
    llx, lly, urx, ury = (float(v) for v in rect)
    return pikepdf.Array(
        [
            x0 + (llx - mb_x0) * scale,
            y0 + (lly - mb_y0) * scale,
            x0 + (urx - mb_x0) * scale,
            y0 + (ury - mb_y0) * scale,
        ]
    )


def fit_pdf_to_a4(src: Path, dst: Path) -> None:
    """Vector-fit every page onto an A4 canvas: scale down (never up) to
    fit within A4 preserving aspect ratio, centered. No rasterization --
    pikepdf embeds each original page as a Form XObject on a fresh A4
    page. The destination rect is pre-computed to already match the
    source aspect ratio, so the result is correct regardless of whether
    the underlying overlay call itself preserves aspect ratio or stretches
    to fill the given rect.

    The canvas is portrait A4 for portrait/square source pages and
    landscape A4 (dimensions swapped) for landscape ones -- always forcing
    a portrait canvas would letterbox landscape pages inside a portrait
    frame, shrinking them far more than necessary and visually flipping
    their orientation.

    `as_form_xobject()` captures only the content stream and resources,
    not the page's /Annots -- form fields, links and (most importantly)
    signature widget appearances would silently vanish. Each source
    page's annotations are copied across explicitly afterwards, with
    their /Rect remapped through the same transform as the content, and
    the document's /AcroForm (if any) is copied once so the widgets stay
    reachable from it -- pikepdf's copy_foreign dedupes objects it has
    already copied in this Pdf-to-Pdf session, so the AcroForm's /Fields
    end up pointing at the very same copied annotations already sitting
    in each page's /Annots, not duplicates."""
    with pikepdf.open(src) as pdf, pikepdf.Pdf.new() as out:
        for page_index, page in enumerate(pdf.pages):
            mediabox = page.mediabox
            src_w = float(mediabox[2]) - float(mediabox[0])
            src_h = float(mediabox[3]) - float(mediabox[1])
            if src_w <= 0 or src_h <= 0:
                # A degenerate mediabox means there is no valid page
                # geometry to place -- silently emitting a blank A4 page
                # here would drop this page's content with no error and
                # no recorded reason. Fail the whole fit instead; the
                # caller (pipeline.py) already falls back to OCR-ing the
                # original file and records why in a4_pdf_skipped_reason.
                raise ValueError(f"page {page_index + 1} has a degenerate mediabox ({src_w}x{src_h}), cannot fit to A4")

            canvas_w, canvas_h = (
                (A4_HEIGHT_PT, A4_WIDTH_PT) if src_w > src_h else (A4_WIDTH_PT, A4_HEIGHT_PT)
            )
            form = page.as_form_xobject()
            new_page = out.add_blank_page(page_size=(canvas_w, canvas_h))
            scale = min(canvas_w / src_w, canvas_h / src_h, 1.0)
            dst_w, dst_h = src_w * scale, src_h * scale
            x0 = (canvas_w - dst_w) / 2
            y0 = (canvas_h - dst_h) / 2
            new_page.add_overlay(form, pikepdf.Rectangle(x0, y0, x0 + dst_w, y0 + dst_h))

            annots = page.get("/Annots")
            if annots:
                copied = [
                    _relocate_annot(out, annot, new_page.obj, mediabox, scale, x0, y0)
                    for annot in annots
                ]
                new_page.obj.Annots = pikepdf.Array(copied)

        if "/AcroForm" in pdf.Root:
            out.Root.AcroForm = out.copy_foreign(pdf.Root.AcroForm)

        out.save(dst)


def _transform_points(values, mediabox, scale: float, x0: float, y0: float) -> pikepdf.Array:
    mb_x0, mb_y0 = float(mediabox[0]), float(mediabox[1])
    transformed = []
    for index in range(0, len(values), 2):
        transformed.extend(
            (
                x0 + (float(values[index]) - mb_x0) * scale,
                y0 + (float(values[index + 1]) - mb_y0) * scale,
            )
        )
    return pikepdf.Array(transformed)


def _relocate_annot(out: pikepdf.Pdf, annot, new_page, mediabox, scale: float, x0: float, y0: float):
    copied = out.copy_foreign(annot)
    if "/Rect" in copied:
        copied.Rect = _transform_rect(copied.Rect, mediabox, scale, x0, y0)
    for key in ("/QuadPoints", "/Vertices", "/L", "/CL"):
        if key in copied and len(copied[key]) % 2 == 0:
            copied[key] = _transform_points(copied[key], mediabox, scale, x0, y0)
    if "/InkList" in copied:
        copied.InkList = pikepdf.Array(
            [_transform_points(stroke, mediabox, scale, x0, y0) for stroke in copied.InkList]
        )
    copied.P = new_page
    return copied
