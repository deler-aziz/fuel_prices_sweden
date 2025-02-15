"""Model providing all config schemas."""
import voluptuous as vol
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)
from .const import (
    CONF_STATION,
    CONF_COUNTY,
    CONF_MUNICIPALITY,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL
)

def main_config_schema(config: dict | None, counties: list[str]) -> dict:
    """Get main schema configuration dict."""
    if config is None:
        config = {
            CONF_UPDATE_INTERVAL: DEFAULT_UPDATE_INTERVAL,
            CONF_COUNTY: ""}

    if counties is None:
        counties = []

    return {
        vol.Required(
            CONF_UPDATE_INTERVAL, default=config.get(CONF_UPDATE_INTERVAL)
        ): int,
        vol.Required(CONF_COUNTY, default=config.get(CONF_COUNTY)): SelectSelector(
            SelectSelectorConfig(
                options=counties,
                multiple=False,
                mode=SelectSelectorMode.DROPDOWN,
            )
        )
    }

def municipality_config_schema(config: dict | None, municipalities: list[str]) -> dict:
    """Get municipality schema configuration dict."""
    if config is None:
        config = {CONF_MUNICIPALITY: ""}
    return {
        vol.Required(CONF_MUNICIPALITY, default=config.get(CONF_MUNICIPALITY)): SelectSelector(
            SelectSelectorConfig(
                options=municipalities,
                multiple=False,
                mode=SelectSelectorMode.DROPDOWN,
            )
        )
    }

def station_config_schema(config: dict | None, stations: list[dict]) -> dict:
    """Get station schema configuration dict."""
    if config is None:
        config = {CONF_STATION: {}}
    return {
        vol.Required(CONF_STATION, default=config.get(CONF_STATION)): SelectSelector(
            SelectSelectorConfig(
                options=[item["name"] for item in stations],
                multiple=False,
                mode=SelectSelectorMode.DROPDOWN,
                sort=True
            )
        )
    }

