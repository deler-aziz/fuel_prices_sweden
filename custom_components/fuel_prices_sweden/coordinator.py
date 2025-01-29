"""FuelPricesCoordinator module."""
import logging
from datetime import timedelta, datetime
import pytz

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import DOMAIN, DATA_TZ, CONF_UPDATED_AT
from .fuel_price_provider import FuelPriceProvider

logger = logging.getLogger(f"custom_components.{DOMAIN}")
TZ = pytz.timezone(DATA_TZ)

class FuelPricesCoordinator(DataUpdateCoordinator):
    """FuelPrices coordinator."""

    def __init__(self, hass, provider: FuelPriceProvider, update_interval: timedelta):
        """Initialize coordinator."""
        super().__init__(
            hass,
            logger,
            name=DOMAIN,
            update_interval=update_interval,

        )
        self._provider = provider

    async def _async_update_data(self):
        logger.debug("[coordinator][update_data] Started")
        try:
            data = await self._provider.async_fetch()
            data.setdefault(CONF_UPDATED_AT, datetime.now(TZ).strftime("%y/%m/%d %H:%M:%S"))
            logger.debug("[coordinator][update_data] Data fetch completed")
            return data
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("[coordinator][update_data] Data fetch failed: %s", e)
            return None
