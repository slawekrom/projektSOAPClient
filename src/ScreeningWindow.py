import io
import os

import cv2
import pyforms
from PIL import Image
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton, ControlTextArea, ControlDockWidget, ControlImage
from zeep import Client
from numpy import asarray

from src.DialogWindow import DialogWindow
from src.ReservationDetailsWindow import ReservationDetailsWindow


class ScreeningWindow(BaseWidget):

    def __init__(self, screening_info: dict, client: Client):
        BaseWidget.__init__(self, 'Person window')
        # Definition of the forms fields
        self._screening_info = screening_info
        self._client = client
        self._image = self._client.service.getImage(self._screening_info['movie']['id_movie'])
        image_open = Image.open(io.BytesIO(self._image))
        rgb_im = image_open.convert('RGB')
        if not os.path.exists("../resources/images"):
            os.makedirs("../resources/images")
        rgb_im.save(f'../resources/images/{str(self._screening_info["movie"]["id_movie"])}.jpg')
        self._dateField = ControlText('Date', enabled=False,
                                          default=self._screening_info['date'].strftime("%d-%m-%Y"))
        self.__timeField = ControlText('Time', enabled=False, default=self._screening_info['date'].strftime("%H:%M"))
        self._titleField = ControlText('Title', enabled=False, default=self._screening_info['movie']['title'])
        self._imageField = ControlImage('Poster')
        self._imageField.value = cv2.imread(f'../resources/images/{str(self._screening_info["id_showing"])}.jpg')
        self._freeSeatsField = ControlTextArea('Free seats', enabled=False, default=self._screening_info['freePlaces'])
        self._chosenSeatsField = ControlText('Chosen seats (write down the numbers and separate them with ";")')
        self._buttonField = ControlButton('Reserve')
        self._panel = ControlDockWidget()
        # Define the button action
        self._buttonField.value = self.__buttonAction

    def __buttonAction(self):
        if self._client.service.ifPlacesFree(self._chosenSeatsField.value, self._screening_info['id_showing']):
            win = ReservationDetailsWindow(self._client, self._chosenSeatsField.value, self._screening_info)
            win.parent = self
            self._panel.show()
            self._panel.label = "Reservation info"
            self._panel.value = win
        else:
            win = DialogWindow("At least one place is taken, change your places")
            win.parent = self
            win.show()

    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(ScreeningWindow)
