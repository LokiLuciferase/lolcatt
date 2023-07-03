import subprocess

from catt.api import CattDevice
from catt.cli import get_config_as_dict
from textual.app import App
from textual.containers import Container

from lolcatt.ui.lolcatt_cast_controls import ControlsConfig
from lolcatt.ui.lolcatt_cast_controls import LolCattControls
from lolcatt.ui.lolcatt_device_info import LolCattDeviceInfo
from lolcatt.ui.lolcatt_playback_info import LolCattPlaybackInfo
from lolcatt.ui.lolcatt_progress import LolCattProgress
from lolcatt.ui.lolcatt_url_input import LolCattUrlInput


class LolCatt(App):
    CSS_PATH = 'lolcatt.css'

    def __init__(
        self, device_name: str = None, controls_cfg: ControlsConfig = None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._catt_cfg = get_config_as_dict()
        self._controls_cfg = (
            controls_cfg
            if controls_cfg is not None
            else ControlsConfig(
                use_utf8=self._catt_cfg['options'].get('lolcatt_use_utf8', 'false').lower()
                == 'true'
            )
        )
        self._refresh_interval = 2.0
        self._device_name = (
            self._catt_cfg['aliases'].get(device_name, device_name)
            if device_name is not None
            else self._catt_cfg['options'].get('device')
        )
        self._catt = CattDevice(self._device_name)
        self._catt_call = None
        self._components = [
            LolCattDeviceInfo(catt=self._catt, refresh_interval=self._refresh_interval),
            LolCattPlaybackInfo(catt=self._catt, refresh_interval=self._refresh_interval),
            LolCattProgress(catt=self._catt, refresh_interval=self._refresh_interval),
            LolCattControls(exit_cb=self.exit, catt=self._catt, config=self._controls_cfg),
            LolCattUrlInput(cast_cb=self.cast),
        ]

    def compose(self):
        yield Container(
            *self._components,
            id='app',
        )

    def cast(self, media: str):
        if self._catt_call is not None:
            self._catt_call.kill()
        self._catt_call = subprocess.Popen(
            ['catt', '-d', self._catt.name, 'cast', '-f', media],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
