"""Module providing const data."""
DOMAIN = "fuel_prices_sweden"
SCHEMA_VERSION = 1
VERSION = "1.0.0"
DEVICE_MANUFACTURER = "ha.deler.dev"
DEVICE_MODEL = "HTML Scraping device"

DATA_TZ = "Europe/Stockholm"
DATA_CURRENCY = "Kr"

DATA_BASE_URL = "https://bensinpriser.nu/"

CONF_UPDATE_INTERVAL = "update_interval"
CONF_INTEGRATION_ID = "id"
CONF_COUNTY = "county"
CONF_MUNICIPALITY = "municipality"
CONF_STATION = "station"

PLACEHOLDER_KEY_COUNTY_NAME = "county_name"
PLACEHOLDER_KEY_MUNICIPALITY_NAME = "municipality_name"
DEFAULT_UPDATE_INTERVAL = 60
DEFAULT_FUEL_TYPE = "95"
