"""Config flow for Kiosker integration."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_IP_ADDRESS, CONF_NAME, CONF_TOKEN
from . import DOMAIN
from .sensor import CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
from .options_flow import KioskerOptionsFlowHandler


class KioskerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Kiosker."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_IP_ADDRESS): str,
                    vol.Required(CONF_TOKEN): str,
                    vol.Optional(
                        CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL
                    ): int,
                }
            ),
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        """Get the options flow handler for Kiosker."""
        return KioskerOptionsFlowHandler(config_entry)
