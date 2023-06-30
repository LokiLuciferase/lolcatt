#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Tuple

from catt.api import CattDevice
from textual import on
from textual.app import App
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button
from textual.widgets import Label
from textual.widgets import Placeholder
from textual.widgets import ProgressBar
from textual.widgets import Static


@dataclass
class ControlsConfig:
    ffwd_secs: int = 30
    rewind_secs: int = 10
    vol_step: float = 0.1


class LolCattControls(Static):
    def __init__(
        self, catt: CattDevice, config: ControlsConfig = ControlsConfig(), *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.catt = catt
        self.config = config

    def compose(self):
        with Container(id='controls'):
            with Container(id='playback_buttons'):
                yield Button('RW', id='rewind')
                yield Button('Play/Pause', id='play_pause')
                yield Button('Stop', id='stop')
                yield Button('FF', id='ffwd')

            with Container(id='volume_buttons'):
                yield Button('Vol-', id='vol_down')
                yield Button('Vol+', id='vol_up')

    @on(Button.Pressed, "#play_pause")
    def toggle_play_pause(self):
        self.catt.controller.play_toggle()

    @on(Button.Pressed, "#stop")
    def stop(self):
        self.catt.stop()

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


class LolCatt(App):
    CSS_PATH = 'lolcatt.css'

    def __init__(
        self, catt: CattDevice, controls_cfg: ControlsConfig = ControlsConfig(), *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.controls_cfg = controls_cfg
        self.catt = catt

    def compose(self):
        yield Container(
            Placeholder(),
            LolCattProgress(catt=self.catt),
            LolCattControls(catt=self.catt, config=self.controls_cfg),
            id='app',
        )


if __name__ == '__main__':
    catt = CattDevice('Living Room TV')
    LolCatt(catt=catt).run()
