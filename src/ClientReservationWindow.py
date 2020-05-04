import os

import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton, ControlTextArea, ControlCheckBox
from zeep import Client

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
        self._availableSeatsField = ControlTextArea('Available seats', enabled=False, visible=False,
                                                    default=str(self._reservation_info['showing']['freePlaces']))
        self._seatsField = ControlTextArea('Seats', enabled=False, default=str(self._reservation_info['places']))
        self._paidField = ControlCheckBox('Is paid?', enabled=False, default=self._reservation_info['isPaid'])
        self._payButton = ControlButton('Pay')
        self._downloadPdfButton = ControlButton('Download PDF')
        self._editReservationButton = ControlButton('Edit')
        self._removeReservationButton = ControlButton('Remove')

        # Define the button action
        self._payButton.value = self._payAction
        self._editReservationButton.value = self._editAction
        self._removeReservationButton.value = self._removeAction
        self._downloadPdfButton.value = self._downloadPdfAction

        self.formset = [('_dateField', '_timeField'), '_titleField', '_availableSeatsField', '_seatsField',
                        '_paidField',
                        ('_payButton', '_editReservationButton', '_removeReservationButton','_downloadPdfButton')]

    def _payAction(self):
        if not self._reservation_info['isPaid']:
            self._client.service.editReservation(self._reservation_info['id_reservation'],
                                                 self._reservation_info['places'],
                                                 not self._reservation_info['isPaid'])
            win = DialogWindow("Thanks for paying for the reservation")
            win.show()
            self.close()
            self.parent.updateInfo()
        else:
            win = DialogWindow("You have already paid for the reservation")
            win.show()
            self.close()

    def _editAction(self):
        if not self._seatsField.enabled and not self._reservation_info['isPaid']:
            print("Seats disabled")
            self._seatsField.enabled = True
            print("Seats enabled")
            self._availableSeatsField.show()
            print("Seats visible")
            win = DialogWindow(
                "Choose the seats you would like to book, press edit one more time after you have chosen")
            win.show()
        elif self._reservation_info['isPaid']:
            win = DialogWindow("You can't change a reservation you already paid for")
            win.show()
            self.close()
        else:
            print("Seats enabled")
            self._seatsField.enabled = False
            self._availableSeatsField.hide()
            self._client.service.editReservation(self._reservation_info['id_reservation'],
                                                 str(self._seatsField.value),
                                                 self._reservation_info['isPaid'])
            win = DialogWindow("Places successfully changed")
            win.show()
            self.close()
            self.parent.updateInfo()

    def _removeAction(self):
        self._client.service.deleteReservation(self._reservation_info['id_reservation'])
        win = DialogWindow("Reservation has been removed")
        win.show()
        self.close()
        self.parent.updateInfo()

    def _downloadPdfAction(self):
        file = self._client.service.getPDFofReservation(self._reservation_info['id_reservation'])
        print(file)
        if not os.path.exists("../resources/pdfs"):
            os.makedirs("../resources/pdfs")
        with open(f'../resources/pdfs/{self._reservation_info["person"]["firstName"]}_{self._reservation_info["person"]["secondName"]}_{self._reservation_info["showing"]["movie"]["title"]}.pdf','wb') as pdf:
            pdf.write(file)
        win = DialogWindow(f"PDF has been saved in {os.path.join(os.getcwd(),'../resources/pdfs/')}")
        win.show()
        self.close()
    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(ClientReservationWindow)
