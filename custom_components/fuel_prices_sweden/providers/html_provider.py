"""HTMLDocProvider module."""
import logging
import requests
from bs4 import BeautifulSoup as BS
from ..const import (DOMAIN, DATA_BASE_URL)

logger = logging.getLogger(f"custom_components.{DOMAIN}")

# bensinpriser.nu serves a different page to clients that identify as
# python-requests, so send headers that look like a regular browser.
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "sv-SE,sv;q=0.9,en;q=0.8",
}


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
        self._session.headers.update(REQUEST_HEADERS)
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
            self._session = requests.Session()
            self._session.headers.update(REQUEST_HEADERS)
        return self._session.get(url=url, timeout=10)
