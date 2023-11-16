"""FuelPriceProvider module."""
import logging
import requests
from bs4 import BeautifulSoup as BS, ResultSet

from .const import (
    DOMAIN, CONF_NAME,
    CONF_FUELTYPES,
    DATA_STATION_CIRCLE_K_URL,
    DATA_STATION_INGO_URL,
    DATA_STATION_OKQ8_URL,
    DATA_STATION_PREEM_URL,
    DATA_STATION_SHELL_URL,
    DATA_STATION_ST1_URL)
from .types import FuelPrice, FuelPriceFetchResult
from .misc import get_entity_station, get_entity_fuel_type

logger = logging.getLogger(f"custom_components.{DOMAIN}")


class FuelPriceProvider:
    """FuelPrice Provider."""

    def __init__(self, hass, stations) -> None:
        """Initialize provider."""
        self.hass = hass
        self._stations = stations
        self._session = None

    async def async_fetch(self) -> FuelPriceFetchResult:
        """Fetch fuel prices."""
        logger.debug("[fuel_prices_provider][fetch] Started")
        # Re-set the session for each run
        self._session = requests.Session()


        result: FuelPriceFetchResult = {}

        for station in self._stations:
            prices = await getattr(self, "async_" + get_entity_station(station[CONF_NAME]) + "_prices")(
                station[CONF_FUELTYPES]
            )
            for price in prices:
                result.setdefault(price["name"], price["price"])

        return result

    async def async_circle_k_prices(self, fuel_types) -> list[FuelPrice]:
        """Get Circle K station fuel prices."""
        logger.debug("[fuel_prices_provider][circlek_prices] Started")
        tables = await self._asyc_get_html_tables(DATA_STATION_CIRCLE_K_URL)
        station_entity_name = get_entity_station("Circle K")
        rows = tables[0].find_all("tr")
        return self._extratct_fuel_type_price(rows, fuel_types, station_entity_name, 1, 2)

    async def async_ingo_prices(self, fuel_types) -> list[FuelPrice]:
        """Get Ingo station fuel prices."""
        logger.debug("[fuel_prices_provider][ingo_prices] Started")
        tables = await self._asyc_get_html_tables(DATA_STATION_INGO_URL)
        station_entity_name = get_entity_station("Ingo")
        rows = tables[0].find_all("tr")
        return self._extratct_fuel_type_price(rows, fuel_types, station_entity_name, 1, 2)

    async def async_okq8_prices(self, fuel_types) -> list[FuelPrice]:
        """Get OKQ8 station fuel prices."""
        logger.debug("[fuel_prices_provider][okq8_prices] Started")
        tables = await self._asyc_get_html_tables(DATA_STATION_OKQ8_URL)
        station_entity_name = get_entity_station("OKQ8")
        rows = tables[0].find_all("tr")
        return self._extratct_fuel_type_price(rows, fuel_types, station_entity_name, 0, 1)

    async def async_preem_prices(self, fuel_types) -> list[FuelPrice]:
        """Get Preem station fuel prices."""
        logger.debug("[fuel_prices_provider][preem_prices] Started")
        tables = await self._asyc_get_html_tables(DATA_STATION_PREEM_URL)
        station_entity_name = get_entity_station("Preem")
        rows = tables[0].find_all("tr")
        return self._extratct_fuel_type_price(rows, fuel_types, station_entity_name, 0, 1)

    async def async_shell_prices(self, fuel_types) -> list[FuelPrice]:
        """Get Shell station fuel prices."""
        logger.debug("[fuel_prices_provider][shell_prices] Started")
        tables = await self._asyc_get_html_tables(DATA_STATION_SHELL_URL)
        station_entity_name = get_entity_station("Shell")
        rows = tables[0].find_all("tr")
        return self._extratct_fuel_type_price(rows, fuel_types, station_entity_name, 0, 1)

    async def async_st1_prices(self, fuel_types) -> list[FuelPrice]:
        """Get St1 station fuel prices."""
        logger.debug("[fuel_prices_provider][st1_prices] Started")
        tables = await self._asyc_get_html_tables(DATA_STATION_ST1_URL)
        station_entity_name = get_entity_station("St1")
        rows = tables[1].find_all("tr")
        return self._extratct_fuel_type_price(rows, fuel_types, station_entity_name, 0, 1)

    async def _asyc_get_html_tables(self, url) -> ResultSet:
        response = await self.hass.async_add_executor_job(self._get, url)
        # &nbsp = \xa0 (non-breaking space)
        raw_html = response.text.replace('\xa0',' ').replace("&nbsp;", " ")
        doc = BS(raw_html, "html.parser")
        return doc.find_all("table")

    def _get(self, url) -> requests.Response:
        return self._session.get(url=url, timeout=10)

    def _extratct_fuel_type_price(self, rows,
                                  fuel_types,
                                  station_entity_name,
                                  name_col,
                                  price_col)-> list[FuelPrice]:
        result: list[FuelPrice] = []
        logger.debug("[fuel_prices_provider][_extratct_fuel_type_price] Started")
        for row in rows:
            th = row.find_all("th")
            if th:
                continue
            cells = row.findAll("td")
            fuel_type_name = self._sanitize_fuel_type_name(cells[name_col].text)
            if fuel_type_name in fuel_types:
                result.append(FuelPrice(
                    name=(
                        station_entity_name
                        + "_"
                        + get_entity_fuel_type(self._sanitize_fuel_type_name(cells[name_col].text))
                    ),
                    price=self._sanitize_fuel_type_price(cells[price_col].text)))
        return result

    def _sanitize_fuel_type_name(self, name) -> str:
        name = name.replace("Produktnamn:", "")
        name = name.strip()
        return name

    def _sanitize_fuel_type_price(self, price) -> float:
         # Order of replace functions matters
        price = str(price)
        price = price.replace("Pris:", "")
        price = price.replace("kr / kg", "")
        price = price.replace("kr/kWh", "")
        price = price.replace("kr/l", "")
        price = price.replace("kr", "")
        price = price.replace(",", ".")
        price = price.strip()
        return float(f"{float(price):.2f}")
