"""FuelPricesCoordinator module."""
import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import DOMAIN
from .providers.fuel_prices_provider import FuelPricesProvider

logger = logging.getLogger(f"custom_components.{DOMAIN}")

class FuelPricesCoordinator(DataUpdateCoordinator):
    """FuelPrices coordinator."""

    def __init__(self, hass, provider: FuelPricesProvider, update_interval: timedelta):
        """Initialize coordinator."""
        super().__init__(
            hass,
            logger,
            name=DOMAIN,
            update_interval=update_interval,

        )
        self._provider = provider

    async def _async_update_data(self):
        logger.debug("[coordinator][_async_update_data] Started")
        try:
            result = await self._provider.async_fetch()
            logger.debug("[coordinator][_async_update_data] Data fetch completed")
            return result
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("[coordinator][_async_update_data] Data fetch failed: %s", e)
            return None
