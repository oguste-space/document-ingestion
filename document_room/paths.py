"""Path handling isolated from manifest parsing."""
from pathlib import Path, PurePosixPath

class UnsafeDocumentPath(ValueError):
    pass

def resolve_ocr_path(room: Path, relative_path: str) -> Path:
    # Archive paths always use forward slashes, regardless of the host OS.
    path = PurePosixPath(relative_path.replace("\\", "/"))
    if path.is_absolute() or not path.parts or ".." in path.parts or path.parts[0] != "ocr":
        raise UnsafeDocumentPath(f"Invalid OCR path: {relative_path}")
    root = room.resolve()
    resolved = root.joinpath(*path.parts).resolve()
    if root not in resolved.parents:
        raise UnsafeDocumentPath(f"Path escaped room: {relative_path}")
    return resolved
