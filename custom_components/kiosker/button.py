from homeassistant.components.button import ButtonEntity
from homeassistant.const import CONF_IP_ADDRESS, CONF_NAME, CONF_TOKEN
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.network import get_url
import aiohttp

BUTTONS = [
    ("navigate_url", "Navigate URL", "mdi:web"),
]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    entities = [KioskerNavigateUrlButton(entry.data)]
    async_add_entities(entities)


class KioskerNavigateUrlButton(ButtonEntity):
    def __init__(self, config):
        self._attr_unique_id = f"kiosker_{config[CONF_NAME]}_navigate_url"
        self._attr_name = f"Kiosker Navigate URL {config[CONF_NAME]}"
        self._attr_icon = "mdi:tablet-dashboard"
        self._config = config
        self._attr_device_info = DeviceInfo(
            identifiers={("kiosker", config[CONF_NAME])},
            name=f"Kiosker {config[CONF_NAME]}",
            manufacturer="Kiosker",
        )

    async def async_press(self) -> None:
        # Build the URL to the Kiosker REST API
        url = f"http://{self._config[CONF_IP_ADDRESS]}:8081/api/v1/navigate/url"
        headers = {
            "Authorization": f"Bearer {self._config[CONF_TOKEN]}",
            "Content-Type": "application/json",
        }
        # Use Home Assistant's URL helper to get the external URL
        hass = self.hass
        ha_url = get_url(hass, prefer_external=True)
        payload = {"url": ha_url}
        async with aiohttp.ClientSession() as session:
            await session.post(url, headers=headers, json=payload)
