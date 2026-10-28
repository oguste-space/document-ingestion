"""Build the report without retaining full OCR contents."""
from .model import Document, DocumentRecord, Fact, IngestionReport, ReadFailure, Property, ReportSummary


def create_report(properties: tuple[Property, ...], documents: list[Document], facts: list[Fact], failures: list[ReadFailure]) -> IngestionReport:
    return IngestionReport(
        schema_version=3,
        summary=ReportSummary(len(documents), len(facts), len(failures), len(properties)),
        properties=properties,
        documents=tuple(DocumentRecord(item.document_id, item.property_id, item.path, item.received_at, item.kind) for item in documents),
        facts=tuple(facts),
        read_failures=tuple(failures),
    )
