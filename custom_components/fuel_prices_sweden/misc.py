"""misc module."""
import re

def get_entity_station(name: str) -> str:
    """Get station entity name"""
    return _convert(name)

def get_entity_fuel_type(name: str) -> str:
    """Get fuel type entity name"""
    return _convert(name)

def _convert(name: str) -> str:
    name =_replace_non_letter_digit(name)
    name = _replace_multi_underscore(name)
    name = _replace_swedish_letters(name)
    name = _removesuffix_lower(name)
    return name

def _replace_non_letter_digit(name: str) -> str:
    return re.sub("\\W","_", name)

def _replace_multi_underscore(name: str) -> str:
    return name.replace("___","_").replace("__","_")

def _replace_swedish_letters(name: str) -> str:
    return name.replace("ä", "a").replace("å", "a").replace("ö", "o")

def _removesuffix_lower(name: str) -> str:
    return name.removesuffix("_").lower()
