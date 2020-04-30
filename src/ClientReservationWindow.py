import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton, ControlTextArea


class ClientReservationWindow(BaseWidget):

    def __init__(self, screening_info: dict):
        print(screening_info)
        BaseWidget.__init__(self, 'Person window')
        # Definition of the forms fields
        self._dateField = ControlText('Date', enabled=False, default=screening_info['date'])
        self.__timeField = ControlText('Time', enabled=False, default=screening_info['time'])
        self._titleField = ControlText('Title', enabled=False, default=screening_info['title'])
        self._freeSeatsField = ControlTextArea('Free seats', enabled=False)
        self._chosenSeatsField = ControlText('Chosen seats (write down the numbers and separate them with ";"')
        self._buttonField = ControlButton('Reserve')

        # Define the button action
        self._buttonField.value = self.__buttonAction

    def __buttonAction(self):
        self.close()

    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(ClientReservationWindow)
