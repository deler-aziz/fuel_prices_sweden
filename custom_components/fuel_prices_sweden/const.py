"""Module providing const data."""
DOMAIN = "fuel_prices_sweden"
SCHEMA_VERSION = 1
VERSION = "1.0.0"
DEVICE_MANUFACTURER = "ha.deler.dev"
DEVICE_MODEL = "HTML Scraping device"

DATA_STATION_CIRCLE_K = "Circle K"
DATA_STATION_CIRCLE_K_URL = "https://www.circlek.se/drivmedel/drivmedelspriser"
DATA_STATION_INGO = "Ingo"
# pylint: disable=line-too-long
DATA_STATION_INGO_URL = "https://www.ingo.se/v%C3%A5ra-l%C3%A5ga-priser/v%C3%A5ra-l%C3%A5ga-priser/aktuella-listpriser"
DATA_STATION_OKQ8 = "OKQ8"
DATA_STATION_OKQ8_URL = "https://www.okq8.se/pa-stationen/drivmedel/"
DATA_STATION_PREEM = "Preem"
DATA_STATION_PREEM_URL = "https://www.preem.se/privat/drivmedel/drivmedelspriser/"
DATA_STATION_SHELL = "Shell"
DATA_STATION_SHELL_URL = "https://www.shell.se/foretagskund/listpriser/listpriser-shell-foretagskort.html"
DATA_STATION_ST1 = "St1"
DATA_STATION_ST1_URL = "https://www.shell.se/foretagskund/listpriser/listpriser-shell-foretagskort.html"
DATA_STATIONS_NAME = sorted(
    [DATA_STATION_CIRCLE_K,
     DATA_STATION_INGO,
     DATA_STATION_OKQ8,
     DATA_STATION_PREEM,
     DATA_STATION_SHELL,
     DATA_STATION_ST1]
)
DATA_CIRCLEK_FUEL_TYPES = [
    "miles 95",
    "miles 98",
    "miles+ 98",
    "miles diesel",
    "miles+ diesel",
    "HVO100",
    "Fordonsgas",
    "E85",
]
DATA_INGO_FUEL_TYPES = ["Bensin 95", "Bensin 98 E5", "Diesel", "Etanol"]
DATA_OKQ8_FUEL_TYPES = [
    "GoEasy Bensin 95 (E10)",
    "GoEasy Bensin Extra 98 (E5)",
    "GoEasy Diesel (B7)",
    "GoEasy Diesel Extra (B0)",
    "Neste MY Förnybar Diesel (HVO100)",
    "Etanol E85",
    "Biogas Bas Sthlm & Uppsala län",
    "Biogas Bas Övriga landet",
    "Biogas 100 Sthlm & Uppsala län",
    "Biogas 100 Övriga landet"
]
DATA_PREEM_FUEL_TYPES = [ "Preem Evolution Bensin 95", "Preem Evolution Diesel", "HVO", "E85"]
DATA_SHELL_FUEL_TYPES = [ "Blyfri 95", "Blyfri 98", "V-Power", "CityDiesel", "E85", "Biogas", "HVO"]
DATA_ST1_FUEL_TYPES = [ "Bensin 95 RE+", "Bensin 95", "Diesel RE+", "Diesel", "E85", "Fordonsgas"]
DATA_TZ = "Europe/Stockholm"

CONF_INTEGRATION_ID = "id"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_STATIONS = "stations"
CONF_NAME = "name"
CONF_FUELTYPES = "fuel_types"
CONF_FUEL_TYPE = "fuel_type"
CONF_PRICE = "price"
CONF_UPDATED_AT = "updated_at"
CONF_ENTRY_TITLE = "Fuel Price"
CONF_IS_MANUAL = "is_manual"

PLACEHOLDER_KEY_STATION_NAME = "station_name"
DEFAULT_UPDATE_INTERVAL = 60
MANUAL_CONFIG_ENTRY_ID = "4428f6a9-fa9b-4282-9fbe-be742eb907f1"
