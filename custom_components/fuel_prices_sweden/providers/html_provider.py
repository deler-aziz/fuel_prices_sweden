"""HTMLDocProvider module."""
import logging
import requests
from bs4 import BeautifulSoup as BS
from ..const import (DOMAIN, DATA_BASE_URL)

logger = logging.getLogger(f"custom_components.{DOMAIN}")


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
        self._session = requests.Session()
        url = DATA_BASE_URL + path
        logger.debug("[html_doc_provider][async_get] URL: '%s", url)
        result = None
        try:
            result = await self._asyc_get_html_doc(url)
        except Exception as e:
            logger.error(f"[html_doc_provider][async_get] Error getting fuel types: {e}")
        return result

    async def _asyc_get_html_doc(self, url) -> BS:
        response = await self.hass.async_add_executor_job(self._get, url)
        # &nbsp = \xa0 (non-breaking space)
        raw_html = response.text.replace('\xa0',' ').replace("&nbsp;", " ")
        doc = BS(raw_html, "html.parser")
        return doc

    def _get(self, url) -> requests.Response:
        if self._session is None:
            self._session = requests.Session()
        return self._session.get(url=url, timeout=10)
