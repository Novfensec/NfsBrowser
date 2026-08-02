import os
import sys
from kivy.resources import resource_add_path

sys.path.insert(0, os.path.dirname(__file__))
resource_add_path(os.path.dirname(__file__))

if sys.platform == "android":
    from libs.android.loading import create_loader, remove_loader, _ACTIVE_LOADERS

    from libs.android.service_manager import service_manager

    create_loader()

import registers

os.environ["devicetype"] = "mobile"

import weakref
import webbrowser
import re
from urllib.parse import urlparse, urlencode, quote_plus

from carbonkivy.app import CarbonApp
from carbonkivy.uix.screen import CScreen
from carbonkivy.uix.screenmanager import CScreenManager
from carbonkivy.uix.notification import CNotificationToast
from carbonkivy.utils import update_system_ui
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.properties import ObjectProperty, DictProperty, StringProperty
from kivy.resources import resource_add_path

from View.base_screen import BanLayout, LoadingLayout
from View.components.AgreementLayout import AgreementLayout

from Model.application_layer_model import ApplicationLayerModel

from libs.confighandler import config_handler
from libs import REFS

Clock.max_iteration = 60


def set_softinput(*args) -> None:
    Window.keyboard_anim_args = {"d": 0.2, "t": "in_out_expo"}
    Window.softinput_mode = "below_target"


Window.on_restore(Clock.schedule_once(set_softinput, 0.1))


SQueries = {
    "google": "https://www.google.com/search?q=",
    "bing": "https://www.bing.com/search?q=",
}


class UI(CScreenManager):
    def __init__(self, *args, **kwargs):
        super(UI, self).__init__(*args, **kwargs)


class MainScreen(CScreen):

    def __init__(self, **kwargs) -> None:
        super(MainScreen, self).__init__(**kwargs)


