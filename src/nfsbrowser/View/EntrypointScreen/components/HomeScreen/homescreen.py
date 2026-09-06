from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior

from carbonkivy.behaviors import SelectableBehavior, SelectionBehavior
from carbonkivy.uix.textinput import CTextInput
from carbonkivy.uix.dropdown import CDropdown
from carbonkivy.uix.boxlayout import CBoxLayout

from View.components.RoundedBoxLayout import RoundedBoxLayout
from View.base_screen import BaseScreenView

from libs.confighandler import config_handler


class SEDropdown(SelectionBehavior, CDropdown):

    def __init__(self, **kwargs):
        super(SEDropdown, self).__init__(**kwargs)

    def on_selected_items(self, *args) -> None:
        self.visibility = False


class SEOption(ButtonBehavior, RoundedBoxLayout, SelectableBehavior):

    title = StringProperty()

    source = StringProperty()

    def __init__(self, **kwargs):
        super(SEOption, self).__init__(**kwargs)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.selected = self.title.lower() == config_handler.get("search_engine")

    def on_selected(self, *args) -> None:
        if self.selected:
            config_handler.update({"search_engine": self.title.lower()})


class FixedTextInput(CTextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_text(self, instance, value):
        if not self.focus:
            Clock.schedule_once(self._reset_cursor_to_start, 0)

    def _reset_cursor_to_start(self, dt):
        if not self.focus:
            self.cursor = (0, 0)
            self.scroll_x = 0

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

    current_se = StringProperty()

    se_source = StringProperty()

    def __init__(self, *args, **kwargs) -> None:
        super(HomeScreen, self).__init__(*args, **kwargs)
        self.se_dropdown = SEDropdown()
        self.current_se = config_handler.get("search_engine", "google")
        self.app.current_se = config_handler.get("search_engine", "google")

    def on_kv_post(self, base_widget):
        self.se_dropdown.master = self.ids.engine_icon
        return super().on_kv_post(base_widget)
