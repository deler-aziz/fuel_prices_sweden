"""Module providing integration configuration setup."""
import logging
import uuid
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.exceptions import HomeAssistantError

from .providers.stations_provider import StationsProvider

from .providers.municipalities_provider import MunicipalitiesProvider
from .providers.counties_provider import CountiesProvider
from .const import (
    CONF_COUNTY,
    CONF_MUNICIPALITY,
    DOMAIN,
    PLACEHOLDER_KEY_MUNICIPALITY_NAME,
    SCHEMA_VERSION,
    CONF_UPDATE_INTERVAL,
    CONF_INTEGRATION_ID,
    CONF_STATION,
    PLACEHOLDER_KEY_COUNTY_NAME
)
from .config_schema import main_config_schema, municipality_config_schema, station_config_schema


logger = logging.getLogger(f"custom_components.{DOMAIN}")

async def validate_input_user(data: dict):
    """Validate input [STEP: user]."""
    if data[CONF_UPDATE_INTERVAL] < 60:
        raise InvalidUpdateInterval
    if data[CONF_COUNTY] == "":
        raise NoCountySelected
    return data

async def validate_input_municipality(data: dict):
    """Validate input [STEP: municipality]."""
    if data[CONF_MUNICIPALITY] == "":
        raise NoMunicipalitySelected
    return data

async def validate_input_station(data: dict):
    """Validate input [STEP: station]."""
    if data[CONF_STATION] == "":
        raise NoStationSelected
    return data

class FuelPricesSwedenFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Fuel Prices Sweden."""

    VERSION = SCHEMA_VERSION
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._data = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        logger.debug("[config_flow][step_user] Started")
        self._data = {}

        counties_provider = CountiesProvider(self.hass)
        counties = await counties_provider.async_get()

        if user_input is None:
            logger.debug("[config_flow][step_user] No user input")
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(main_config_schema(user_input, counties)),
                last_step=False,
            )

        try:
            user_input = await validate_input_user(user_input)
        except InvalidUpdateInterval:
            logger.debug("[config_flow][setup_user(validate)] Invalid update interval")
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(main_config_schema(user_input, counties)),
                errors={"base": "invalid_update_interval"},
                last_step=False,
            )
        except NoCountySelected:
            logger.debug("[config_flow][setup_user(validate)] County is not selected")
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(main_config_schema(user_input, counties)),
                errors={"base": "no_county_selected"},
                last_step=False,
            )

        integration_id = str(uuid.uuid4())
        await self.async_set_unique_id(integration_id)
        self._data.update(user_input)
        self._data[CONF_INTEGRATION_ID] = integration_id

        return await self.async_step_municipality()

    async def async_step_municipality(self, user_input=None):
        """Municipality configuration step."""
        logger.debug("[config_flow][step_municipality] Started")
        placeholders = {
            PLACEHOLDER_KEY_COUNTY_NAME: self._data.get(CONF_COUNTY, "county")
            }

        municipalities_provider = MunicipalitiesProvider(self.hass)
        municipalities = await municipalities_provider.async_get(county=self._data.get(CONF_COUNTY, ""))

        if user_input is None:
            logger.debug("[config_flow][step_municipality] No user input")
            return self.async_show_form(
                step_id="municipality",
                data_schema=vol.Schema(municipality_config_schema(user_input, municipalities)),
                description_placeholders=placeholders,
                last_step=False,
            )

        try:
            user_input = await validate_input_municipality(user_input)
        except NoMunicipalitySelected:
            logger.debug(
                "[config_flow][setup_municipality(validate)] Municipality is not selected"
            )
            return self.async_show_form(
                step_id="municipality",
                data_schema=vol.Schema(municipality_config_schema(user_input, municipalities)),
                errors={"base": "no_municipality_selected"},
                description_placeholders=placeholders,
                last_step=False,
            )

        self._data[CONF_MUNICIPALITY] = user_input.get(CONF_MUNICIPALITY)
        return await self.async_step_station()

    async def async_step_station(self, user_input=None):
        """Station configuration step."""
        logger.debug("[config_flow][step_station] Started")
        placeholders = {
            PLACEHOLDER_KEY_COUNTY_NAME: self._data.get(CONF_COUNTY, "county"),
            PLACEHOLDER_KEY_MUNICIPALITY_NAME: self._data.get(CONF_MUNICIPALITY, "municipality")
            }

        stations_provider = StationsProvider(self.hass)
        stations = await stations_provider.async_get(county=self._data.get(CONF_COUNTY, ""), municipality=self._data.get(CONF_MUNICIPALITY, ""))

        if user_input is None:
            logger.debug("[config_flow][step_station] No user input")
            return self.async_show_form(
                step_id="station",
                data_schema=vol.Schema(station_config_schema(user_input, stations)),
                description_placeholders=placeholders,
                last_step=True,
            )

        try:
            user_input = await validate_input_station(user_input)
        except NoStationSelected:
            logger.debug(
                "[config_flow][step_station(validate)] Station is not selected"
            )
            return self.async_show_form(
                step_id="station",
                data_schema=vol.Schema(station_config_schema(user_input, stations)),
                errors={"base": "no_station_selected"},
                description_placeholders=placeholders,
                last_step=True,
            )

        logger.debug("[config_flow][step_station] Data: %s", self._data)
        filtered_station = next((item for item in stations if item["name"] == user_input.get(CONF_STATION)), None)
        self._data[CONF_STATION] = filtered_station
        logger.debug("[config_flow][step_station] Data: %s", self._data)
        return self.async_create_entry(title=self._data[CONF_STATION]["name"], data=self._data)

class InvalidUpdateInterval(HomeAssistantError):
    """Error: The update interval is not a valid value."""

class NoCountySelected(HomeAssistantError):
    """Error: No county is selected."""

class NoMunicipalitySelected(HomeAssistantError):
    """Error: No municipality is selected."""

class NoStationSelected(HomeAssistantError):
    """Error: No station is selected."""
