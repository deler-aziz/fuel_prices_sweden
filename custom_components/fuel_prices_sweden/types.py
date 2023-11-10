"""Types module."""
from __future__ import annotations

from typing import TypedDict

class FuelPrice(TypedDict):
    """FuelPrice type."""

    name: str
    price: float


FuelPriceFetchResult = dict[str, float]
