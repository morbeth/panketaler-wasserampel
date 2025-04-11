"""Sensor platform for Panketaler Wasserampel integration."""
import logging
import asyncio
from datetime import timedelta
import aiohttp
from bs4 import BeautifulSoup
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_NAME, DEFAULT_URL, CONF_URL

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_URL, default=DEFAULT_URL): cv.string,
})

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Panketaler Wasserampel sensor platform."""
    name = config.get(CONF_NAME)
    url = config.get(CONF_URL)

    coordinator = PanketalerDataCoordinator(hass, url)
    await coordinator.async_refresh()

    async_add_entities([
        PanketalerWasserampelSensor(coordinator, name),
        PanketalerWasserampelNumerischSensor(coordinator, name + " Numerisch")
    ])

class PanketalerDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Panketaler Wasserampel data."""

    def __init__(self, hass, url):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.url = url
        self.data = {"status": "Unbekannt", "numeric_status": 0}

    async def _async_update_data(self):
        """Update data."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Website responded with status {response.status}")
                    html = await response.text()

            soup = BeautifulSoup(html, 'html.parser')
            
            # Versuche verschiedene Selektoren, die auf der Webseite funktionieren könnten
            selectors_to_try = [
                ".post-content strong span",        # Original-Selektor
                ".post-content p strong span",      # Alternativer Original-Selektor
                ".wasserampel-status",              # Beispiel für einen neuen Selektor
                "#wasserampel strong",              # Weiteres Beispiel
                "div.ampel-status",                 # Noch ein Beispiel
            ]

            element = None
            for selector in selectors_to_try:
                _LOGGER.debug(f"Trying selector: {selector}")
                element = soup.select_one(selector)
                if element:
                    _LOGGER.debug(f"Found element with selector {selector}: {element.text.strip()}")
                    break

            # Wenn kein Element gefunden wurde, versuche einen allgemeineren Ansatz
            if not element:
                _LOGGER.debug("No specific selector matched, trying to find by content")
                # Suche nach Text, der "grün", "gelb" oder "rot" enthält
                for tag in soup.find_all(["strong", "span", "div", "p"]):
                    text = tag.get_text().lower()
                    if any(color in text for color in ["grün", "gruen", "gelb", "rot"]):
                        _LOGGER.debug(f"Found element with color text: {tag.text.strip()}")
                        element = tag
                        break

            if not element:
                raise UpdateFailed("Could not find status element on website")

            status_text = element.get_text().strip().lower()
            
            if "grün" in status_text or "gruen" in status_text:
                status = "Grün"
                numeric_status = 1
            elif "gelb" in status_text:
                status = "Gelb"
                numeric_status = 2
            elif "rot" in status_text:
                status = "Rot"
                numeric_status = 3
            else:
                status = "Unbekannt"
                numeric_status = 0

            return {"status": status, "numeric_status": numeric_status}
        
        except Exception as error:
            _LOGGER.error(f"Error updating sensor: {error}")
            raise UpdateFailed(error) from error

class PanketalerWasserampelSensor(Entity):
    """Representation of a Panketaler Wasserampel sensor."""

    def __init__(self, coordinator, name):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._name = name
        self._attr_unique_id = f"{DOMAIN}_{name.lower().replace(' ', '_')}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("status")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        status = self.coordinator.data.get("status", "").lower()
        if status == "grün":
            return "mdi:water"
        elif status == "gelb":
            return "mdi:water-alert"
        elif status == "rot":
            return "mdi:water-off"
        return "mdi:water-question"

    @property
    def should_poll(self):
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update the entity."""
        await self.coordinator.async_request_refresh()

class PanketalerWasserampelNumerischSensor(PanketalerWasserampelSensor):
    """Representation of a numeric Panketaler Wasserampel sensor."""

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("numeric_status")

    @property
    def state_attributes(self):
        """Return the state attributes."""
        return {
            "status_text": self.coordinator.data.get("status"),
            "1": "Grün",
            "2": "Gelb",
            "3": "Rot",
            "0": "Unbekannt"
        }
