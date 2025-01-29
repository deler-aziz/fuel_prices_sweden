"""FuelPriceProvider module."""
import logging
import requests
import json
import jmespath
from bs4 import BeautifulSoup as BS, ResultSet

from .const import (
    DOMAIN, CONF_NAME,
    CONF_FUEL_TYPES,
    DATA_STATION_CIRCLE_K_URL,
    DATA_STATION_INGO_URL,
    DATA_STATION_OKQ8_URL,
    DATA_STATION_PREEM_URL,
    DATA_STATION_SHELL_URL,
    DATA_STATION_ST1_URL,
    DATA_STATION_TANKA_URL)
from .types import FuelPrice, FuelPriceFetchResult
from .misc import get_entity_station, get_entity_fuel_type
from .unit_helper import get_fuel_type_unit

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
            try:
                prices = await getattr(self, "async_" + get_entity_station(station[CONF_NAME]) + "_prices")(
                station[CONF_FUEL_TYPES]
                )
                for price in prices:
                    result.setdefault(price["name"], {"price": price["price"], "unit": price["unit"]})
            except Exception as e:
                logger.error(f"[fuel_prices_provider][fetch] Error fetching prices for {station[CONF_NAME]}: {e}")
                continue

        return result

    async def async_circle_k_prices(self, fuel_types) -> list[FuelPrice]:
        """Get Circle K station fuel prices."""
        logger.debug("[fuel_prices_provider][circlek_prices] Started")
        tables = await self._async_get_html_tables(DATA_STATION_CIRCLE_K_URL)
        rows = self._get_rows(tables, 0)
        return self._extract_fuel_type_price_html(rows, fuel_types, "Circle K", 1, 2)

    async def async_ingo_prices(self, fuel_types) -> list[FuelPrice]:
        """Get Ingo station fuel prices."""
        logger.debug("[fuel_prices_provider][ingo_prices] Started")
        tables = await self._async_get_html_tables(DATA_STATION_INGO_URL)
        rows = self._get_rows(tables, 0)
        return self._extract_fuel_type_price_html(rows, fuel_types, "Ingo", 1, 2)

    async def async_okq8_prices(self, fuel_types) -> list[FuelPrice]:
        """Get OKQ8 station fuel prices."""
        logger.debug("[fuel_prices_provider][okq8_prices] Started")
        tables = await self._async_get_html_tables(DATA_STATION_OKQ8_URL)
        rows = self._get_rows(tables, 0)
        return self._extract_fuel_type_price_html(rows, fuel_types, "OKQ8", 0, 1)

    async def async_preem_prices(self, fuel_types) -> list[FuelPrice]:
        """Get Preem station fuel prices."""
        logger.debug("[fuel_prices_provider][preem_prices] Started")
        tables = await self._async_get_html_tables(DATA_STATION_PREEM_URL)
        rows = self._get_rows(tables, 0)
        return self._extract_fuel_type_price_html(rows, fuel_types, "Preem", 0, 1)

    async def async_shell_prices(self, fuel_types) -> list[FuelPrice]:
        """Get Shell station fuel prices."""
        logger.debug("[fuel_prices_provider][shell_prices] Started")
        response = await self.hass.async_add_executor_job(self._get, DATA_STATION_SHELL_URL)
        jsonData = json.loads(response.text)
        queryResult = jmespath.search("children[].children[].children[].children[?model.title == 'Shellstationer'].model | [0] | [0]", jsonData)
        table = BS(queryResult['text'], "html.parser")
        rows = table.find_all("tr")
        return self._extract_fuel_type_price_html(rows, fuel_types, "Shell", 0, 1)

    async def async_st1_prices(self, fuel_types) -> list[FuelPrice]:
        """Get St1 station fuel prices."""
        logger.debug("[fuel_prices_provider][st1_prices] Started")
        response = await self.hass.async_add_executor_job(self._get, DATA_STATION_ST1_URL)
        jsonData = json.loads(response.text)
        queryResult = jmespath.search("children[].children[].children[].children[?model.title == 'St1-stationer'].model | [0] | [0]", jsonData)
        table = BS(queryResult['text'], "html.parser")
        rows = table.find_all("tr")
        return self._extract_fuel_type_price_html(rows, fuel_types, "St1", 0, 1)

    async def async_tanka_prices(self, fuel_types) -> list[FuelPrice]:
        """Get Tanka station fuel prices."""
        logger.debug("[fuel_prices_provider][tanka_prices] Started")
        response = await self.hass.async_add_executor_job(self._get, DATA_STATION_TANKA_URL)
        return self._extract_fuel_type_price_json(fuel_types, "Tanka", json.loads(response.text))

    async def _async_get_html_tables(self, url) -> ResultSet:
        response = await self.hass.async_add_executor_job(self._get, url)
        # &nbsp = \xa0 (non-breaking space)
        raw_html = response.text.replace('\xa0',' ').replace("&nbsp;", " ")
        doc = BS(raw_html, "html.parser")
        return doc.find_all("table")

    def _get(self, url) -> requests.Response:
        return self._session.get(url=url, timeout=10)

    def _get_rows(self, tables: ResultSet, tableIndex: int):
        rows = None
        if tables and len(tables) > 0:
            table = tables[tableIndex]
            if table:
                rows = table.find_all("tr") or None
        return rows

    def _extract_fuel_type_price_html(self, rows,
                                  fuel_types,
                                  station_name,
                                  name_col,
                                  price_col)-> list[FuelPrice]:
        result: list[FuelPrice] = []
        logger.debug("[fuel_prices_provider][_extract_fuel_type_price_html] Started")
        station_entity_name = get_entity_station(station_name)

        if rows is None:
            logger.warning(f"[fuel_prices_provider][_extract_fuel_type_price_html] No prices found for {station_name}")
            return self._set_default_prices(fuel_types, station_name)

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
                    price=self._sanitize_fuel_type_price(cells[price_col].text),
                    unit=get_fuel_type_unit(station_name, fuel_type_name)))
        return result

    def _set_default_prices(self, fuel_types, station_name):
        result: list[FuelPrice] = []
        logger.debug("[fuel_prices_provider][_set_default_prices] Started")
        station_entity_name = get_entity_station(station_name)
        for fuel_type_name in fuel_types:
                result.append(FuelPrice(
                    name=(
                        station_entity_name
                        + "_"
                        + get_entity_fuel_type(fuel_type_name)
                    ),
                    price=0,
                    unit=get_fuel_type_unit(station_name, fuel_type_name)))
        return result

    def _extract_fuel_type_price_json(self, fuel_types, station_name, json_data)-> list[FuelPrice]:
        result: list[FuelPrice] = []
        logger.debug("[fuel_prices_provider][_extract_fuel_type_price_json] Started")
        station_entity_name = get_entity_station(station_name)
        for fuel_type in fuel_types:
            result.append(FuelPrice(
                name=(
                    station_entity_name
                    + "_"
                    + get_entity_fuel_type(fuel_type)
                ),
                price=self._sanitize_fuel_type_price(json_data[fuel_type]),
                unit=get_fuel_type_unit(station_name, fuel_type)))
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
