"""Validator module."""
# ruff: noqa: F401
import sys
import logging
# pylint: disable=unused-import
from .const import (DOMAIN,
                    DEFAULT_UPDATE_INTERVAL,
                    CONF_NAME,
                    CONF_UPDATE_INTERVAL,
                    CONF_STATIONS,
                    CONF_FUELTYPES,
                    DATA_STATIONS_NAME,
                    DATA_CIRCLEK_FUEL_TYPES,
                    DATA_INGO_FUEL_TYPES,
                    DATA_OKQ8_FUEL_TYPES,
                    DATA_PREEM_FUEL_TYPES,
                    DATA_SHELL_FUEL_TYPES,
                    DATA_ST1_FUEL_TYPES,
                    DATA_TANKA_FUEL_TYPES)
from .misc import get_attribute_station_name

logger = logging.getLogger(f"custom_components.{DOMAIN}")

def validate_config(config: dict) -> bool:
    """Validate config."""
    logger.debug("[validator][validate_config] Started")
    this_module = sys.modules[__name__]
    if config is None:
        return False

    update_interval = config.get(CONF_UPDATE_INTERVAL) or 0
    if update_interval < DEFAULT_UPDATE_INTERVAL:
        logger.error("[validator][validate_config] Invalid update_interval")
        return False

    stations:list(dict) = config.get(CONF_STATIONS)
    if stations is None:
        logger.error("[validator][validate_config] Invalid stations. At least one station is required")
        return False

    for station in stations:
        if station.get(CONF_NAME) not in DATA_STATIONS_NAME:
            logger.error("[validator][validate_config] Invalid station name: %s. Supported stations: %s" ,
                         station.get(CONF_NAME),
                         DATA_STATIONS_NAME)
            return False
        station_name:str = get_attribute_station_name(station.get(CONF_NAME))
        fuel_types = station.get(CONF_FUELTYPES)
        if fuel_types is None:
            logger.error("[validator][validate_config] Invalid fuel_types for station: %s" ,
                          station.get(CONF_NAME))
            return False

        for fuel_type in fuel_types:
            supported_fuel_types = [item["name"] for item in getattr(this_module, "DATA_"+station_name+"_FUEL_TYPES")]
            if fuel_type not in  supported_fuel_types:
                logger.error("[validator][validate_config] Invalid fuel_types for station: %s. Supported fuel types: %s"
                             , station.get(CONF_NAME),
                             supported_fuel_types)
                return False

    logger.debug("[validator][validate_config] Completed")
    return True
