
'''
Example of a list with two lines per row.
'''

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GObject

# content list to add to the listview
content = (
            ('Into the New', 'Angus Guild'),
            ('Now to the Sea', 'Anne Toner'),
            ('Sleeping Gypsy', 'Ralph Bennett-Eades'),
            ('Angels in Silence', 'The Wastrels'),
            ('Deeply in Love', 'Duo Montagne'),
            ('No Bridges', 'Martin Way')
            )


class DataObject(GObject.GObject):
    '''
    object to hold the data for each row
    '''
    def __init__(self, text: str):
        super().__init__()
        self.text = text


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super(AppWindow, self).__init__(application=app)
        self.init_ui()

    def init_ui(self):
        self.title="Double List"
        self.default_height=400
        self.default_width=400
        
        listview = Gtk.ListView()
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self.setup)
        factory.connect("bind", self.bind)
        listview.set_factory(factory)

        selection = Gtk.SingleSelection()
        store = Gio.ListStore.new(DataObject)
        selection.set_model(store)
        listview.set_model(selection)
        
        #add rows to the listview from the content list
        for row in content:
            line1, line2 = row
            item = line1 + '\n' + line2
            store.append(DataObject(item))
            
        self.set_child(listview)
        
    def setup(self, widget, item):
        """Setup the widget (Gtk.ListItem) to show in the Gtk.ListView"""
        label = Gtk.Label(
            margin_top = 2,
            margin_start = 8,
            margin_end = 8,
            halign = Gtk.Align.START
            )
        item.set_child(label)

    def bind(self, widget, item):
        """bind data (Gtk.ListItem) from the store object to the widget"""
        label = item.get_child()
        obj = item.get_item()
        label.set_label(obj.text)
        
def on_activate(app):
    win = AppWindow(app)
    win.present()


app = Gtk.Application(application_id='com.example.doublelist')
app.connect('activate', on_activate)
app.run(None)
