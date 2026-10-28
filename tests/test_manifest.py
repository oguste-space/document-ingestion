from datetime import date
import tempfile
import unittest
from pathlib import Path
from document_room.json_io import dump_json
from document_room.manifest import ManifestError, load_manifest
from document_room.model import Manifest, ManifestEntry, Property
from tests.helpers import ROOM


class ManifestTests(unittest.TestCase):
    def test_fixture_loads(self) -> None:
        manifest = load_manifest(ROOM)
        self.assertEqual(17, len(manifest.documents))
        self.assertEqual(17, len({entry.document_id for entry in manifest.documents}))
        self.assertEqual(3, len(manifest.properties))

    def test_duplicate_id_is_rejected(self) -> None:
        manifest = Manifest("room", (Property("a", "Local A"),), (
            ManifestEntry("x", "a", "ocr/x.txt", date(2025, 1, 1)),
            ManifestEntry("x", "a", "ocr/y.txt", date(2025, 1, 2)),
        ))
        with tempfile.TemporaryDirectory() as temp:
            room = Path(temp)
            (room / "manifest.json").write_text(dump_json(manifest), encoding="utf-8")
            with self.assertRaises(ManifestError):
                load_manifest(room)

    def test_unknown_property_is_rejected(self) -> None:
        manifest = Manifest("room", (), (ManifestEntry("x", "unknown", "ocr/x.txt", date(2025, 1, 1)),))
        with tempfile.TemporaryDirectory() as temp:
            room = Path(temp)
            (room / "manifest.json").write_text(dump_json(manifest), encoding="utf-8")
            with self.assertRaises(ManifestError):
                load_manifest(room)
