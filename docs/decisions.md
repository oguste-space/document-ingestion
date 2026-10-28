# Implementation notes

- OCR is performed upstream. The local extractor reads explicitly labelled fields.
- A property represents the unit identified in the manifest. Its ID is independent of its display name.
- Dates of receipt and dates of reference have different meanings. An absent or invalid reference date remains unknown.
- Document text is retained during processing and excluded from the report.
- Unreadable files are reported individually so ingestion can continue.
- Paths use forward slashes and must remain inside the collection directory.
- Domain entities are immutable dataclasses. The catalog maintains a collection of registered sources for the in-memory batch.
- JSON schema version 3 uses `properties`, `facts`, nested `source` citations and `read_failures`.
