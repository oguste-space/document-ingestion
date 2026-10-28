import unittest
from document_room.model import FactField, IngestionReport
from document_room.pipeline import ingest_room
from tests.helpers import ROOM


class PipelineTests(unittest.TestCase):
    report: IngestionReport

    @classmethod
    def setUpClass(cls) -> None:
        cls.report = ingest_room(ROOM)

    def test_all_documents_are_present(self) -> None:
        self.assertEqual(17, self.report.summary.documents)
        self.assertEqual(3, self.report.summary.properties)

    def test_facts_are_extracted(self) -> None:
        self.assertEqual(19, self.report.summary.facts)
        fields = {fact.field for fact in self.report.facts}
        self.assertIn(FactField.ANNUAL_RENT_EUR, fields)
        self.assertIn(FactField.PARCEL_ID, fields)

    def test_invoice_does_not_produce_facts(self) -> None:
        self.assertFalse(any(fact.source.document_id in {"atlas-invoice-13", "bastille-invoice-14"} for fact in self.report.facts))