class NfsBrowser(CarbonApp):

    current_webview = ObjectProperty()

    tabs = DictProperty()

    current_se = StringProperty()

    se_source = StringProperty()

    def __init__(self, *args, **kwargs):
        self.defaults = False
        self.theme = config_handler.get("theme", "White")
        super(NfsBrowser, self).__init__(*args, **kwargs)
        self.load_all_kv_files(os.path.join(self.directory, "View"))
        self.manager_screens = UI()
        self.loading_layout = LoadingLayout()
        self.notification = CNotificationToast()
        self.ban_layout = BanLayout()
        self.view_model = ApplicationLayerModel()

    def on_current_se(self, *args) -> None:
        self.se_source = REFS.get(self.current_se, "")

    def on_theme(self, *args) -> None:
        config_handler.update({"theme": self.theme})
        super(CarbonApp, self).on_theme(*args)
        self.apply_styles()

    def apply_styles(self, *args) -> None:
        Window.clearcolor = self.background
        icon_style = "Dark" if self.theme in ["White", "Gray10"] else "Light"
        update_system_ui(
            self.background, self.background, icon_style=icon_style, pad_nav=True
        )

    def build(self) -> UI:
        self.main_screen = MainScreen(name="main screen")
        self.apply_styles()
        return self.main_screen

    def build_app(self) -> UI:
        self.main_screen = MainScreen(name="main screen")
        self.apply_styles()
        return self.main_screen

    def generate_application_screens(self, *args) -> None:
        # adds different screen widgets to the screen manager
        import View.screens

        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["view_model"]()
            view = screens[name_screen]["object"](view_model=model)
            model.add_observer(view)
            view.manager_screens = self.manager_screens
            view.name = name_screen

            self.manager_screens.add_widget(view)

    def on_start(self):
        lt = AgreementLayout()
        if not os.path.isfile(os.path.join(self.directory, ".accepted")):
            Window.add_widget(lt)

        self.generate_application_screens()
        self.main_screen.ids.main_layout.add_widget(self.manager_screens)
        self._running = True
        self.loading_state(False)

    def on_resume(self):
        if self.current_webview:
            self.current_webview.resume_webview()
        return super().on_resume()

    def on_pause(self, *args) -> None:
        if self.current_webview:
            self.current_webview.pause_webview()
        return True

    def on_stop(self, *args) -> None:
        self._running = False
        if self.current_webview:
            self.current_webview.destroy_webview()
        if sys.platform == "android":
            service_manager.terminate_pool()

    def accept_agreement(self, *args) -> None:
        with open(
            os.path.join(self.directory, ".accepted"), "w", encoding="utf-8"
        ) as agreement_file:
            agreement_file.write("")

    def referrer(self, destination: str = None) -> None:
        if self.manager_screens.current != destination:
            self.manager_screens.current = destination
        # try:
        #         # if not destination in self.manager_screens.upstream_views:
        #         #     self.manager_screens.switch(destination)
        #         # else:
        #         #     self.manager_screens.current = destination
        # except Exception as e:
        #     print(e)

    def notify(
        self,
        title: str = "",
        subtitle: str = "",
        status: str = "Info",
        time_caption_enabled: bool = True,
        *args,
    ) -> None:
        self.notification.title = title
        self.notification.subtitle = subtitle
        self.notification.status = status
        self.notification.time_caption_enabled = time_caption_enabled
        self.notification.open()

    def web_open(self, url: str) -> None:
        webbrowser.open_new_tab(url)

    @mainthread
    def ban_state(self, state: bool = False, master: object = Window, *args) -> None:
        try:
            if state and not (
                hasattr(master, "ban_layout") and master.ban_layout != None
            ):
                master.ban_layout = BanLayout()
                _layout_ref = weakref.ref(master.ban_layout)
                master.add_widget(master.ban_layout)
                _layout_ref = None
            else:
                master.remove_widget(master.ban_layout)
                master.ban_layout = None
        except:
            return None

    @mainthread
    def loading_state(
        self, state: bool = False, master: object = Window, *args
    ) -> None:
        if sys.platform == "android":
            if not _ACTIVE_LOADERS.get("default", None) and state:
                create_loader()
            else:
                remove_loader()
            return
        try:
            if state and not (
                hasattr(master, "loading_layout") and master.loading_layout != None
            ):
                master.loading_layout = LoadingLayout()
                _layout_ref = weakref.ref(master.loading_layout)
                master.add_widget(master.loading_layout)
                _layout_ref = None
            else:
                master.remove_widget(master.loading_layout)
                master.loading_layout = None
        except Exception as e:
            Logger.error(f"NfsBrowser: Loading State Error {e}")
            return None

    #### SEARCH #######

    def search(self, text, *args) -> None:
        if not text or not isinstance(text, str) or not text.strip():
            self._handle_empty_input()
            return
            
        query = text.strip()

        if len(query) > 2048:
            self._handle_error("Query exceeds maximum allowed length.")
            return

        if self._is_url(query):
            self._navigate_to_url(query)
            return

        if '"' in query or "site:" in query or "OR" in query:
            self._execute_advanced_search(query)
            return

        self._execute_standard_search(query)

    def _is_url(self, text: str) -> bool:
        """
        Determines if a string is a likely URL. 
        Catches explicit (http://) and implicit (example.com) URLs.
        """
        parsed = urlparse(text)
        if parsed.scheme and parsed.netloc:
            return True

        url_pattern = re.compile(
            r'^(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{2,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
        )
        return bool(url_pattern.match(text))

    def _navigate_to_url(self, url: str) -> None:
        if not url.startswith(('http://', 'https://', 'file://', 'ftp://')):
            url = f"https://{url}"
        if self.current_webview:
            Clock.schedule_once(lambda dt: self.current_webview.load_url(url), 0.15)
        print(f"[ACTION] Navigating directly to URL: {url}")

    def _execute_standard_search(self, query: str) -> None:
        url = f"{SQueries[self.current_se]}{quote_plus(query)}"
        if self.current_webview:
            Clock.schedule_once(lambda dt: self.current_webview.load_url(url), 0.15)
        print(f"[ACTION] Executing standard text search for: '{query}'")

    def _execute_advanced_search(self, query: str) -> None:
        url = f"{SQueries[self.current_se]}{quote_plus(query)}"
        if self.current_webview:
            Clock.schedule_once(lambda dt: self.current_webview.load_url(url), 0.15)
        print(f"[ACTION] Executing advanced text search for: '{query}'")

    def _handle_empty_input(self) -> None:
        print("[ACTION] Ignored: Input is empty or invalid.")

    def _handle_error(self, message: str) -> None:
        print(f"[ERROR] {message}")

def main(*args) -> None:
    app = NfsBrowser()
    app.run()


if __name__ == "__main__":
    main()
