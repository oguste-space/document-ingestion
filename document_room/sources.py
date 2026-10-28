"""Resolve extraction references into document citations."""
from dataclasses import dataclass
from pathlib import PurePosixPath
from .model import Document, ExtractedFact, Fact, SourceCitation


@dataclass(frozen=True)
class RegisteredSource:
    reference: str
    document_id: str


class SourceCatalog:
    def __init__(self) -> None:
        self._sources: list[RegisteredSource] = []

    def register(self, document: Document) -> None:
        source = RegisteredSource(PurePosixPath(document.path).name, document.document_id)
        for index, existing in enumerate(self._sources):
            if existing.reference == source.reference:
                self._sources[index] = source
                return
        self._sources.append(source)

    def resolve(self, extracted: ExtractedFact) -> Fact:
        source = next((item for item in self._sources if item.reference == extracted.source_reference), None)
        return Fact(
            property_id=extracted.property_id,
            field=extracted.field,
            value=extracted.value,
            source=SourceCitation(source.document_id if source is not None else None, extracted.line),
            reference_date=extracted.reference_date,
        )
