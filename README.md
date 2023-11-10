

# 🇸🇪 Fuel Prices Sweden

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]



<p align="center">
  <img src="https://raw.githubusercontent.com/deler-aziz/fuel_prices_sweden/main/images/logo.png">
</p>


The integration is providing fuel prices in Sweden. It is using a web scraper to scrap the stations website and extarct the prices.


## 🚀 Installation
### Using HACS (recommended)
1. If you don't have it already, install HACS [Check here](https://hacs.xyz/docs/setup/download/)
2. Go into HACS and search for `Fuel Prices Sweden`
3. Follow the [configuration](#Configuration) section to setup the integration


### Manual
1. Download the latest release from [here](https://github.com/deler-aziz/fuel_prices_sweden/releases)
2. Unzip the release into **custom_components** directory inside your home assistant **config** directory
3. Follow the [configuration](#Configuration) section to setup the integration

## ⚙️ Configuration
### UI (recommended)
1. Go to `Settings->Devices&Services->Integrations` and click on `Add integration`
2. Search for `Fuel Prices Sweden` and follow the configuration wizard

### Using configuration.yaml
1. Add `fuel_prices_sweden` section into your configuration.yaml. Check the following example

    ```
    fuel_prices_sweden:
      update_interval: 60
      stations:
        - name: St1
          fuel_types:
            - Fordonsgas
            - Diesel
        - name: Circle K
          fuel_types:
            - miles 95
            - miles 98
    ```
2. Make sure you only use the [supported station and fuel types](#Supported-stations-and-fuel-types)
3. Restart your Home Assistant


## ⛽︎ Supported stations and fuel types

- **Circle K**

    <table>
        <tr><td>miles 95</td><td>miles 98</td><td>miles+ 98</td></tr>
        <tr><td>miles diesel</td><td>miles+ diesel</td><td>HVO100</td></tr>
        <tr><td>Fordonsgas</td><td>E85</td><td></td></tr>
    </table>

- Ingo
    <table>
        <tr><td>Bensin 95</td><td>Bensin 98 E5</td></tr>
        <tr><td>Diesel</td><td>Etanol</td></tr>
    </table>

- OKQ8
    <table>
        <tr><td>GoEasy Bensin 95 (E10)</td><td>GoEasy Bensin Extra 98 (E5)</td><td>GoEasy Diesel (B7)</td></tr>
        <tr><td>GoEasy Diesel Extra (B0)</td><td>Neste MY Förnybar Diesel (HVO100)</td><td>Etanol E85</td></tr>
        <tr><td>Biogas Bas Sthlm & Uppsala län</td><td>Biogas Bas Övriga landet</td><td>Biogas 100 Sthlm & Uppsala län</td></tr>
        <tr><td>Biogas 100 Övriga landet</td><td></td><td></td></tr>
    </table>

- Preem
    <table>
        <tr><td>Preem Evolution Bensin 95</td><td>Preem Evolution Diesel</td></tr>
        <tr><td>HVO</td><td>E85</td></tr>
    </table>

- Shell
    <table>
        <tr><td>Blyfri 95</td><td>Blyfri 98</td><td>V-Power</td></tr>
        <tr><td>CityDiesel</td><td>E85</td><td>Biogas</td></tr>
        <tr><td>HVO</td><td></td><td></td></tr>
    </table>

- St1
    <table>
        <tr><td>Bensin 95 RE+</td><td>Bensin 95</td><td>Diesel RE+</td></tr>
        <tr><td>Diesel</td><td>E85</td><td>Fordonsgas</td></tr>
    </table>


## 🙏🏽 Special thanks
- [ludeeus](https://github.com/ludeeus) for [integration_blueprint](https://github.com/ludeeus/integration_blueprint)
- [J-Lindvig](https://github.com/J-Lindvig) for [the idea](https://github.com/J-Lindvig/Fuelprices_DK)

***
[releases]: https://github.com/deler-aziz/fuel_prices_sweden/releases
[releases-shield]: https://img.shields.io/github/v/release/deler-aziz/fuel_prices_sweden?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/deler-aziz/fuel_prices_sweden?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-deler%20aziz-blue?style=for-the-badge



