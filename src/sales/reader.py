"""CSV and text data parsing for sales records."""

import logging
from pathlib import Path
from typing import Union

from sales.models import SaleRecord

logger = logging.getLogger(__name__)


def read_data(file_path: Union[str, Path]) -> list[SaleRecord]:
    """Read a UTF-8 encoded text file with sales data and parse valid records.

    Expected line format:
        ``product_name,category,unit_price,quantity``

    Processing rules according to specification:

    - Each valid line must contain exactly 4 comma-separated fields.
    - unit_price must be convertable to float (>= 0).
    - quantity must be an integer (> 0). Fractional quantities (e.g. 5.5) are considered invalid.
    - Malformed lines (wrong field count, type errors, negative values) do not stop processing; they are skipped.
    - Blank lines are ignored.

    Args:
        file_path: Path to the input data file.

    Returns:
        List of valid SaleRecord instances.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Input sales file not found: {path}")

    records: list[SaleRecord] = []

    with path.open(mode="r", encoding="utf-8") as f:
        for line_num, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                continue

            parts = [part.strip() for part in line.split(",")]
            if len(parts) != 4:
                logger.warning(
                    "Skipping line %d: expected 4 fields, got %d ('%s')",
                    line_num,
                    len(parts),
                    line,
                )
                continue

            name, category, price_str, qty_str = parts

            # Quantity must be an integer, not fractional (e.g. reject '5.5' or '5.0')
            try:
                # If qty_str contains a dot, it's fractional -> invalid according to spec
                if "." in qty_str:
                    logger.warning(
                        "Skipping line %d: fractional quantity '%s' is prohibited",
                        line_num,
                        qty_str,
                    )
                    continue
                quantity = int(qty_str)
            except ValueError:
                logger.warning(
                    "Skipping line %d: invalid quantity integer '%s'",
                    line_num,
                    qty_str,
                )
                continue

            try:
                unit_price = float(price_str)
            except ValueError:
                logger.warning(
                    "Skipping line %d: invalid unit price float '%s'",
                    line_num,
                    price_str,
                )
                continue

            try:
                record = SaleRecord(
                    product_name=name,
                    category=category,
                    unit_price=unit_price,
                    quantity=quantity,
                )
                records.append(record)
            except ValueError as err:
                logger.warning("Skipping line %d: %s", line_num, err)
                continue

    return records
