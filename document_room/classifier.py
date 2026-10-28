"""Document classification using filenames and OCR text."""
from pathlib import PurePosixPath
from .model import DocumentKind


def detect_type(path: str, text: str) -> DocumentKind:
    name = PurePosixPath(path).name.lower()
    sample = text[:500].lower()
    if "rent_statement" in name or "etat locatif" in sample:
        return DocumentKind.RENT_STATEMENT
    if "lease" in name or "bail commercial" in sample:
        return DocumentKind.LEASE
    if "diagnostic" in name or "technical survey" in sample:
        return DocumentKind.TECHNICAL_REPORT
    if "tax" in name or "taxe fonciere" in sample:
        return DocumentKind.TAX_NOTICE
    if "title" in name or "acte de vente" in sample:
        return DocumentKind.TITLE_DEED
    if "invoice" in name or "facture" in sample:
        return DocumentKind.INVOICE
    return DocumentKind.OTHER
