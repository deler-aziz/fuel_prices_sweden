"""CountiesProvider module."""
import logging
from .html_provider import HtmlProvider
from ..const import DOMAIN

logger = logging.getLogger(f"custom_components.{DOMAIN}")

class CountiesProvider:
    """Counties Provider."""

    COUNTY_SELECT_ID = "county"

    def __init__(self, hass) -> None:
        """Initialize provider."""
        self.hass = hass
        self._html_provider = HtmlProvider(self.hass)

    async def async_get(self) -> list[str]:
        """Get counties."""
        logger.debug("[counties_provider][async_get] Fetching counties")
        html = await self._html_provider.async_get("stationer/")

        if not html:
            logger.warning("[counties_provider][async_get] No HTML content retrieved")
            return []

        return await self._get_counties(html)


    async def _get_counties(self, html) -> list[str]:
        """Extract counties from HTML."""
        select = html.find("select", {"id": self.COUNTY_SELECT_ID})
        if not select:
            logger.warning("[counties_provider][async_get_counties] No select element found with id='%s'", self.COUNTY_SELECT_ID)
            return []

        counties = [
            option.text.strip()
            for option in select.find_all("option")
            if option.text.strip().lower() != "alla län"
        ]

        logger.debug("[counties_provider][async_get_counties] Retrieved %d counties", len(counties))
        return counties
