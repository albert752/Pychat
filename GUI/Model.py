from View import View
from codes import *


class Model:

    def __init__(self):
        self.chat_hist = []
        self._view = View()
        self.connection_state = 0

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

    @property
    def state(self):
        return self.state

    def set_connection_state(self, state):
        self.connection_state = state
