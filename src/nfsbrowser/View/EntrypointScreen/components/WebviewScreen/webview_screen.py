from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty

from View.base_screen import BaseScreenView

from carbonkivy.uix.divider import CDivider

from nfswebview import NfsWebviewWidget


class ProgressDivider(CDivider):

    progressive_width = NumericProperty()

    def __init__(self, **kwargs):
        super(ProgressDivider, self).__init__(**kwargs)
        self.animation = Animation()

    def update_progressive(self, progress, *args) -> None:
        self.animation.cancel_all(self)
        self.animation = Animation(progressive_width=progress, d=0.15)
        self.animation.start(self)


class WebviewScreen(BaseScreenView):

    url = StringProperty()

    icon = StringProperty()

    progress = NumericProperty()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.generate_webview()

    def generate_webview(self, *args) -> None:
        default_webview = NfsWebviewWidget(url="about:blank")
        self.app.current_webview = default_webview
        self.app.tabs.update({len(self.app.tabs.keys()) + 1: default_webview})

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.attach_webview()

    def attach_webview(self, *args) -> None:
        self.ids.webview_layout.add_widget(self.app.current_webview)
        self.app.current_webview.bind(on_url_changed=self.setter("url"))
        self.app.current_webview.bind(on_icon_changed=self.setter("icon"))
        self.app.current_webview.bind(on_progress=self.setter("progress"))

    def on_url(self, *args) -> None:
        if self.url == "about:blank":
            self.manager_screens.current = "home"
            self.app.current_webview.go_home()
