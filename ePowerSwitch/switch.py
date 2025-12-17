from homeassistant.components.switch import SwitchEntity
import aiohttp
from .coordinator import EPSCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = EPSCoordinator(hass, entry.data["host"])
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [EPSSwitch(coordinator, port) for port in range(1, 9)]
    )

class EPSSwitch(SwitchEntity):
    def __init__(self, coordinator, port):
        self.coordinator = coordinator
        self.port = port

    @property
    def name(self):
        return f"P{self.port:02d}"

    @property
    def is_on(self):
        key = f"P{self.port:02d}="
        for line in self.coordinator.data.splitlines():
            if line.startswith(key):
                return line.endswith("1")
        return False

    async def async_turn_on(self, **kwargs):
        await self._set_state(1)

    async def async_turn_off(self, **kwargs):
        await self._set_state(0)

    async def _set_state(self, value):
        async with aiohttp.ClientSession() as session:
            await session.get(
                f"http://{self.coordinator.host}/hidden.htm?P{self.port:02d}={value}"
            )
        await self.coordinator.async_request_refresh()

    @property
    def device_info(self):
        return self.coordinator.device_info
