from homeassistant.helpers.entity import Entity
from .coordinator import EPSCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = EPSCoordinator(hass, entry.data["host"])
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        EPSPowerSensor(coordinator, "Power A"),
        EPSPowerSensor(coordinator, "Power B"),
    ])

class EPSPowerSensor(Entity):
    def __init__(self, coordinator, key):
        self.coordinator = coordinator
        self.key = key

    @property
    def name(self):
        return self.key

    @property
    def state(self):
        for line in self.coordinator.data.splitlines():
            if line.startswith(self.key):
                return int(line.split("=")[1])
        return 0

    @property
    def device_info(self):
        return self.coordinator.device_info
