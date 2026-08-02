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
        section = html.find("section", attrs={"aria-labelledby": "current-prices-h2"})
        price_list = section.find("ul") if section else None
        if not price_list:
            logger.warning("[fuel_prices_provider][_get_prices] No current price list found")
            return fuel_prices

        for item in price_list.find_all("li"):
            fuel_type_tag = item.find("span")
            price_tag = item.find("strong")
            if not fuel_type_tag or not price_tag:
                continue

            fuel_type = fuel_type_tag.get_text(strip=True)
            price_text = price_tag.get_text(strip=True).split("kr")[0].strip().replace(",", ".")

            try:
                total_price = float(price_text)
            except ValueError:
                logger.warning("[fuel_prices_provider][_get_prices] Failed to parse price for fuel type: %s", fuel_type)
                total_price = 0.0

            fuel_prices[fuel_type] = total_price

        return fuel_prices
