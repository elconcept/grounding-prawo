from __future__ import annotations

import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

import httpx
import pymupdf

from ..adapters import azure_document
from .base import OCRProvider, OCRResult

API_VERSION = "2024-11-30"
MODEL = "prebuilt-read"


class AzureProvider(OCRProvider):
    """Azure AI Document Intelligence (prebuilt-read) przez REST.

    AZURE_DOCUMENT_ENDPOINT (np. https://<zasob>.cognitiveservices.azure.com)
    i AZURE_DOCUMENT_KEY. Darmowy tier F0: 500 stron/miesiac, max 2 strony
    na zadanie: PDF idzie paczkami po AZURE_DOCUMENT_PAGES_PER_REQUEST stron
    (domyslnie 2), strony sa skladane w jeden wynik. Gdy Azure zwroci mniej
    stron niz paczka, adapter zglasza blad i lancuch idzie dalej.
    """

    name = "azure"

    def __init__(self, *, timeout: float = 600, poll_interval: float = 2):
        self.timeout = timeout
        self.poll_interval = poll_interval

    def is_available(self) -> tuple[bool, str]:
        if _endpoint() and os.getenv("AZURE_DOCUMENT_KEY", "").strip():
            return True, ""
        if os.getenv("AZURE_DOCUMENT_RESOURCE", "").strip() and shutil.which("az"):
            return True, ""
        return False, ("no Azure Document Intelligence credentials (AZURE_DOCUMENT_ENDPOINT + AZURE_DOCUMENT_KEY, "
                       "or AZURE_DOCUMENT_RESOURCE with a logged-in az CLI)")

    def recognize(self, path: Path) -> OCRResult:
        available, reason = self.is_available()
        if not available:
            return OCRResult(text="", backend=self.name, error=reason)
        try:
            endpoint, key = _credentials()
            raw = self._analyze(path, endpoint, key)
            document = azure_document(raw, path)
            return OCRResult(text=document.text, backend=self.name, raw=raw, document=document)
        except Exception as exc:
            return OCRResult(text="", backend=self.name, error=f"Azure: {exc}")

    def _analyze(self, path: Path, endpoint: str, key: str) -> dict[str, Any]:
        per_request = max(1, int(os.getenv("AZURE_DOCUMENT_PAGES_PER_REQUEST", "2")))
        with pymupdf.open(path) as pdf:
            page_count = len(pdf)
            if page_count <= per_request:
                return self._analyze_bytes(path.read_bytes(), endpoint, key)
            pages: list[dict[str, Any]] = []
            for first in range(0, page_count, per_request):
                chunk = pymupdf.open()
                try:
                    chunk.insert_pdf(pdf, from_page=first, to_page=min(first + per_request, page_count) - 1)
                    content = chunk.tobytes(garbage=3, deflate=True)
                finally:
                    chunk.close()
                result = self._analyze_bytes(content, endpoint, key).get("analyzeResult") or {}
                chunk_pages = result.get("pages") or []
                expected = min(per_request, page_count - first)
                if len(chunk_pages) != expected:
                    raise ValueError(f"Azure returned {len(chunk_pages)} of {expected} pages for pages {first + 1}-{first + expected}")
                for offset, page in enumerate(chunk_pages):
                    pages.append({**page, "pageNumber": first + offset + 1})
        return {"status": "succeeded", "analyzeResult": {"pages": pages}}

    def _analyze_bytes(self, content: bytes, endpoint: str, key: str) -> dict[str, Any]:
        auth = {"Ocp-Apim-Subscription-Key": key}
        url = f"{endpoint}/documentintelligence/documentModels/{MODEL}:analyze?api-version={API_VERSION}"
        deadline = time.monotonic() + self.timeout
        with httpx.Client(timeout=120.0) as client:
            for attempt in range(6):  # F0 throttles with 429 + Retry-After
                response = client.post(url, headers={**auth, "Content-Type": "application/pdf"}, content=content)
                if response.status_code != 429:
                    break
                time.sleep(float(response.headers.get("Retry-After") or 5 * (attempt + 1)))
            response.raise_for_status()
            operation = response.headers["Operation-Location"]
            while True:
                poll = client.get(operation, headers=auth)
                if poll.status_code == 429:
                    time.sleep(float(poll.headers.get("Retry-After") or 3))
                    continue
                poll.raise_for_status()
                result = poll.json()
                status = result.get("status")
                if status == "succeeded":
                    return result
                if status in {"failed", "canceled"}:
                    raise RuntimeError(str(result.get("error") or f"analysis {status}"))
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"analysis did not finish within {self.timeout:g}s")
                time.sleep(float(poll.headers.get("Retry-After") or self.poll_interval))


def _endpoint() -> str:
    return os.getenv("AZURE_DOCUMENT_ENDPOINT", "").strip().rstrip("/")


def _credentials() -> tuple[str, str]:
    """Endpoint and key from the environment, else from the logged-in az CLI (AZURE_DOCUMENT_RESOURCE)."""
    endpoint, key = _endpoint(), os.getenv("AZURE_DOCUMENT_KEY", "").strip()
    if endpoint and key:
        return endpoint, key
    resource = os.environ["AZURE_DOCUMENT_RESOURCE"].strip()
    group = os.getenv("AZURE_DOCUMENT_RESOURCE_GROUP", "").strip()
    base = ["az", "cognitiveservices", "account"]
    scope = ["--name", resource] + (["--resource-group", group] if group else [])
    if not endpoint:
        endpoint = _az(base + ["show", *scope, "--query", "properties.endpoint", "-o", "tsv"]).rstrip("/")
    return endpoint, key or _az(base + ["keys", "list", *scope, "--query", "key1", "-o", "tsv"])


def _az(args: list[str]) -> str:
    out = subprocess.run(args, capture_output=True, text=True, timeout=120)
    if out.returncode != 0 or not out.stdout.strip():
        raise RuntimeError(f"az CLI failed: {out.stderr.strip()[-300:]}")
    return out.stdout.strip()
