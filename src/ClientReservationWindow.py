import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton, ControlTextArea, ControlCheckBox
from suds.client import Client

from src.DialogWindow import DialogWindow


class ClientReservationWindow(BaseWidget):

    def __init__(self, reservation_info: dict, client: Client):
        BaseWidget.__init__(self, 'Person window')
        # Definition of the forms fields
        self._client = client
        self._reservation_info = reservation_info
        self._dateField = ControlText('Date', enabled=False,
                                      default=self._reservation_info['showing']['date'].strftime("%d-%m-%Y"))
        self._timeField = ControlText('Time', enabled=False,
                                      default=self._reservation_info['showing']['date'].strftime("%H:%M"))
        self._titleField = ControlText('Title', enabled=False,
                                       default=str(self._reservation_info['showing']['movie']['title']))
        self._seatsField = ControlTextArea('Seats', enabled=False, default=str(self._reservation_info['places']))
        self._paidField = ControlCheckBox('Is paid?', enabled=False, default=self._reservation_info['isPaid'])
        self._payButton = ControlButton('Pay')
        self._editReservationButton = ControlButton('Edit')
        self._removeReservationButton = ControlButton('Remove')

        # Define the button action
        self._payButton.value = self._payAction
        self._editReservationButton.value = self._editAction
        self._removeReservationButton.value = self._removeAction

        self.formset = [('_dateField', '_timeField'), '_titleField', '_seatsField', '_paidField',
                        ('_payButton', '_editReservationButton', '_removeReservationButton')]

    def _payAction(self):
        # self._client.service.editReservation()
        pass

    def _editAction(self):
        self._client.service.ifPlacesFree(self)

    def _removeAction(self):
        self._client.service.deleteReservation(self._reservation_info['id_reservation'])
        win = DialogWindow("Reservation has been removed")
        # win.parent = self
        win.show()
        self.close()
        self.parent.updateInfo()

    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(ClientReservationWindow)
