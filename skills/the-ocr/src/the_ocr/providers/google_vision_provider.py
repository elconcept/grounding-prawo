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

from ..adapters import polygon_document
from .base import OCRProvider, OCRResult

ENDPOINT = "https://vision.googleapis.com/v1/images:annotate"
BREAKS = {"SPACE": " ", "SURE_SPACE": " ", "EOL_SURE_SPACE": "\n", "LINE_BREAK": "\n", "HYPHEN": "-\n"}


class GoogleVisionProvider(OCRProvider):
    """Google Cloud Vision DOCUMENT_TEXT_DETECTION over REST (free tier: 1000 units/month).

    Every PDF page is rendered (GOOGLE_VISION_DPI, default 200) and sent as an image, a few per
    request. Auth: GOOGLE_VISION_API_KEY, otherwise an access token from Application Default
    Credentials (`gcloud auth application-default print-access-token`); the quota project comes
    from GOOGLE_CLOUD_PROJECT, the ADC file or `gcloud config get-value project`.
    """

    name = "google-vision"
    per_request = 4

    def is_available(self) -> tuple[bool, str]:
        if os.getenv("GOOGLE_VISION_API_KEY"):
            return True, ""
        if shutil.which("gcloud") and _adc_file():
            return True, ""
        return False, "no GOOGLE_VISION_API_KEY and no gcloud Application Default Credentials"

    def recognize(self, path: Path) -> OCRResult:
        available, reason = self.is_available()
        if not available:
            return OCRResult(text="", backend=self.name, error=reason)
        try:
            dpi = int(os.getenv("GOOGLE_VISION_DPI", "200"))
            images = _render_pages(path, dpi)
            headers, params = self._auth()
            responses: list[dict[str, Any]] = []
            with httpx.Client(timeout=180.0) as client:
                for start in range(0, len(images), self.per_request):
                    batch = images[start:start + self.per_request]
                    body = {"requests": [
                        {
                            "image": {"content": base64.b64encode(png).decode()},
                            "features": [{"type": "DOCUMENT_TEXT_DETECTION"}],
                            "imageContext": {"languageHints": ["pl", "en"]},
                        }
                        for png, _, _ in batch
                    ]}
                    response = client.post(ENDPOINT, headers=headers, params=params, json=body)
                    response.raise_for_status()
                    for item in response.json().get("responses", []):
                        if item.get("error"):
                            raise RuntimeError(json.dumps(item["error"], ensure_ascii=False))
                        responses.append(item)
            pages = [_vision_page(item, width, height) for item, (_, width, height) in zip(responses, images)]
            document = polygon_document(pages, path, provider=self.name, metadata={"dpi": dpi})
            return OCRResult(text=document.text, backend=self.name, raw={"responses": responses}, document=document)
        except Exception as exc:
            return OCRResult(text="", backend=self.name, error=f"Google Vision failed: {exc}")

    def _auth(self) -> tuple[dict[str, str], dict[str, str]]:
        key = os.getenv("GOOGLE_VISION_API_KEY", "").strip()
        if key:
            return {}, {"key": key}
        token = subprocess.run(["gcloud", "auth", "application-default", "print-access-token"],
                               capture_output=True, text=True, timeout=60)
        if token.returncode != 0 or not token.stdout.strip():
            raise RuntimeError(f"gcloud token failed: {token.stderr.strip()[-300:]}")
        headers = {"Authorization": f"Bearer {token.stdout.strip()}"}
        project = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip() or _adc_quota_project() or _gcloud_project()
        if project:
            headers["x-goog-user-project"] = project
        return headers, {}


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


def _render_pages(path: Path, dpi: int) -> list[tuple[bytes, float, float]]:
    out = []
    with pymupdf.open(path) as document:
        for page in document:
            pix = page.get_pixmap(dpi=dpi)
            out.append((pix.tobytes("png"), float(pix.width), float(pix.height)))
    return out


def _vision_page(item: dict[str, Any], width: float, height: float) -> dict[str, Any]:
    """Vision blocks (pixel vertices) -> neutral page for polygon_document; one line per paragraph."""
    lines = []
    for page in (item.get("fullTextAnnotation") or {}).get("pages") or []:
        for block in page.get("blocks") or []:
            for paragraph in block.get("paragraphs") or []:
                words, text = [], ""
                for word in paragraph.get("words") or []:
                    word_text = "".join(symbol.get("text", "") for symbol in word.get("symbols") or [])
                    last = (word.get("symbols") or [{}])[-1]
                    brk = ((last.get("property") or {}).get("detectedBreak") or {}).get("type", "")
                    text += word_text + BREAKS.get(brk, "")
                    words.append({"text": word_text, "polygon": _vertices(word), "confidence": word.get("confidence")})
                lines.append({"text": text.strip(), "polygon": _vertices(paragraph), "words": words})
    return {"width": width, "height": height, "lines": lines}


def _vertices(item: dict[str, Any]) -> list[float]:
    flat: list[float] = []
    for vertex in (item.get("boundingBox") or {}).get("vertices") or []:
        flat += [float(vertex.get("x", 0)), float(vertex.get("y", 0))]
    return flat
