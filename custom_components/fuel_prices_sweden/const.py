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
DATA_STATION_SHELL_URL = "https://www.shell.se/foretagskund/listpriser/listpriser-shell-foretagskort.model.json"
DATA_STATION_ST1 = "St1"
DATA_STATION_ST1_URL = "https://www.shell.se/foretagskund/listpriser/listpriser-shell-foretagskort.model.json"
DATA_STATION_TANKA = "Tanka"
DATA_STATION_TANKA_URL = "https://tanka.se/api/prices/single"
DATA_STATIONS_NAME = sorted(
    [DATA_STATION_CIRCLE_K,
     DATA_STATION_INGO,
     DATA_STATION_OKQ8,
     DATA_STATION_PREEM,
     DATA_STATION_SHELL,
     DATA_STATION_ST1,
     DATA_STATION_TANKA]
)
DATA_CIRCLEK_FUEL_TYPES = [
    { "name": "miles 95", "unit": "l" },
    { "name": "miles 98", "unit": "l" },
    { "name": "miles+ 98", "unit": "l" },
    { "name": "miles diesel", "unit": "l" },
    { "name": "miles+ diesel", "unit": "l" },
    { "name": "HVO100", "unit": "l" },
    { "name": "Fordonsgas", "unit": "kg" },
    { "name": "E85", "unit": "l" }
]
DATA_INGO_FUEL_TYPES = [
    { "name": "Bensin 95", "unit": "l" },
    { "name": "Bensin 98 E5",  "unit": "l" },
    { "name": "Diesel",  "unit": "l" },
    { "name": "Etanol", "unit": "l" }
]
DATA_OKQ8_FUEL_TYPES = [
    { "name": "GoEasy Bensin 95 (E10)", "unit": "l" },
    { "name": "GoEasy Bensin Extra 98 (E5)", "unit": "l" },
    { "name": "GoEasy Diesel (B7)", "unit": "l" },
    { "name": "GoEasy Diesel Extra (B0)", "unit": "l" },
    { "name": "Neste MY Förnybar Diesel (HVO100)", "unit": "l" },
    { "name": "Etanol E85", "unit": "l" },
    { "name": "Biogas Bas Sthlm & Uppsala län", "unit": "kg" },
    { "name": "Biogas Bas Övriga landet", "unit": "kg" },
    { "name": "Biogas 100 Sthlm & Uppsala län", "unit": "kg" },
    { "name": "Biogas 100 Övriga landet", "unit": "kg" },
    { "name": "AdBlue", "unit": "l" },
    { "name": "Snabbladdning 150 kW", "unit": "kWh" },
    { "name": "Snabbladdning 50 kW", "unit": "kWh" },
]
DATA_PREEM_FUEL_TYPES = [
    { "name": "Preem Evolution Bensin 95", "unit": "l" },
    { "name": "Preem Evolution Diesel", "unit": "l" },
    { "name": "HVO100", "unit": "l" },
    { "name": "E85", "unit": "l" }
]
DATA_SHELL_FUEL_TYPES = [
    { "name": "Blyfri 95", "unit": "l" },
    { "name": "Blyfri 98", "unit": "l" },
    { "name": "V-Power", "unit": "l" },
    { "name": "CityDiesel", "unit": "l" },
    { "name": "E85", "unit": "l" },
    { "name": "Biogas", "unit": "kg" },
    { "name": "HVO", "unit": "l" }
]
DATA_ST1_FUEL_TYPES = [
    { "name": "Bensin 95", "unit": "l" },
    { "name": "Diesel RE+r", "unit": "l" },
    { "name": "Diesel", "unit": "l" },
    { "name": "E85", "unit": "l" },
    { "name": "Fordonsgas", "unit": "kg" }
]
DATA_TANKA_FUEL_TYPES = [
    { "name": "95", "unit": "l" },
    { "name": "e85", "unit": "l" },
    { "name": "diesel", "unit": "l" },
    { "name": "hvo100", "unit": "l" }
]
DATA_TZ = "Europe/Stockholm"
DATA_CURRENCY = "kr"

CONF_INTEGRATION_ID = "id"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_STATIONS = "stations"
CONF_NAME = "name"
CONF_FUEL_TYPES = "fuel_types"
CONF_FUEL_TYPE = "fuel_type"
CONF_PRICE = "price"
CONF_UPDATED_AT = "updated_at"
CONF_ENTRY_TITLE = "Fuel Prices"
CONF_IS_MANUAL = "is_manual"

PLACEHOLDER_KEY_STATION_NAME = "station_name"
DEFAULT_UPDATE_INTERVAL = 60
MANUAL_CONFIG_ENTRY_ID = "4428f6a9-fa9b-4282-9fbe-be742eb907f1"
