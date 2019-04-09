import threading
from model import Model

class Controller ():
    def __init__(self):
        self.model = Model()
        self.backup = self.model

    def startInput (self, line):
        thread = threading.Thread(target=self.read, args=line)
        thread.daemon = True
        thread.start()

    def startOutput (self):
        thread_chat = threading.Thread(target=self.tcp_connection, args=[])
        thread_chat.daemon = True
        thread_chat.start()

    def read(self, args):
        if args[0]== ":":
            #process command
        else:
            self.model().insert(args[0])



