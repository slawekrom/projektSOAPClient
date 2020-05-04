import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton, ControlPassword, ControlText, ControlDockWidget
from zeep import Client

from src.RegisterWindow import RegisterWindow


class LoginWindow(BaseWidget):

    def __init__(self, client: Client):
        BaseWidget.__init__(self, 'Login')
        # Definition of the forms fields
        self._client = client
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
        self.parent.show()
        self.parent.setUserPesel(self._loginField.value)
        self.close()

    def _registerAction(self):
        win = RegisterWindow(self._client)
        win.parent = self
        win.show()
    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(LoginWindow)
