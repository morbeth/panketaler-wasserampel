"""Config flow for Panketaler Wasserampel integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import CONF_NAME

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class PanketalerWasserampelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Panketaler Wasserampel."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Hier könntest du eine Validierung durchführen, wenn nötig
            # z.B. testen, ob die API erreichbar ist

            return self.async_create_entry(
                title=user_input.get(CONF_NAME, "Panketaler Wasserampel"),
                data=user_input,
            )

        # Wenn keine Eingabe benötigt wird (Minimal-Setup)
        return self.async_create_entry(
            title="Panketaler Wasserampel",
            data={},
        )

        # ODER wenn du vom Benutzer Konfigurationsoptionen benötigst:
        # data_schema = vol.Schema({
        #     vol.Required(CONF_NAME, default="Panketaler Wasserampel"): str,
        #     # Weitere Konfigurationsoptionen hier...
        # })
        #
        # return self.async_show_form(
        #     step_id="user", data_schema=data_schema, errors=errors
        # )
