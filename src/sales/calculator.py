"""Calculations, filtering, and aggregations for sales records."""

from typing import Iterable
from sales.models import SaleRecord


def calculate_total(
    records: Iterable[SaleRecord],
    discount: float = 0.0,
) -> float:
    """Calculate the sum of all sales records with an optional discount.

    Args:
        records: Collection of SaleRecord items.
        discount: Optional percentage discount in range [0.0, 100.0].

    Returns:
        Total price rounded to 2 decimal places.

    Raises:
        ValueError: If discount is outside the valid [0.0, 100.0] range.
    """
    if discount < 0.0 or discount > 100.0:
        raise ValueError(f"Discount must be between 0.0 and 100.0%, got: {discount}")

    subtotal = float(sum(record.total_price for record in records))
    if discount > 0.0:
        discounted = subtotal * (1.0 - (discount / 100.0))
        return round(discounted, 2)

    return round(subtotal, 2)


def filter_by_threshold(
    records: Iterable[SaleRecord],
    threshold: float,
) -> list[SaleRecord]:
    """Filter records whose total amount (unit_price * quantity) is >= threshold.

    Args:
        records: Collection of SaleRecord items.
        threshold: Minimum line item total amount.

    Returns:
        List of matching SaleRecord instances.

    Raises:
        ValueError: If threshold is negative.
    """
    if threshold < 0.0:
        raise ValueError(f"Threshold cannot be negative, got: {threshold}")

    return [record for record in records if record.total_price >= threshold]


def aggregate_by_categories(
    records: Iterable[SaleRecord],
) -> dict[str, float]:
    """Group sales records by product category and calculate category totals.

    Args:
        records: Collection of SaleRecord items.

    Returns:
        Dictionary mapping category names to total sales amount, rounded to 2 decimals.
    """
    totals: dict[str, float] = {}
    for record in records:
        totals[record.category] = totals.get(record.category, 0.0) + record.total_price

    return {cat: round(amt, 2) for cat, amt in totals.items()}
