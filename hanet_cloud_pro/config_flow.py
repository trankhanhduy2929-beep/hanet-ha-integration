import logging
import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_URL
from .const import DOMAIN, DEFAULT_URL

_LOGGER = logging.getLogger(__name__)

class HanetConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hanet AI Bridge."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Validate connection
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{user_input[CONF_URL]}/api/states", timeout=5) as response:
                        if response.status == 200:
                            return self.async_create_entry(
                                title="Hanet AI Bridge",
                                data=user_input
                            )
                        else:
                            errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_URL, default=DEFAULT_URL): str,
            }),
            errors=errors,
        )


