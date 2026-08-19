"""Domain entities and value objects for the sales package."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SaleRecord:
    """Represents a validated single sale transaction.

    Attributes:
        product_name: Human-readable name of the item.
        category: Logical grouping category (e.g., 'drinks', 'bakery').
        unit_price: Price per single unit.
        quantity: Integer quantity of items sold.
    """

    product_name: str
    category: str
    unit_price: float
    quantity: int

    def __post_init__(self) -> None:
        """Validate attribute constraints."""
        if not self.product_name or not self.product_name.strip():
            raise ValueError("Product name cannot be empty")
        if not self.category or not self.category.strip():
            raise ValueError("Category cannot be empty")
        if self.unit_price < 0:
            raise ValueError(f"Unit price cannot be negative: {self.unit_price}")
        if self.quantity <= 0:
            raise ValueError(f"Quantity must be a positive integer: {self.quantity}")

    @property
    def total_price(self) -> float:
        """Calculate line item total amount: unit_price * quantity."""
        return round(self.unit_price * self.quantity, 2)
