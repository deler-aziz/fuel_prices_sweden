"""StationsProvider module."""
import logging
from .html_provider import HtmlProvider
from ..const import DEFAULT_FUEL_TYPE, DOMAIN
from bs4 import BeautifulSoup as BS

logger = logging.getLogger(f"custom_components.{DOMAIN}")

class StationsProvider:
    """Stations Provider."""

    STATIONS_LIST_ID = "price_table"

    def __init__(self, hass) -> None:
        """Initialize provider."""
        self.hass = hass
        self._html_provider = HtmlProvider(self.hass)

    async def async_get(self, county: str, municipality: str) -> list[dict]:
        """Get stations."""
        logger.debug("[stations_provider][async_get] Fetching stations")

        if not county or not municipality:
            logger.warning("[stations_provider][async_get] County and/or municipality parameter is empty")
            return []

        stations = []
        page_index = 1

        while True:
            html = await self._get_html_for_page(county, municipality, page_index)
            if not html:
                logger.warning("[stations_provider][async_get] No HTML content for page %d", page_index)
                break

            station_found = await self._get_stations(html)
            if not station_found:
                break  # Stop if no stations found

            stations.extend(station_found)

            # Check if pagination exists and if last page is reached
            pagination = html.find("ul", class_="pagination")
            if not pagination or "disabled" in (pagination.find_all("li")[-1].get("class") or []):
                logger.debug("[stations_provider][async_get] No more pages, exiting loop.")
                break

            page_index += 1

        return stations

    async def _get_stations(self, html) -> list[dict]:
        """Extract stations from HTML."""
        station_list = html.find(id=self.STATIONS_LIST_ID)
        if not station_list:
            logger.warning("[stations_provider][_get_stations] No list found with id='%s'", self.STATIONS_LIST_ID)
            return []

        stations = []
        for row in station_list.find_all("li", class_="cp-row"):
            tap = row.find("a", class_="cp-row-tap")
            info = row.find("div", class_="cp-info")
            if not tap or not info:
                continue

            url_path = tap.get("href")
            title_tag = info.find("div", class_="cp-title")
            addr_tag = info.find("div", class_="cp-addr")

            if title_tag and url_path:
                stations.append({
                    "name": self._format_station_name(title_tag, addr_tag),
                    "url_path": url_path.replace("/station/", "")
                })

        logger.debug("[stations_provider][_get_stations] Retrieved %d stations", len(stations))
        return stations

    def _format_station_name(self, title_tag, addr_tag) -> str:
        """Format the station name."""
        brand_tag = title_tag.find("b")
        commune_tag = title_tag.find("span", class_="cp-commune")

        brand_name = brand_tag.get_text(strip=True) if brand_tag else ""
        commune_name = commune_tag.get_text(strip=True) if commune_tag else ""
        address = addr_tag.get_text(strip=True) if addr_tag else ""

        return f"{brand_name} {commune_name} ({address})"

    def _url_safe(self, name: str) -> str:
        """Convert name to a URL-safe format."""
        return name.lower().replace(" ", "-").translate(str.maketrans("äåö", "aao"))

    async def _get_html_for_page(self, county: str, municipality: str, page_index: int) -> BS | None:
        """Retrieve HTML content for a given page index."""
        url = f"stationer/{DEFAULT_FUEL_TYPE}/{self._url_safe(county)}/{self._url_safe(municipality)}/{page_index}"
        return await self._html_provider.async_get(url)
