#!/usr/bin/python

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class DialogWindow(Gtk.Dialog):
    def __init__(
        self, 
        parent,
        text
        ):
        super().__init__(transient_for = parent)
        self.title="Song Details", 
        self.use_header_bar = True
        self.connect('response', self.dialog_response)

        self.set_modal(True)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        btn_close = self.get_widget_for_response(
            response_id=Gtk.ResponseType.CLOSE,
        )

        label1 = Gtk.Label()
        label1.set_text("This is a dialog window")
        label1.set_margin_start(5)
        label1.set_margin_end(5)
        label1.set_margin_bottom(5)
        label1.set_margin_top(5)
        self.get_content_area().append(label1)

        label2 = Gtk.Label()
        label2.set_text(text)
        label2.set_margin_start(5)
        label2.set_margin_end(5)
        label2.set_margin_bottom(5)
        label2.set_margin_top(5)
        self.get_content_area().append(label2)

    def dialog_response(self, dialog, response): 
        if response == Gtk.ResponseType.CLOSE:
            print('pressed the CLOSE button')
        dialog.close()     

class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super(AppWindow, self).__init__(application=app)
        self.init_ui()

    def init_ui(self):
        self.set_title('Simple')
        self.set_default_size(350, 250)

        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        vbox.valign = Gtk.Align.FILL
        vbox.halign = Gtk.Align.FILL
        vbox.hexpand=True
        vbox.vexpand=True
        
        label = Gtk.Label()
        label.set_text("This is a window. Click the button")
        label.set_wrap(True)
        label.valign = Gtk.Align.FILL
        label.halign = Gtk.Align.FILL
        label.hexpand=True
        label.vexpand=True
        label.set_size_request(350, 250)
        button = Gtk.Button(label="Open Dialog")
        button.set_valign(Gtk.Align.END)
        button.hexpand=False
        button.vexpand=False
        button.connect("clicked", self.on_dialog_clicked)
        
        vbox.append(label)
        vbox.append(button)
        self.set_child(vbox)
        
        self.text = "Show this in the dialog"

    def on_dialog_clicked(self, button):
        song_dialog = DialogWindow(self, self.text)
        song_dialog.present()

def on_activate(app):
    win = AppWindow(app)
    win.present()

app = Gtk.Application(application_id='com.example.dialog')
app.connect('activate', on_activate)
app.run(None)
