import io
import os

import cv2
import pyforms
from PIL import Image
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton, ControlTextArea, ControlDockWidget, ControlImage, ControlList
from pyforms.controls import ControlText
from zeep import Client


class ScreeningWindow(BaseWidget):

    def __init__(self, screening_info: dict, client: Client, pesel: str):
        BaseWidget.__init__(self, 'Person window')
        # Definition of the forms fields
        self._screening_info = screening_info
        self._client = client
        self._pesel = pesel
        self._image = self._client.service.getImage(self._screening_info['movie']['id_movie'])
        image_open = Image.open(io.BytesIO(self._image))
        rgb_im = image_open.convert('RGB')
        if not os.path.exists("../resources/images"):
            os.makedirs("../resources/images")
        rgb_im.save(f'../resources/images/{str(self._screening_info["movie"]["id_movie"])}.jpg')
        self._dateField = ControlText('Date', enabled=False,
                                      default=self._screening_info['date'].strftime("%d-%m-%Y"))
        self._timeField = ControlText('Time', enabled=False, default=self._screening_info['date'].strftime("%H:%M"))
        self._titleField = ControlText('Title', enabled=False, default=self._screening_info['movie']['title'])
        self._descriptionField = ControlTextArea('Description', enabled=False,
                                                 default=self._screening_info['movie']['description'])
        self._actorField = ControlList('Actors', enabled=False)
        self._actorField.horizontal_headers = ['Name', 'Surname']
        for actor in self._screening_info['movie']['actors']:
            self._actorField += [actor['firstName'], actor['secondName']]
        self._directorField = ControlList("Director", enabled=False)
        self._directorField.horizontal_headers = ['Name', 'Surname']
        self._directorField += [self._screening_info['movie']['director']['firstName'],
                                self._screening_info['movie']['director']['secondName']]
        self._imageField = ControlImage('Poster')
        self._imageField.value = cv2.imread(f'../resources/images/{str(self._screening_info["id_showing"])}.jpg')
        self._freeSeatsField = ControlTextArea('Free seats', enabled=False, default=self._screening_info['freePlaces'])
        self._chosenSeatsField = ControlText('Chosen seats (write down the numbers and separate them with ";")')
        self._buttonField = ControlButton('Reserve')
        self._panel = ControlDockWidget()
        # Define the button action
        self._buttonField.value = self.__buttonAction

        self.formset = [('_dateField', '_timeField'), ('_imageField', ['_titleField', '_descriptionField']),
                        ('_directorField', '_actorField'),
                        ('_freeSeatsField', '_chosenSeatsField'), '_buttonField', '_panel']

    def __buttonAction(self):
        if_places_free = self._client.service.ifPlacesFree(self._chosenSeatsField.value,
                                                           self._screening_info['id_showing'])
        print(if_places_free)
        if if_places_free:
            person = self._client.service.getPersonByPesel(self._pesel)
            self._client.service.addNewReservation(self._chosenSeatsField.value, False, person['id_person'],
                                                   self._screening_info['id_showing'])
            print("Reservation added")
            self.message("Seats successfully booked", 'Booked')
            self.parent.updateInfo()
            self.close()
            # win.parent = self
            # win.show()
        else:
            self.alert("At least one place is taken, change your places", "Warning")

    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(ScreeningWindow)
