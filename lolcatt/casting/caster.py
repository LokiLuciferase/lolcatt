#!/usr/bin/env python3
import subprocess
from dataclasses import dataclass
from typing import List
from typing import Optional

from catt.api import CattDevice
from catt.api import discover
from catt.cli import get_config_as_dict


@dataclass
class CastState:
    cast_info: dict
    info: dict


class Caster:

    CATT_ARGS = []
    CAST_ARGS = ['-f']

    def __init__(self, name_or_alias: str = 'default'):
        self._device = None
        self._available_devices = None
        self._catt_call = None
        self._catt_config = get_config_as_dict()
        if name_or_alias == 'default':
            self._device_name = self._catt_config['options'].get('device')
        elif name_or_alias is not None:
            self._device_name = self._catt_config['aliases'].get(name_or_alias, name_or_alias)
        else:
            self._device_name = None

        if self._device_name is not None:
            self._device = CattDevice(self._device_name)

    def cast(self, url_or_path: str):
        if self._catt_call is not None:
            self._catt_call.kill()
        if self._device is None:
            raise ValueError('Can\'t cast: No device selected.')
        self._catt_call = subprocess.Popen(
            [
                'catt',
                *self.CATT_ARGS,
                '-d',
                self._device_name,
                'cast',
                *self.CAST_ARGS,
                url_or_path,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def get_available_devices(self) -> List[str]:
        self._available_devices = discover()
        return self._available_devices

    def change_device(self, name_or_alias: str):
        self._device_name = self._catt_config['aliases'].get(name_or_alias, name_or_alias)
        for device in self.get_available_devices():
            if device.name == self._device_name:
                self._device = device
                return
        raise ValueError('Can\'t change device: Device not found.')

    def get_device(self) -> CattDevice:
        return self._device

    def get_device_name(self) -> Optional[str]:
        return self._device_name

    def get_cast_state(self) -> CastState:
        if self._device is None:
            raise ValueError('Can\'t get cast state: No device selected.')
        return CastState(self._device.controller.cast_info, self._device.controller.info)

    def update_cast_status(self):
        if self._device is None:
            raise ValueError('Can\'t update cast status: No device selected.')
        self._device.controller._update_status()
