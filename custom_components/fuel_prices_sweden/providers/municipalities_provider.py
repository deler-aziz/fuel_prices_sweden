"""MunicipalitiesProvider module."""
import logging
from .html_provider import HtmlProvider
from ..const import (DOMAIN, DEFAULT_FUEL_TYPE)

logger = logging.getLogger(f"custom_components.{DOMAIN}")

class MunicipalitiesProvider:
    """Municipalities Provider."""

    COMMUNE_SELECT_ID = "commune"

    def __init__(self, hass) -> None:
        """Initialize provider."""
        self.hass = hass
        self._html_provider = HtmlProvider(self.hass)

    async def async_get(self, county: str) -> list[str]:
        """Get municipalities for a given county."""
        logger.debug("[municipalities_provider][async_get] Fetching municipalities for county='%s'", county)

        if county == "":
            logger.warning("[municipalities_provider][async_get] County paramter was empty")
            return []

        html = await self._html_provider.async_get(f"stationer/{DEFAULT_FUEL_TYPE}/{self._county_url_safe(county)}/")

        if not html:
            logger.warning("[municipalities_provider][async_get] No HTML content retrieved for county='%s'", county)
            return []

        select = html.find("select", {"id": self.COMMUNE_SELECT_ID})
        if not select:
            logger.warning("[municipalities_provider][async_get] No select element found with id='%s'", self.COMMUNE_SELECT_ID)
            return []

        municipalities = [
            option.text.strip()
            for option in select.find_all("option")
            if option.text.strip().lower() not in {"alla kommuner", "välj län först"}
        ]

        logger.debug("[municipalities_provider][async_get] Retrieved %d municipalities for county='%s'", len(municipalities), county)
        return municipalities

    def _county_url_safe(self, county: str) -> str:
        """Convert county name to a URL-safe format."""
        county = county.lower().replace(" ", "-")
        translation_table = str.maketrans("äåö", "aao")
        return county.translate(translation_table)
