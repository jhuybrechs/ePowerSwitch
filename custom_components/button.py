from homeassistant.components.button import ButtonEntity
import aiohttp
import asyncio
from .coordinator import EPSCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = EPSCoordinator(hass, entry.data["host"])
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [EPSRestartButton(coordinator, port) for port in range(1, 9)]
    )

class EPSRestartButton(ButtonEntity):
    def __init__(self, coordinator, port):
        self.coordinator = coordinator
        self.port = port

    @property
    def name(self):
        return f"P{self.port:02d} Restart"

    async def async_press(self):
        async with aiohttp.ClientSession() as session:
            await session.get(
                f"http://{self.coordinator.host}/hidden.htm?P{self.port:02d}=0"
            )
            await asyncio.sleep(3)
            await session.get(
                f"http://{self.coordinator.host}/hidden.htm?P{self.port:02d}=1"
            )
        await self.coordinator.async_request_refresh()

    @property
    def device_info(self):
        return self.coordinator.device_info
