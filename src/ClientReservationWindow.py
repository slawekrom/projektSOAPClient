import asyncio
import json
import os
import shutil
from datetime import datetime

import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton, ControlTextArea, ControlCheckBox
from pyforms.controls import ControlText
from requests import Session

class ClientReservationWindow(BaseWidget):

    def __init__(self, reservation_info: dict, url: str, session: Session):
        BaseWidget.__init__(self, 'Person window')
        # Definition of the forms fields
        self._url = url
        self._session = session
        self._reservation_info = reservation_info
        self._dateField = ControlText('Date', enabled=False,
                                      default=datetime.utcfromtimestamp(
                                          self._reservation_info['showing']['date'] / 1000).replace(
                                          microsecond=self._reservation_info['showing']['date'] % 1000 * 1000).strftime(
                                          "%d-%m-%Y"))
        self._timeField = ControlText('Time', enabled=False,
                                      default=datetime.utcfromtimestamp(
                                          self._reservation_info['showing']['date'] / 1000).replace(
                                          microsecond=self._reservation_info['showing']['date'] % 1000 * 1000).strftime(
                                          "%H:%M"))
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
                        ('_payButton', '_editReservationButton', '_removeReservationButton', '_downloadPdfButton')]

    def _payAction(self):
        if not self._reservation_info['isPaid']:
            updated = {'places': str(self._reservation_info['places']),
                       'paid': str(not self._reservation_info['isPaid']),
                       'userId': self._reservation_info["user"]['id_user'],
                       'showingId': self._reservation_info['showing']['id_showing']}
            self._session.put(self._reservation_info['links'][0]['uri'], json=updated)
            self.message("Thanks for paying for the reservation", "Reservation payed")
            self.close()
            asyncio.get_event_loop().run_until_complete(self.parent.updateInfo())
        else:
            self.warning("You have already paid for the reservation", "Reservation already payed for")
            self.close()

    def _editAction(self):
        if not self._seatsField.enabled and not self._reservation_info['isPaid']:
            self._seatsField.enabled = True
            self._availableSeatsField.show()
            self.message(
                "Choose the seats you would like to book, press edit one more time after you have chosen",
                "Choose the seats")
        elif self._reservation_info['isPaid']:
            self.warning("You can't change a reservation you already paid for", "Reservation already paid for")
            self.close()
        else:
            self._seatsField.enabled = False
            self._availableSeatsField.hide()
            self._session.put(self._reservation_info['links'][0]['uri'], data=json.dumps(
                {'places': str(self._seatsField.value), 'paid': self._reservation_info['isPaid'],
                 'userId': self._reservation_info["user"]['id_user'],
                 'showingId': self._reservation_info['showing']['id_showing']}),
                              headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
            self.message("Places successfully changed", "Changed places")
            self.close()
            asyncio.get_event_loop().run_until_complete(self.parent.updateInfo())

    def _removeAction(self):
        self._session.delete(self._url + f'/reservations/{self._reservation_info["id_reservation"]}')
        self.alert("Reservation has been removed", "Removed reservation")
        self.close()
        asyncio.get_event_loop().run_until_complete(self.parent.updateInfo())

    def _downloadPdfAction(self):
        file = self._session.get(self._reservation_info['links'][1]['uri'],
                                 stream=True)
        if not os.path.exists("../resources/pdfs"):
            os.makedirs("../resources/pdfs")
        with open(
                f'../resources/pdfs/{self._reservation_info["user"]["firstName"]}_{self._reservation_info["user"]["secondName"]}_{self._reservation_info["showing"]["movie"]["title"]}.pdf',
                'wb') as pdf:
            file.raw.decode_content = True
            shutil.copyfileobj(file.raw, pdf)
        file_path = os.path.abspath("../resources/pdfs")
        self.message(
            f"PDF has been saved in {os.path.join(file_path, '{}_{}_{}.pdf'.format(self._reservation_info['user']['firstName'], self._reservation_info['user']['secondName'], self._reservation_info['showing']['movie']['title']))}",
            "PDF generated")
        self.close()
    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(ClientReservationWindow)
