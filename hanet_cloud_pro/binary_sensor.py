import time
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

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
            sensors.append(HanetMotionSensor(coordinator, device_id, camera_name))
    async_add_entities(sensors)

class HanetMotionSensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator, device_id, camera_name):
        super().__init__(coordinator)
        self.device_id = device_id
        self._attr_name = f"{camera_name} Motion"
        self._attr_unique_id = f"hanet_{device_id}_motion"
        self._attr_device_class = "motion"
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": camera_name,
            "manufacturer": "Hanet",
        }

    @property
    def is_on(self):
        data = self.coordinator.data.get(self.device_id)
        if not data: return False
        
        # Active if timestamp < 10 seconds ago
        last_ts = data.get("timestamp", 0)
        return (time.time() - last_ts) < 10


