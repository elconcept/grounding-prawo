from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

import httpx
import pymupdf

from ..adapters import polygon_document
from .base import OCRProvider, OCRResult

API_VERSION = "2024-11-30"
MODEL = "prebuilt-read"


class AzureDocumentIntelligenceProvider(OCRProvider):
    """Azure Document Intelligence (prebuilt-read) over REST, no SDK.

    Credentials: AZURE_DOCUMENT_ENDPOINT + AZURE_DOCUMENT_KEY, or - when the key is not set -
    AZURE_DOCUMENT_RESOURCE (+ AZURE_DOCUMENT_RESOURCE_GROUP) resolved at run time through a
    logged-in `az` CLI, so the key never lands in a file.

    The free tier (F0: 500 pages/month) analyses only the first 2 pages of a document, so the
    PDF is sent in chunks of AZURE_DOCUMENT_PAGES_PER_CALL pages (default 2) and merged.
    """

    name = "azure-di"

    def __init__(self, *, timeout: float = 600, poll_interval: float = 1.5):
        self.timeout = timeout
        self.poll_interval = poll_interval

    def is_available(self) -> tuple[bool, str]:
        if os.getenv("AZURE_DOCUMENT_ENDPOINT") and os.getenv("AZURE_DOCUMENT_KEY"):
            return True, ""
        if os.getenv("AZURE_DOCUMENT_RESOURCE") and shutil.which("az"):
            return True, ""
        return False, "AZURE_DOCUMENT_ENDPOINT/AZURE_DOCUMENT_KEY not set and no AZURE_DOCUMENT_RESOURCE + az CLI"

    def recognize(self, path: Path) -> OCRResult:
        available, reason = self.is_available()
        if not available:
            return OCRResult(text="", backend=self.name, error=reason)
        try:
            endpoint, key = self._credentials()
            per_call = max(1, int(os.getenv("AZURE_DOCUMENT_PAGES_PER_CALL", "2")))
            pages: list[dict[str, Any]] = []
            with tempfile.TemporaryDirectory() as tmp:
                for chunk in _pdf_chunks(path, per_call, Path(tmp)):
                    pages.extend(self._analyze(chunk, endpoint, key)["pages"])
            raw = {"pages": pages, "model": MODEL, "api_version": API_VERSION}
            document = polygon_document(
                [_azure_page(page) for page in pages], path, provider=self.name,
                metadata={"model": MODEL, "api_version": API_VERSION, "pages_per_call": per_call},
            )
            return OCRResult(text=document.text, backend=self.name, raw=raw, document=document)
        except Exception as exc:
            return OCRResult(text="", backend=self.name, error=f"Azure DI failed: {exc}")

    def _credentials(self) -> tuple[str, str]:
        endpoint = os.getenv("AZURE_DOCUMENT_ENDPOINT", "").strip()
        key = os.getenv("AZURE_DOCUMENT_KEY", "").strip()
        if endpoint and key:
            return endpoint.rstrip("/"), key
        resource = os.environ["AZURE_DOCUMENT_RESOURCE"].strip()
        group = os.getenv("AZURE_DOCUMENT_RESOURCE_GROUP", "").strip()
        base = ["az", "cognitiveservices", "account"]
        scope = ["--name", resource] + (["--resource-group", group] if group else [])
        if not endpoint:
            endpoint = _az(base + ["show", *scope, "--query", "properties.endpoint", "-o", "tsv"])
        key = _az(base + ["keys", "list", *scope, "--query", "key1", "-o", "tsv"])
        return endpoint.rstrip("/"), key

    def _analyze(self, pdf: Path, endpoint: str, key: str) -> dict[str, Any]:
        url = f"{endpoint}/documentintelligence/documentModels/{MODEL}:analyze?api-version={API_VERSION}"
        headers = {"Ocp-Apim-Subscription-Key": key}
        deadline = time.monotonic() + self.timeout
        with httpx.Client(timeout=120.0) as client:
            for attempt in range(6):
                response = client.post(url, headers={**headers, "Content-Type": "application/pdf"},
                                       content=pdf.read_bytes())
                if response.status_code != 429:
                    break
                time.sleep(float(response.headers.get("Retry-After", 5 * (attempt + 1))))
            response.raise_for_status()
            operation = response.headers["Operation-Location"]
            while time.monotonic() < deadline:
                poll = client.get(operation, headers=headers)
                if poll.status_code == 429:
                    time.sleep(float(poll.headers.get("Retry-After", 3)))
                    continue
                poll.raise_for_status()
                body = poll.json()
                status = body.get("status")
                if status == "succeeded":
                    return body["analyzeResult"]
                if status in {"failed", "canceled"}:
                    raise RuntimeError(json.dumps(body.get("error"), ensure_ascii=False))
                time.sleep(self.poll_interval)
        raise TimeoutError(f"analysis did not finish within {self.timeout:g}s")


def _az(args: list[str]) -> str:
    out = subprocess.run(args, capture_output=True, text=True, timeout=120)
    if out.returncode != 0 or not out.stdout.strip():
        raise RuntimeError(f"az CLI failed: {out.stderr.strip()[-300:]}")
    return out.stdout.strip()


def _pdf_chunks(path: Path, size: int, tmp: Path) -> list[Path]:
    with pymupdf.open(path) as source:
        if len(source) <= size:
            return [path]
        chunks = []
        for start in range(0, len(source), size):
            part = pymupdf.open()
            part.insert_pdf(source, from_page=start, to_page=min(start + size, len(source)) - 1)
            target = tmp / f"chunk_{start:05d}.pdf"
            part.save(target)
            part.close()
            chunks.append(target)
        return chunks


def _azure_page(page: dict[str, Any]) -> dict[str, Any]:
    """Azure page (polygons in page units: inch for PDF) -> neutral page for polygon_document."""
    words = page.get("words") or []
    lines = []
    for line in page.get("lines") or []:
        spans = line.get("spans") or []
        members = [
            word for word in words
            if any(span["offset"] <= word["span"]["offset"] < span["offset"] + span["length"] for span in spans)
        ]
        lines.append({
            "text": line.get("content", ""),
            "polygon": line.get("polygon") or [],
            "words": [
                {"text": w.get("content", ""), "polygon": w.get("polygon") or [], "confidence": w.get("confidence")}
                for w in members
            ],
        })
    return {"width": float(page["width"]), "height": float(page["height"]), "lines": lines}
