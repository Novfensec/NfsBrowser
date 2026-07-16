import threading

from kivy.app import App
from kivy.clock import Clock

from carbonkivy.uix.modal import CModal
from View.components.SelectionItem import SelectionItem


class CarSelectionModal(CModal):

    def __init__(self, **kwargs) -> None:
        super(CarSelectionModal, self).__init__(**kwargs)
        self.app = App.get_running_app()
        Clock.schedule_once(self.add_cars_list)

    def add_cars_list(self, *args) -> None:
        for items in self.app.view_model.valid_cars:
            self.ids.list_cars.add_widget(SelectionItem(text=items[0]))

    def progress(self, *args) -> None:

        if self.ids.tab_manager.current == "t2":
            if len(self.ids.list_categories.selected_items) <= 0:
                self.ids.list_categories._line_color = self.app.support_error
                return
            self.app.view_model.selected_categories = [
                item.text
                for item in list(self.ids.list_categories.selected_items.keys())
            ]
            self.dismiss()

        elif len(self.ids.list_cars.selected_items) == 1:
            self.app.view_model.selected_car = list(
                self.ids.list_cars.selected_items.keys()
            )[0].text
            self.add_cars_categories(self.app.view_model.selected_car)
            self.ids.tab_manager.current = "t2"
        else:
            self.ids.list_cars._line_color = self.app.support_error

    def add_cars_categories(self, name: str, *args) -> None:
        for cars in self.app.view_model.valid_cars:
            if cars[0] == name:
                self.app.dbhandler.update_state("car_name", cars[0])
                self.app.dbhandler.update_state("native_cat", cars[2])
                self.app.dbhandler.update_state("unique_car", cars[1])
                for values in self.app.view_model.sheet_categories[cars[2]]:
                    self.ids.list_categories.add_widget(
                        SelectionItem(text=values, selection_type="multiple")
                    )
                return
