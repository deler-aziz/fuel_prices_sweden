"""Sensor module."""
import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.core import callback, HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import (DOMAIN,
                    DEVICE_MODEL,
                    DEVICE_MANUFACTURER)
from .misc import get_entity_name, get_entity_station

logger = logging.getLogger(f"custom_components.{DOMAIN}")

class FuelPriceEntity(CoordinatorEntity, SensorEntity):
    """Representation of a sensor."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class: SensorStateClass | str | None = SensorStateClass.TOTAL

    def __init__(self, data: dict, coordinator):
        """Initialize."""
        super().__init__(coordinator)

        self._coordinator = coordinator
        self._sensor_name: str = data.get("name", "")
        self._device_id: str = data.get("entry_id", "")
        self._device_name: str = data.get("entry_name", "")

        station_name = get_entity_station(self._device_name)
        fuel_type_name = get_entity_name(self._sensor_name)
        self._sensor_id = f"{station_name}_{fuel_type_name}"
        self.entity_id = f"sensor.{self._sensor_id}"

        self._attr_native_value: float = 0.0
        self._attr_suggested_display_precision = 2

    @property
    def should_poll(self) -> bool:
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    @property
    def unique_id(self) -> str:
        """Return a unique ID for this entity."""
        return self._sensor_id

    @property
    def state_class(self) -> SensorStateClass | str | None:
        """Return a unique ID for this entity."""
        return self._attr_state_class

    @property
    def device_info(self) -> dict:
        """Return device information for Home Assistant."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_name,
            "manufacturer": DEVICE_MANUFACTURER,
            "model": DEVICE_MODEL,
        }

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._sensor_name

    @property
    def icon(self) -> str:
        """Return the icon for the entity."""
        return "mdi:gas-station"

    @property
    def state(self) -> float:
        """Return the state of the sensor (fuel price)."""
        if not self._coordinator.data:
            return 0.0
        return self._coordinator.data.get("fuel_prices", {}).get(self._sensor_name, 0.0)

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement for this sensor."""
        if self._sensor_name.lower() == "fordonsgas":
            return "kr/kg"
        return "kr/l"


    @property
    def extra_state_attributes(self) -> dict:
        """Get extra_state_attributes."""
        attr = {}
        if self._coordinator.data and "updated_at" in self._coordinator.data:
            attr["updated_at"] = self._coordinator.data.get("updated_at")
        return attr

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()



def _get_entities(hass: HomeAssistant, config, entry_id) -> list[FuelPriceEntity] | None:
    """Retrieve fuel price entities."""
    logger.debug("[sensor][_get_entities] Started")

    coordinator = hass.data.get(DOMAIN, {}).get(entry_id, {}).get("coordinator")
    if not coordinator or not coordinator.data:
        logger.error("[sensor][_get_entities] No valid coordinator or data found")
        return None

    station_name = config.get("station", {}).get("name")
    fuel_prices = coordinator.data.get("fuel_prices")

    if not station_name or not fuel_prices:
        logger.error("[sensor][_get_entities] Missing station name or fuel prices in config")
        return None

    return [
        FuelPriceEntity(
            {"entry_id": entry_id, "entry_name": station_name, "name": fuel_type},
            coordinator
        )
        for fuel_type in fuel_prices
    ]


async def async_setup_entry(hass: HomeAssistant,
                            config_entry: ConfigEntry,
                            async_add_entities: AddEntitiesCallback) -> None:
    """Start the setup sensor platform for the ui."""
    logger.debug("[sensor][async_setup_entry] Started")

    config = config_entry.data
    logger.debug("[sensor][async_setup_entry] Config: %s", config)

    entities = _get_entities(hass, config, config_entry.entry_id)
    if entities is None:
        return

    async_add_entities(entities, True)
    logger.debug("[sensor][async_setup_entry] Completed")
