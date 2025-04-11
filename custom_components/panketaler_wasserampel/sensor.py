"""Sensor platform for Panketaler Wasserampel."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Panketaler Wasserampel sensor based on a config entry."""
    name = entry.data.get(CONF_NAME)
    
    async_add_entities([PanketalerWasserampelSensor(name, entry.data)], True)


class PanketalerWasserampelSensor(SensorEntity):
    """Implementation of a Panketaler Wasserampel sensor."""

    def __init__(self, name, config):
        """Initialize the sensor."""
        self._name = name
        self._config = config
        self._state = None
        self._attributes = {}
        # Füge eine eindeutige ID hinzu, damit Home Assistant die Entität korrekt verfolgen kann
        self._attr_unique_id = f"panketaler_wasserampel_{name}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    async def async_update(self):
        """Fetch new state data for the sensor."""
        # Hier würde man die Wasserdaten abrufen
        # Zum Testen verwenden wir einen Dummy-Wert
        self._state = "Grün"  # oder "Gelb", "Rot" abhängig vom Wasserstand
        self._attributes = {
            "last_update": "2023-01-01 12:00:00",
            "water_level": 50,  # Beispielwert
            "source": "Panketaler Wasserampel"
        }
