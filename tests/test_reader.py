"""Unit tests for the sales reader and domain models."""

import pytest
from sales.models import SaleRecord
from sales.reader import read_data


def test_sale_record_creation_and_properties():
    """Verify SaleRecord valid attributes and calculated total_price."""
    record = SaleRecord("tea", "drinks", 7.0, 5)
    assert record.product_name == "tea"
    assert record.category == "drinks"
    assert record.unit_price == 7.0
    assert record.quantity == 5
    assert record.total_price == 35.0


def test_sale_record_validation():
    """Verify SaleRecord invariant validations in post-init."""
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        SaleRecord("", "drinks", 10.0, 1)

    with pytest.raises(ValueError, match="Category cannot be empty"):
        SaleRecord("tea", "   ", 10.0, 1)

    with pytest.raises(ValueError, match="Unit price cannot be negative"):
        SaleRecord("tea", "drinks", -1.0, 1)

    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        SaleRecord("tea", "drinks", 10.0, 0)

    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        SaleRecord("tea", "drinks", 10.0, -5)


def test_read_data_valid(sample_csv_file):
    """Test reading a standard valid CSV file."""
    records = read_data(sample_csv_file)
    assert len(records) == 5
    assert records[0] == SaleRecord("tea", "drinks", 7.0, 5)
    assert records[1].total_price == 37.5
    assert records[4] == SaleRecord("apple", "fruit", 4.0, 6)


def test_read_data_file_not_found():
    """Test that missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_data("non_existent_file_path_xyz.csv")


def test_read_data_empty_file(tmp_path):
    """Test reading an empty file returns an empty list."""
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("", encoding="utf-8")
    records = read_data(empty_file)
    assert records == []


def test_read_data_ignores_invalid_rows(tmp_path):
    """Test that invalid lines are skipped according to specification."""
    content = (
        "tea,drinks,7.0,5\n"
        "\n"  # blank line
        "only_two,fields\n"  # insufficient fields
        "too,many,fields,in,this,row\n"  # too many fields
        "bad_qty,drinks,10.0,five\n"  # non-numeric quantity
        "fractional_qty,drinks,10.0,2.5\n"  # fractional quantity is prohibited
        "bad_price,drinks,not_a_float,2\n"  # non-numeric price
        "negative_price,drinks,-10.0,2\n"  # negative price
        "negative_qty,drinks,10.0,-2\n"  # negative quantity
        " ,drinks,10.0,2\n"  # empty product name
        "coffee,drinks,12.5,3\n"
    )
    test_file = tmp_path / "mixed.csv"
    test_file.write_text(content, encoding="utf-8")

    records = read_data(test_file)
    assert len(records) == 2
    assert records[0].product_name == "tea"
    assert records[1].product_name == "coffee"


def test_read_data_whitespace_stripping(tmp_path):
    """Test that whitespace around comma-separated fields is handled properly."""
    content = "  tea  ,  drinks  ,  7.0  ,  5  \n"
    test_file = tmp_path / "spaces.csv"
    test_file.write_text(content, encoding="utf-8")

    records = read_data(test_file)
    assert len(records) == 1
    assert records[0] == SaleRecord("tea", "drinks", 7.0, 5)
