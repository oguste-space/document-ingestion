"""Manifest loading and structural validation."""
from datetime import date
from pathlib import Path
from .json_io import load_json
from .model import Manifest, ManifestEntry, Property


class ManifestError(ValueError):
    pass


def load_manifest(room: Path) -> Manifest:
    try:
        raw = load_json((room / "manifest.json").read_text(encoding="utf-8"))
        properties = tuple(Property(row.string("property_id"), row.string("name")) for row in raw.objects("properties"))
        documents = tuple(ManifestEntry(
            row.string("document_id"), row.string("property_id"),
            row.string("path"), date.fromisoformat(row.string("received_at")),
        ) for row in raw.objects("documents"))
        manifest = Manifest(raw.string("room_id"), properties, documents)
    except (OSError, UnicodeError, ValueError) as exc:
        raise ManifestError(f"Cannot load manifest: {exc}") from exc
    property_ids = {item.property_id for item in properties}
    if len(property_ids) != len(properties):
        raise ManifestError("Duplicate property id")
    if len({item.document_id for item in documents}) != len(documents):
        raise ManifestError("Duplicate document id")
    if any(item.property_id not in property_ids for item in documents):
        raise ManifestError("Document references an unknown property")
    return manifest
