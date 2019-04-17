import gi, os, sys
import datetime
from codes import *

gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject, GdkPixbuf, Gdk, Pango
from pprint import pprint as pp

WORKINGDIR = os.getcwd()

class View(Gtk.Window):
    __gsignals__ = {
        'send': (GObject.SignalFlags.RUN_FIRST, None, (str,))
    }

    def __init__(self):
        Gtk.Window.__init__(self, title="Pychat")
        self.set_default_size(450, 700)
        self.set_resizable(False)

        self.create_layout()

        self.create_conversation_textview()
        self.create_message_entry()
        self.create_send_button()
        self.create_top_menubar()

        self.apply_styles()

    def apply_styles(self):
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path('./styles/main.css')
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def create_layout(self):
        self.grid = Gtk.Grid()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)
        self.box.pack_start(self.grid, True, True, 0)

    def create_send_button(self):
        send_button = Gtk.Button(label="Send!", name="send_button")
        send_button.connect("clicked", self.on_send_button_clicked)
        self.grid.attach(send_button, 1, 2, 1, 1)

    def create_message_entry(self):
        self.message_entry = Gtk.Entry(name="message_entry")
        self.message_entry.set_text(":open albert752@127.0.0.1:1234")
        self.message_entry.connect("activate", self.on_enter_message_entry)
        self.grid.attach(self.message_entry, 0, 2, 1, 1)

    def create_conversation_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 2, 1)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.CHAR)
        self.textview.set_editable(False)

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("Welcome to Pychat!, enter help to see a list of available commands.")
        scrolledwindow.add(self.textview)

        tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
        tag_italic = self.textbuffer.create_tag("italic", style=Pango.Style.ITALIC)
        tag_underline = self.textbuffer.create_tag("underline", underline=Pango.Underline.SINGLE)
        tag_found = self.textbuffer.create_tag("found", background="yellow")

    def create_top_menubar(self):
        mb = Gtk.MenuBar()
        menu1 = Gtk.Menu()

        settings_menu = Gtk.MenuItem(label="Settings")
        #1settings_menu.set_submenu(menu1)

        #chk = Gtk.CheckMenuItem(label="Checkable")
        #menu1.append(chk)
        #radio1 = Gtk.RadioMenuItem(None, label="Radio1")
        #radio2 = Gtk.RadioMenuItem(radio1, label="Radio2")
        #menu1.append(radio1)
        #menu1.append(radio2)
        #sep = Gtk.SeparatorMenuItem()
        #menu1.append(sep)
        #menu2 = Gtk.Menu()

        about_entry = Gtk.MenuItem(label="About")
        #about_entry.connect("clicked", self.on_send_button_clicked)

        mb.append(settings_menu)
        mb.append(about_entry)
        self.grid.attach(mb, 0, 0, 2, 1)

    def on_send_button_clicked(self, widget):
        self.emit('send', self.message_entry.get_text())
        self.message_entry.set_text("")

    def on_enter_message_entry(self, widget):
        self.emit('send', self.message_entry.get_text())
        self.message_entry.set_text("")

    def about(self, widget, data=None):

        APP_TITLE = "PYCHAT"
        APP_LICENCE = "MIT"
        APP_COMMENTS = "hello"
        APP_COPYRIGHT = "..MIT"
        HOME_PAGE = "Hello"
        APP_AUTHORS = "me"

        about_dialog = Gtk.AboutDialog()
        dialog = about_dialog
        dialog.set_name(APP_TITLE)

        try:
            data = open('/usr/share/doc/nativecam/copyright', 'r').read()
            dialog.set_license(data)
        except:
            dialog.set_license(APP_LICENCE)

        dialog.set_authors(APP_AUTHORS)
        dialog.set_comments(APP_COMMENTS)
        dialog.set_copyright(APP_COPYRIGHT)
        dialog.set_website(HOME_PAGE)
        dialog.run()
        dialog.destroy()

    def update(self, payload):

        if payload[0] == NEW_MESSAGE:
            handler = self.update_conversation_textview_message
            params = payload[1]
        elif payload[0] == STD_OUT:
            handler = self.update_conversation_textview_stdout
            params = payload[1]
        elif payload[0] == STD_ERR:
            handler = self.update_conversation_textview_stderr
            params = payload[1]

        GLib.idle_add(handler, params)

    def update_conversation_textview_message(self, payload):
        self.textbuffer.insert(self.textbuffer.get_end_iter(), '\n'+payload[0] + ' > ' + payload[1])

    def update_conversation_textview_stdout(self, payload):
        print("This is the payload " + payload)
        self.textbuffer.insert(self.textbuffer.get_end_iter(), '\n[OK]: ' + payload)

    def update_conversation_textview_stderr(self, payload):
        self.textbuffer.insert(self.textbuffer.get_end_iter(), '\n[ER]: ' + payload)