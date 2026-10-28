from datetime import date
import unittest
from document_room.config import IngestSettings
from document_room.model import ManifestEntry, ReadFailureCode
from document_room.reader import read_document
from tests.helpers import ROOM


class ReaderTests(unittest.TestCase):
    def test_missing_file_is_nonfatal(self) -> None:
        result = read_document(ROOM, ManifestEntry("missing", "atlas", "ocr/not-here.txt", date(2025, 1, 1)), IngestSettings())
        self.assertIsNone(result.document)
        self.assertIsNotNone(result.failure)
        assert result.failure is not None
        self.assertEqual(ReadFailureCode.READ_ERROR, result.failure.code)
