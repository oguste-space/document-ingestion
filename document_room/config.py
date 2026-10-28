"""Ingestion configuration."""
from dataclasses import dataclass


@dataclass(frozen=True)
class IngestSettings:
    max_document_bytes: int = 512_000


DEFAULT_SETTINGS = IngestSettings()
