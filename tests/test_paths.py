import unittest
from document_room.paths import UnsafeDocumentPath, resolve_ocr_path
from tests.helpers import ROOM

class PathTests(unittest.TestCase):
    def test_nested_path_resolves(self) -> None:
        path = resolve_ocr_path(ROOM, "ocr/atlas/leases/lease_summary.txt")
        self.assertTrue(path.is_file())

    def test_escape_is_rejected(self) -> None:
        with self.assertRaises(UnsafeDocumentPath):
            resolve_ocr_path(ROOM, "ocr/../../secret.txt")
