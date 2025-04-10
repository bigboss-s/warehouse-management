from .database.database_manager import DatabaseManager
from .item import Item
from .dialogs.item_dialog import ItemDialog
from .dialogs.report_dialog import ReportDialog
from .dialogs.digit_check import digit_dot_input_check, digit_input_check
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

class WarehouseApp(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.db = DatabaseManager()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.create_widgets()
        self.refresh_tree()

    def create_widgets(self):
        # Frame for actions
        self.action_frame = ttk.Frame(self, padding=5)
        self.action_frame.grid(row=0, column=0, sticky=tk.N)

        # Frame for searching items
        self.search_frame = ttk.Frame(self.action_frame, padding=10)
        self.search_frame.grid(row=0, column=0)

        ttk.Label(self.search_frame, text='Search by:  ').grid(row=0, column=0)

        self.search_option = tk.StringVar()

        self.search_by_id_radio = ttk.Radiobutton(self.search_frame, text='ID', variable=self.search_option, value='ID')
        self.search_by_id_radio.grid(row=0, column=1)

        self.search_by_name_radio = ttk.Radiobutton(self.search_frame, text='Name', variable=self.search_option,
                                                   value='NAME')
        self.search_by_name_radio.grid(row=0, column=2)

        self.search_option.set('ID')

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.grid(row=1, column=0, columnspan=2, padx=5)
        self.search_entry.bind('<Return>', lambda x: self.search())

        self.search_button = ttk.Button(self.search_frame, text='Search', command=self.search)
        self.search_button.grid(row=1, column=2, columnspan=2, padx=5)

        # Frame for adding new items
        vcmd = (self.register(digit_input_check), '%d', '%S')
        vcmd_dot = (self.register(digit_dot_input_check), '%d', '%S')

        self.add_frame = ttk.Frame(self.action_frame, padding=5)
        self.add_frame.grid(row=2, column=0)

        ttk.Label(self.add_frame, text='Add New Item').grid(row=0, column=0, sticky=tk.W, pady=5)

        ttk.Label(self.add_frame, text='Name:').grid(row=1, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(self.add_frame)
        self.name_entry.grid(row=1, column=1, sticky=tk.W)
        self.name_entry.bind('<Return>', lambda x: self.add())

        ttk.Label(self.add_frame, text='Description:').grid(row=2, column=0, sticky=tk.W)
        self.desc_entry = ttk.Entry(self.add_frame)
        self.desc_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.desc_entry.bind('<Return>', lambda x: self.add())

        ttk.Label(self.add_frame, text='Price:').grid(row=3, column=0, sticky=tk.W)
        self.price_entry = ttk.Entry(self.add_frame, validate='key', validatecommand=vcmd_dot)
        self.price_entry.grid(row=3, column=1, sticky=tk.W, pady=(0, 5))
        self.price_entry.bind('<Return>', lambda x: self.add())

        ttk.Label(self.add_frame, text='Amount:').grid(row=4, column=0, sticky=tk.W)
        self.amount_entry = ttk.Entry(self.add_frame, validate='key', validatecommand=vcmd)
        self.amount_entry.grid(row=4, column=1, sticky=tk.W)
        self.amount_entry.bind('<Return>', lambda x: self.add())

        self.add_button = ttk.Button(self.add_frame, text='Add Item', command=self.add)
        self.add_button.grid(row=5, column=0, columnspan=2, pady=(10, 5))

        # Generating report
        ttk.Button(self.action_frame, text='Generate report...', command=self.report_choice).grid(row=5, column=0, pady=10)

        # Separators
        ttk.Separator(self.action_frame, orient='horizontal').grid(row=1, column=0, sticky=tk.EW, padx=10)
        ttk.Separator(self.action_frame, orient='horizontal').grid(row=3, column=0, sticky=tk.EW, padx=10)

        # Right click menu
        def show_menu(event):
            menu = tk.Menu(self, tearoff=0)

            selection_count = len(self.tree.selection())
            menu.add_command(label='Edit item', command=self.edit)
            menu.add_command(label='Delete item' if selection_count < 1 else 'Delete items', command=self.delete)

            menu.post(event.x_root, event.y_root)

        # Sorting vars
        self.last_sorted_by = None
        self.sort_reversed = False

        # Frame for displaying items
        self.display_frame = ttk.Frame(self, padding=5)
        self.display_frame.grid(row=0, column=1, rowspan=3, sticky=tk.NSEW, pady=5, padx=5)
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(self.display_frame, columns=('ID', 'Name', 'Description', 'Price', 'Amount'),
                                 show='headings')

        self.tree.heading('ID', text='ID', anchor=tk.W, command=lambda: self.sort_tree('ID'))
        self.tree.column('ID', width=50)
        self.tree.heading('Name', text='Name', anchor=tk.W, command=lambda: self.sort_tree('Name'))
        self.tree.heading('Description', text='Description', anchor=tk.W, command=lambda: self.sort_tree('Description'))
        self.tree.heading('Price', text='Price', anchor=tk.W, command=lambda: self.sort_tree('Price', is_number=True))
        self.tree.heading('Amount', text='Amount', anchor=tk.W, command=lambda: self.sort_tree('Amount', is_number=True))
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)

        self.tree.bind('<Button-2>', show_menu)
        self.tree.bind('<Button-3>', show_menu)


    def search(self):
        if self.search_entry.get() == '':
            self.refresh_tree()
            return
        try:
            if self.search_option.get() == 'ID':
                items = self.db.search_by_id(self.search_entry.get())
            elif self.search_option.get() == 'NAME':
                items = self.db.search_by_name(self.search_entry.get())
            self.list_to_tree(items)
        except UserWarning as err:
            messagebox.showerror('No items found', err)

    def list_to_tree(self, items, force=False):
        if len(items) == 0 and not force:
            raise UserWarning('No items found')
        self.tree.delete(*self.tree.get_children())
        for row in items:
            self.tree.insert(parent='', index='end', iid=row['ID'], text='',
                             values=(row['ID'], row['name'], row['description'], row['price'],
                                     row['num_of_available_items']))

    def refresh_tree(self, force=False):
        items = self.db.fetch_all_items()
        self.list_to_tree(items, force=force)

    def add(self):
        try:
            item = Item(self.name_entry.get(), self.desc_entry.get(),
                        self.price_entry.get(),
                        self.amount_entry.get())
            self.db.insert_item(item)
            self.refresh_tree()
        except ValueError as err:
            messagebox.showerror('Invalid data', err)

    def edit(self):
        selection = self.tree.selection()
        if len(selection) == 0:
            messagebox.showerror('Error', 'No item selected')
            return
        if len(selection) > 1:
            messagebox.showerror('Error', 'You can only edit one item at a time')
            return
        item = self.tree.item(selection[0])['values']
        item = Item(item[1], item[2], item[3], item[4], id=item[0])

        dialog = ItemDialog(self, item)
        self.wait_window(dialog)
        item = dialog.new_item

        if item is None:
            return

        self.db.edit_item(item)
        self.refresh_tree()

    def delete(self):
        selection = self.tree.selection()
        if len(selection) == 0:
            messagebox.showerror('Error', 'No items selected')
            return
        confirm = messagebox.askyesno('Confirmation', f'Are you sure you want to delete {len(selection)} item{"s" if len(selection) > 1 else ""}?')
        if not confirm:
            return
        self.db.delete_items(selection)
        self.refresh_tree(force=True)

    def report_choice(self):
        ReportDialog(self, self.db)

    def sort_tree(self, col, is_number=False):
        if self.last_sorted_by == col:
            self.sort_reversed = not self.sort_reversed
        else:
            self.sort_reversed = False

        for column_id in self.tree['columns']:
            self.tree.heading(column_id, text=column_id)

        arrow = ' \u25bc' if self.sort_reversed else ' \u25b2'
        self.tree.heading(col, text=col + arrow)

        self.last_sorted_by = col
        tuple_list = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        if is_number:
            key = lambda x: float(x[0])
        else:
            key = lambda x: x[0]
        tuple_list.sort(reverse=self.sort_reversed, key=key)

        for id, (val, k) in enumerate(tuple_list):
            self.tree.move(k, '', id)
