"""On-demand archival of ONE unchanged PDF to a private Cloudflare R2 bucket.

Invoked explicitly by the LLM after reviewing all OCR pages. No watch,
scheduler, automatic ingest, public URL or mutation of the source.
The Markdown transcription goes to Basic Memory; the PDF itself goes only here.
Install with: pip install 'the-ocr[archive]'.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

BUCKET = "legal-pdf-originals"


def _client():
    try:
        import boto3
        from botocore.config import Config
    except ImportError as exc:
        raise RuntimeError("Install archive extra: pip install 'the-ocr[archive]'") from exc

    account = os.environ.get("R2_ACCOUNT_ID")
    endpoint = os.environ.get("R2_S3_ENDPOINT") or (f"https://{account}.r2.cloudflarestorage.com" if account else "")
    access = os.environ.get("R2_ACCESS_KEY_ID")
    secret = os.environ.get("R2_SECRET_ACCESS_KEY")
    if not endpoint.startswith("https://"):
        raise ValueError("R2 requires a configured HTTPS S3 endpoint")
    if not access or not secret:
        raise ValueError("Missing R2 S3 credentials in environment")
    return boto3.client("s3", endpoint_url=endpoint,
                        aws_access_key_id=access, aws_secret_access_key=secret,
                        region_name="auto",
                        config=Config(signature_version="s3v4",
                                      retries={"max_attempts": 3, "mode": "standard"}))


def _check_object(client, bucket: str, key: str, expected_size: int) -> bool:
    from botocore.exceptions import ClientError
    try:
        head = client.head_object(Bucket=bucket, Key=key)
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") in ("404", "NoSuchKey", "NotFound"):
            return False
        raise
    if head.get("ContentLength") != expected_size:
        raise RuntimeError(f"Object exists but has different size: {bucket}/{key}")
    return True


def archive_verified_pdf(source: Path, key: str, bucket: str = BUCKET) -> dict[str, str]:
    """Store the PDF in R2; report success only after an independent HEAD check."""
    source = Path(source)
    if not source.is_file() or source.suffix.lower() != ".pdf":
        raise ValueError("Source must be an existing original PDF")
    if not key or key.startswith("/") or ".." in Path(key).parts or not key.lower().endswith(".pdf"):
        raise ValueError("Object key must be a relative PDF path without traversal")
    size = source.stat().st_size
    if size < 1:
        raise ValueError("Empty PDF")
    from .config import load_env
    load_env()
    client = _client()
    client.head_bucket(Bucket=bucket)  # R2 bucket pre-created privately
    if not _check_object(client, bucket, key, size):
        # This is called explicitly by LLM, never by a background scanner.
        client.upload_file(str(source), bucket, key, ExtraArgs={"ContentType": "application/pdf"})
    if not _check_object(client, bucket, key, size):
        raise RuntimeError("r2: uploaded object not found/size mismatch")
    return {"r2": f"r2://{bucket}/{key}"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Archive one unchanged PDF to private Cloudflare R2")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--key", required=True, help="immutable object key including .pdf")
    parser.add_argument("--bucket", default=BUCKET)
    args = parser.parse_args(argv)
    try:
        result = archive_verified_pdf(args.pdf, args.key, args.bucket)
    except Exception as exc:
        parser.exit(1, f"archive failed (do not mark ingest complete): {exc}\n")
    for service, locator in result.items():
        print(f"{service}: {locator}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
