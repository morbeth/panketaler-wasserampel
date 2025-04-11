"""Sensor platform for Panketaler Wasserampel."""
from datetime import datetime
import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up Panketaler Wasserampel sensor based on a config entry."""
    name = entry.data.get(CONF_NAME)
    
    async_add_entities([
        PanketalerWasserampelSensor(name, entry.data),
        PanketalerWasserampelNumericSensor(name, entry.data)
    ], True)


class PanketalerWasserampelSensor(SensorEntity):
    """Implementation of a Panketaler Wasserampel sensor (text version)."""

    def __init__(self, name, config):
        """Initialize the sensor."""
        self._name = name
        self._config = config
        self._state = None
        self._attributes = {}
        self._attr_unique_id = f"panketaler_wasserampel_{name.lower().replace(' ', '_')}"
        self._attr_icon = "mdi:water"

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
        try:
            # Hier würdest du die Wasserdaten abrufen
            # Zum Testen verwenden wir einen Dummy-Wert
            ampel_status = "grün"  # Beispiel mit Kleinbuchstaben
            
            # Status normalisieren und dann numerischen Wert ermitteln
            normalized_status = self._normalize_status(ampel_status)
            numeric_value = self._get_numeric_value(normalized_status)
            
            # Status in normalisierter Form (erste Buchstabe groß) zurückgeben
            self._state = normalized_status
            self._attributes = {
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "numeric_value": numeric_value,
                "source": "Panketaler Wasserampel",
                "original_status": ampel_status  # Original-Status für Debug-Zwecke
            }
            _LOGGER.debug("Wasserampel Status: %s (original: %s), Numerischer Wert: %s", 
                         normalized_status, ampel_status, numeric_value)
        except Exception as ex:
            _LOGGER.error("Fehler beim Aktualisieren der Wasserampel: %s", ex)
            self._state = "Unbekannt"
            self._attributes = {"error": str(ex)}

    def _normalize_status(self, status):
        """Normalisiere den Status (erste Buchstabe groß, Rest klein)."""
        if not status:
            return "Unbekannt"
            
        # Alle Status-Strings in Kleinbuchstaben definieren
        valid_statuses = {
            "grün": "Grün", 
            "grun": "Grün",  # Für den Fall, dass Umlaute fehlen
            "gruen": "Grün", # Alternative Schreibweise
            "gelb": "Gelb",
            "rot": "Rot",
            "unbekannt": "Unbekannt"
        }
        
        # Normalisiere Eingabe und versuche zu matchen
        normalized = status.lower().strip()
        return valid_statuses.get(normalized, "Unbekannt")
        
    def _get_numeric_value(self, status):
        """Übersetze den Ampelstatus in einen numerischen Wert.
        
        Grün = 1
        Gelb = 2
        Rot = 3
        """
        translations = {
            "Grün": 1,
            "Gelb": 2,
            "Rot": 3,
            "Unbekannt": 0
        }
        return translations.get(status, 0)


class PanketalerWasserampelNumericSensor(SensorEntity):
    """Implementation of a Panketaler Wasserampel sensor (numeric version)."""

    def __init__(self, name, config):
        """Initialize the sensor."""
        self._name = f"{name} Numerisch"
        self._config = config
        self._state = None
        self._attributes = {}
        self._attr_unique_id = f"panketaler_wasserampel_numeric_{name.lower().replace(' ', '_')}"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:water-percent"

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
        try:
            # Hier würdest du die Wasserdaten abrufen
            # Zum Testen verwenden wir einen Dummy-Wert
            ampel_status = "grün"  # Beispiel mit Kleinbuchstaben
            
            # Status normalisieren und dann numerischen Wert ermitteln
            normalized_status = self._normalize_status(ampel_status)
            
            # Direkt den numerischen Wert als Status setzen
            self._state = self._get_numeric_value(normalized_status)
            
            self._attributes = {
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "text_status": normalized_status,
                "source": "Panketaler Wasserampel"
            }
            _LOGGER.debug("Numerischer Wasserampel Wert: %s, Status: %s", 
                         self._state, normalized_status)
        except Exception as ex:
            _LOGGER.error("Fehler beim Aktualisieren des numerischen Sensors: %s", ex)
            self._state = 0  # Standardwert bei Fehler
            self._attributes = {"error": str(ex)}

    def _normalize_status(self, status):
        """Normalisiere den Status (erste Buchstabe groß, Rest klein)."""
        if not status:
            return "Unbekannt"
            
        # Alle Status-Strings in Kleinbuchstaben definieren
        valid_statuses = {
            "grün": "Grün", 
            "grun": "Grün",  # Für den Fall, dass Umlaute fehlen
            "gruen": "Grün", # Alternative Schreibweise
            "gelb": "Gelb",
            "rot": "Rot",
            "unbekannt": "Unbekannt"
        }
        
        # Normalisiere Eingabe und versuche zu matchen
        normalized = status.lower().strip()
        return valid_statuses.get(normalized, "Unbekannt")
        
    def _get_numeric_value(self, status):
        """Übersetze den Ampelstatus in einen numerischen Wert.
        
        Grün = 1
        Gelb = 2
        Rot = 3
        """
        translations = {
            "Grün": 1,
            "Gelb": 2,
            "Rot": 3,
            "Unbekannt": 0
        }
        return translations.get(status, 0)
