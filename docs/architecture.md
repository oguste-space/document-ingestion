# Architecture

`load_manifest` produces a `Manifest` containing `Property` and `ManifestEntry` entities. The reader produces a `ReadResult`: either a `Document` or a `ReadFailure`.

The extractor emits `ExtractedFact` entities with the text value, reference date and source reference. After importing the collection, `SourceCatalog` resolves references into `SourceCitation` entities. Each resulting `Fact` carries its citation.

The report builder returns an `IngestionReport` with typed metadata and a `ReportSummary`. The CLI serializes the report to JSON without exposing OCR contents.

JSON objects are decoded into boundary entities, validated and converted into domain entities. Collections within the service contain entities rather than untyped records.
