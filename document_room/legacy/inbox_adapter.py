"""Older email attachment naming policy (not in the current ingestion path)."""
import re

def suggested_filename(subject: str, attachment_name: str) -> str:
    prefix = re.sub(r"[^a-z0-9]+", "-", subject.lower()).strip("-")[:32]
    suffix = attachment_name.replace("/", "_").replace("\\", "_")
    return f"{prefix}--{suffix}" if prefix else suffix
