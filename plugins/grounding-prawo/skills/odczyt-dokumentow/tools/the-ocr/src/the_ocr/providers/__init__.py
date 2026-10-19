from .azure_provider import AzureProvider
from .base import ChainAttempt, OCRProvider, OCRResult
from .datalab_provider import DatalabProvider
from .google_vision_provider import GoogleVisionProvider
from .llamaparse_provider import LlamaParseProvider
from .rapidocr_provider import RapidOCRProvider

#: Older names still used by callers (grounding-prawo, earlier releases).
PROVIDER_ALIASES = {"azure-di": "azure", "azure_di": "azure", "google-vision": "google_vision"}


def canonical_provider_name(name: str) -> str:
    return PROVIDER_ALIASES.get(name.strip(), name.strip())


__all__ = [
    "PROVIDER_ALIASES",
    "canonical_provider_name",
    "AzureProvider",
    "ChainAttempt",
    "DatalabProvider",
    "GoogleVisionProvider",
    "LlamaParseProvider",
    "OCRProvider",
    "OCRResult",
    "RapidOCRProvider",
]
