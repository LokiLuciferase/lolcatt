from dataclasses import dataclass
from typing import Callable

from catt.cli import get_config_as_dict
from catt.error import CastError
from textual import on
from textual.containers import Container
from textual.widgets import Button
from textual.widgets import Static

from lolcatt.casting.caster import Caster


@dataclass
class ControlsConfig:
    ffwd_secs: int = 30
    rewind_secs: int = 10
    vol_step: float = 0.1
    use_utf8: bool = False


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
        caster: Caster,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._caster = caster
        self._config = ControlsConfig(
            use_utf8=get_config_as_dict()['options'].get('lolcatt_use_utf8', 'false').lower()
            == 'true'
        )
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
            self._caster.get_device().controller.play_toggle()
        except ValueError:
            pass

    @on(Button.Pressed, "#stop")
    def stop(self):
        self._caster.get_device().stop()
        self._exit_func()

    @on(Button.Pressed, "#vol_down")
    def vol_down(self):
        self._caster.get_device().volumedown(self._config.vol_step)

    @on(Button.Pressed, "#vol_up")
    def vol_up(self):
        self._caster.get_device().volumeup(self._config.vol_step)

    @on(Button.Pressed, "#ffwd")
    def ffwd(self):
        try:
            self._caster.get_device().ffwd(self._config.ffwd_secs)
        except CastError:
            pass

    @on(Button.Pressed, "#rewind")
    def rewind(self):
        try:
            self._caster.get_device().rewind(self._config.rewind_secs)
        except CastError:
            pass
