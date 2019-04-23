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
        self.create_toolbar()
        self.create_about_link_button()

        self.apply_styles()

    # Styles
    def apply_styles(self):
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path('./styles/main.css')
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    # Creation of the layout and widgets
    def create_layout(self):
        self.grid = Gtk.Grid()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)
        self.box.pack_start(self.grid, True, True, 0)

    def create_send_button(self):
        send_button = Gtk.Button(label="Send!", name="send_button")
        send_button.connect("clicked", self.on_send_button_clicked)
        self.grid.attach(send_button, 5, 2, 1, 1)

    def create_message_entry(self):
        self.message_entry = Gtk.Entry(name="message_entry")
        self.message_entry.set_text(":open albert752@127.0.0.1:1234")
        self.message_entry.connect("activate", self.on_enter_message_entry)
        self.grid.attach(self.message_entry, 0, 2, 5, 1)

    def create_conversation_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 6, 1)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.CHAR)
        self.textview.set_editable(False)

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("Welcome to Pychat!, enter help to see a list of available commands.")
        scrolledwindow.add(self.textview)

        self.tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
        self.tag_italic = self.textbuffer.create_tag("italic", style=Pango.Style.ITALIC)
        self.tag_underline = self.textbuffer.create_tag("underline", underline=Pango.Underline.SINGLE)
        self.tag_found = self.textbuffer.create_tag("found", background="yellow")

    def create_toolbar(self):
        toolbar = Gtk.Box(spacing=5)
        self.grid.attach(toolbar, 0, 0, 6, 1)

        title_label = Gtk.Label()
        title_label.set_markup("<big>PyChat</big>")
        toolbar.pack_start(title_label, True, True, 0)

        self.search_entry = Gtk.Entry(name="message_entry")
        toolbar.pack_start(self.search_entry, True, True, 0)
        self.search_entry.connect("activate", self.on_search_clicked)

        button_search = Gtk.Button(label="Serach")
        button_search.connect("clicked", self.on_search_clicked)
        toolbar.pack_start(button_search, True, True, 0)

    def create_about_link_button(self):
        button = Gtk.LinkButton("https://github.com/albert752/Pychat", "© SevenFiveTwo - About", name="about")
        self.grid.attach(button,  0, 3, 12, 1)
        button.connect("clicked", self.about)

    # Widget handlers
    def on_send_button_clicked(self, widget):
        self.emit('send', self.message_entry.get_text())
        self.message_entry.set_text("")

    def on_enter_message_entry(self, widget):
        self.emit('send', self.message_entry.get_text())
        self.message_entry.set_text("")

    def on_save_button_clicked(self, widget):
        pass

    def on_close_button_clicked(self, widget):
        pass

    def on_search_clicked(self, widget):
        cursor_mark = self.textbuffer.get_insert()
        start = self.textbuffer.get_iter_at_mark(cursor_mark)
        if start.get_offset() == self.textbuffer.get_char_count():
            start = self.textbuffer.get_start_iter()

        def _handler(match_start, match_end):
            self.textbuffer.apply_tag(self.tag_found, match_start, match_end)
        self._search(self.search_entry.get_text(), start, _handler)

    def about(self, widget, data=None):

        APP_TITLE = "PyChat"
        APP_LICENCE = "MIT - More details at https://github.com/albert752/Pychat/blob/master/LICENSE"
        APP_COMMENTS = "A simple but powerful Py(thon) Chat"
        APP_COPYRIGHT = "albert752, jplanas98 and mefiso"
        HOME_PAGE = "https://github.com/albert752/Pychat/b"
        APP_AUTHORS = ["albert752","jplanas98","mefiso"]

        about_dialog = Gtk.AboutDialog()
        dialog = about_dialog
        dialog.set_name(APP_TITLE)

        try:
            data = open('./LICENSE', 'r').read()
            dialog.set_license(data)
        except:
            dialog.set_license(APP_LICENCE)

        dialog.set_authors(APP_AUTHORS)
        dialog.set_comments(APP_COMMENTS)
        dialog.set_copyright(APP_COPYRIGHT)
        dialog.set_website(HOME_PAGE)
        dialog.run()
        dialog.destroy()

    # Updating methods
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
        GLib.idle_add(self._set_format_text)

    def update_conversation_textview_message(self, payload):
        self.textbuffer.insert(self.textbuffer.get_end_iter(), '\n*'+payload[0] + ' > *')
        self.textbuffer.insert(self.textbuffer.get_end_iter(), payload[1])

    def update_conversation_textview_stdout(self, payload):
        self.textbuffer.insert(self.textbuffer.get_end_iter(), '\n_[OK]: ' + payload+'_')

    def update_conversation_textview_stderr(self, payload):
        self.textbuffer.insert(self.textbuffer.get_end_iter(), '\n_[ER]: ' + payload+'_')

    # Private support methods
    def _set_format_text(self):
        self._set_style_text('*', self.tag_bold)
        self._set_style_text('_', self.tag_italic)
        self._set_style_text('-', self.tag_underline)
        self._search('*', self.textbuffer.get_start_iter(), self.textbuffer.delete)
        self._search('_', self.textbuffer.get_start_iter(), self.textbuffer.delete)
        self._search('-', self.textbuffer.get_start_iter(), self.textbuffer.delete)

    def _set_style_text(self, text, tag, start=None):
        if start is None:
            start = self.textbuffer.get_start_iter()
        EOB = self.textbuffer.get_end_iter()

        match = start.forward_search(text, 0, EOB)

        if match is not None:
            start, end = match
            match = end.forward_search(text, 0, EOB)
            _, end = match
            self.textbuffer.apply_tag(tag, start, end)
            self._set_style_text(text, tag, start=end)

    def _search(self, text, start, handler):
        end = self.textbuffer.get_end_iter()
        match = start.forward_search(text, 0, end)

        if match is not None:
            match_start, match_end = match
            handler(match_start, match_end)
            self._search(text, match_end, handler)
