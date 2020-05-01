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
        self._dateField = ControlText('Date', enabled=False, default=self._screening_info['date'].strftime("%d-%m-%Y"))
        self.__timeField = ControlText('Time', enabled=False, default=self._screening_info['date'].strftime("%H:%M"))
        self._titleField = ControlText('Title', enabled=False, default=self._screening_info['movie']['title'])
        self._seatsField = ControlTextArea('Seats', enabled=False)
        self._paidField = ControlCheckBox('Is paid?')
        self._payButton = ControlButton('Pay')
        self._editReservationButton = ControlButton('Edit')
        self._removeReservationButton = ControlButton('Remove')

        # Define the button action
        self._payButton.value = self._payAction
        self._editReservationButton.value = self._editAction
        self._removeReservationButton.value = self._removeAction

        self.formset = ['_titleField', '_buttonField']

    def _payAction(self):
        self._client.service.ifPlacesFree(self)

    def _editAction(self):
        self._client.service.ifPlacesFree(self)

    def _removeAction(self):
        self._client.service.ifPlacesFree(self)

    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(ClientReservationWindow)
