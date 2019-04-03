import gi, os, sys
import datetime

gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject, GdkPixbuf, Gdk, Pango
from pprint import pprint as pp

WORKINGDIR = os.getcwd()

class Window(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Pychat")
        self.set_default_size(400, 700)
        self.set_resizable(False)

        self.create_layout()

        self.create_conversation_textview()
        self.create_message_entry()
        self.create_send_button()
        self.create_top_menubar()

        self.apply_styles()


    def create_layout(self):
        self.grid = Gtk.Grid()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)
        self.box.pack_start(self.grid, True, True, 0)

    def apply_styles(self):
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path('./styles/main.css')
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def create_send_button(self):
        send_button = Gtk.Button(label="Send!", name="send_button")
        self.grid.attach(send_button, 1, 2, 1, 1)

    def create_message_entry(self):
        message_entry = Gtk.Entry(name="message_entry")
        message_entry.set_text("Type here your message...")
        self.grid.attach(message_entry, 0, 2, 1, 1)

    def create_conversation_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 2, 1)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.CHAR)

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("This is some text inside of a Gtk.TextView. "
                                 + "Select text and click one of the buttons 'bold', 'italic', "
                                 + "or 'underline' to modify the text accordingly.")
        scrolledwindow.add(self.textview)

        self.tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
        self.tag_italic = self.textbuffer.create_tag("italic", style=Pango.Style.ITALIC)
        self.tag_underline = self.textbuffer.create_tag("underline", underline=Pango.Underline.SINGLE)
        self.tag_found = self.textbuffer.create_tag("found", background="yellow")

    def create_top_menubar(self):
        menubar = Gtk.MenuBar()
        im = Gtk.MenuItem('About')
        # im.set_action_and_target_value()
        menubar.append(im)
        self.grid.attach(menubar, 0, 0, 2, 1)



if __name__ == '__main__':
    win = Window()
    win.show_all()
    Gtk.main()
