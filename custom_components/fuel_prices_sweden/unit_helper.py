"""Validator module."""
# ruff: noqa: F401
import sys
import logging
# pylint: disable=unused-import
from .const import (DOMAIN,
                    DATA_CURRENCY,
                    DATA_STATIONS_NAME,
                    DATA_CIRCLEK_FUEL_TYPES,
                    DATA_INGO_FUEL_TYPES,
                    DATA_OKQ8_FUEL_TYPES,
                    DATA_PREEM_FUEL_TYPES,
                    DATA_SHELL_FUEL_TYPES,
                    DATA_ST1_FUEL_TYPES)
from .misc import get_attribute_station_name

logger = logging.getLogger(f"custom_components.{DOMAIN}")

def get_fuel_type_unit(station_name, fuel_type) -> str:
    """Get fuel type unit."""
    logger.debug("[unit_helper][get_fuel_type_unit] Started")
    this_module = sys.modules[__name__]
    fuel_units = {item["name"]: item["unit"] for item in getattr(this_module, "DATA_"+get_attribute_station_name(station_name)+"_FUEL_TYPES")}
    unit = fuel_units.get(fuel_type, None)
    logger.debug("[unit_helper][get_fuel_type_unit] Completed")
    return None if unit is None else f"{DATA_CURRENCY}/{unit}"

