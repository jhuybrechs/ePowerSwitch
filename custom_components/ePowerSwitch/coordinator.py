import aiohttp
import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

class EPSCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host):
        self.host = host
        super().__init__(
            hass,
            _LOGGER,
            name=f"EPS {host}",
            update_interval=timedelta(seconds=10),
        )

    async def _async_update_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{self.host}/hidden.htm", timeout=10) as resp:
                resp.raise_for_status()
                return await resp.text()

    @property
    def device_info(self):
        return {
            "identifiers": {("eps_8m", self.host)},
            "name": f"EPS 8M+ ({self.host})",
            "manufacturer": "ePowerSwitch",
            "model": "8M+",
        }
