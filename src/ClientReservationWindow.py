import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton, ControlTextArea, ControlCheckBox
from suds.client import Client


class ClientReservationWindow(BaseWidget):

    def __init__(self, screening_info: dict, client: Client):
        print(screening_info)
        BaseWidget.__init__(self, 'Person window')
        # Definition of the forms fields
        self._client = client
        self._dateField = ControlText('Date', enabled=False, default=screening_info['date'])
        self._timeField = ControlText('Time', enabled=False, default=screening_info['time'])
        self._titleField = ControlText('Title', enabled=False, default=screening_info['title'])
        self._seatsField = ControlTextArea('Seats', enabled=False)
        self._paidField = ControlCheckBox('Is paid?')
        self._buttonField = ControlButton('Pay')

        # Define the button action
        self._buttonField.value = self.__buttonAction

    def __buttonAction(self):
        self._client.service.ifPlacesFree(self)

    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(ClientReservationWindow)
