from catt.api import CattDevice
from textual.containers import Container
from textual.widgets import Label
from textual.widgets import Static


class LolCattDeviceInfo(Static):
    def __init__(self, catt: CattDevice, refresh_interval: float = 2.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._catt = catt
        self._refresh_interval = refresh_interval
        self.label = Label(self._get_device_info())

    def _get_device_info(self) -> str:
        if hasattr(self._catt, 'name'):
            info = self._catt.name
            msg = f'Connected to: "{info}"'
        else:
            msg = 'Not connected to a device.'
        return msg

    def _update_label(self):
        self.label.update(self._get_device_info())

    def on_mount(self):
        self._update_label()
        self.set_interval(interval=self._refresh_interval, callback=self._update_label)

    def compose(self):
        yield Container(self.label, id='device_info')
