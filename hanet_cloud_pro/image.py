import logging
import aiohttp
from homeassistant.components.image import ImageEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = []
    if coordinator.data:
        for device_id, data in coordinator.data.items():
            camera_name = data.get("camera_name", device_id)
            sensors.append(HanetImage(coordinator, device_id, camera_name))
    async_add_entities(sensors)

class HanetImage(CoordinatorEntity, ImageEntity):
    def __init__(self, coordinator, device_id, camera_name):
        super().__init__(coordinator)
        ImageEntity.__init__(self, coordinator.hass)
        self.device_id = device_id
        self._attr_name = f"{camera_name} Snapshot"
        self._attr_unique_id = f"hanet_{device_id}_image"
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": camera_name,
            "manufacturer": "Hanet",
        }
        self._last_filename = None

    @property
    def image_last_updated(self):
        """Timestamp update check."""
        data = self.coordinator.data.get(self.device_id)
        if data and data.get("timestamp"):
             return dt_util.utc_from_timestamp(data.get("timestamp"))
        return None

    async def async_image(self) -> bytes | None:
        """Fetch image from Addon."""
        data = self.coordinator.data.get(self.device_id)
        if not data: 
            return None
        
        filename = data.get("filename")
        if not filename: 
            return None

        # Build URL to the addon
        base_url = self.coordinator.url
        image_url = f"{base_url}/img/{self.device_id}/{filename}"
        
        try:
            # Sử dụng session không check SSL để đảm bảo chạy tốt trong mạng nội bộ
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url, timeout=10) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        _LOGGER.warning(f"Failed to fetch image {image_url}: Status {response.status}")
        except Exception as e:
            _LOGGER.error(f"Error fetching image from {image_url}: {e}")
            pass
        return None


