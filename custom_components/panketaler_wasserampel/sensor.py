"""Sensor platform for Panketaler Wasserampel integration."""
import logging
import asyncio
import aiohttp
import async_timeout
import voluptuous as vol
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import CONF_NAME
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# URL der Panketaler Wasserampel
URL = "https://www.panketalerwasserampel.de/"

# Scanintervall in Sekunden
SCAN_INTERVAL = timedelta(minutes=30)

# Mögliche Farben der Wasserampel
COLORS = {
    "GRÜN": "green",
    "GELB": "yellow",
    "ROT": "red",
}

# Zuordnung der Farben zu numerischen Werten
COLOR_VALUES = {
    "green": 1,
    "yellow": 2,
    "red": 3,
}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform from YAML configuration."""
    name = config.get(CONF_NAME, "Panketaler Wasserampel")
    
    coordinator = PanketalerWasserampelCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    
    async_add_entities([PanketalerWasserampelSensor(coordinator, name)], True)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up Panketaler Wasserampel sensor based on a config entry."""
    # Verwende den konfigurierten Namen oder Standard
    name = entry.data.get(CONF_NAME, "Panketaler Wasserampel")
    
    coordinator = PanketalerWasserampelCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    
    async_add_entities([PanketalerWasserampelSensor(coordinator, name)], True)


class PanketalerWasserampelCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, h
