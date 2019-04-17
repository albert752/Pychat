from View import View
from codes import *


class Model:

    def __init__(self):
        self.chat_hist = []
        self._view = View()

    def add_message(self, usr, message):
        self.chat_hist.append({usr: message})
        self._view.update([NEW_MESSAGE, [usr, message]])

    def add_output(self, text):
        self._view.update([STD_OUT, text])

    def add_err_output(self, text):
        self._view.update([STD_ERR, text])

    @property
    def view(self):
        return self._view
