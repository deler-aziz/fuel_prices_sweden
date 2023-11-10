"""Types module."""
from __future__ import annotations

from typing import TypedDict, Dict

class FuelPrice(TypedDict):
    """FuelPrice type."""

    name: str
    price: float


FuelPriceFetchResult = Dict[str, float]
