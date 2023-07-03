from typing import Tuple

from catt.api import CattDevice
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Label
from textual.widgets import ProgressBar
from textual.widgets import Static


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
