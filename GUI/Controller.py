import gi
from Model import Model
from View import View
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from TCP.client import Client
from TCP.server import Server


class Controller(object):

    def __init__(self, model, view):
        self._model = model
        self._view = view

        self._client = Client("albert752")
        self._client.start()

        self._view.connect('send', self.send)
        self._view.connect('destroy', Gtk.main_quit)

        self._view.show_all()

    def send(self, *args):
        self._client.send_message(args[1])


if __name__ == '__main__':
    Controller(Model(), View())
    Gtk.main()
