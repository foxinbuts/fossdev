"""Unit tests for report generation."""

from sales.reporter import generate_report
from sales.models import SaleRecord


def test_generate_report_standard(sample_records):
    """Test report matches exact specification layout."""
    expected = (
        "Report\n"
        "------\n"
        "drinks: 72.5\n"
        "bakery: 55.6\n"
        "fruit: 24.0\n"
        "------\n"
        "Total: 152.1"
    )
    report = generate_report(sample_records)
    assert report == expected


def test_generate_report_with_discount(sample_records):
    """Test report with 10% discount."""
    expected = (
        "Report\n"
        "------\n"
        "drinks: 72.5\n"
        "bakery: 55.6\n"
        "fruit: 24.0\n"
        "------\n"
        "Total: 136.89"
    )
    report = generate_report(sample_records, discount=10.0)
    assert report == expected


def test_generate_report_empty():
    """Test report with no records."""
    report = generate_report([])
    expected = (
        "Report\n"
        "------\n"
        "(no sales data)\n"
        "------\n"
        "Total: 0.0"
    )
    assert report == expected
