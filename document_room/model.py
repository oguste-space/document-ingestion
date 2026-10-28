"""Entities exchanged by the document ingestion pipeline."""
from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class DocumentKind(str, Enum):
    LEASE = "lease"
    RENT_STATEMENT = "rent_statement"
    TECHNICAL_REPORT = "technical_report"
    TAX_NOTICE = "tax_notice"
    TITLE_DEED = "title_deed"
    INVOICE = "invoice"
    OTHER = "other"


class FactField(str, Enum):
    TENANT = "tenant"
    LEASE_END = "lease_end"
    ANNUAL_RENT_EUR = "annual_rent_eur"
    SURFACE_SQM = "surface_sqm"
    PARCEL_ID = "parcel_id"


class ReadFailureCode(str, Enum):
    READ_ERROR = "read_error"
    TOO_LARGE = "too_large"


@dataclass(frozen=True)
class Property:
    property_id: str
    name: str


@dataclass(frozen=True)
class ManifestEntry:
    document_id: str
    property_id: str
    path: str
    received_at: date


@dataclass(frozen=True)
class Manifest:
    room_id: str
    properties: tuple[Property, ...]
    documents: tuple[ManifestEntry, ...]


@dataclass(frozen=True)
class Document:
    document_id: str
    property_id: str
    path: str
    received_at: date
    kind: DocumentKind
    text: str = field(repr=False)


@dataclass(frozen=True)
class ExtractedFact:
    property_id: str
    field: FactField
    value: str
    source_reference: str
    line: int
    reference_date: date | None = None


@dataclass(frozen=True)
class SourceCitation:
    document_id: str | None
    line: int


@dataclass(frozen=True)
class Fact:
    property_id: str
    field: FactField
    value: str
    source: SourceCitation
    reference_date: date | None = None


@dataclass(frozen=True)
class ReadFailure:
    code: ReadFailureCode
    message: str
    document_id: str | None = None


@dataclass(frozen=True)
class ReadResult:
    document: Document | None = None
    failure: ReadFailure | None = None

    def __post_init__(self) -> None:
        if (self.document is None) == (self.failure is None):
            raise ValueError("A read must produce either a document or an failure")


@dataclass(frozen=True)
class DocumentRecord:
    document_id: str
    property_id: str
    path: str
    received_at: date
    kind: DocumentKind


@dataclass(frozen=True)
class ReportSummary:
    documents: int
    facts: int
    read_failures: int
    properties: int


@dataclass(frozen=True)
class IngestionReport:
    schema_version: int
    summary: ReportSummary
    properties: tuple[Property, ...]
    documents: tuple[DocumentRecord, ...]
    facts: tuple[Fact, ...]
    read_failures: tuple[ReadFailure, ...]
