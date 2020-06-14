import json

import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton, ControlPassword, ControlText, ControlDockWidget
from requests import Session

from src.RegisterWindow import RegisterWindow


class LoginWindow(BaseWidget):

    def __init__(self, url: str, session: Session):
        BaseWidget.__init__(self, 'Login')
        # Definition of the forms fields
        self._url = url
        self._session = session
        self._loginField = ControlText("PESEL:")
        self._passwordField = ControlPassword("Password:")
        self._loginButton = ControlButton("Login")
        self._registerButton = ControlButton("Register")
        # Define the button action
        self._loginButton.value = self._loginAction
        self._registerButton.value = self._registerAction
        self._panel = ControlDockWidget()
        self._panel.hide()

        self.formset = ['_loginField', '_passwordField', ('_loginButton', '_registerButton')]

    def _loginAction(self):
        if_authorized = json.loads(self._session.get(
            self._url + f"/user/auth?pesel={str(self._loginField.value)}&password={str(self._passwordField.value)}").text)
        if if_authorized:
            self.message("Logged in", "Logged in")
            self.parent.setUserPesel(self._loginField.value)
            self.parent.show()
            self.close()
        else:
            self.alert("Credentials are incorrect, try again", "Wrong credentials")

    def _registerAction(self):
        win = RegisterWindow(self._url, self._session)
        win.parent = self
        win.show()
    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(LoginWindow)
