"""HTMLDocProvider module."""
import logging
import requests
from bs4 import BeautifulSoup as BS
from homeassistant.const import __version__ as HA_VERSION
from ..const import (DOMAIN, DATA_BASE_URL)

logger = logging.getLogger(f"custom_components.{DOMAIN}")

# bensinpriser.nu is behind Cloudflare, which blocks requests sent with generic
# library User-Agents such as python-requests. Identify the integration instead.
USER_AGENT = (
    f"HomeAssistant/{HA_VERSION} {DOMAIN} "
    "(+https://github.com/deler-aziz/fuel_prices_sweden)"
)


class HtmlProvider:
    """HTMLDoc Provider."""

    def __init__(self, hass) -> None:
        """Initialize provider."""
        self.hass = hass
        self._session = None

    async def async_get(self, path: str = "") -> BS | None:
        """Get html doc."""
        logger.debug("[html_doc_provider][async_get] Started")
        # Re-set the session for each run
        self._session = self._create_session()
        url = DATA_BASE_URL + path
        logger.debug("[html_doc_provider][async_get] URL: '%s", url)
        result = None
        try:
            result = await self._asyc_get_html_doc(url)
        except Exception as e:
            logger.error(f"[html_doc_provider][async_get] Error getting fuel types: {e}")
        return result

    async def _asyc_get_html_doc(self, url) -> BS | None:
        response = await self.hass.async_add_executor_job(self._get, url)
        if response.status_code != 200:
            logger.warning(
                "[html_doc_provider][async_get] HTTP %s from %s: %s",
                response.status_code,
                url,
                response.text[:300].replace("\n", " "),
            )
            return None
        # Replace non-breaking spaces (\xa0 and the HTML entity) with plain spaces
        raw_html = response.text.replace('\xa0',' ').replace("&nbsp;", " ")
        doc = BS(raw_html, "html.parser")
        return doc

    def _get(self, url) -> requests.Response:
        if self._session is None:
            self._session = self._create_session()
        return self._session.get(url=url, timeout=10)

    @staticmethod
    def _create_session() -> requests.Session:
        session = requests.Session()
        session.headers["User-Agent"] = USER_AGENT
        return session
