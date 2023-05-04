import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#Few global variables

# C.S.Lewis
random_quote = "Hardships often prepare ordinary people for an extraordinary destiny"

dict_align = {
"START":Gtk.Align.START,
"END":Gtk.Align.END,
"CENTER":Gtk.Align.CENTER,
"FILL":Gtk.Align.FILL,
"BASELINE":Gtk.Align.BASELINE
}

list_hexpand = ["hexpand=True", "hexpand=False"]
list_vexpand = ["vexpand=True", "vexpand=False"]

list_halign = [
    "halign=START",
    "halign=END",
    "halign=CENTER",
    "halign=FILL",
    "halign=BASELINE"
    ]
list_valign = [
    "valign=START",
    "valign=END",
    "valign=CENTER",
    "valign=FILL",
    "valign=BASELINE"
    ]

css = b"""
.hbox {
    background-color: #FFC0CB;
}
.vbox {
    background-color: #D3FFcC;
}
"""

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Layout Example")
        self.set_default_size(200, 200)
                
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.vbox.get_style_context().add_class("vbox")
        
        grid = Gtk.Grid(hexpand=True, vexpand=False)
        
        hbox1 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            hexpand=True,
            vexpand=True,
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL
            )
        hbox1.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        hbox1.get_style_context().add_class("hbox")
            
        hbox2 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            hexpand=True,
            vexpand=True,
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL
            )

        hbox2.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        hbox2.get_style_context().add_class("hbox")
           
        hbox3 = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            hexpand=True,
            vexpand=True,
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL
            )

        hbox3.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        hbox3.get_style_context().add_class("hbox")
        
        self.rb_group = None
        rb_labels = ["vbox", "hbox", "button"]

        n=0
        
        for label in rb_labels:
            radio_button = Gtk.RadioButton(group=self.rb_group, label=label)
            if self.rb_group is None:
                self.rb_group = radio_button
            grid.attach(
                child=radio_button, 
                left=0, 
                top=n, 
                width=1, 
                height=1)
                
            n += 1
        
        # First Row for the vbox settings
        cb_hexpand = Gtk.ComboBoxText(name="hexpand")
        cb_hexpand.set_active(0)
        cb_hexpand.connect("changed", self.cb_changed)
        cb_vexpand = Gtk.ComboBoxText(name="vexpand", active=0)
        cb_vexpand.set_active(0)
        cb_vexpand.connect("changed", self.cb_changed)
        cb_halign = Gtk.ComboBoxText(name="halign", active=0)
        cb_halign.set_active(0)
        cb_halign.connect("changed", self.cb_changed)
        cb_valign = Gtk.ComboBoxText(name="valign", active=0)
        cb_valign.set_active(0)
        cb_valign.connect("changed", self.cb_changed)
        
        for setting in list_hexpand:
            cb_hexpand.append_text(setting)

        for setting in list_vexpand:
            cb_vexpand.append_text(setting)

        for setting in list_halign:
            cb_halign.append_text(setting)

        for setting in list_valign:
            cb_valign.append_text(setting)
        
        grid.attach(
            child=cb_hexpand,
            left=1,
            top=0,
            width=1,
            height=1
            )
        
        grid.attach(
            child=cb_vexpand,
            left=1,
            top=1,
            width=1,
            height=1
            )        

        grid.attach(
            child=cb_halign,
            left=2,
            top=0,
            width=1,
            height=1
            )            

        grid.attach(
            child=cb_valign,
            left=2,
            top=1,
            width=1,
            height=1
            )    

        labels = random_quote.split()
        
        for label in labels[0:3]:
            button = Gtk.Button(label=label)
            hbox1.pack_start(button,True, True, 0)
            
        for label in labels[3:6]:
            button = Gtk.Button(label=label)
            hbox2.pack_start(button,True, True, 0)    

        for label in labels[6:9]:
            button = Gtk.Button(label=label)
            hbox3.pack_start(button,True, True, 0)            

        self.vbox.pack_start(grid,True, True, 5)
        self.vbox.pack_start(hbox1,True, True, 5)
        self.vbox.pack_start(hbox2,True, True, 5)        
        self.vbox.pack_start(hbox3,True, True, 5)        
        self.add(self.vbox)

    def cb_changed(self, widget):
        cb_name = widget.get_name()
        cb_text = widget.get_active_text()
        to_change = self.determine_selected()
        if to_change == "vbox":
            self.update_item(self.vbox, cb_name, cb_text)
        elif to_change == "hbox":
            for child in self.vbox.get_children():
                if isinstance(child, Gtk.Box):
                    self.update_item(child, cb_name, cb_text)
        elif to_change == "button":
            for child in self.vbox.get_children():
                if isinstance(child, Gtk.Box):
                    for child in child.get_children():
                        if isinstance(child, Gtk.Button):
                            self.update_item(child, cb_name, cb_text)

    def determine_selected(self):
        for radio_button in self.rb_group.get_group():
            if radio_button.get_active():
                rb_name = radio_button.get_label()
                print(rb_name)
                return(rb_name)       
    
    def update_item(self, item, cb_name, cb_text):
        setting = cb_text.split("=")[1]
        if cb_name == "hexpand":
            item.set_hexpand(eval(setting))
        elif cb_name =="vexpand":
            item.set_vexpand(eval(setting))
        elif cb_name == "halign":
            item.set_halign(dict_align[setting])
        elif cb_name == "valign":
            item.set_valign(dict_align[setting])
        
                
win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
