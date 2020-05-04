from calendar import monthrange
from datetime import date

from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlNumber, ControlButton, ControlList, ControlDockWidget
from zeep import Client

from src.ClientReservationWindow import ClientReservationWindow
from src.LoginWindow import LoginWindow
from src.ScreeningWindow import ScreeningWindow


class CinemaManager(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Cinema manager')

        self._pesel = ""
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
        self._all_showings = self._client.service.getShowingsByDate(self._selected_date.year, self._selected_date.month,
                                                                    self._selected_date.day)
        self._search_screenings_button.value = self._searchScreeningsButton

        for showing in self._all_showings:
            self._screening_list += [showing.date.strftime("%H:%M"), str(showing.movie.title),
                                     str(showing.movie.description)]

        # Client window
        self._all_reservations = []

        self._reservation_list = ControlList('Reservations', readonly=True, select_entire_row=True,
                                             cell_double_clicked_event=self._reservation_changed_event)
        self._reservation_list.horizontal_headers = ['Date', 'Time', 'Movie', 'Seats', 'Paid']
        self._screening_panel = ControlDockWidget()
        self._screening_panel.hide()
        self._reservation_panel = ControlDockWidget()
        self._reservation_panel.hide()
        self._loginWindow = LoginWindow(self._client)
        self.hide()
        self._loginWindow.parent = self
        self._loginWindow.show()
        print(self._client.service)
        # Define the organization of the Form Controls
        self.formset = [{
            'a:Screening': [('_screening_day', '_screening_month', '_screening_year', '_search_screenings_button'), '=',
                            '_screening_list'],
            'b:Client': ['_reservation_list']
        },
        ]

    def _screening_changed_event(self, row, column):
        self._all_showings = self._client.service.getShowingsByDate(self._selected_date.year, self._selected_date.month,
                                                                    self._selected_date.day)
        print(self._all_showings)
        win = ScreeningWindow(self._all_showings[row], self._client, self._pesel)
        win.parent = self
        self._screening_panel.show()
        self._reservation_panel.hide()
        self._screening_panel.label = "Screening info"
        self._screening_panel.value = win

    def _reservation_changed_event(self, row, column):
        self._all_reservations = self._client.service.getUserReservationsByPesel(self._pesel)
        win = ClientReservationWindow(self._all_reservations[row], self._client)
        win.parent = self
        self._screening_panel.hide()
        self._reservation_panel.show()
        self._reservation_panel.label = "Reservation details"
        self._reservation_panel.value = win

    def setUserPesel(self,pesel):
        self._pesel = pesel
        self.updateInfo()

    def updateInfo(self):
        self._screening_list.clear()
        self._all_showings = self._client.service.getShowingsByDate(self._selected_date.year, self._selected_date.month,
                                                                    self._selected_date.day)
        for show in self._all_showings:
            self._screening_list += [show.date.strftime("%H:%M"), str(show.movie.title),
                                     str(show.movie.description)]
        self._reservation_list.clear()
        self._all_reservations = self._client.service.getUserReservationsByPesel(self._pesel)
        for reservation in self._all_reservations:
            self._reservation_list += [reservation['showing']['date'].strftime("%d-%m-%Y"),
                                       reservation['showing']['date'].strftime("%H:%M"),
                                       str(reservation['showing']['movie']['title']), str(reservation['places']),
                                       "Yes" if reservation['isPaid'] is True else "No"]

    def _searchScreeningsButton(self):
        self._screening_list.clear()
        self._all_showings = self._client.service.getShowingsByDate(self._selected_date.year, self._selected_date.month,
                                                                    self._selected_date.day)
        for show in self._all_showings:
            self._screening_list += [show.date.strftime("%H:%M"), str(show.movie.title),
                                     str(show.movie.description)]

    def _change_day(self):
        self._selected_date = self._selected_date.replace(day=int(self._screening_day.value))

    def _change_month(self):
        self._selected_date = self._selected_date.replace(month=int(self._screening_month.value), day=1)
        self._screening_day.max = monthrange(self._selected_date.year, self._selected_date.month)[1]
        self._screening_day.value = 1


if __name__ == '__main__':
    from pyforms import start_app

    start_app(CinemaManager)
