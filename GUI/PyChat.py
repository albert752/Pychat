#!/usr/bin/python3

import gi
from Model import Model
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GObject
from TCP.client import Client
from codes import *
import sys
from threading import Thread
from server import server


class Controller(object):

    def __init__(self, model):
        """
        Initialites the whole app
        :param model: Instance of the desired model
        """
        self._model = model
        self._client = None
        self.username = ""

        self._model.view.connect('send', self.send)
        self._model.view.connect('destroy', Gtk.main_quit)

        self._model.view.show_all()
        try:
            if sys.argv[1] == "-s":
                self._model.set_is_server(True)
                def _target():
                    try:
                        s = server()
                        s.run()
                    except:
                        self._model.set_is_server(False)
                thread = Thread(target=_target)
                thread.daemon = True
                thread.start()
        except:
            print("Server could not be lauched")

    def send(self, *args):
        """
        Parses the typed command typed on the send entry.
        :param args:
        :return:
        """
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
                    self._client.listen(self.receive, self._model.add_output)
                except:
                    self._model.add_err_output("Error while connecting to the server.")

            elif command == "help":
                try:
                    with open("/usr/share/PyChat/var/help.outpt", 'r') as fp:
                        text=fp.read()
                    self._model.add_output(text)
                except:
                    self._model.add_err_output("Error while reading help file")
            elif command == "server":
                self._model.add_output(str(self._model.is_server))
            elif command == "close":
                self.close()
            elif command == "save":
                self._save_conver(path=arguments)
            else:
                self._model.add_err_output("Command not found.")

        else:
            self._client.send_message(args)
            self._model.add_message(self.username, args)

    def receive(self, username, message):
        """
        Saves the received message to the model
        :param username: Str with the uname of the src
        :param message: Str with the actual message
        :return:
        """
        self._model.add_message(username, message)

    def _save_conver(self, path="./history.txt"):
        """
        Saves the conversation to the given path. It will overwrite!
        :param path: str cintaining the full or relative path to the file.
        :return:
        """
        try:
            with open(path, 'w') as fp:
                fp.write(self._model.report_messages())
            self._model.add_output("Conversation saved succesfuly")
        except:
            self._model.add_err_output("Error while saving the conversation")

    def close(self):
        """
        If open, closes the TCP connection and clears its variables.
        :return:
        """
        if self._client is not None:
            self._client.disconnect(self._model.add_output)
            self._client = None
            self.username = ""


if __name__ == '__main__':

    app = Controller(Model())
    Gtk.main()
    app.close()

