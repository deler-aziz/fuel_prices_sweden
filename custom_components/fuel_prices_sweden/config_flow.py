"""Module providing integration configuration setup."""
import logging
import uuid
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.exceptions import HomeAssistantError
from .const import (
    DOMAIN,
    SCHEMA_VERSION,
    CONF_FUELTYPES,
    CONF_STATIONS,
    CONF_UPDATE_INTERVAL,
    CONF_INTEGRATION_ID,
    CONF_ENTRY_TITLE,
    CONF_NAME,
    PLACEHOLDER_KEY_STATION_NAME,
)

from .config_schema import main_config_schema, station_config_schema

logger = logging.getLogger(f"custom_components.{DOMAIN}")


async def validate_input_user(data: dict):
    """Validate input [STEP: user]."""
    if data[CONF_UPDATE_INTERVAL] < 60:
        raise InvalidUpdateInterval
    if len(data[CONF_STATIONS]) < 1:
        raise NoStationSelected
    return data


async def validate_input_station(data: dict):
    """Validate input [STEP: user]."""
    if len(data[CONF_FUELTYPES]) < 1:
        raise NoFuelTypSelected
    return data


class FuelPricesSwedenFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Fuel Prices Sweden."""

    VERSION = SCHEMA_VERSION
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}
        self._data = {}
        self._current_station_index = 0
        self._stations = []

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        logger.debug("[config_flow][step_user] Started")
        self._errors = {}
        self._data = {}

        if user_input is None:
            logger.debug("[config_flow][step_user] No user input")
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(main_config_schema(user_input)),
                last_step=False,
            )

        try:
            user_input = await validate_input_user(user_input)
        except InvalidUpdateInterval:
            self._errors[CONF_UPDATE_INTERVAL] = "invalid_update_interval"
            logger.debug("[config_flow][setup_user(validate)] Invalid update interval")
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(main_config_schema(user_input)),
                errors=self._errors,
                last_step=False,
            )
        except NoStationSelected:
            self._errors[CONF_STATIONS] = "no_station_selected"
            logger.debug("[config_flow][setup_user(validate)] No station is selcted")
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(main_config_schema(user_input)),
                errors=self._errors,
                last_step=False,
            )

        integration_id = str(uuid.uuid4())
        await self.async_set_unique_id(integration_id)
        self._data[CONF_INTEGRATION_ID] = integration_id
        self._data[CONF_UPDATE_INTERVAL] = user_input[CONF_UPDATE_INTERVAL]
        self._data[CONF_STATIONS] = [{CONF_NAME: name, CONF_FUELTYPES: []} for name in user_input[CONF_STATIONS]]

        self._stations = user_input[CONF_STATIONS]
        self._current_station_index = 0

        return await self.async_step_station()

    async def async_step_station(self, user_input=None):
        """Station configuration step."""
        logger.debug("[config_flow][step_station] Started")
        self._errors = {}
        last_step = self.check_last_step()
        current_station = self.get_current_station()
        placeholders = {PLACEHOLDER_KEY_STATION_NAME: current_station}

        if user_input is not None:
            try:
                user_input = await validate_input_station(user_input)
            except NoFuelTypSelected:
                self._errors[CONF_FUELTYPES] = "no_fuel_type_selected"
                logger.debug(
                    "[config_flow][setup_station(validate)] No fuel type selected"
                )
                return self.async_show_form(
                    step_id="station",
                    data_schema=vol.Schema(
                        station_config_schema(current_station, user_input)
                    ),
                    errors=self._errors,
                    description_placeholders=placeholders,
                    last_step=last_step,
                )
            self._data[CONF_STATIONS][self.get_station_index(current_station)][
                CONF_FUELTYPES
            ] = user_input.get(CONF_FUELTYPES)

            if not last_step:
                self._current_station_index = self._current_station_index + 1
                return await self.async_step_station()

            entry_result = self.async_create_entry(title=CONF_ENTRY_TITLE, data=self._data)
            logger.debug("[config_flow][step_station] Entry created.")
            return entry_result

        return self.async_show_form(
            step_id="station",
            data_schema=vol.Schema(station_config_schema(current_station, user_input)),
            errors=self._errors,
            description_placeholders=placeholders,
            last_step=last_step,
        )

    def check_last_step(self):
        """Check if the step is last step."""
        return self._current_station_index == len(self._stations) - 1

    def get_current_station(self):
        """Get current station."""
        return self._stations[self._current_station_index]

    def get_station_index(self, station):
        """Get the station index."""
        return [
            index
            for index, st in enumerate(self._data[CONF_STATIONS])
            if st[CONF_NAME] == station
        ][0]


class InvalidUpdateInterval(HomeAssistantError):
    """Error: The update interval is not a valid value."""


class NoStationSelected(HomeAssistantError):
    """Error: No station is seleced."""


class NoFuelTypSelected(HomeAssistantError):
    """Error: No fuel type is seleced."""
