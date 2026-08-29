"""Unit tests for calculation, filtering, and aggregation functions."""

import pytest
from sales.calculator import (
    calculate_total,
    filter_by_threshold,
    aggregate_by_categories,
)
from sales.models import SaleRecord


def test_calculate_total_standard(sample_records):
    """Test grand total without discount: 72.5 + 55.6 + 24.0 = 152.1."""
    total = calculate_total(sample_records)
    assert total == 152.1


def test_calculate_total_with_discount(sample_records):
    """Test grand total with 10% discount: 152.1 * 0.9 = 136.89."""
    total = calculate_total(sample_records, discount=10.0)
    assert total == 136.89


def test_calculate_total_boundary_discounts(sample_records):
    """Test 0% and 100% discount boundaries."""
    assert calculate_total(sample_records, discount=0.0) == 152.1
    assert calculate_total(sample_records, discount=100.0) == 0.0


def test_calculate_total_invalid_discount(sample_records):
    """Test that invalid discount percentages raise ValueError."""
    with pytest.raises(ValueError, match="Discount must be between 0.0 and 100.0%"):
        calculate_total(sample_records, discount=-5.0)

    with pytest.raises(ValueError, match="Discount must be between 0.0 and 100.0%"):
        calculate_total(sample_records, discount=105.0)


def test_calculate_total_empty():
    """Test total for empty list is 0.0."""
    assert calculate_total([]) == 0.0
    assert calculate_total([], discount=20.0) == 0.0


def test_filter_by_threshold(sample_records):
    """Filter records by line item total threshold."""
    # Item totals:
    # tea: 35.0
    # coffee: 37.5
    # croissant: 30.4
    # baguette: 25.2
    # apple: 24.0
    filtered = filter_by_threshold(sample_records, threshold=30.0)
    assert len(filtered) == 3
    assert {r.product_name for r in filtered} == {"tea", "coffee", "croissant"}

    # Exact threshold match
    exact = filter_by_threshold(sample_records, threshold=35.0)
    assert len(exact) == 2
    assert {r.product_name for r in exact} == {"tea", "coffee"}

    # Threshold higher than any record
    assert filter_by_threshold(sample_records, threshold=100.0) == []

    # Threshold 0 includes all records
    assert len(filter_by_threshold(sample_records, threshold=0.0)) == 5


def test_filter_by_threshold_invalid():
    """Test negative threshold raises ValueError."""
    with pytest.raises(ValueError, match="Threshold cannot be negative"):
        filter_by_threshold([], threshold=-1.0)


def test_aggregate_by_categories(sample_records):
    """Test category grouping and sums."""
    categories = aggregate_by_categories(sample_records)
    assert categories == {
        "drinks": 72.5,
        "bakery": 55.6,
        "fruit": 24.0,
    }


def test_aggregate_by_categories_empty():
    """Test empty records return empty dict."""
    assert aggregate_by_categories([]) == {}
