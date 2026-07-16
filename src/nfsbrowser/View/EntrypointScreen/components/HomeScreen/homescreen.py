from View.base_screen import BaseScreenView

from carbonkivy.uix.textinput import CTextInput


class FixedTextInput(CTextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def window_on_textedit(self, window, ime_input):
        if self._ime_composition:
            ci = self.cursor_index()
            len_ime = len(self._ime_composition)

            self._selection_from = max(0, ci - len_ime)
            self._selection_to = ci
            self._selection = True

            self.delete_selection()

        if ime_input:
            if self._selection:
                self.delete_selection()
            self.insert_text(ime_input)

        self._ime_composition = ime_input
        self._ime_cursor = self.cursor


class HomeScreen(BaseScreenView):

    def __init__(self, *args, **kwargs) -> None:
        super(HomeScreen, self).__init__(*args, **kwargs)
