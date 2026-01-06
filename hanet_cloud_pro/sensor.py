from homeassistant.components.sensor import SensorEntity
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
    """Set up sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    # Create sensors for all devices found in the first update
    sensors = []
    if coordinator.data:
        for device_id, data in coordinator.data.items():
            camera_name = data.get("camera_name", device_id)
            sensors.append(HanetSensor(coordinator, device_id, camera_name, "name", "Tên người"))
            sensors.append(HanetSensor(coordinator, device_id, camera_name, "type", "Loại người"))
            sensors.append(HanetSensor(coordinator, device_id, camera_name, "time", "Thời gian"))

    async_add_entities(sensors)

class HanetSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id, camera_name, sensor_type, sensor_name_suffix):
        super().__init__(coordinator)
        self.device_id = device_id
        self.sensor_type = sensor_type
        self._attr_name = f"{camera_name} {sensor_name_suffix}"
        self._attr_unique_id = f"hanet_{device_id}_{sensor_type}"
        self._attr_icon = "mdi:face-recognition"
        if sensor_type == "time":
             self._attr_icon = "mdi:clock-outline"
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": camera_name,
            "manufacturer": "Hanet",
            "model": "AI Camera",
        }

    @property
    def native_value(self):
        data = self.coordinator.data.get(self.device_id)
        if not data:
            return None
            
        if self.sensor_type == "name":
            return data.get("name", "Unknown")
        
        if self.sensor_type == "type":
            type_code = str(data.get("type_code", "2"))
            if type_code in ["0", "FAM"]: return "Gia đình"
            if type_code in ["1", "ACQ"]: return "Người quen"
            return "Người lạ"
            
        if self.sensor_type == "time":
            return data.get("time_str", "")

        return None


