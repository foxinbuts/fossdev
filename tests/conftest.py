"""Pytest fixtures and test data setup."""

import pytest
from sales.models import SaleRecord


@pytest.fixture
def sample_records() -> list[SaleRecord]:
    """Provide a standard list of valid sale records matching specification example."""
    return [
        SaleRecord(product_name="tea", category="drinks", unit_price=7.0, quantity=5),
        SaleRecord(product_name="coffee", category="drinks", unit_price=12.5, quantity=3),
        SaleRecord(product_name="croissant", category="bakery", unit_price=15.2, quantity=2),
        SaleRecord(product_name="baguette", category="bakery", unit_price=25.2, quantity=1),
        SaleRecord(product_name="apple", category="fruit", unit_price=4.0, quantity=6),
    ]


@pytest.fixture
def sample_csv_file(tmp_path) -> str:
    """Create a temporary valid sales CSV file."""
    csv_file = tmp_path / "valid_sales.csv"
    csv_file.write_text(
        "tea,drinks,7.0,5\n"
        "coffee,drinks,12.5,3\n"
        "croissant,bakery,15.2,2\n"
        "baguette,bakery,25.2,1\n"
        "apple,fruit,4.0,6\n",
        encoding="utf-8",
    )
    return str(csv_file)
