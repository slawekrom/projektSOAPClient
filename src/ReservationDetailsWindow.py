import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton, ControlTextArea, ControlDockWidget
from zeep import Client

from src.DialogWindow import DialogWindow


class ReservationDetailsWindow(BaseWidget):

    def __init__(self, client: Client, seats: str, screening_info: dict):
        BaseWidget.__init__(self, 'Person window')
        # Definition of the forms fields
        self._client = client
        self._screening_info = screening_info
        self._seats = seats
        self._nameField = ControlText('Name')
        self._surnameField = ControlText('Surname')
        self._peselField = ControlText('PESEL')
        self._buttonField = ControlButton('Reserve')
        # Define the button action
        self._buttonField.value = self.__buttonAction
        print("ReservationDetails:", self._client, self._seats, self._screening_info)

    def __buttonAction(self):
        print(self._peselField.value)
        person_exists = self._client.service.checkIfPersonExist(str(self._peselField.value))
        if not person_exists:
            print("Before commit")
            self._client.service.addPerson(self._nameField.value, self._surnameField.value, self._peselField.value)
            person = self._client.service.getPersonByPesel(str(self._peselField.value))
            print("Person commited")
        else:
            person = self._client.service.getPersonByPesel(str(self._peselField.value))
            win = DialogWindow(
                f"User already exists, adding to user with name: {person['firstName'] + ' ' + person['secondName']}")
            win.parent = self
            win.show()

        self._client.service.addNewReservation(self._seats, False, person['id_person'],
                                               self._screening_info['id_showing'])

        win = DialogWindow("Seats successfully booked")
        win.parent = self
        win.show()
        self.close()
        self.parent.close()
        self.parent.parent.updateInfo()
    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(ReservationDetailsWindow)
