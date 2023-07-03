from dataclasses import dataclass
from typing import Callable

from catt.api import CattDevice
from catt.error import CastError
from textual import on
from textual.containers import Container
from textual.widgets import Button
from textual.widgets import Static


@dataclass
class ControlsConfig:
    ffwd_secs: int = 30
    rewind_secs: int = 10
    vol_step: float = 0.1
    use_utf8: bool = True


class LolCattControls(Static):
    CONTROLS = {
        'play_pause': '⏯',
        'stop': '⏹',
        'rewind': '⏪',
        'ffwd': '⏩',
        'vol_down': '',
        'vol_up': '',
    }

    CONTROLS_ASCII = {
        'play_pause': 'Play/Pause',
        'stop': 'Stop',
        'rewind': 'RW',
        'ffwd': 'FW',
        'vol_down': 'Vol-',
        'vol_up': 'Vol+',
    }

    def __init__(
        self,
        exit_cb: Callable,
        catt: CattDevice,
        config: ControlsConfig = ControlsConfig(),
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._catt = catt
        self._config = config
        self._exit_func = exit_cb

    def _get_control_label(self, control: str) -> str:
        if self._config.use_utf8:
            return self.CONTROLS[control]
        else:
            return self.CONTROLS_ASCII[control]

    def compose(self):
        with Container(id='controls'):
            with Container(id='playback_buttons'):
                yield Button(self._get_control_label('play_pause'), id='play_pause')
                yield Button(self._get_control_label('stop'), id='stop')

            with Container(id='wind_buttons'):
                yield Button(self._get_control_label('rewind'), id='rewind')
                yield Button(self._get_control_label('ffwd'), id='ffwd')

            with Container(id='volume_buttons'):
                yield Button(self._get_control_label('vol_down'), id='vol_down')
                yield Button(self._get_control_label('vol_up'), id='vol_up')

    @on(Button.Pressed, "#play_pause")
    def toggle_play_pause(self):
        try:
            self._catt.controller.play_toggle()
        except ValueError:
            pass

    @on(Button.Pressed, "#stop")
    def stop(self):
        self._catt.stop()
        self._exit_func()

    @on(Button.Pressed, "#vol_down")
    def vol_down(self):
        self._catt.volumedown(self._config.vol_step)

    @on(Button.Pressed, "#vol_up")
    def vol_up(self):
        self._catt.volumeup(self._config.vol_step)

    @on(Button.Pressed, "#ffwd")
    def ffwd(self):
        try:
            self._catt.ffwd(self._config.ffwd_secs)
        except CastError:
            pass

    @on(Button.Pressed, "#rewind")
    def rewind(self):
        try:
            self._catt.rewind(self._config.rewind_secs)
        except CastError:
            pass
