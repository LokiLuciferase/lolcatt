from textual import on
from textual.containers import Container
from textual.widgets import Input

from lolcatt.ui.caster_static import CasterStatic


class LolCattUrlInput(CasterStatic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._input = Input(id='url_input', placeholder='Enter URL to cast...')
        self._input.cursor_blink = False

    @on(Input.Submitted, "#url_input")
    def cast_url(self):
        if self._input.value == '':
            return
        if self._input.value:
            self._caster.cast(self._input.value)
            self._input.value = ''

    def compose(self):
        yield Container(self._input, id='url_input_container')
