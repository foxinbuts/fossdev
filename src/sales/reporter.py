"""Sales report formatting according to specification."""

from typing import Iterable
from sales.models import SaleRecord
from sales.calculator import aggregate_by_categories, calculate_total


def generate_report(
    records: Iterable[SaleRecord],
    discount: float = 0.0,
) -> str:
    """Generate a multi-line formatted text report.

    Structure::

        Report
        ------
        <category>: <amount>
        ...
        ------
        Total: <grand_total>

    Args:
        records: Collection of SaleRecord items.
        discount: Optional discount percentage applied to total.

    Returns:
        Formatted multi-line report string.
    """
    category_totals = aggregate_by_categories(records)
    grand_total = calculate_total(records, discount=discount)

    lines: list[str] = ["Report", "------"]
    if category_totals:
        for cat, amount in category_totals.items():
            lines.append(f"{cat}: {amount}")
    else:
        lines.append("(no sales data)")

    lines.append("------")
    lines.append(f"Total: {grand_total}")

    return "\n".join(lines)
