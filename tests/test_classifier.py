import unittest
from document_room.classifier import detect_type

class ClassificationTests(unittest.TestCase):
    def test_lease_by_text(self) -> None:
        self.assertEqual("lease", detect_type("ocr/scans/x.txt", "Bail commercial\n"))

    def test_other(self) -> None:
        self.assertEqual("other", detect_type("ocr/scans/notes.txt", "Meeting notes"))
