"""Extract structured fields and source references from OCR text."""

import re
from dataclasses import dataclass
from datetime import date
from pathlib import PurePosixPath

from .model import Document, DocumentKind, ExtractedFact, FactField


@dataclass(frozen=True)
class FieldAlias:
    label: str
    field: FactField


FIELD_ALIASES = (
    FieldAlias("tenant", FactField.TENANT),
    FieldAlias("lease end", FactField.LEASE_END),
    FieldAlias("annual rent eur", FactField.ANNUAL_RENT_EUR),
    FieldAlias("surface sqm", FactField.SURFACE_SQM),
    FieldAlias("parcel", FactField.PARCEL_ID),
)
KEY_VALUE = re.compile(r"^\s*([A-Za-z ]{3,30})\s*:\s*(.+?)\s*$")
EXTRACTABLE_KINDS = {
    DocumentKind.LEASE,
    DocumentKind.RENT_STATEMENT,
    DocumentKind.TITLE_DEED,
    DocumentKind.TECHNICAL_REPORT,
}


def extract_facts(document: Document) -> list[ExtractedFact]:
    if document.kind not in EXTRACTABLE_KINDS:
        return []
    reference_date: date | None = None
    lines = document.text.splitlines()
    for line in lines:
        if line.startswith("Reference date:"):
            try:
                reference_date = date.fromisoformat(line.partition(":")[2].strip())
            except ValueError:
                reference_date = None
    facts: list[ExtractedFact] = []
    for line_number, line in enumerate(lines, 1):
        match = KEY_VALUE.match(line)
        if not match:
            continue
        raw_key, value = match.groups()
        label = " ".join(raw_key.lower().split())
        alias = next((item for item in FIELD_ALIASES if item.label == label), None)
        if alias is not None and value.strip():
            facts.append(
                ExtractedFact(
                    property_id=document.property_id,
                    field=alias.field,
                    value=value.strip(),
                    source_reference=PurePosixPath(document.path).name,
                    line=line_number,
                    reference_date=reference_date,
                )
            )
    return facts
