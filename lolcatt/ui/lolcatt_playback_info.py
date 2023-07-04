from textual.containers import Container
from textual.widgets import Label

from lolcatt.ui.caster_static import CasterStatic


class LolCattPlaybackInfo(CasterStatic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = Label('', id='title')

    def _get_playback_info(self) -> str:
        playing = self._caster.get_cast_state().cast_info.get('title')
        if playing:
            return f'Playing: "{playing}"'
        else:
            display_name = self._caster.get_cast_state().info.get('display_name')
            if display_name is not None and display_name != 'Backdrop':
                return f'Displaying: "{display_name}"'
            else:
                return f'Nothing is playing.'

    def _update_label(self):
        self.label.update(self._get_playback_info())

    def compose(self):
        yield Container(self.label, id='playback_info')

    def on_mount(self):
        self.set_interval(interval=self._caster.get_update_interval(), callback=self._update_label)
