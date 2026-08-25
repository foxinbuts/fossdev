"""Sales domain package.

A reusable library for processing sales transaction records,
filtering by threshold, aggregating by product categories,
and generating summary reports.
"""

from sales.models import SaleRecord
from sales.reader import read_data
from sales.calculator import (
    calculate_total,
    filter_by_threshold,
    aggregate_by_categories,
)
from sales.reporter import generate_report

__version__ = "0.1.0"

__all__ = [
    "SaleRecord",
    "read_data",
    "calculate_total",
    "filter_by_threshold",
    "aggregate_by_categories",
    "generate_report",
    "__version__",
]
