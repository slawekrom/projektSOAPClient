import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton, ControlPassword, ControlText
from zeep import Client


class RegisterWindow(BaseWidget):

    def __init__(self,client:Client):
        BaseWidget.__init__(self, 'Login')
        # Definition of the forms fields
        self._client = client
        self._nameField = ControlText("Name:")
        self._surnameField = ControlText("Surname:")
        self._loginField = ControlText("PESEL:")
        self._passwordField = ControlPassword("Password:")
        self._registerButton = ControlButton("Register")
        # Define the button action
        self._registerButton.value = self._registerAction

    def _registerAction(self):
        self.close()

    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(RegisterWindow)
