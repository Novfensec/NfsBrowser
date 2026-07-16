from carbonkivy.uix.anchorlayout import CAnchorLayout


class AgreementLayout(CAnchorLayout):

    def __init__(self, *args, **kwargs) -> None:
        super(AgreementLayout, self).__init__(*args, **kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Let children handle it if they want
            super().on_touch_down(touch)
            return True  # <-- stops event from propagating below
        return False

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            super().on_touch_up(touch)
            return True
        return False
