import json

import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton, ControlPassword, ControlText
from requests import Session


class RegisterWindow(BaseWidget):

    def __init__(self, url: str,session:Session):
        BaseWidget.__init__(self, 'Login')
        # Definition of the forms fields
        self._url = url
        self._session=session
        self._nameField = ControlText("Name:")
        self._surnameField = ControlText("Surname:")
        self._peselField = ControlText("PESEL:")
        self._passwordField = ControlPassword("Password:")
        self._confirmPasswordField = ControlPassword("Confirm password:")
        self._registerButton = ControlButton("Register")
        # Define the button action
        self._registerButton.value = self._registerAction

    def _registerAction(self):
        if self._passwordField.value == self._confirmPasswordField.value:
            if_user_exists = json.loads(self._session.get(self._url + f'/user/pesel/{str(self._peselField.value)}').text)
            if if_user_exists:
                self.alert("User with this PESEL already exists, change it", "Existing user")
            else:
                self._session.post(self._url + '/user', json={'firstName': str(self._nameField.value), "secondName": str(
                    self._surnameField.value), 'pesel': str(self._peselField.value),
                                                         'password': str(self._passwordField.value)})
                self.message("User created, log in with your credentials", "Registration successful")
                self.close()
        else:
            self.alert("Passwords don't match", "Incorrect passwords")

    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(RegisterWindow)
