import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton, ControlTextArea, ControlCheckBox, ControlLabel
from suds.client import Client


class DialogWindow(BaseWidget):

    def __init__(self, title: str):
        BaseWidget.__init__(self, '')
        # Definition of the forms fields
        self._titleField = ControlLabel(title)
        self._buttonField = ControlButton('OK')

        # Define the button action
        self._buttonField.value = self.__buttonAction

        self.formset = ['_titleField', '_buttonField']

    def __buttonAction(self):
        self.close()

    # Execute the application


if __name__ == "__main__":
    pyforms.start_app(DialogWindow)
