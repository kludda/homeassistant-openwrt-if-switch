from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.device_registry import format_mac
from homeassistant.helpers.entity import DeviceInfo
import paramiko
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'openwrt_wifi_switch'


def setup_platform(hass: HomeAssistant,
                   config: ConfigType,
                   add_entities: AddEntitiesCallback,
                   discovery_info: DiscoveryInfoType | None = None
                   ) -> None:
    for device in hass.data[DOMAIN]["devices"]:
        add_entities([WifiSwitch(device)])


class WifiSwitch(SwitchEntity):
    def __init__(self, device):
        self._attr_is_on = False
        self._device = device

    @property
    def name(self) -> str:
        return "Switch at %s using %s" % (self._device["host"], self._device["ifname"])

    @property
    def icon(self) -> str:
        return "mdi:wifi-strength-4"

    @property
    def unique_id(self) -> str:
        return "%s_%s" % (self._device["host"], self._device["ifname"])

    @property
    def is_on(self) -> bool:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#        ssh.connect(hostname=self._device["host"], port=self._device["port"], username=self._device["username"], password=self._device["password"])
        ssh.connect(hostname=self._device["host"], port=self._device["port"], key_filename="/root/.ssh/openwrt-key")

        #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("uci get wireless.%s.disabled" % self._device["ifname"])
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("wifi-status " % self._device["ifname"])        
        ssh_stdout = ssh_stdout.readlines()

        if len(ssh_stdout) == 0:
            ssh.exec_command("uci set wireless.%s.disabled=0" % self._device["ifname"])
            ssh.close()
            return True

        ssh.close()

        if "0" in ssh_stdout[0]:
            return True
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect(hostname=self._device["host"], port=self._device["port"], username=self._device["username"], password=self._device["password"])
        #ssh.exec_command("uci set wireless.%s.disabled=0" % self._device["ifname"])
        #ssh.exec_command("uci commit wireless")
        #ssh.exec_command("wifi")
        ssh.connect(hostname=self._device["host"], port=self._device["port"], key_filename="/root/.ssh/openwrt-key")        
        ssh.exec_command("wifi-up " % self._device["ifname"])
        ssh.close()

    async def async_turn_off(self, **kwargs: Any) -> None:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect(hostname=self._device["host"], port=self._device["port"], username=self._device["username"], password=self._device["password"])
        #ssh.exec_command("uci set wireless.%s.disabled=1" % self._device["ifname"])
        #ssh.exec_command("uci commit wireless")
        #ssh.exec_command("wifi")
        ssh.connect(hostname=self._device["host"], port=self._device["port"], key_filename="/root/.ssh/openwrt-key")        
        ssh.exec_command("wifi-up " % self._device["ifname"])
        ssh.close()