#!/usr/bin/env python3
from re import S
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
from textual.widgets import Label
from textual.widgets import ProgressBar
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
        self.catt = catt
        self.config = config
        self.exit = exit_cb

    def _get_control_label(self, control: str) -> str:
        if self.config.use_utf8:
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
        self.catt.controller.play_toggle()

    @on(Button.Pressed, "#stop")
    def stop(self):
        self.catt.stop()
        self.exit()

    @on(Button.Pressed, "#vol_down")
    def vol_down(self):
        self.catt.volumedown(self.config.vol_step)

    @on(Button.Pressed, "#vol_up")
    def vol_up(self):
        self.catt.volumeup(self.config.vol_step)

    @on(Button.Pressed, "#ffwd")
    def ffwd(self):
        self.catt.ffwd(self.config.ffwd_secs)

    @on(Button.Pressed, "#rewind")
    def rewind(self):
        self.catt.rewind(self.config.rewind_secs)


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

    def __init__(self, catt: CattDevice, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.catt = catt
        self.pb = ProgressBar(id='progress_bar', total=100, show_bar=True, show_eta=False)
        self.pblabel = Label('(00:00/00:00)', id='progress_label')
        self.set_interval(interval=2.0, callback=self.update_progress)

    def update_progress(self) -> int:
        self.catt.controller._update_status()
        self.current, self.duration, self.percent_complete = self._extract_progress(
            self.catt.controller.cast_info
        )
        self.pb.update(progress=self.percent_complete)
        current_fmt = self._format_time(self.current)
        duration_fmt = self._format_time(self.duration)
        self.pblabel.update(f'({current_fmt}/{duration_fmt})')

    def on_mount(self):
        self.update_progress()

    def compose(self):
        yield Container(self.pb, self.pblabel, id='progress')


class LolCattTitle(Static):
    def __init__(self, catt: CattDevice, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.catt = catt
        self.label = Label(self.get_title(), id='title')

    def get_title(self) -> str:
        playing = self.catt.controller.cast_info.get('title')
        if playing:
            return f'Playing: "{playing}"'
        else:
            return f'Nothing is playing.'

    def compose(self):
        yield Container(self.label, id='title_container')

    def on_mount(self):
        self.set_interval(interval=2.0, callback=self.update_title)

    def update_title(self):
        self.label.update(self.get_title())


class LolCatt(App):
    CSS_PATH = 'lolcatt.css'

    def __init__(self, device_name: str, controls_cfg: ControlsConfig = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.catt_cfg = get_config_as_dict()
        self.controls_cfg = (
            controls_cfg
            if controls_cfg is not None
            else ControlsConfig(
                use_utf8=self.catt_cfg['options'].get('lolcatt_use_utf8', 'false').lower() == 'true'
            )
        )
        self._device_name = (
            self.catt_cfg['aliases'].get(device_name, device_name)
            if device_name is not None
            else self.catt_cfg['options'].get('device')
        )
        self.catt = CattDevice(self._device_name)

    def compose(self):
        yield Container(
            Label(f'Connected to "{self._device_name}".', id='device_label'),
            LolCattTitle(catt=self.catt),
            LolCattProgress(catt=self.catt),
            LolCattControls(exit_cb=self.exit, catt=self.catt, config=self.controls_cfg),
            id='app',
        )

    def cast(self, media: str):
        subprocess.Popen(
            ['catt', '-d', self.catt.name, 'cast', '-f', media],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


if __name__ == '__main__':
    LolCatt('Kitchen speaker').run()
