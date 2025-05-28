"""INIT module."""
from __future__ import annotations
import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import Platform
from homeassistant.helpers import device_registry as dr
import voluptuous as vol

from .coordinator import FuelPricesCoordinator
from .providers.fuel_prices_provider import FuelPricesProvider
from .const import (
    DEVICE_MANUFACTURER,
    DEVICE_MODEL,
    DOMAIN,
    CONF_UPDATE_INTERVAL,
    SCHEMA_VERSION,
)

logger = logging.getLogger(f"custom_components.{DOMAIN}")

# Configuration.yaml config
CONFIG_SCHEMA = vol.Schema({}, extra=vol.ALLOW_EXTRA)
async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the integration from the config yaml."""
    logger.debug("[__init__][setup] Started")
    return True


# UI config
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up fuel prices sweden entries."""
    logger.debug("[__init__][async_setup_entry] Started with entry Id: %s", entry.entry_id)

    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.entry_id)},
        manufacturer=DEVICE_MANUFACTURER,
        model=DEVICE_MODEL,
        name=entry.data.get("station", {}).get("name")
    )

    logger.debug("[__init__][async_setup_entry] Device with Id: '%s' is setup", entry.entry_id)
    result = await _do_setup(hass=hass, config=entry.data, entry_id=entry.entry_id)
    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR])
    entry.add_update_listener(reload_entry)
    logger.debug("[__init__][async_setup_entry] Completed")
    return result

async def _do_setup(hass, config, entry_id):
    logger.debug("[__init__][_do_setup] Started")

    update_interval = timedelta(minutes=config[CONF_UPDATE_INTERVAL])
    provider = FuelPricesProvider(hass, config)
    coordinator = FuelPricesCoordinator(hass,
                                       provider=provider,
                                       update_interval=update_interval)
    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()
    hass.data.setdefault(
        DOMAIN, {}
        ).setdefault(
            entry_id, {}).setdefault(
                "coordinator", coordinator)

    logger.debug("[__init__][_do_setup] Completed")

    return True

async def reload_entry(hass, entry):
    """Reload."""
    logger.debug("[__init__][reload_entry] Started")
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
    logger.debug("[__init__][reload_entry] Completed")


async def async_unload_entry(hass, entry):
    """Unload entry."""
    logger.debug("[__init__][unload_entry] Started")
    await hass.config_entries.async_forward_entry_unload(entry, Platform.SENSOR)
    logger.debug("[__init__][unload_entry] Completed")
    return True


async def async_migrate_entry(hass, config_entry: ConfigEntry): # pylint: disable=unused-argument
    """Migration."""
    logger.debug("[migrate_entry] Started")
    logger.debug(
        "[migrate_entry] Migrating from version %s to version %s",
        config_entry.version,
        SCHEMA_VERSION,
    )

    return True
