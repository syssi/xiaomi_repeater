"""
Support for Xiaomi Mi WiFi Repeater 2

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/device_tracker.xiaomi_miio/
"""
import logging

from datetime import timedelta
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.device_tracker import (DOMAIN, PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_TOKEN)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_TOKEN): vol.All(cv.string, vol.Length(min=32, max=32)),
})

MIN_TIME_BETWEEN_SCANS = timedelta(seconds=30)

REQUIREMENTS = ['python-miio==0.3.8']


def get_scanner(hass, config):
    """Return a Xiaomi MiIO device scanner."""
    scanner = XiaomiMiioDeviceScanner(hass, config[DOMAIN])
    return scanner if scanner.success_init else None


class XiaomiMiioDeviceScanner(DeviceScanner):
    """This class queries a Xiaomi Mi WiFi Repeater."""

    def __init__(self, hass, config):
        """Initialize the scanner."""
        from miio import Device, DeviceException

        host = config.get(CONF_HOST)
        token = config.get(CONF_TOKEN)

        self.success_init = False
        self.last_results = []

        _LOGGER.info(
            "Initializing with host %s (token %s...)", host, token[:5])

        try:
            self.device = Device(host, token)
            self.device_info = self.device.info()
            _LOGGER.info("%s %s %s detected",
                         self.device_info.model,
                         self.device_info.firmware_version,
                         self.device_info.hardware_version)
            self.success_init = True
        except DeviceException as ex:
            _LOGGER.error("Device unavailable or token incorrect: %s", ex)
            self.success_init = False

    async def async_scan_devices(self):
        """Scan for devices and return a list containing found device ids."""
        await self._async_update_info()
        return self.last_results

    async def async_get_device_name(self, device):
        """The repeater doesn't provide the name of the associated device."""
        return None

    @Throttle(MIN_TIME_BETWEEN_SCANS)
    async def _async_update_info(self):
        """
        Query the repeater for associated devices
        Returns boolean if scanning successful.
        """
        from miio import DeviceException

        try:
            station_info = await self.hass.async_add_job(
                self._device.raw_command('get_repeater_sta_info', [])
            )
            _LOGGER.debug("Got new station info: %s", station_info)

            last_results = []
            for device in station_info['mat']:
                last_results.append(device['mac'])

            self.last_results = last_results

        except DeviceException as ex:
            _LOGGER.error("Got exception while fetching the state: %s", ex)
