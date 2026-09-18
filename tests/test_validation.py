import pytest

from backend.config import REQUIRED_TABLES
from backend.services.validation import InputValidationError, UploadedTable, validate_uploads


def make_package():
    return [UploadedTable(name=f"{name}.csv", content=b"column\nvalue\n") for name in REQUIRED_TABLES]


def test_complete_package_is_accepted():
    assert len(validate_uploads(make_package())) == 8


def test_missing_table_is_rejected():
    with pytest.raises(InputValidationError, match="Expected 8 CSV files"):
        validate_uploads(make_package()[:-1])


def test_non_csv_is_rejected():
    package = make_package()
    package[0] = UploadedTable(name="01_LINES.txt", content=b"content")
    with pytest.raises(InputValidationError, match="not a CSV"):
        validate_uploads(package)
