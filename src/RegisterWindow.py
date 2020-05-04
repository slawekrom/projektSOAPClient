import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton, ControlPassword, ControlText
from zeep import Client


class RegisterWindow(BaseWidget):

    def __init__(self, client: Client):
        BaseWidget.__init__(self, 'Login')
        # Definition of the forms fields
        self._client = client
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
            if_user_exists = self._client.service.checkIfUserExist(str(self._peselField.value))
            if if_user_exists:
                self.alert("User with this PESEL already exists, change it", "Existing user")
            else:
                self._client.service.addUser(str(self._nameField.value), str(self._surnameField.value),
                                             str(self._peselField.value), str(self._passwordField.value))
                self.message("User created, log in with your credentials", "Registration successful")
                self.close()
        else:
            self.alert("Passwords don't match", "Incorrect passwords")

    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(RegisterWindow)
