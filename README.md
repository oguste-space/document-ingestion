# Document Ingestion

Import property documents from OCR text exports and produce a JSON report of extracted information and its documentary sources.

## How it works

A document collection belongs to a real-estate review. The manifest lists the properties and their documents. OCR has already converted scanned pages to text; this service reads those text files, classifies the documents and extracts fields such as tenant, annual rent and surface area.

Each extracted fact includes a source citation: the document ID and the one-based line number in its OCR text. A reviewer uses that citation to check the original wording. A citation identifies where a statement came from; it does not establish that the statement is true.

```text
Manifest + OCR text → documents → extracted facts → source citations → JSON report
```

## Vocabulary

| Term | Meaning |
| --- | --- |
| Property | The real-estate unit being reviewed. `atlas`, `bastille` and `saintmartin` are IDs of three example units; their display names are in the manifest. |
| Document | A piece of the collection: a lease, title deed, survey, rent statement or invoice. |
| Lease | A rental contract (`bail`). |
| Rent statement | A property manager's rent schedule (`état locatif`) describing rent at a given date. |
| Fact | One extracted statement, such as “annual rent: EUR 63,500”. It is not independently verified. |
| Source citation | A document ID and OCR line locating the text behind a fact. Sometimes called evidence or provenance. |
| Reference date | The date for which a statement applies, when explicitly present in the document. This differs from the date the file was received. |

In the example collection, annual rents refer to the identified unit, in EUR per year, excluding VAT and service charges. Statements with different reference dates describe different points in time. Surface measurements may use different definitions and require human interpretation.

## Requirements and installation

Python 3.10 or later. No third-party packages are required.

```sh
git clone https://github.com/oguste-space/document-ingestion.git
cd document-ingestion
python3 --version
```

On Windows, use `py -3` instead of `python3`.

## Usage

```sh
python3 -m document_room ingest --room sample_data/room_01 --output result.json
```

The command prints a summary and writes an indented JSON report to `result.json`. Open that file to inspect the properties, document metadata and extracted facts. Files that could not be read are listed in `read_failures`. Full OCR contents remain in the source files.

Example of a fact in schema version 3:

```json
{
  "property_id": "saintmartin",
  "field": "annual_rent_eur",
  "value": "63500",
  "source": {"document_id": "saintmartin-lease-03", "line": 4},
  "reference_date": "2025-04-01"
}
```

This states that the annual rent of the Saint-Martin unit is reported as EUR 63,500 as of 1 April 2025, citing line 4 of the lease's OCR text.

```sh
python3 -m document_room ingest --help
```

## Development

```sh
python3 -m unittest discover -s tests -v
```

Application interfaces exchange typed dataclass entities defined in `document_room/model.py`. JSON parsing and serialization live in `json_io.py`.

```text
document_room/    Ingestion service and CLI
sample_data/     Example collection and OCR exports
tests/           Unit and integration tests
docs/            Technical documentation
```
