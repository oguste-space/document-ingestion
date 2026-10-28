"""Cross-platform command-line entry point."""
import argparse
import sys
from pathlib import Path
from .json_io import dump_json
from .manifest import ManifestError
from .pipeline import ingest_room

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import a document collection")
    commands = parser.add_subparsers(dest="command", required=True)
    ingest = commands.add_parser("ingest", help="Ingest pre-extracted OCR from a room")
    ingest.add_argument("--room", type=Path, required=True, help="Folder with manifest.json")
    ingest.add_argument("--output", type=Path, help="Write report as JSON (optional)")
    return parser

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = ingest_room(args.room)
    except (ManifestError, OSError, ValueError) as exc:
        print(f"Ingestion failed: {exc}", file=sys.stderr)
        return 2
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(dump_json(report, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote JSON report to {args.output}")
    print(dump_json(report.summary, indent=2))
    if report.read_failures:
        print("Files not imported:")
        for failure in report.read_failures[:5]:
            print(f"  {failure.code.value}: {failure.message}")
    return 0
