from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlNumber, ControlText, ControlButton, ControlList, ControlEmptyWidget, \
    ControlDockWidget
from calendar import monthrange
from datetime import date

from src.ClientReservationWindow import ClientReservationWindow
from src.ReservationWindow import ReservationWindow


class ComputerVisionAlgorithm(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Cinema manager')
        self._selected_date = date.today()
        # Screening window
        self._screening_day = ControlNumber("Day:", default=self._selected_date.day, minimum=1,
                                            maximum=monthrange(self._selected_date.year, self._selected_date.month)[1],
                                            changed_event=self._change_day)
        self._screening_month = ControlNumber("Month:", default=self._selected_date.month, minimum=1,
                                              maximum=12, changed_event=self._change_month)
        self._screening_year = ControlNumber("Year:", default=self._selected_date.year,
                                             minimum=self._selected_date.year,
                                             maximum=self._selected_date.year + 1,
                                             changed_event=self._change_day)
        self._screening_list = ControlList('Screenings', readonly=True, select_entire_row=True,
                                           cell_double_clicked_event=self._screening_changed_event)
        self._screening_list.horizontal_headers = ['Time', 'Movie', 'Description']
        self._screening_list += ['Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'B', 'C']
        self._screening_list += ['D', 'E', 'F']

        # Client window
        self._pesel_control = ControlText("PESEL:")
        self._search_button = ControlButton("Search")

        self._reservation_list = ControlList('Reservations', readonly=True, select_entire_row=True,
                                             cell_double_clicked_event=self._resrvation_changed_event)
        self._reservation_list.horizontal_headers = ['Day', 'Time', 'Movie', 'Seats', 'Paid']
        self._reservation_list += ['A', 'B', 'C', 'X', True]
        self._reservation_list += ['D', 'E', 'F', 'Z', 1]

        self._screening_panel = ControlDockWidget()
        self._screening_panel.hide()
        self._reservation_panel = ControlDockWidget()
        self._reservation_panel.hide()
        # Define the organization of the Form Controls
        self.formset = [{
            'a:Screening': [('_screening_day', '_screening_month', '_screening_year'), '_panel', '=',
                            '_screening_list'],
            'b:Client': [('_pesel_control', '_search_button'), '_reservation_list']
        },
        ]

    def _screening_changed_event(self, row, column):
        data_dict = {'time': self._screening_list.value[row][0], 'title': self._screening_list.value[row][1],
                     'date': self._selected_date.strftime("%d-%m-%Y")}
        win = ReservationWindow(data_dict)
        win.parent = self
        self._screening_panel.show()
        self._reservation_panel.hide()
        self._screening_panel.label = "Reservation info"
        self._screening_panel.value = win

    def _resrvation_changed_event(self, row, column):
        data_dict = {'time': self._screening_list.value[row][0], 'title': self._screening_list.value[row][1],
                     'date': self._selected_date.strftime("%d-%m-%Y")}
        win = ClientReservationWindow(data_dict)
        win.parent = self
        self._screening_panel.show()
        self._reservation_panel.hide()
        self._screening_panel.label = "Reservation info"
        self._screening_panel.value = win

    def _addPersonBtnAction(self):
        """
        Add person button event.
        """
        # A new instance of the PersonWindow is opened and shown to the user.
        pass

    def _change_day(self):
        self._selected_date = self._selected_date.replace(day=int(self._screening_day.value))
        print(self._selected_date)

    def _change_month(self):
        self._selected_date = self._selected_date.replace(month=int(self._screening_month.value), day=1)
        self._screening_day.max = monthrange(self._selected_date.year, self._selected_date.month)[1]
        self._screening_day.value = 1
        print(self._selected_date)

    def __buttonAction(self):
        """Button action event"""
        self._fullname.value = str(self._selected_date)


if __name__ == '__main__':
    from pyforms import start_app

    start_app(ComputerVisionAlgorithm)
