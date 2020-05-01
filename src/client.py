from calendar import monthrange
from datetime import date

from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlNumber, ControlText, ControlButton, ControlList, ControlDockWidget
from suds.client import Client

from src.ClientReservationWindow import ClientReservationWindow
from src.ReservationWindow import ReservationWindow


class CinemaManager(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Cinema manager')

        self._client = Client('http://localhost:8080/projekt?wsdl')
        self._selected_date = date.today()

        # Screening window
        self._search_screenings_button = ControlButton("Search")
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
        self._all_showings = self._client.service.getAllShowings()
        self._search_screenings_button.value = self._searchScreeningsButton

        for showing in self._all_showings:
            print(showing)
            self._screening_list += [showing.date.strftime("%H:%M"), str(showing.movie.title),
                                     str(showing.movie.description)]

        # Client window
        self._all_reservations = [['A', 'B', 'C', 'D', 'E']]
        self._pesel_control = ControlText("PESEL:")
        self._search_reservations_button = ControlButton("Search")

        self._reservation_list = ControlList('Reservations', readonly=True, select_entire_row=True,
                                             cell_double_clicked_event=self._reservation_changed_event)
        self._reservation_list.horizontal_headers = ['Date', 'Time', 'Movie', 'Seats', 'Paid']
        for reservation in self._all_reservations:
            print(reservation)
            self._reservation_list += [reservation[0], reservation[1], reservation[2], reservation[3], reservation[4]]
        self._screening_panel = ControlDockWidget()
        self._screening_panel.hide()
        self._reservation_panel = ControlDockWidget()
        self._reservation_panel.hide()

        self._search_reservations_button.value = self._searchReservationsButton
        # Define the organization of the Form Controls
        self.formset = [{
            'a:Screening': [('_screening_day', '_screening_month', '_screening_year', '_search_screenings_button'), '=',
                            '_screening_list'],
            'b:Client': [('_pesel_control', '_search_reservations_button'), '_reservation_list']
        },
        ]

    def _screening_changed_event(self, row, column):
        win = ReservationWindow(self._all_showings[row], self._client)
        win.parent = self
        self._screening_panel.show()
        self._reservation_panel.hide()
        self._screening_panel.label = "Reservation info"
        self._screening_panel.value = win

    def _reservation_changed_event(self, row, column):
        win = ClientReservationWindow(self._all_reservations[row], self._client)
        win.parent = self
        self._screening_panel.hide()
        self._reservation_panel.show()
        self._screening_panel.label = "Reservation details"
        self._screening_panel.value = win

    def _searchScreeningsButton(self):
        self._screening_list.clear()

    def _searchReservationsButton(self):
        self._reservation_list.clear()

    def _change_day(self):
        self._selected_date = self._selected_date.replace(day=int(self._screening_day.value))
        print(self._selected_date)

    def _change_month(self):
        self._selected_date = self._selected_date.replace(month=int(self._screening_month.value), day=1)
        self._screening_day.max = monthrange(self._selected_date.year, self._selected_date.month)[1]
        self._screening_day.value = 1
        print(self._selected_date)


if __name__ == '__main__':
    from pyforms import start_app

    start_app(CinemaManager)
