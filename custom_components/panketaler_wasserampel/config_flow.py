"""Config flow for Panketaler Wasserampel integration."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_NAME

from .const import DOMAIN, DEFAULT_NAME

class PanketalerWasserampelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Panketaler Wasserampel."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Erfolgreicher Abruf - erstelle Config Entry
            return self.async_create_entry(
                title=user_input.get(CONF_NAME, DEFAULT_NAME),
                data=user_input
            )

        # Schema für das Formular
        schema = vol.Schema({
            vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
