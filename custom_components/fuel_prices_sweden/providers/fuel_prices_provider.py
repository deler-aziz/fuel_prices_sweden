"""FuelPricesProvider module."""
import logging
from datetime import datetime
import pytz
from .html_provider import HtmlProvider
from ..const import (DOMAIN, DATA_TZ)
from ..types import FuelPriceFetchResult

logger = logging.getLogger(f"custom_components.{DOMAIN}")
TZ = pytz.timezone(DATA_TZ)

class FuelPricesProvider:
    """FuelPrices Provider."""

    def __init__(self, hass, config) -> None:
        """Initialize provider."""
        self.hass = hass
        self._config = config
        self._html_provider = HtmlProvider(self.hass)

    async def async_fetch(self) -> FuelPriceFetchResult | None:
        """Fetch fuel prices."""
        logger.debug("[fuel_prices_provider][async_fetch] Started")

        url_path = self._config.get("station", {}).get("url_path")
        if not url_path:
            logger.warning("[fuel_prices_provider][async_fetch] No URL path found")
            return None

        html = await self._html_provider.async_get(f"station/{url_path}")

        if not html:
            logger.warning("[fuel_prices_provider][async_get] No HTML content retrieved")
            return None

        prices = await self._get_prices(html)
        updated_at = datetime.now(TZ).strftime("%y/%m/%d %H:%M:%S")
        logger.debug("[fuel_prices_provider][async_fetch] Prices: %s", prices)
        return {
            "name": self._config.get("station", {}).get("name"),
            "fuel_prices": prices,
            "updated_at": updated_at
            }

    async def _get_prices(self, html) -> dict:
        """Extract fuel prices from HTML."""
        fuel_prices = {}
        form_groups = html.find_all("div", class_="form-group")

        for group in form_groups:
            fuel_type_tag = group.find("b")
            if not fuel_type_tag:
                continue

            fuel_type = fuel_type_tag.get_text(strip=True)
            input_fields = group.find_all("input", type="number")
            if len(input_fields) < 2:
                logger.warning("[fuel_prices_provider][_get_prices] Skipping fuel type %s due to missing input fields", fuel_type)
                continue

            kronor = input_fields[0].get("placeholder")
            oren = input_fields[1].get("placeholder")

            try:
                kronor = float(kronor.replace(",", "")) if kronor and kronor.replace(",", "").isdigit() else 0.0
                oren = float(oren) / 100 if oren and oren.isdigit() else 0.0
                total_price = kronor + oren
            except ValueError:
                logger.warning("[fuel_prices_provider][_get_prices] Failed to parse price for fuel type: %s", fuel_type)
                total_price = 0.0

            fuel_prices[fuel_type] = total_price

        return fuel_prices
