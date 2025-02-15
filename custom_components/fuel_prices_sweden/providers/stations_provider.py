"""StationsProvider module."""
import logging
from .html_provider import HtmlProvider
from ..const import DEFAULT_FUEL_TYPE, DOMAIN
from bs4 import BeautifulSoup as BS

logger = logging.getLogger(f"custom_components.{DOMAIN}")

class StationsProvider:
    """Stations Provider."""

    STATIONS_TABLE_ID = "price_table"

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
        table = html.find("table", id=self.STATIONS_TABLE_ID)
        if not table:
            logger.warning("[stations_provider][_get_stations] No table found with id='%s'", self.STATIONS_TABLE_ID)
            return []

        stations = []
        for row in table.select("tbody tr.table-row"):
            station_td = row.find("td")
            if not station_td:
                continue

            name_tag = station_td.find("b")
            location_tag = station_td.find("small")
            url_path = row.get("data-href")

            if name_tag and location_tag and url_path:
                stations.append({
                    "name": self._format_station_name(name_tag, location_tag, station_td),
                    "url_path": url_path.replace("/station/", "")
                })

        logger.debug("[stations_provider][_get_stations] Retrieved %d stations", len(stations))
        return stations

    def _format_station_name(self, name_tag, location_tag, station_td) -> str:
        """Format the station name."""
        station_name = name_tag.get_text(strip=True)
        location_name = location_tag.get_text(strip=True)

        station_name = station_name.replace(location_name, "").strip()
        address = station_td.get_text(separator=" ", strip=True)
        address = address.replace(station_name, "").replace(location_name, "").strip()

        return f"{station_name} {location_name} ({address})"

    def _url_safe(self, name: str) -> str:
        """Convert name to a URL-safe format."""
        return name.lower().replace(" ", "-").translate(str.maketrans("äåö", "aao"))

    async def _get_html_for_page(self, county: str, municipality: str, page_index: int) -> BS | None:
        """Retrieve HTML content for a given page index."""
        url = f"stationer/{DEFAULT_FUEL_TYPE}/{self._url_safe(county)}/{self._url_safe(municipality)}/{page_index}"
        return await self._html_provider.async_get(url)
