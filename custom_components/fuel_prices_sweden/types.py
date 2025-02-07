"""Types module."""
from __future__ import annotations

from typing import TypedDict


class FuelPriceFetchResult(TypedDict):
    """FuelPriceFetchResult type."""

    name: str
    fuel_prices: dict
    updated_at: str
