

# 🇸🇪 Fuel Prices Sweden

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]



<p align="center">
  <img src="https://raw.githubusercontent.com/deler-aziz/fuel_prices_sweden/main/images/logo.png">
</p>


The integration provides fuel prices in Sweden by using a web scraper to extract prices from the [Bensinpriser](https://bensinpriser.nu/) website.


## 🚀 Installation
### Using HACS store (recommended)
1. If you don't have it already, install HACS [Check here](https://hacs.xyz/docs/setup/download/)
2. Go into HACS and Add https://github.com/deler-aziz/fuel_prices_sweden as custom repository
3. In HACS search for `Fuel Prices Sweden` Or [![Open your Home Assistant instance and open Fuel Prices Sweden repository inside the HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=deler-aziz&repository=fuel_prices_sweden)
4. Follow the [configuration](#Configuration) section to setup the integration


### Manual
1. Download the latest release from [here](https://github.com/deler-aziz/fuel_prices_sweden/releases)
2. Unzip the release into **custom_components** directory inside your home assistant **config** directory
3. Follow the [configuration](#Configuration) section to setup the integration

## ⚙️ Configuration
### UI (recommended)
1. Go to `Settings->Devices&Services->Integrations` and click on `Add integration`
2. Search for `Fuel Prices Sweden` and follow the configuration wizard

### Using configuration.yaml (Currently not supported)



## ⛽︎ Data source

The integration retrieves data from [Bensinpriser](https://bensinpriser.nu/).

**NOTE: Prices may not always be accurate**.



***
[releases]: https://github.com/deler-aziz/fuel_prices_sweden/releases
[releases-shield]: https://img.shields.io/github/v/release/deler-aziz/fuel_prices_sweden?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/deler-aziz/fuel_prices_sweden?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-deler%20aziz-blue?style=for-the-badge



