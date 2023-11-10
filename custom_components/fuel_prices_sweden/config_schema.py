"""Model providing all config schemas."""
import voluptuous as vol
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)
from .const import (
    DATA_STATION_CIRCLE_K,
    DATA_STATION_INGO,
    DATA_STATION_OKQ8,
    DATA_STATION_PREEM,
    DATA_STATION_SHELL,
    DATA_STATION_ST1,
    DATA_STATIONS_NAME,
    DATA_CIRCLEK_FUEL_TYPES,
    DATA_INGO_FUEL_TYPES,
    DATA_OKQ8_FUEL_TYPES,
    DATA_PREEM_FUEL_TYPES,
    DATA_SHELL_FUEL_TYPES,
    DATA_ST1_FUEL_TYPES,
    CONF_STATIONS,
    CONF_FUELTYPES,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
)


def main_config_schema(config: dict = None) -> dict:
    """Get main schema configuration dict."""
    if config is None:
        config = {CONF_UPDATE_INTERVAL: DEFAULT_UPDATE_INTERVAL, CONF_STATIONS: []}
    return {
        vol.Required(
            CONF_UPDATE_INTERVAL, default=config.get(CONF_UPDATE_INTERVAL)
        ): int,
        vol.Required(CONF_STATIONS, default=config.get(CONF_STATIONS)): SelectSelector(
            SelectSelectorConfig(
                options=DATA_STATIONS_NAME,
                multiple=True,
                mode=SelectSelectorMode.DROPDOWN,
            )
        ),
    }


def station_config_schema(step_id, config: dict = None) -> dict:
    """Get station schema configuration dict."""
    options = []
    if config is None:
        config = {CONF_FUELTYPES: []}
    if step_id == DATA_STATION_CIRCLE_K:
        options = DATA_CIRCLEK_FUEL_TYPES
    elif step_id == DATA_STATION_INGO:
        options = DATA_INGO_FUEL_TYPES
    elif step_id == DATA_STATION_OKQ8:
        options = DATA_OKQ8_FUEL_TYPES
    elif step_id == DATA_STATION_PREEM:
        options = DATA_PREEM_FUEL_TYPES
    elif step_id == DATA_STATION_SHELL:
        options = DATA_SHELL_FUEL_TYPES
    elif step_id == DATA_STATION_ST1:
        options = DATA_ST1_FUEL_TYPES
    return {
        vol.Required(
            CONF_FUELTYPES, default=config.get(CONF_FUELTYPES)
        ): SelectSelector(
            SelectSelectorConfig(
                options=options,
                multiple=True,
                mode=SelectSelectorMode.LIST,
            )
        ),
    }
