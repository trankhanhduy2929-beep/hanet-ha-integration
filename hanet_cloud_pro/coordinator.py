import logging
import aiohttp
import async_timeout
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class HanetDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Hanet data."""

    def __init__(self, hass: HomeAssistant, url: str):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            # Update every 1 second for realtime sensor
            update_interval=timedelta(seconds=1),
        )
        self.url = url.rstrip('/')

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            async with async_timeout.timeout(5):
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.url}/api/states") as response:
                        if response.status != 200:
                            raise UpdateFailed(f"Error fetching data: {response.status}")
                        return await response.json()
        except Exception as err:
            # Chỉ log warning thay vì error để tránh spam log khi addon restart
            _LOGGER.warning(f"Error communicating with Hanet Addon: {err}")
            return {}


