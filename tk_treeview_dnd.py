#!/usr/bin/python3
'''
This is an example of tkinter drag n drop within and between treeviews.
Created to help me understand how to do it for a bigger project.
Try to keep things clear and explicit so I can understand it later.
Uses the tkinter dnd module rather than any third-party module.
It is a bit hackish but gets the job done.
'''

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import dnd

class TreeviewDnD:
    def __init__(self, master):
        '''
        create treeviews and add some rows
        '''
        self.master = master
        master.title("Treeview DND Test")
        master.minsize(840, 420)

        self.frame1 = ttk.Frame(master)

        # Configure the style of Heading in Treeview widget
        tree_style = ttk.Style()
        tree_style.theme_use('clam')
        tree_style.configure('Treeview.Heading', background="gray78")

        self.label_drag = ttk.Label(self.frame1)
        self.label_drag.configure(
            borderwidth=2, 
            relief="groove"
            )

        self.tv1 = ttk.Treeview(self.frame1)
        column_names = ('album', 'title')
        self.tv1.configure(
            selectmode=tk.BROWSE,
            columns=column_names
            )        
        self.tv1.column('#0', anchor='w', width=80)
        self.tv1.column('album', anchor='w', width=80)
        self.tv1.column('title', anchor='w', width=80)

        self.tv1.heading('#0', text='Artist', anchor='w')
        self.tv1.heading('album', text='Album', anchor='w')
        self.tv1.heading('title', text='Title', anchor='w')


        self.tv1.insert(
            index=2,
            parent='', 
            text='Alison Thorsteinsen', 
            values=(
                "Sometimes I'm There",
                'Cowboy'
                )
            )
        self.tv1.insert(
            index=2,
            parent='', 
            text='The Wastrels', 
            values=(
                'The Jenner Affair',
                'Angels in Silence'
                )
            )
        self.tv1.insert(
            index=1,
            parent='', 
            text='Ralph Bennett-Eades', 
            values=(
                'Sleeping Gypsy',
                'When I Was Your Age Kid'
                )
            )
        self.tv1.insert(
            index=0,
            parent='', 
            text='Paolo Jorge', 
            values=(
                'The most beautiful solos of Portuguese guitar',
                'fado lopes'
                )
            )
        self.tv1.insert(
            index=1,
            parent='', 
            text='Orlando Vasquez & Carlos Paula', 
            values=(
                'Barcelona',
                'Hasta Siempre Comandante'
                )
            )
        self.tv1.bind("<Button-1>", self.press)
        self.tv1.dnd_accept = self.dnd_accept
        self.tv1.dnd_commit = self.dnd_commit
        self.tv1.pack(padx=20, pady=(20, 10), side=tk.TOP, fill='both', expand=True)

        self.tv2 = ttk.Treeview(self.frame1)
        column_names = ('album', 'title')
        self.tv2.configure(
            selectmode=tk.BROWSE,
            columns=column_names
            )        
        self.tv2.column('#0', anchor='w', width=80)
        self.tv2.column('album', anchor='w', width=80)
        self.tv2.column('title', anchor='w', width=80)

        self.tv2.heading('#0', text='Artist', anchor='w')
        self.tv2.heading('album', text='Album', anchor='w')
        self.tv2.heading('title', text='Title', anchor='w')

        self.tv2.insert(
            index=tk.END, 
            parent='', 
            text='Duo Montagne', 
            values=(
                'Continental Lounge',
                'Deeply in Love'
                )
            )
        self.tv2.insert(
            index=1, 
            parent='', 
            text='Angus Guild', 
            values=(
                'Into The New',
                'Into The New'
                )
            )
        self.tv2.insert(
            index=tk.END, 
            parent='', 
            text='Nuala Honan', 
            values=(
                'The Tortoise', 
                'Wake & Howl'
                )
            )

        self.tv2.bind("<Button-1>", self.press)
        self.tv2.dnd_accept = self.dnd_accept
        self.tv2.dnd_commit = self.dnd_commit
        self.tv2.pack(padx=20, pady=(10, 20), side=tk.TOP, fill='both', expand=True)
        self.frame1.pack(side=tk.TOP, fill='both', expand=True)

    def press(self, event):
        '''
        starts dnd by calling dnd_start
        '''
        # set to zero then check if a row is selected for dragging
        self.drag_row = 0
        # if dnd_motion is triggered then change this to 1
        self.moved = 0
        
        #check if we have picked up a row
        if dnd.dnd_start(self, event):
            widget=event.widget
            widget._drag_start_x = event.x
            widget._drag_start_y = event.y
            row = widget.identify_row(event.y)
            row_item = widget.item(row)
            row_values = row_item['values']
            #print(row)
            if row_values:
                self.drag_row = 1
            else:
                self.drag_row = 0

    def dnd_leave(self, source, event):
        '''
        called by the dnd module when leaving the original widget
        '''
        #print("leave")
        pass
    
    def dnd_enter(self, source, event):
        '''
        called by the dnd module when starting the drag
        or moving to a new widget
        '''
        #print("enter")
        pass

    def dnd_motion(self, source, event):
        '''
        this is what we do when dragging
        in this case it is moving a blank label to indicate dragging
        '''
        widget = event.widget
        # only move if there is a row selected
        if self.drag_row:
            row_width = widget.winfo_width()        
            #the default row height seems to be 20
            #can set this in the tree style if necessary
            win_x = widget.winfo_x()  - widget._drag_start_x + event.x
            win_y = widget.winfo_y() - 10 + event.y
            row_height = 20
            self.label_drag.lift()
            self.label_drag.place(x = win_x, y = win_y, width=row_width, height= row_height)
            self.moved = 1
    
    def dnd_accept(self, source, event):
        '''
        Enable the dnd module to drop the dnd on the widget
        '''
        return self

    def dnd_commit(self, source, event):
        '''
        Not sure what this does,
        possibly called by the dnd module when the drag is released 
        over an accepting widget
        but does not behave consistently
        can't see any use for it in this example
        '''
        pass

    def dnd_end(self, target, event):
        '''
        action to take on mouse release after drag
        get the destination and source treeview widgets
        pass to a function to do the move
        '''
        self.label_drag.place_forget()
        x = self.master.winfo_pointerx()
        y = self.master.winfo_pointery()
        source_treeview = event.widget
        row = source_treeview.identify_row(event.y)
        row_item = source_treeview.item(row)
        destination_treeview = self.master.winfo_containing(x, y, displayof=0)
        #print(str(source_treeview))
        print(str(destination_treeview))
        if destination_treeview:
            if 'treeview' in destination_treeview._name:
                if self.drag_row and self.moved:
                    self.move_row(source_treeview, destination_treeview)
                else:
                    print('Nothing to do here')

    def move_row(self, source_treeview, destination_treeview):
        '''
        move the dragged row to its destination
        '''
        source_selected_item = source_treeview.focus()
        #print("source_selected_item: " + source_selected_item)
        source_row_item = source_treeview.item(source_selected_item)
        #print("source_row_item: " + str(source_row_item))
        # identify the destination row and use the index to 
        # position a new row to be created from the dragged one
        y = (self.master.winfo_pointery()) - (destination_treeview.winfo_rooty())
        destination_row = destination_treeview.identify_row(y)
        destination_row_details = destination_treeview.item(destination_row)
        if destination_row:
            previous_row = destination_treeview.prev(destination_row)
            if previous_row:
                row_index = (destination_treeview.index(previous_row) + 1)
            else: row_index = 0
        else:
            row_index = tk.END
        
        print(str(row_index))

        destination_treeview.insert(
            index=row_index, 
            parent='', 
            text=source_row_item['text'],
            values=tuple(source_row_item['values'])
            )        

        source_treeview.delete(source_selected_item)

root = tk.Tk()
tvdnd = TreeviewDnD(root)
root.mainloop()
