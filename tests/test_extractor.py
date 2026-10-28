from datetime import date
import unittest
from document_room.extractor import extract_facts
from document_room.model import Document, DocumentKind, FactField


class ExtractionTests(unittest.TestCase):
    def test_known_fields_only(self) -> None:
        document = Document("doc-01", "atlas", "ocr/atlas/lease.txt", date(2025, 4, 7), DocumentKind.LEASE,
                            "Tenant: Baker Bakery\nNoisy label: ignored\nAnnual rent EUR: 50000")
        facts = extract_facts(document)
        self.assertEqual([FactField.TENANT, FactField.ANNUAL_RENT_EUR], [fact.field for fact in facts])
        self.assertEqual([1, 3], [fact.line for fact in facts])

    def test_reference_date_is_independent_of_receipt_date(self) -> None:
        document = Document("doc-01", "atlas", "ocr/rent_statement.txt", date(2025, 4, 7), DocumentKind.RENT_STATEMENT,
                            "Reference date: 2025-04-01\nAnnual rent EUR: 96000")
        fact = extract_facts(document)[0]
        self.assertEqual(date(2025, 4, 1), fact.reference_date)
        self.assertEqual(2, fact.line)

    def test_missing_or_invalid_reference_date_stays_unknown(self) -> None:
        for header in ("", "Reference date: invalid\n"):
            with self.subTest(header=header):
                document = Document("doc-01", "atlas", "ocr/lease.txt", date(2025, 4, 7), DocumentKind.LEASE, header + "Annual rent EUR: 50000")
                self.assertIsNone(extract_facts(document)[0].reference_date)
