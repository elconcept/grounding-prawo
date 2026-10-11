"""Compatibility import for the non-embedding text-layer implementation."""

from .text_layer import (
    build_document_searchable_pdf as _build_document_searchable_pdf,
    build_searchable_pdf as _build_searchable_pdf,
)

build_searchable_pdf = _build_searchable_pdf
build_document_searchable_pdf = _build_document_searchable_pdf
