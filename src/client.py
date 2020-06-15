import asyncio
import json
from calendar import monthrange
from datetime import date, datetime

from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlNumber, ControlButton, ControlList, ControlDockWidget
from requests import Session

from src.ClientReservationWindow import ClientReservationWindow
from src.LoginWindow import LoginWindow
from src.ScreeningWindow import ScreeningWindow


class CinemaManager(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Cinema manager')

        self._pesel = ""
        self._session = Session()
        # self._session.proxies = {'http': 'http://localhost:4040', 'https': 'https://localhost:4040'}
        self._url = 'http://localhost:8080/kinoService_war_exploded'
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
        self._all_showings = []
        self._all_reservations = []
        self._reservation_list = ControlList('Reservations', readonly=True, select_entire_row=True,
                                             cell_double_clicked_event=self._reservation_changed_event)
        self._reservation_list.horizontal_headers = ['Date', 'Time', 'Movie', 'Seats', 'Paid']
        asyncio.get_event_loop().run_until_complete(self.updateInfo())
        self._search_screenings_button.value = self._searchScreeningsButton

        # Client window
        self._screening_panel = ControlDockWidget()
        self._screening_panel.hide()
        self._reservation_panel = ControlDockWidget()
        self._reservation_panel.hide()
        self._loginWindow = LoginWindow(self._url, self._session)
        self.hide()
        self._loginWindow.parent = self
        self._loginWindow.show()
        # Define the organization of the Form Controls
        self.formset = [{
            'a:Screening': [('_screening_day', '_screening_month', '_screening_year', '_search_screenings_button'), '=',
                            '_screening_list'],
            'b:Client': ['_reservation_list']
        },
        ]

    def _screening_changed_event(self, row, column):
        self._all_showings = json.loads(self._session.get(
            self._url + f'/showings/showing/{self._selected_date.year}/{self._selected_date.month}/{self._selected_date.day}').text)
        selected_showing = json.loads(
            self._session.get(self._url + f'/showings/{self._all_showings[row]["id_showing"]}').text)
        win = ScreeningWindow(selected_showing, self._url, self._pesel, self._session)
        win.parent = self
        self._screening_panel.show()
        self._reservation_panel.hide()
        self._screening_panel.label = "Screening info"
        self._screening_panel.value = win

    def _reservation_changed_event(self, row, column):
        self._all_reservations = json.loads(self._session.get(self._url + f'/user/reservation/{self._pesel}').text)
        chosen_reservation = json.loads(
            self._session.get(self._url + f'/reservations/{self._all_reservations[row]["id_reservation"]}').text)
        win = ClientReservationWindow(chosen_reservation, self._url, self._session)
        win.parent = self
        self._screening_panel.hide()
        self._reservation_panel.show()
        self._reservation_panel.label = "Reservation details"
        self._reservation_panel.value = win

    def setUserPesel(self, pesel):
        self._pesel = pesel
        asyncio.get_event_loop().run_until_complete(self.updateInfo())

    async def updateInfo(self):
        self._screening_list.clear()
        self._all_showings = json.loads(self._session.get(
            self._url + f'/showings/showing/{self._selected_date.year}/{self._selected_date.month}/{self._selected_date.day}').text)
        for show in self._all_showings:
            self._screening_list += [
                datetime.strptime(show["date"], '%Y-%m-%dT%H:%M:%SZ[UTC]').strftime(
                    "%H:%M"), str(show['movie']["title"]),
                str(show["movie"]["description"])]
        self._reservation_list.clear()
        self._all_reservations = json.loads(self._session.get(self._url + f'/user/reservation/{self._pesel}').text)
        for reservation in self._all_reservations:
            self._reservation_list += [
                datetime.strptime(reservation['showing']['date'], '%Y-%m-%dT%H:%M:%SZ[UTC]').strftime("%d-%m-%Y"),
                datetime.strptime(reservation['showing']['date'], '%Y-%m-%dT%H:%M:%SZ[UTC]').strftime("%H:%M"),
                str(reservation['showing']['movie']['title']), str(reservation['places']),
                "Yes" if reservation['isPaid'] is True else "No"]

    def _searchScreeningsButton(self):
        self._screening_list.clear()
        self._all_showings = json.loads(self._session.get(
            self._url + f'/showings/showing/{self._selected_date.year}/{self._selected_date.month}/{self._selected_date.day}').text)
        for show in self._all_showings:
            self._screening_list += [
                datetime.strptime(show["date"], '%Y-%m-%dT%H:%M:%SZ[UTC]').strftime("%H:%M"),
                str(show['movie']['title']),
                str(show['movie']['description'])]

    def _change_day(self):
        self._selected_date = self._selected_date.replace(day=int(self._screening_day.value))

    def _change_month(self):
        self._selected_date = self._selected_date.replace(month=int(self._screening_month.value), day=1)
        self._screening_day.max = monthrange(self._selected_date.year, self._selected_date.month)[1]
        self._screening_day.value = 1


if __name__ == '__main__':
    from pyforms import start_app

    start_app(CinemaManager)
