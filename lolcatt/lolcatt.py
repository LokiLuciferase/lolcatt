#!/usr/bin/env python3
import subprocess
from dataclasses import dataclass
from typing import Callable
from typing import Tuple

from catt.api import CattDevice
from catt.cli import get_config_as_dict
from textual import on
from textual.app import App
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import ProgressBar
from textual.widgets import Static


@dataclass
class ControlsConfig:
    ffwd_secs: int = 30
    rewind_secs: int = 10
    vol_step: float = 0.1
    use_utf8: bool = True


@dataclass
class CastState:
    cast_info: dict
    info: dict


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
        self._catt.controller.play_toggle()

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
        self._catt.ffwd(self._config.ffwd_secs)

    @on(Button.Pressed, "#rewind")
    def rewind(self):
        self._catt.rewind(self._config.rewind_secs)


class LolCattProgress(Static):
    current = reactive(0)
    duration = reactive(0)
    percent_complete = reactive(0)

    @staticmethod
    def _extract_progress(cast_info: dict) -> Tuple[float, float, float]:
        current = cast_info.get('current_time', 0.0)
        duration = cast_info.get('duration', 0.0)
        percent_complete = current / duration * 100 if duration else 0.0
        return current, duration, percent_complete

    def _format_time(self, seconds: float) -> str:
        if seconds is None:
            return '--:--'
        minutes, seconds = divmod(seconds, 60)
        return f'{minutes:02.0f}:{seconds:02.0f}'

    def __init__(self, catt: CattDevice, refresh_interval: float = 2.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._catt = catt
        self.pb = ProgressBar(id='progress_bar', total=100, show_bar=True, show_eta=False)
        self.pblabel = Label('(00:00/00:00)', id='progress_label')
        self._refresh_interval = refresh_interval

    def update_progress(self) -> int:
        self._catt.controller._update_status()
        self.current, self.duration, self.percent_complete = self._extract_progress(
            self._catt.controller.cast_info
        )
        self.pb.update(progress=self.percent_complete)
        current_fmt = self._format_time(self.current)
        duration_fmt = self._format_time(self.duration)
        self.pblabel.update(f'({current_fmt}/{duration_fmt})')

    def on_mount(self):
        self.update_progress()
        self.set_interval(interval=self._refresh_interval, callback=self.update_progress)

    def compose(self):
        yield Container(self.pb, self.pblabel, id='progress')


class LolCattDeviceInfo(Static):
    def __init__(self, catt: CattDevice, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._catt = catt
        self.label = Label(self._get_device_info(), id='device_info')

    def _get_device_info(self) -> str:
        info = self._catt.controller.info
        return f'{info.get("display_name")} ({info.get("manufacturer")} {info.get("model_name")})'

    def _update_label(self):
        self.label.update(self._get_device_info())

    def compose(self):
        yield Container(self.label, id='device')


class LolCattPlaybackInfo(Static):
    def __init__(self, catt: CattDevice, refresh_interval: float = 2.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._catt = catt
        self._refresh_interval = refresh_interval
        self.label = Label(self._get_playback_info(), id='title')

    def _get_playback_info(self) -> str:
        playing = self._catt.controller.cast_info.get('title')
        if playing:
            return f'Playing: "{playing}"'
        else:
            display_name = self._catt.controller.info.get('display_name')
            print(display_name)
            if display_name is not None and display_name != 'Backdrop':
                return display_name
            else:
                return f'Nothing is playing.'

    def _update_label(self):
        self.label.update(self._get_playback_info())

    def compose(self):
        yield Container(self.label, id='title_container')

    def on_mount(self):
        self.set_interval(interval=self._refresh_interval, callback=self._update_label)


class LolCattUrlInput(Static):
    def __init__(self, cast_cb: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cast_cb = cast_cb
        self._input = Input(id='url_input', placeholder='Enter URL to cast...')
        self._input.cursor_blink = False

    @on(Input.Submitted, "#url_input")
    def cast_url(self):
        if self._input.value == '':
            return
        if self._input.value:
            self._cast_cb(self._input.value)
            self._input.value = ''

    def compose(self):
        yield Container(self._input, id='url_input_container')


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
            Label(f'Connected to "{self._device_name}".', id='device_label'),
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


if __name__ == '__main__':
    LolCatt().run()
