import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from document_room.json_io import load_json
from tests.helpers import ROOM


class CliTests(unittest.TestCase):
    def test_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "summary.json"
            result = subprocess.run(
                [sys.executable, "-m", "document_room", "ingest", "--room", str(ROOM), "--output", str(output)],
                capture_output=True, text=True, timeout=20,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            text = output.read_text(encoding="utf-8")
            self.assertIn('\n  "facts": [\n', text)
            report = load_json(text)
            self.assertEqual(3, report.get("schema_version"))
            self.assertEqual(17, report.child("summary").get("documents"))
            self.assertEqual(19, len(report.objects("facts")))
            self.assertFalse(any(member.name == "text" for member in report.objects("documents")[0].members))
