import logging
from datetime import timedelta
import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_IP_ADDRESS, CONF_NAME, CONF_TOKEN
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)
SENSOR_TYPES = [
    ("batteryLevel", "%", "Battery Level"),
    ("batteryState", None, "Battery State"),
    ("model", None, "Model"),
    ("osVersion", None, "OS Version"),
    ("lastInteraction", None, "Last Interaction"),
    ("lastMotion", None, "Last Motion"),
    ("date", None, "Date"),
    ("deviceId", None, "Device ID"),
]

CONF_UPDATE_INTERVAL = "update_interval"
DEFAULT_UPDATE_INTERVAL = 5  # minutes


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    update_interval = entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    coordinator = KioskerCoordinator(hass, entry.data, update_interval)
    entities = [
        KioskerSensor(coordinator, entry.data, sensor_type, unit, name)
        for sensor_type, unit, name in SENSOR_TYPES
    ]
    async_add_entities(entities)
    await coordinator.async_refresh()


class KioskerCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config, update_interval):
        super().__init__(
            hass,
            _LOGGER,
            name="Kiosker Status",
            update_interval=timedelta(minutes=update_interval),
        )
        self.config = config
        self.session = aiohttp.ClientSession()

    async def _async_update_data(self):
        url = f"http://{self.config[CONF_IP_ADDRESS]}:8081/api/v1/status"
        headers = {
            "Authorization": f"Bearer {self.config[CONF_TOKEN]}",
            "Content-Type": "application/json",
        }
        async with self.session.get(url, headers=headers) as resp:
            data = await resp.json()
            return data.get("status", {})


class KioskerSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, config, sensor_type, unit, friendly_name):
        super().__init__(coordinator)
        self._attr_unique_id = f"kiosker_{config[CONF_NAME]}_{sensor_type}"
        self._attr_name = f"Kiosker {friendly_name} {config[CONF_NAME]}"
        self._sensor_type = sensor_type
        self._unit = unit
        self._config = config
        self._attr_device_info = DeviceInfo(
            identifiers={("kiosker", config[CONF_NAME])},
            name=f"Kiosker {config[CONF_NAME]}",
            manufacturer="Kiosker",
        )
        if unit:
            self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self):
        """Return the value reported by the sensor."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._sensor_type)
