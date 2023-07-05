from typing import Callable

from textual.app import App
from textual.containers import Container
from textual.screen import Screen

from lolcatt.casting.caster import Caster
from lolcatt.ui.lolcatt_controls import LolCattControls
from lolcatt.ui.lolcatt_device_info import LolCattDeviceInfo
from lolcatt.ui.lolcatt_playback_info import LolCattPlaybackInfo
from lolcatt.ui.lolcatt_progress import LolCattProgress
from lolcatt.ui.lolcatt_url_input import LolCattUrlInput


class RemoteScreen(Screen):
    """A screen for the remote control UI."""

    def __init__(self, caster: Caster, exit_cb: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caster = caster
        self.exit = exit_cb
        self._components = [
            LolCattDeviceInfo(),
            LolCattPlaybackInfo(),
            LolCattProgress(),
            LolCattControls(),
            LolCattUrlInput(),
        ]

    def compose(self):
        yield Container(
            *self._components,
            id='app',
        )


class QueueScreen(Screen):
    """A screen for the queue UI."""

    def __init__(self, caster: Caster, exit_cb: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caster = caster
        self.exit = exit_cb
        self._components = []

    def compose(self):
        yield Container(
            *self._components,
            id='queue',
        )


class LolCatt(App):
    """The main application class for lolcatt."""

    CSS_PATH = 'ui/lolcatt.css'

    def __init__(self, device_name: str = None, *args, **kwargs):
        self.caster = Caster(device_name)
        super().__init__(*args, **kwargs)

    def on_mount(self):
        self.install_screen(RemoteScreen(caster=self.caster, exit_cb=self.exit), name='remote')
        self.install_screen(QueueScreen(caster=self.caster, exit_cb=self.exit), name='queue')
        self.push_screen('remote')


if __name__ == '__main__':
    app = LolCatt('default')
    app.run()
