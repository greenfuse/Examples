'''
Example of a list with columns and expandable nodes.
Thanks to Tim Lauridsen for examples used for reference at 
https://github.com/timlau/gtk4_examples
'''

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GObject  # noqa

class DataObject(GObject.GObject):
    def __init__(self, fruit: str, colour: str, children=None):
        super(DataObject, self).__init__()
        self.fruit = fruit
        self.colour = colour
        self.children = children
        
def add_tree_node(item):
    if not item.children:
        return None
    store = Gio.ListStore.new(DataObject)
    for child in item.children:
        store.append(child)
    return store

'''
The following bind and setup signals take a GtkListItem as argument, which is a 
wrapper object that lets you get at the model item 
(with gtk_list_item_get_item()) and also lets you deliver the new 
row widget (with gtk_list_item_set_child()).
With a columnview you need to set a factory for each columnviewcolumn
'''

def setup_fruit(widget, item):
    """Setup the widget to show in the fruit column"""
    label = Gtk.Label()
    label.props.xalign = 0.0
    expander = Gtk.TreeExpander.new()
    expander.set_child(label)
    item.set_child(expander)

def setup_colour(widget, item):
    """Setup the widget to show in the colour column"""
    label = Gtk.Label()
    label.props.xalign = 0.0
    item.set_child(label)


def bind_fruit(widget, item):
    """bind data from the store object to the widget"""
    expander = item.get_child()
    label = expander.get_child()
    row = item.get_item()
    expander.set_list_row(row)
    obj = row.get_item()
    label.set_label(obj.fruit)    

def bind_colour(widget, item):
    """bind data from the store object to the widget"""
    label = item.get_child()
    row = item.get_item()
    obj = row.get_item()
    label.set_label(obj.colour)


def on_activate(app):
    win = Gtk.ApplicationWindow(
        application=app,
        title="tree with columns",
        default_height=400,
        default_width=400,
    )
    sw = Gtk.ScrolledWindow()
    column_view = Gtk.ColumnView()
    column_view.props.show_row_separators = True
    column_view.props.show_column_separators = True
    fruit_col = Gtk.ColumnViewColumn.new("Fruit")
    fruit_col.set_resizable(True)
    fruit_col.set_fixed_width(200)
    
    fruit_factory = Gtk.SignalListItemFactory()
    fruit_factory.connect("setup", setup_fruit)
    fruit_factory.connect("bind", bind_fruit)
    
    fruit_col.set_factory(fruit_factory)
    column_view.append_column(fruit_col)
    
    colour_col = Gtk.ColumnViewColumn.new("colour")
    colour_col.set_resizable(True)
    colour_col.set_fixed_width(200)
    
    colour_factory = Gtk.SignalListItemFactory()
    colour_factory.connect("setup", setup_colour)
    colour_factory.connect("bind", bind_colour)
    
    colour_col.set_factory(colour_factory)
    column_view.append_column(colour_col)
    
    selection = Gtk.SingleSelection()
    store = Gio.ListStore.new(DataObject)
    model = Gtk.TreeListModel.new(store, False, True, add_tree_node)
    model.set_autoexpand(False)
    selection.set_model(model)
    column_view.set_model(selection)
    
    apple_children = [DataObject("apple slice", "white") for i in range(5)]
    banana_children = [DataObject("banana split", "cream") for i in range(3)]
    orange_children = [DataObject("orange segment", "orange") for i in range(8)]
    store.append(DataObject("Apple", "Green", apple_children))
    store.append(DataObject("Banana", "Yellow", banana_children))
    store.append(DataObject("Orange", "Orange", orange_children))
    sw.set_child(column_view)
    win.set_child(sw)
    win.present()

app = Gtk.Application(application_id="an.id.random")
app.connect("activate", on_activate)
app.run(None)
