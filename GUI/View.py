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
        #self.create_top_menubar()
        self.create_toolbar()
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
        self.grid.attach(send_button, 5, 2, 1, 1)
        #send_button.set_property("width-request", 1)
        #send_button.set_property("height-request", 1)

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
        toolbar = Gtk.Toolbar()
        self.grid.attach(toolbar, 0, 0, 6, 1)

        save_button = Gtk.ToolButton(label="Save")
        toolbar.insert(save_button, 0)

        save_button.connect("clicked", self.on_save_button_clicked)

        toolbar.insert(Gtk.SeparatorToolItem(), 1)

        title_label = Gtk.Label()
        title_label.set_markup("<big>PyChat</big>")
        #toolbar.insert(title_label, 2)

        toolbar.insert(Gtk.SeparatorToolItem(), 3)

        close_button = Gtk.ToolButton()
        close_button.set_icon_name("edit-clear-symbolic")
        close_button.connect("clicked", self.on_close_button_clicked)
        toolbar.insert(close_button, 4)

        toolbar.insert(Gtk.SeparatorToolItem(), 5)

        self.search_entry = Gtk.Entry(name="message_entry")
        #toolbar.insert(self.search_entry, 6)

        button_search = Gtk.ToolButton()
        button_search.set_icon_name("system-search-symbolic")
        button_search.connect("clicked", self.on_search_clicked)
        toolbar.insert(button_search, 7)

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
        self.textbuffer.insert(self.textbuffer.get_end_iter(), '\n'+payload[0] + ' > ')
        start = self.textbuffer.get_iter_at_line_offset(self.textbuffer.get_line_count(), 0)
        end = self.textbuffer.get_end_iter()

        print("Line start" +str(start.get_line()))
        print("Line end"+str(end.get_line()))
        print("pos start"+str(start.get_line_index()))
        print("pos end"+str(end.get_line_index()))

        self.textbuffer.apply_tag(self.tag_bold, start, end)

        self.textbuffer.insert(self.textbuffer.get_end_iter(), payload[1])

    def update_conversation_textview_stdout(self, payload):
        self.textbuffer.insert(self.textbuffer.get_end_iter(), '\n[OK]: ' + payload)

    def update_conversation_textview_stderr(self, payload):
        self.textbuffer.insert(self.textbuffer.get_end_iter(), '\n[ER]: ' + payload)

    def _set_format_text(self):
        pass

    def _set_bold_text(self):
        start = self.textbuffer.get_iter_at_mark(Gtk.TextBuffer.create_mark("*"))
        end = self.textbuffer.get_end_iter()
        self.textbuffer.apply_tag(self.tag_bold, start, end)

    def on_search_clicked(self, widget):
        cursor_mark = self.textbuffer.get_insert()
        start = self.textbuffer.get_iter_at_mark(cursor_mark)
        if start.get_offset() == self.textbuffer.get_char_count():
            start = self.textbuffer.get_start_iter()

        self._search_and_mark(self.search_entry.get_text(), start)

    def _search_and_mark(self, text, start):
        end = self.textbuffer.get_end_iter()
        match = start.forward_search(text, 0, end)

        if match is not None:
            match_start, match_end = match
            self.textbuffer.apply_tag(self.tag_found, match_start, match_end)
            self._search_and_mark(text, match_end)
