"""Read text produced by the upstream OCR pipeline."""
from pathlib import Path
from .classifier import detect_type
from .config import IngestSettings
from .model import Document, ManifestEntry, ReadFailure, ReadFailureCode, ReadResult
from .paths import UnsafeDocumentPath, resolve_ocr_path


def read_document(room: Path, entry: ManifestEntry, settings: IngestSettings) -> ReadResult:
    try:
        source = resolve_ocr_path(room, entry.path)
        if source.stat().st_size > settings.max_document_bytes:
            return ReadResult(failure=ReadFailure(ReadFailureCode.TOO_LARGE, "OCR text exceeds size limit", entry.document_id))
        text = source.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError, UnsafeDocumentPath) as exc:
        return ReadResult(failure=ReadFailure(ReadFailureCode.READ_ERROR, str(exc), entry.document_id))
    return ReadResult(document=Document(
        entry.document_id, entry.property_id, entry.path, entry.received_at,
        detect_type(entry.path, text), text,
    ))
