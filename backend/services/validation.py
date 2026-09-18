"""Validate uploaded network-instance tables before invoking the engine."""

from dataclasses import dataclass

from backend.config import REQUIRED_TABLES, settings


class InputValidationError(ValueError):
    """Raised when the network package cannot be safely scheduled."""


@dataclass(frozen=True)
class UploadedTable:
    name: str
    content: bytes


def validate_uploads(files: list[UploadedTable]) -> dict[str, bytes]:
    if len(files) != len(REQUIRED_TABLES):
        raise InputValidationError(
            f"Expected {len(REQUIRED_TABLES)} CSV files; received {len(files)}."
        )

    matched: dict[str, bytes] = {}
    uploaded_names = [item.name for item in files]

    for item in files:
        if not item.name.lower().endswith(".csv"):
            raise InputValidationError(f"{item.name} is not a CSV file.")
        if not item.content:
            raise InputValidationError(f"{item.name} is empty.")
        if len(item.content) > settings.max_file_size_bytes:
            raise InputValidationError(f"{item.name} exceeds the 25 MB upload limit.")

    for keyword in REQUIRED_TABLES:
        candidates = [
            item for item in files if keyword.casefold() in item.name.casefold()
        ]
        if not candidates:
            raise InputValidationError(
                f"Missing required table {keyword}. Uploaded: {', '.join(uploaded_names)}"
            )
        if len(candidates) > 1:
            raise InputValidationError(f"Multiple files match required table {keyword}.")
        matched[candidates[0].name] = candidates[0].content

    if len(matched) != len(REQUIRED_TABLES):
        raise InputValidationError("Each uploaded file must match one required source table.")

    return matched
