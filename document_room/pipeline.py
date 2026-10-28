"""Import documents, extract facts, resolve citations and build a report."""
from pathlib import Path
from .config import DEFAULT_SETTINGS, IngestSettings
from .extractor import extract_facts
from .manifest import load_manifest
from .model import Document, ExtractedFact, IngestionReport, ReadFailure
from .reader import read_document
from .report import create_report
from .sources import SourceCatalog


def ingest_room(room: Path, settings: IngestSettings = DEFAULT_SETTINGS) -> IngestionReport:
    manifest = load_manifest(room)
    documents: list[Document] = []
    extracted: list[ExtractedFact] = []
    failures: list[ReadFailure] = []
    catalog = SourceCatalog()
    for entry in manifest.documents:
        result = read_document(room, entry, settings)
        if result.failure is not None:
            failures.append(result.failure)
            continue
        assert result.document is not None
        documents.append(result.document)
        catalog.register(result.document)
        extracted.extend(extract_facts(result.document))
    facts = [catalog.resolve(item) for item in extracted]
    return create_report(manifest.properties, documents, facts, failures)
