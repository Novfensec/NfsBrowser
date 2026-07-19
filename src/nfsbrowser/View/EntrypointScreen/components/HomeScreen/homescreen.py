from View.base_screen import BaseScreenView

from carbonkivy.uix.textinput import CTextInput


class FixedTextInput(CTextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def window_on_textedit(self, window, ime_input):
        if not self._lines:
            self._refresh_text(self.text)

        if self._selection:
            self.delete_selection()

        current_ci = self.cursor_index()
        cursor_restored = False

        if self._ime_composition:
            ci = getattr(
                self, "_ime_absolute_cursor", self.cursor_index(self._ime_cursor)
            )
            start_ci = max(0, ci - len(self._ime_composition))

            if self.text[start_ci:ci] == self._ime_composition:
                self._selection_from = start_ci
                self._selection_to = ci
                self._selection = True
                self.delete_selection()

                if current_ci >= ci:
                    current_ci -= len(self._ime_composition)
                elif current_ci > start_ci:
                    current_ci = start_ci
                cursor_restored = True

            else:
                start_ci_curr = max(0, current_ci - len(self._ime_composition))
                if self.text[start_ci_curr:current_ci] == self._ime_composition:
                    self._selection_from = start_ci_curr
                    self._selection_to = current_ci
                    self._selection = True
                    self.delete_selection()

                    current_ci = start_ci_curr
                    cursor_restored = True

        if cursor_restored:
            self.cursor = self.get_cursor_from_index(current_ci)

        if ime_input:
            self.insert_text(ime_input)

        self._ime_composition = ime_input
        self._ime_cursor = self.cursor
        self._ime_absolute_cursor = self.cursor_index()


class HomeScreen(BaseScreenView):

    def __init__(self, *args, **kwargs) -> None:
        super(HomeScreen, self).__init__(*args, **kwargs)
