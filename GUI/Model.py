from View import View
from codes import *
import datetime

class Model:

    def __init__(self):
        self.chat_hist = []
        self._view = View()
        self.connection_state = 0

    def add_message(self, usr, message):
        currentDT = datetime.datetime.now()
        date_usr = " ".join([currentDT.strftime("[%d/%m %H:%M]"),usr])
        self.chat_hist.append([date_usr, message])
        self._view.update([NEW_MESSAGE, [date_usr, message]])

    def add_output(self, text):
        self._view.update([STD_OUT, text])

    def add_err_output(self, text):
        self._view.update([STD_ERR, text])

    def report_messages(self, ):
        text_aux = []
        for x in self.chat_hist:
            text_aux.append("> ".join([x[0],x[1]]))
        return "\n".join(text_aux)

    @property
    def view(self):
        return self._view

    @property
    def state(self):
        return self.state

    def set_connection_state(self, state):
        self.connection_state = state

if __name__=='__main__':
    model = Model()
    model.add_message("Mefiso", "GG")
    model.add_message("albert752", "The game")
    model.add_message("Mefiso", "Aaaah...tu si kereh listoh")
    print(model.chat)
