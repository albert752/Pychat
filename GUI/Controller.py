import gi
from Model import Model
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GObject
from TCP.client import Client
from codes import *
import json


class Controller(object):

    def __init__(self, model):
        self._model = model
        self._client = None
        self.username = ""

        self._model.view.connect('send', self.send)
        self._model.view.connect('destroy', Gtk.main_quit)

        self._model.view.show_all()

    def send(self, *args):
        args = args[1]
        if args[0] == COMAND_SCAPE_CHAR:

            command = args[1:].split(' ')
            if len(command) > 1:
                arguments = command[1]
            command = command[0]

            if command == "open":
                try:
                    self.username = arguments.split('@')[0]
                    ip = arguments.split('@')[1].split(':')[0]
                    port = int(arguments.split('@')[1].split(':')[1])

                    self._client = Client(self.username, ip, port)
                    self._client.start(self._model.add_output)
                    self._client.listen(self.receive)
                except:
                    self._model.add_err_output("Error while connecting to the server.")

            elif command == "help":
                self._model.add_output("Possible commands:\t:open (username)@(ip):(port)\n\t\tUsed to open connection")

            elif command == "close":
                self._client.disconnect(self._model.add_output)
                self._client = None
                self.username = ""
            elif command == "save":
                try:
                    with open(arguments, 'w') as fp:
                        fp.write(self._model.report_messages())
                    self._model.add_output("Conversation saved succesfuly")
                except:
                    self._model.add_err_output("Error while saving the conversation")
            else:
                self._model.add_err_output("Command not found.")

        else:
            self._client.send_message(args)
            self._model.add_message(self.username, args)

    def receive(self, username, message):
        self._model.add_message(username, message)

    def close(self):
        if self._client is not None:
            self._client.disconnect(self._model.add_output)


if __name__ == '__main__':
    app = Controller(Model())
    Gtk.main()
    app.close()

