from catt.api import CattDevice
from textual.containers import Container
from textual.widgets import Label
from textual.widgets import Static


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
            if display_name is not None and display_name != 'Backdrop':
                return f'Displaying: "{display_name}"'
            else:
                return f'Nothing is playing.'

    def _update_label(self):
        self.label.update(self._get_playback_info())

    def compose(self):
        yield Container(self.label, id='playback_info')

    def on_mount(self):
        self.set_interval(interval=self._refresh_interval, callback=self._update_label)
