from typing import Any

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import ObjectProperty

from carbonkivy.behaviors import SelectionBehavior

from View.base_screen import BaseScreenView
from View.components.RoundedBoxLayout import RoundedBoxLayout

from libs.android.service_manager import service_manager


class CTabHeaderCircular(SelectionBehavior, RoundedBoxLayout):

    tab_manager = ObjectProperty()

    def __init__(self, **kwargs) -> None:
        super(CTabHeaderCircular, self).__init__(**kwargs)

    def on_tab_manager(self, *args) -> None:
        for widgets in self.children:
            widgets.tab_manager = self.tab_manager

    def add_widget(self, widget, *args, **kwargs) -> Any:
        if hasattr(widget, "tab_manager"):
            widget.tab_manager = self.tab_manager
        return super().add_widget(widget, *args, **kwargs)


class EntrypointScreenView(BaseScreenView):

    def __init__(self, *args, **kwargs) -> None:
        super(EntrypointScreenView, self).__init__(*args, **kwargs)
        Window.bind(on_keyboard=self.on_key_press)

    def on_key_press(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            if self.manager_screens.current != "entrypoint screen":
                self.manager_screens.current = "entrypoint screen"
                return True
            elif self.app.current_webview and self.app.current_webview.can_go_back() and self.ids.manager_screens.get_screen("webview").url != "about:blank":
                self.go_back()
                return True
            elif self.ids.manager_screens.current != "home":
                self.ids.manager_screens.current = "home"
                return True
        return False

    def go_back(self, *args) -> None:
        Window.release_all_keyboards()
        Clock.schedule_once(self._execute_safe_go_back, 0.15)

    def _execute_safe_go_back(self, dt) -> None:
        if self.app.current_webview:
            self.app.current_webview.go_back()

    def go_forward(self, *args) -> None:
        Window.release_all_keyboards()
        Clock.schedule_once(self._execute_safe_go_forward, 0.15)

    def _execute_safe_go_forward(self, dt) -> None:
        if self.app.current_webview:
            self.app.current_webview.go_forward()

    def go_home(self, *args) -> None:
        Window.release_all_keyboards()
        Clock.schedule_once(self._execute_safe_go_home, 0.15)

    def _execute_safe_go_home(self, dt) -> None:
        if self.app.current_webview:
            self.app.current_webview.go_home()

    def reload(self, *args) -> None:
        Window.release_all_keyboards()
        Clock.schedule_once(self._execute_safe_reload, 0.15)

    def _execute_safe_reload(self, dt) -> None:
        if self.app.current_webview:
            self.app.current_webview.reload()