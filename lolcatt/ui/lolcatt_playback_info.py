from textual.containers import Container
from textual.widgets import Label
from textual.reactive import reactive

from lolcatt.ui.caster_static import CasterStatic
from lolcatt.utils.utils import marquee


class LolCattPlaybackInfo(CasterStatic):

    label_str = reactive('')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = Label('', id='title')
        self._marquee_gen = None

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
        self.label_str = self._get_playback_info() + ' '
        self.label.update(next(self._marquee_gen))

    def watch_label_str(self, value):
        self._marquee_gen = marquee(value, self.size.width, 2)

    def on_resize(self, value):
        self._marquee_gen = marquee(self.label_str, self.size.width, 2)

    def compose(self):
        yield Container(self.label, id='playback_info')

    def on_mount(self):
        self.set_interval(interval=self._caster.get_update_interval(), callback=self._update_label)
