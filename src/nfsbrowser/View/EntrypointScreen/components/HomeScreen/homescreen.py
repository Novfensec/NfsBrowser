from View.base_screen import BaseScreenView

from carbonkivy.uix.textinput import CTextInput


class FixedTextInput(CTextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def window_on_textedit(self, window, ime_input):
        if self.readonly or self.disabled:
            return

        if not self._lines:
            self._refresh_text(self.text)

        if self._selection:
            self.delete_selection()

        current_ci = self.cursor_index()

        if self._ime_composition:
            ci = getattr(self, '_ime_absolute_cursor', None)
            if ci is None:
                ci = self.cursor_index(self._ime_cursor)
            start_ci = max(0, ci - len(self._ime_composition))

            removed = False
            if self.text[start_ci:ci] == self._ime_composition:
                current_ci = self._remove_ime_range(start_ci, ci, current_ci)
                removed = True
            else:
                start_ci2 = max(0, current_ci - len(self._ime_composition))
                if self.text[start_ci2:current_ci] == self._ime_composition:
                    current_ci = self._remove_ime_range(
                        start_ci2, current_ci, current_ci)
                    removed = True

            if not removed:
                pass

        if ime_input:
            self.insert_text(ime_input, from_undo=True)

        self._ime_composition = ime_input
        self._ime_cursor = self.cursor
        self._ime_absolute_cursor = self.cursor_index()

    def _remove_ime_range(self, start_ci, end_ci, current_ci):
        self._selection_from = start_ci
        self._selection_to = end_ci
        self._selection = True
        self.delete_selection(from_undo=True)

        if current_ci >= end_ci:
            current_ci -= (end_ci - start_ci)
        elif current_ci > start_ci:
            current_ci = start_ci

        self.cursor = self.get_cursor_from_index(current_ci)
        return current_ci


class HomeScreen(BaseScreenView):

    def __init__(self, *args, **kwargs) -> None:
        super(HomeScreen, self).__init__(*args, **kwargs)
