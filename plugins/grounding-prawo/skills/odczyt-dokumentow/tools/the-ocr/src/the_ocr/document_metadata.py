"""Conservative metadata extraction from OCR text (never from the filename or OCR clock).

Fields are emitted only when the source actually contains a recognizable
identifier, explicit date label or document heading. Original value spelling
is preserved; ambiguous dates or references are deliberately omitted.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Iterable

from .models import OCRDocument


# A case number is not classified as a court signature without a judicial
# format and a matching "Sygn. akt" label. Ds. and RSoW have distinct origins.
_COURT_CASE = re.compile(
    r"\b(?:[IVXLCDM]{1,8}\s+)?[A-Z]{1,4}(?:\s+[A-Z]{1,4})?\s+"
    r"\d{1,7}/\d{2,4}(?:/[A-Z]{1,4})?\b",
    re.IGNORECASE,
)
_COURT_LABEL = re.compile(
    r"\b(?:sygn(?:atura|\.)\s*(?:akt|sądowa|sprawy)?|sygnatura\s+sądowa)\s*[:.]?\s*",
    re.IGNORECASE,
)
_PROSECUTOR_CASE = re.compile(
    r"\b(?:(?:PR|PO|PK)\s*\d{1,3}\s+)?Ds\.\s*\d{1,7}(?:[./]\d{2,4}){1,2}\b",
    re.IGNORECASE,
)
_POLICE_CASE = re.compile(r"\bRSoW\s*[-:]?\s*\d{1,7}(?:[./-]\d{1,4}){1,2}\b", re.IGNORECASE)
_POLICE_LABEL = re.compile(
    r"\b(?:sygnatura(?:\s+sprawy)?\s+policji|sygn\.\s*policji|"
    r"nr\.?\s*sprawy\s+policji)\s*[:#-]?\s*",
    re.IGNORECASE,
)
_KARTA = re.compile(
    r"^\s*(?:karta\s+akt|karty\s+akt|karta|k\.)\s*[:.]?\s*"
    r"(?P<value>\d{1,6}[a-z]?(?:\s*[-–]\s*\d{1,6}[a-z]?)?)\b",
    re.IGNORECASE,
)

_DATE = re.compile(
    r"(?<!\d)(?:[0-3]?\d[./-][01]?\d[./-](?:19|20)\d{2}|"
    r"(?:19|20)\d{2}-[01]?\d-[0-3]?\d)(?!\d)"
)
_PRINT_DATE_LABEL = re.compile(
    r"\b(?:data\s+wydruku|wydrukowano\s*(?:dnia)?|wydruk\s+z\s+dnia)\s*[:\-]?\s*",
    re.IGNORECASE,
)
_ISSUE_DATE_LABEL = re.compile(
    r"\b(?:data\s+wystawienia|wystawiono\s*(?:dnia)?|"
    r"data\s+sporządzenia|sporządzono\s*(?:dnia)?)\s*[:\-]?\s*",
    re.IGNORECASE,
)
_RECEIVED_DATE_LABEL = re.compile(
    r"\b(?:data\s+wpływu|wpłynęło\s*(?:dnia)?)\s*[:\-]?\s*",
    re.IGNORECASE,
)
_CITY_DATE = re.compile(r"^[^\n,:]{2,35},\s*dnia\s+", re.IGNORECASE)
_KIND = re.compile(
    r"^(?P<value>"
    r"notatka\s+urzędowa|"
    r"protokół(?:\s+(?:przesłuchania(?:\s+(?:świadka|obwinionego|podejrzanego))?"
    r"|rozprawy|oględzin))?|"
    r"postanowienie|"
    r"wyrok(?:\s+nakazowy)?|"
    r"zawiadomienie|"
    r"wezwanie|"
    r"uzasadnienie|"
    r"decyzja|"
    r"zaświadczenie|"
    r"pismo\s+procesowe|"
    r"wniosek(?:\s+o\s+[^\n,.;:]{3,60})?"
    r")\b",
    re.IGNORECASE,
)


def _lines(document: OCRDocument) -> list[str]:
    return [
        line.strip()
        for page in document.pages
        for block in page.blocks
        for line in block.text.splitlines()
        if line.strip()
    ]


def _date_in(value: str) -> str | None:
    """Match an actual calendar date, preserving its literal OCR spelling."""
    for match in _DATE.finditer(value[:60]):
        candidate = match.group(0)
        for pattern in ("%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
            try:
                datetime.strptime(candidate, pattern)
                return candidate
            except ValueError:
                continue
    return None


def _labeled_date(lines: Iterable[str], label: re.Pattern[str]) -> str | None:
    for line in lines:
        matched = label.search(line)
        if matched:
            date = _date_in(line[matched.end():])
            if date is not None:
                return date
    return None


def _document_kind(document: OCRDocument, lines: list[str]) -> str | None:
    # Prefer the provider's actual "title" block, then early lines. We do
    # not turn a random sentence mentioning a document into its kind.
    title_lines = [
        line
        for page in document.pages[:1]
        for block in page.blocks[:30]
        if block.block_type == "title"
        for line in block.text.splitlines()
    ]
    for line in [*title_lines, *lines[:25]]:
        match = _KIND.match(re.sub(r"^\s*#{1,6}\s*", "", line.strip()))
        if match:
            return re.sub(r"\s+", " ", match.group("value")).strip()
    return None


def extract_document_metadata(document: OCRDocument) -> dict[str, str]:
    """Extract document facts from OCR data only. Never infer absent fields."""
    lines = _lines(document)
    metadata: dict[str, str] = {}
    for line in lines:
        label = _COURT_LABEL.search(line)
        if label:
            case = _COURT_CASE.search(line[label.end():label.end() + 100])
            if case:
                metadata["sygnatura_sad"] = re.sub(r"\s+", " ", case.group()).strip()
                break

    for line in lines:
        case = _PROSECUTOR_CASE.search(line)
        if case:
            metadata["sygnatura_prokuratura"] = re.sub(r"\s+", " ", case.group()).strip()
            break

    for line in lines:
        case = _POLICE_CASE.search(line)
        if case:
            metadata["sygnatura_policja"] = re.sub(r"\s+", " ", case.group()).strip()
            break
        label = _POLICE_LABEL.search(line)
        if label:
            value = re.split(r"[;,]|\s{2,}", line[label.end():], maxsplit=1)[0].strip(" .:-")
            if re.search(r"\d", value) and 4 <= len(value) <= 50:
                metadata["sygnatura_policja"] = value
                break

    for line in lines:
        card = _KARTA.search(line)
        if card:
            metadata["karta_akt"] = re.sub(r"\s+", "", card.group("value"))
            break

    kind = _document_kind(document, lines)
    if kind:
        metadata["rodzaj_dokumentu"] = kind

    print_date = _labeled_date(lines, _PRINT_DATE_LABEL)
    if print_date:
        metadata["data_wydruku"] = print_date

    issue_date = _labeled_date(lines, _ISSUE_DATE_LABEL)
    if not issue_date:
        for line in lines[:20]:
            city = _CITY_DATE.search(line)
            if city:
                issue_date = _date_in(line[city.end():])
                if issue_date:
                    break
    if issue_date:
        metadata["data_wystawienia"] = issue_date

    received = _labeled_date(lines, _RECEIVED_DATE_LABEL)
    if received:
        metadata["data_wplywu"] = received

    return metadata
