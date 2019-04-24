from View import View
from codes import *
import datetime


class Model:

    def __init__(self, is_server=False):
        self.chat_hist = []
        self._view = View()
        self._is_server = is_server
        self.log = []

    def add_message(self, usr, message):
        """
        Notifies the view and adds a message to the database
        :param usr: username
        :param message: actual message
        :return:
        """
        currentDT = datetime.datetime.now()
        date_usr = " ".join([currentDT.strftime("[%d/%m %H:%M]"),usr])
        self.chat_hist.append([date_usr, message])
        self._view.update([NEW_MESSAGE, [date_usr, message]])

    def add_output(self, text):
        """
        Adds a std output to the view.
        :param text: str
        :return:
        """
        self.log.append(text)
        self._view.update([STD_OUT, text])

    def add_err_output(self, text):
        """
        Adds a stderr output to the view.
        :param text:
        :return:
        """
        self.log.append(text)
        self._view.update([STD_ERR, text])

    def report_messages(self, ):
        """
        Returns a string containing all chat history.
        :return: str
        """
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

    @property
    def is_server(self):
        return self._is_server

    def set_is_server(self, value):
        self._is_server = value

    def set_connection_state(self, state):
        self.connection_state = state


if __name__=='__main__':
    model = Model()
    model.add_message("Mefiso", "GG")
    model.add_message("albert752", "The game")
    model.add_message("Mefiso", "Aaaah...tu si kereh listoh")
    print(model.chat)
