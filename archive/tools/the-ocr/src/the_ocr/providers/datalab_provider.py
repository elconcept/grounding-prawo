from __future__ import annotations

import os
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

import httpx

from ..adapters import datalab_document
from .base import OCRProvider, OCRResult


class DatalabProvider(OCRProvider):
    name = "datalab"

    def __init__(self, *, base_url: str | None = None, timeout: float = 1800, poll_interval: float = 2):
        self.base_url = (base_url or os.getenv("DATALAB_API_URL") or "https://www.datalab.to").rstrip("/")
        self.timeout = timeout
        self.poll_interval = poll_interval

    def is_available(self) -> tuple[bool, str]:
        if not self._credential_candidates():
            return False, "no Datalab key set (DATALAB_API_KEY_EU/US or DATALAB_API_KEY)"
        return True, ""

    def recognize(self, path: Path) -> OCRResult:
        available, reason = self.is_available()
        if not available:
            return OCRResult(text="", backend=self.name, error=reason)
        errors: list[str] = []
        for region, api_key, base_url in self._credential_candidates():
            try:
                raw = self._convert(path, api_key, base_url)
                document = datalab_document(raw, path)
                document = replace(document, provider_metadata={**document.provider_metadata, "region": region})
                return OCRResult(text=document.text, backend=self.name, raw=raw, document=document)
            except Exception as exc:
                errors.append(f"{region}: {exc}")
        return OCRResult(text="", backend=self.name, error="Datalab attempts failed: " + "; ".join(errors))

    def _convert(self, path: Path, api_key: str, base_url: str) -> dict[str, Any]:
        headers = {"X-Api-Key": api_key}
        form = {
            "output_format": "json",
            "mode": "accurate",
            "word_bboxes": "true",
            "add_block_ids": "true",
            "extras": "new_block_types",
            "include_markdown_in_chunks": "true",
            "disable_image_extraction": "true",
            "additional_config": '{"keep_pageheader_in_output": true, "keep_pagefooter_in_output": true}',
        }
        deadline = time.monotonic() + self.timeout
        with httpx.Client(timeout=120.0, follow_redirects=True) as client:
            with path.open("rb") as handle:
                response = client.post(
                    f"{base_url}/api/v1/convert",
                    headers=headers,
                    data=form,
                    files={"file": (path.name, handle, _media_type(path))},
                )
            response.raise_for_status()
            submitted = response.json()
            if not submitted.get("success"):
                raise RuntimeError(submitted.get("error") or "request rejected")
            check_url = submitted.get("request_check_url")
            if not check_url:
                raise RuntimeError("response has no request_check_url")
            if not str(check_url).startswith("http"):
                check_url = f"{base_url}/{str(check_url).lstrip('/')}"

            while time.monotonic() < deadline:
                poll = client.get(check_url, headers=headers)
                poll.raise_for_status()
                result = poll.json()
                if result.get("status") == "complete":
                    if not result.get("success"):
                        raise RuntimeError(result.get("error") or "conversion failed")
                    if result.get("result_url"):
                        downloaded = client.get(result["result_url"], headers={})
                        downloaded.raise_for_status()
                        payload = downloaded.json()
                        payload.update({key: value for key, value in result.items() if value is not None})
                        result = payload
                    if not isinstance(result.get("json"), dict):
                        raise RuntimeError("conversion returned no JSON document")
                    return result
                if result.get("status") not in {"processing", "pending"}:
                    raise RuntimeError(result.get("error") or f"unexpected status: {result.get('status')}")
                time.sleep(self.poll_interval)
        raise TimeoutError(f"conversion did not finish within {self.timeout:g}s")

    def _credential_candidates(self) -> list[tuple[str, str, str]]:
        configured = os.environ.get("DATALAB_REGION_ORDER", "eu,us")
        order = [region.strip().lower() for region in configured.split(",")]
        order = [region for region in order if region in {"eu", "us"}] or ["eu", "us"]
        candidates: list[tuple[str, str, str]] = []
        for region in order:
            key = os.environ.get(f"DATALAB_API_KEY_{region.upper()}", "").strip()
            if key:
                url = os.environ.get(f"DATALAB_API_URL_{region.upper()}", "").strip() or self.base_url
                candidates.append((region, key, url.rstrip("/")))
        generic = os.environ.get("DATALAB_API_KEY", "").strip()
        if generic:
            region = os.environ.get("DATALAB_REGION", "default").strip().lower() or "default"
            candidates.append((region, generic, self.base_url))
        return candidates


def _media_type(path: Path) -> str:
    return {
        ".pdf": "application/pdf",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
    }.get(path.suffix.lower(), "application/octet-stream")
