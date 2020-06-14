import asyncio
import json
import os
import shutil
from datetime import datetime

import cv2
import pyforms
import requests
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton, ControlTextArea, ControlDockWidget, ControlImage, ControlList
from pyforms.controls import ControlText
from requests import Session


class ScreeningWindow(BaseWidget):

    async def downloadImage(self):
        self._image = self._session.get(self._url + f"/movies/image/{self._screening_info['movie']['id_movie']}",
                                        stream=True)
        if not os.path.exists("../resources/images"):
            os.makedirs("../resources/images")
        with open(f'../resources/images/{str(self._screening_info["movie"]["id_movie"])}.jpg', 'wb') as file:
            self._image.raw.decode_content = True
            shutil.copyfileobj(self._image.raw, file)
        self._imageField.value = cv2.imread(f'../resources/images/{str(self._screening_info["movie"]["id_movie"])}.jpg')

    def __init__(self, screening_info: dict, url: str, pesel: str, session: Session):
        BaseWidget.__init__(self, 'Person window')
        # Definition of the forms fields
        self._screening_info = screening_info
        self._url = url
        self._session = session
        self._pesel = pesel
        self._image = None
        self._dateField = ControlText('Date', enabled=False,
                                      default=datetime.strptime(
                                          self._screening_info["date"], '%Y-%m-%dT%H:%M:%SZ[UTC]').strftime("%d-%m-%Y"))
        self._timeField = ControlText('Time', enabled=False,
                                      default=datetime.strptime(
                                          self._screening_info["date"], '%Y-%m-%dT%H:%M:%SZ[UTC]').strftime("%H:%M"))
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
        asyncio.get_event_loop().run_until_complete(self.downloadImage())
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
        if_places_free = json.loads(requests.get(
            self._url + f'/showings/showing?places={self._chosenSeatsField.value}&showingId={self._screening_info["id_showing"]}').text)
        if if_places_free:
            person = json.loads(requests.get(self._url + f'/user/pesel?pesel={self._pesel}').text)
            r = requests.post(self._url + f'/reservations',
                              json={'places': self._chosenSeatsField.value, 'paid': False, 'userId': person['id_user'],
                                    'showingId': self._screening_info['id_showing']})
            print(r.text)
            print(r.content)
            print(r.status_code)
            self.message("Seats successfully booked", 'Booked')
            asyncio.get_event_loop().run_until_complete(self.parent.updateInfo())
            self.close()
        else:
            self.alert("At least one place is taken, change your places", "Warning")


# Execute the application
if __name__ == "__main__":
    pyforms.start_app(ScreeningWindow)
