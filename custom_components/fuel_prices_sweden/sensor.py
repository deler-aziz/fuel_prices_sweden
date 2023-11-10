"""Sensor module."""
import logging
import random

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.core import callback, HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import (DOMAIN,
                    CONF_STATIONS,
                    CONF_FUELTYPES,
                    CONF_NAME,
                    CONF_FUEL_TYPE,
                    CONF_UPDATED_AT,
                    CONF_IS_MANUAL,
                    DEVICE_MODEL,
                    DEVICE_MANUFACTURER,
                    MANUAL_CONFIG_ENTRY_ID)
from .misc import get_entity_station, get_entity_fuel_type

logger = logging.getLogger(f"custom_components.{DOMAIN}")

def _get_entities(hass:  HomeAssistant, config, entry_id, is_manual = False):
    logger.debug("[sensor][_get_entities] Started")

    coordinator = hass.data[DOMAIN][entry_id]["coordinator"]
    if coordinator is None:
        logger.error("[sensor][_get_entities] No coordinator found")
        return None

    entities: list(FuelPriceEntity) = []
    for station in config[CONF_STATIONS]:
        for fuel_type in station[CONF_FUELTYPES]:
            entities.append(
                FuelPriceEntity(
                    data={CONF_NAME: station[CONF_NAME],
                          CONF_FUEL_TYPE: fuel_type,
                          CONF_IS_MANUAL: is_manual},
                    coordinator=coordinator,
                )
            )

    return entities


async def async_setup_platform(hass: HomeAssistant,
                               config: ConfigType, # pylint: disable=unused-argument
                               async_add_devices: AddEntitiesCallback,
                               discovery_info: DiscoveryInfoType | None = None) -> None:
    """Start the setup sensor platform for the manual config yaml."""
    logger.debug("[sensor][setup_platform] Started")
    if discovery_info is None:
        logger.error("[sensor][setup_entry] No discovery_info")
        return
    entities = _get_entities(hass, discovery_info, MANUAL_CONFIG_ENTRY_ID, True)
    if entities is None:
        return
    async_add_devices(entities, True)
    logger.debug("[sensor][setup_platform] Completed")


async def async_setup_entry(hass: HomeAssistant,
                            config_entry: ConfigEntry,
                            async_add_entities: AddEntitiesCallback) -> None:
    """Start the setup sensor platform for the ui."""
    config = config_entry.data
    logger.debug("[sensor][setup_entry] Started")
    entities = _get_entities(hass, config, config_entry.entry_id)
    if entities is None:
        return
    async_add_entities(entities, True)
    logger.debug("[sensor][setup_entry] Completed")


class FuelPriceEntity(CoordinatorEntity, SensorEntity):
    """Representation of a sensor."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL

    def __init__(self, data, coordinator):
        """Initialize."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._is_manual = bool(data[CONF_IS_MANUAL])
        self._id = (
            get_entity_station(data[CONF_NAME])
            + "_"
            + get_entity_fuel_type(data[CONF_FUEL_TYPE])
            )
        self.entity_id = "sensor." + self._id
        self._sensor_name = data[CONF_FUEL_TYPE]
        self._attr_native_value = 0
        self._attr_suggested_display_precision = 2
        self._updated_at = None
        self._device_id = get_entity_station(data[CONF_NAME])
        self._device_name = data[CONF_NAME]

    @property
    def should_poll(self):
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    @property
    def unique_id(self):
        """Get unique_id."""
        if self._is_manual:
            return f"{self._id}_{random.randint(1, 100)}"
        return self._id

    @property
    def device_class(self):
        """Get device_class."""
        return self._attr_device_class

    @property
    def state_class(self) -> str:
        """Get state_class."""
        return self._attr_state_class

    @property
    def device_info(self):
        """Get device_info."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_name,
            "manufacturer": DEVICE_MANUFACTURER,
            "model": DEVICE_MODEL
        }

    @property
    def name(self):
        """Get name."""
        if self._is_manual:
            return f"{self._device_name} - {self._sensor_name}"
        return self._sensor_name

    @property
    def icon(self):
        """Get icon."""
        return "mdi:gas-station"

    @property
    def extra_state_attributes(self):
        """Get extra_state_attributes."""
        attr = {}
        attr[CONF_UPDATED_AT] = self._updated_at
        return attr

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensore_from_coordinator_data()
        self.async_write_ha_state()

    def _update_sensore_from_coordinator_data(self):
        data =  self._coordinator.data or []
        self._attr_native_value = data.get(self._id) or 0
        self._updated_at = self._coordinator.updated_at
