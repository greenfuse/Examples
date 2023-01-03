#!/usr/bin/python

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, app):

        super(AppWindow, self).__init__(application=app)

        self.init_ui()

    def init_ui(self):

        self.set_title('Scale Slider')

        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 8)
        hbox1 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 8)
        hbox2 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 8)
        self.scale = Gtk.Scale()
        self.label = Gtk.Label.new('0')
        
        self.scale.set_digits(0)  # Number of decimal places to use
        self.scale.set_range(0, 1000)
        self.scale.set_draw_value(False)  # Don't show a label with current value
        self.scale.set_value(0)  # Sets the current value/position
        self.scale.connect('value-changed', self.scale_changed)
        #self.scale.set_halign(Gtk.Align.FILL)
        self.scale.set_hexpand(True)
        
        self.adjustment = Gtk.Adjustment(
            value=0, 
            lower=0, 
            upper=1000, 
            step_increment=50, 
            page_increment=100, 
            page_size=50)
            
        self.spinbutton = Gtk.SpinButton()
        self.spinbutton.set_adjustment(self.adjustment)
        self.spinbutton.set_value(0)

        self.button = Gtk.Button(label="Set")
        self.button.connect("clicked", self.update_scale)

        vbox.set_margin_start(5)
        vbox.set_margin_top(5)
        vbox.set_margin_bottom(5)
        hbox1.append(self.scale)
        vbox.append(self.label)
        hbox2.append(self.spinbutton)
        hbox2.append(self.button)
        vbox.append(hbox1)
        vbox.append(hbox2)    
            
        self.set_title('Scale Slider')
        self.set_default_size(250, 80)
        self.set_child(vbox)

    def scale_changed(self, scale):
        value = str(int(scale.get_value()))
        self.label.set_label(value)
        
    def update_scale(self, button):
        value = self.spinbutton.get_value()
        self.scale.set_value(value)


def on_activate(app):

    win = AppWindow(app)
    win.present()


app = Gtk.Application(application_id='com.example.scale')
app.connect('activate', on_activate)
app.run(None)
