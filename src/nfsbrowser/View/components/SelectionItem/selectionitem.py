from carbonkivy.behaviors import DeclarativeBehavior
from carbonkivy.behaviors.selectable_behavior import SelectableBehavior
from carbonkivy.uix.focuscontainer import FocusContainer
from kivy.clock import Clock
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    OptionProperty,
    StringProperty,
)


class SelectionItem(FocusContainer, SelectableBehavior, DeclarativeBehavior):

    text = StringProperty()

    name = StringProperty()

    selection_type = OptionProperty("single", options=["single", "multiple"])

    selected = BooleanProperty(False)

    default = BooleanProperty(False)

    selection_color = ColorProperty()

    def __init__(self, **kwargs) -> None:
        super(SelectionItem, self).__init__(**kwargs)

    def on_selected(self, *args) -> None:
        if self.selection_type == "single":
            if self.selected:
                for item in self.parent.children:
                    if item != self and hasattr(item, "selected"):
                        item.ids.checkbox.active = False
            else:
                if not any(
                    item.selected
                    for item in self.parent.children
                    if hasattr(item, "selected")
                ):
                    self.ids.checkbox.active = True

    def on_default(self, *args) -> None:

        def set_selected(*args) -> None:
            self.ids["checkbox"].active = True

        Clock.schedule_once(set_selected)
