from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Any

import httpx
import pymupdf

from ..adapters import google_vision_document
from .base import OCRProvider, OCRResult

ENDPOINT = "https://vision.googleapis.com/v1/files:annotate"
PAGES_PER_REQUEST = 5  # limit synchronicznego files:annotate
VISION_SCOPE = "https://www.googleapis.com/auth/cloud-vision"
CLOUD_SCOPE = "https://www.googleapis.com/auth/cloud-platform"


class GoogleVisionProvider(OCRProvider):
    """Google Cloud Vision DOCUMENT_TEXT_DETECTION przez REST.

    Uwierzytelnienie, w tej kolejnosci: klucz API (GOOGLE_VISION_API_KEY),
    plik JSON konta uslugi (GOOGLE_VISION_CREDENTIALS, sciezka wzgledna wobec
    katalogu .env), Application Default Credentials (`gcloud auth
    application-default login` albo GOOGLE_APPLICATION_CREDENTIALS) czytane
    przez google-auth, bez programu `gcloud`. Projekt rozliczeniowy dla ADC:
    GOOGLE_CLOUD_PROJECT > quota_project_id z ADC > projekt aktywnej
    konfiguracji gcloud. Darmowe 1000 jednostek/miesiac; PDF idzie paczkami po 5 stron.
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
        if _adc_file() is not None:
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
                if response.is_error:
                    raise RuntimeError(f"HTTP {response.status_code}: {_api_error(response)}")
                batch = (response.json().get("responses") or [{}])[0]
                if batch.get("error"):
                    raise RuntimeError(batch["error"].get("message", "request failed"))
                pages.extend(sorted(batch.get("responses") or [], key=lambda item: (item.get("context") or {}).get("pageNumber", 0)))
        return pages


def _api_error(response: httpx.Response) -> str:
    """Google's own error message (API disabled, quota project, permission) instead of a bare status."""
    try:
        return response.json()["error"]["message"]
    except (ValueError, KeyError, TypeError):
        return response.text[:300]


def _credentials_path() -> Path | None:
    configured = os.getenv("GOOGLE_VISION_CREDENTIALS", "").strip()
    if not configured:
        return None
    path = Path(configured).expanduser()
    if not path.is_absolute():
        from ..config import config_directory

        path = config_directory() / path
    return path


def _auth() -> tuple[dict[str, str], dict[str, str]]:
    """Parametry zapytania i naglowki: klucz API, konto uslugi albo ADC."""
    key = os.getenv("GOOGLE_VISION_API_KEY", "").strip()
    if key:
        return {"key": key}, {}
    path = _credentials_path()
    if path is not None:
        from google.oauth2 import service_account

        credentials = service_account.Credentials.from_service_account_file(str(path), scopes=[VISION_SCOPE])
        _refresh(credentials, f"service account {path.name}")
        return {}, {"Authorization": f"Bearer {credentials.token}"}
    return {}, _adc_headers()


def _adc_headers() -> dict[str, str]:
    """Bearer token from Application Default Credentials plus the quota project header."""
    import google.auth

    credentials, adc_project = google.auth.default(scopes=[CLOUD_SCOPE])
    _refresh(credentials, "gcloud Application Default Credentials (run: gcloud auth application-default login)")
    headers = {"Authorization": f"Bearer {credentials.token}"}
    project = (
        os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
        or getattr(credentials, "quota_project_id", None)
        or adc_project
    )
    if project:
        headers["x-goog-user-project"] = project
    return headers


def _refresh(credentials: Any, source: str) -> None:
    from google.auth.exceptions import GoogleAuthError
    from google.auth.transport.requests import Request

    try:
        credentials.refresh(Request())
    except GoogleAuthError as exc:
        raise RuntimeError(f"{source}: {exc}") from exc


def _adc_file() -> Path | None:
    candidates = [os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")]
    config = os.getenv("CLOUDSDK_CONFIG", "")
    if config:
        candidates.append(str(Path(config) / "application_default_credentials.json"))
    if os.name == "nt" and os.getenv("APPDATA"):
        candidates.append(str(Path(os.environ["APPDATA"]) / "gcloud" / "application_default_credentials.json"))
    candidates.append(str(Path.home() / ".config" / "gcloud" / "application_default_credentials.json"))
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return Path(candidate)
    return None
