from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

import httpx
import pymupdf

from ..adapters import google_vision_document
from .base import OCRProvider, OCRResult

ENDPOINT = "https://vision.googleapis.com/v1/files:annotate"
PAGES_PER_REQUEST = 5  # limit synchronicznego files:annotate


class GoogleVisionProvider(OCRProvider):
    """Google Cloud Vision DOCUMENT_TEXT_DETECTION przez REST.

    Uwierzytelnienie: klucz API (GOOGLE_VISION_API_KEY) albo plik JSON konta
    uslugi (GOOGLE_VISION_CREDENTIALS, sciezka wzgledna wobec katalogu .env),
    albo Application Default Credentials zalogowanego `gcloud` (projekt
    rozliczeniowy: GOOGLE_CLOUD_PROJECT, quota_project_id z ADC albo projekt gcloud).
    Darmowe 1000 jednostek/miesiac; PDF idzie paczkami po 5 stron.
    """

    name = "google_vision"

    def is_available(self) -> tuple[bool, str]:
        if os.getenv("GOOGLE_VISION_API_KEY", "").strip():
            return True, ""
        credentials = _credentials_path()
        if credentials is not None:
            if not credentials.is_file():
                return False, f"Google Vision credentials file not found: {credentials}"
            return True, ""
        if shutil.which("gcloud") and _adc_file():
            return True, ""
        return False, ("no Google Vision credentials (GOOGLE_VISION_API_KEY, GOOGLE_VISION_CREDENTIALS "
                       "or gcloud Application Default Credentials)")

    def recognize(self, path: Path) -> OCRResult:
        available, reason = self.is_available()
        if not available:
            return OCRResult(text="", backend=self.name, error=reason)
        try:
            responses = self._annotate(path)
            document = google_vision_document(responses, path)
            return OCRResult(text=document.text, backend=self.name, raw=responses, document=document)
        except Exception as exc:
            return OCRResult(text="", backend=self.name, error=f"Google Vision: {exc}")

    def _annotate(self, path: Path) -> list[dict[str, Any]]:
        with pymupdf.open(path) as pdf:
            page_count = len(pdf)
        content = base64.b64encode(path.read_bytes()).decode("ascii")
        params, headers = _auth()
        pages: list[dict[str, Any]] = []
        with httpx.Client(timeout=300.0) as client:
            for first in range(1, page_count + 1, PAGES_PER_REQUEST):
                numbers = list(range(first, min(first + PAGES_PER_REQUEST, page_count + 1)))
                body = {
                    "requests": [
                        {
                            "inputConfig": {"content": content, "mimeType": "application/pdf"},
                            "features": [{"type": "DOCUMENT_TEXT_DETECTION"}],
                            "imageContext": {"languageHints": ["pl"]},
                            "pages": numbers,
                        }
                    ]
                }
                response = client.post(ENDPOINT, params=params, headers=headers, json=body)
                response.raise_for_status()
                batch = (response.json().get("responses") or [{}])[0]
                if batch.get("error"):
                    raise RuntimeError(batch["error"].get("message", "request failed"))
                pages.extend(sorted(batch.get("responses") or [], key=lambda item: (item.get("context") or {}).get("pageNumber", 0)))
        return pages


def _credentials_path() -> Path | None:
    configured = os.getenv("GOOGLE_VISION_CREDENTIALS", "").strip()
    if not configured:
        return None
    path = Path(configured).expanduser()
    if not path.is_absolute():
        from ..config import runtime_directory

        path = runtime_directory() / path
    return path


def _auth() -> tuple[dict[str, str], dict[str, str]]:
    """Parametry zapytania i naglowki: klucz API albo token konta uslugi."""
    key = os.getenv("GOOGLE_VISION_API_KEY", "").strip()
    if key:
        return {"key": key}, {}
    if _credentials_path() is None:
        return {}, _gcloud_headers()
    from google.auth.transport.requests import Request
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file(
        str(_credentials_path()), scopes=["https://www.googleapis.com/auth/cloud-vision"]
    )
    credentials.refresh(Request())
    return {}, {"Authorization": f"Bearer {credentials.token}"}


def _gcloud_headers() -> dict[str, str]:
    """Bearer token from `gcloud auth application-default` plus the quota project header."""
    token = subprocess.run(["gcloud", "auth", "application-default", "print-access-token"],
                           capture_output=True, text=True, timeout=60)
    if token.returncode != 0 or not token.stdout.strip():
        raise RuntimeError(f"gcloud token failed: {token.stderr.strip()[-300:]}")
    headers = {"Authorization": f"Bearer {token.stdout.strip()}"}
    project = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip() or _adc_quota_project() or _gcloud_project()
    if project:
        headers["x-goog-user-project"] = project
    return headers


def _adc_file() -> Path | None:
    candidates = [os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")]
    config = os.getenv("CLOUDSDK_CONFIG", "")
    if config:
        candidates.append(str(Path(config) / "application_default_credentials.json"))
    candidates.append(str(Path.home() / ".config" / "gcloud" / "application_default_credentials.json"))
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return Path(candidate)
    return None


def _adc_quota_project() -> str:
    adc = _adc_file()
    try:
        return json.loads(adc.read_text()).get("quota_project_id", "") if adc else ""
    except (OSError, ValueError):
        return ""


def _gcloud_project() -> str:
    out = subprocess.run(["gcloud", "config", "get-value", "project"], capture_output=True, text=True, timeout=60)
    return out.stdout.strip() if out.returncode == 0 else ""
