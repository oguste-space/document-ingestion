from datetime import date
import unittest
from document_room.json_io import dump_json, load_json
from document_room.model import Fact, FactField, SourceCitation


class JsonTests(unittest.TestCase):
    def test_nested_entity_preserves_dates_enums_and_unicode(self) -> None:
        fact = Fact("atlas", FactField.TENANT, 'Société "Lumière"\nParis', SourceCitation(None, 4), date(2025, 4, 1))
        compact = load_json(dump_json(fact))
        loaded = load_json(dump_json(fact, indent=2))
        self.assertEqual(compact, loaded)
        self.assertEqual(fact.value, loaded.string("value"))
        self.assertEqual("tenant", loaded.string("field"))
        self.assertEqual("2025-04-01", loaded.string("reference_date"))
        self.assertIsNone(loaded.child("source").get("document_id"))
        self.assertEqual(4, loaded.child("source").get("line"))

    def test_duplicate_members_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            load_json('{"room_id":"a", "room_id":"b"}')

    def test_invalid_structure_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            load_json('[]')
        with self.assertRaises(ValueError):
            load_json('{"documents":[1]}').objects("documents")
        with self.assertRaises(ValueError):
            load_json('{"room_id":null}').string("room_id")
