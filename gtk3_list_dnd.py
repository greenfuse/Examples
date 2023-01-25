import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class TwoListsWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="List drag and drop")

        # Create a Grid to hold the two lists
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_column_homogeneous(True)
        grid.set_margin_start(5)
        grid.set_margin_end(5)
        grid.set_margin_top(5)
        grid.set_margin_bottom(10)
        
        self.add(grid)
        
        label1 = Gtk.Label()
        label1.set_text("List 1")
        
        label2 = Gtk.Label()
        label2.set_text("List 2")
        
        button1 = Gtk.Button("Delete")
        button1.connect("clicked", self.on_button_clicked)

        # Create the ListStore models for the two lists
        self.liststore1 = Gtk.ListStore(str, str)
        self.liststore2 = Gtk.ListStore(str, str)

        # Create the TreeView widgets for the two lists
        self.treeview1 = Gtk.TreeView(model=self.liststore1)
        self.treeview1.set_name("t1")
        self.treeview2 = Gtk.TreeView(model=self.liststore2)
        self.treeview2.set_name("t2")

        # Create the columns for the two lists
        self.create_columns(self.treeview1)
        self.create_columns(self.treeview2)

        # Enable drag and drop support for the TreeView widgets
        self.treeview1.enable_model_drag_source(
            Gdk.ModifierType.BUTTON1_MASK,
            [("text/plain", 0, 0)],
            Gdk.DragAction.COPY)
        self.treeview1.connect("drag-data-get", self.on_drag_data_get)

        self.treeview2.enable_model_drag_source(
            Gdk.ModifierType.BUTTON1_MASK,
            [("text/plain", 0, 0)],
            Gdk.DragAction.MOVE)
        self.treeview2.connect("drag-data-get", self.on_drag_data_get)

        self.treeview2.enable_model_drag_dest(
            [("text/plain", 0, 0)],
            Gdk.DragAction.MOVE)
        self.treeview2.connect("drag-data-received", self.on_drag_data_received)

        # Add the TreeView widgets to the Grid
        grid.attach(label1, 0, 0, 1, 1)
        grid.attach(label2, 1, 0, 1, 1)        
        grid.attach(self.treeview1, 0, 1, 1, 1)
        grid.attach(self.treeview2, 1, 1, 1, 1)
        grid.attach(button1, 1, 2, 1, 1)

        self.liststore1.append(["Forest", "Lush"])
        self.liststore1.append(["Ocean", "Vast"])
        self.liststore1.append(["Mountain", "Towering"])
        self.liststore1.append(["River", "Meandering"])
        self.liststore1.append(["Desert", "Arid"])
        self.liststore1.append(["Jungle", "Dense"])
        self.liststore1.append(["Wildlife", "Abundant"])
        self.liststore1.append(["Sunflower", "Golden"])
        self.liststore1.append(["Storm", "Violent"])
        self.liststore1.append(["Sunset", "Magical"])        
        self.liststore2.append(["Storm", "Violent"])
        self.liststore2.append(["Sunset", "Magical"])

    def create_columns(self, treeview):
        renderer = Gtk.CellRendererText()

        column1 = Gtk.TreeViewColumn("Item", renderer, text=0)
        column2 = Gtk.TreeViewColumn("Description", renderer, text=1)
        treeview.append_column(column1)
        treeview.append_column(column2)

    def on_button_clicked(self, widget):
        model, tree_iter = self.treeview2.get_selection().get_selected()
        model.remove(tree_iter)
        
    def on_drag_data_get(self, treeview, context, selection, info, timestamp):
        model, tree_iter = treeview.get_selection().get_selected()
        if tree_iter is not None:
            self.drag_source_widget = treeview
            row = model[tree_iter]
            col1 = row[0]
            col2 = row[1]
            items = (col1, col2)
            text = str(items)
            selection.set_text(text, -1)

    def on_drag_data_received(self, treeview, drag_context, x, y, selection, info, timestamp):
        actions = drag_context.get_actions()
        model = treeview.get_model()
        text = selection.get_text()
        items = eval(text)

        source_treeview = self.drag_source_widget
        source_treeview_name = source_treeview.get_name()
        treeview_name = treeview.get_name()
        dest_path, drop_position = treeview.get_dest_row_at_pos(x, y) or (
            None, None)

        model = self.treeview2.get_model()
        if dest_path is None:
            # If there is no destination row, append the new row to the end of the list
            tree_iter = model.append(items)

        else:
            # If there is a destination row, insert the new row before or after it
            tree_iter = model.insert_before(model.get_iter(dest_path), items)
        
        
        #if moving in the list, remove the :
        if actions == Gdk.DragAction(4):
            source_liststore = treeview.get_model()
            source_selection = treeview.get_selection()
            source_model, source_treeiter = source_selection.get_selected()
            source_liststore.remove(source_treeiter)
        
        #Select the new row
        path = model.get_path(tree_iter)
        treeview.set_cursor(path)
        

win = TwoListsWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
