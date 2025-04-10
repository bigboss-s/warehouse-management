from tkinter import Toplevel
import tkinter as tk
import tkinter.ttk as ttk
from .digit_check import digit_input_check, digit_dot_input_check
from tkinter import messagebox

class ItemDialog(tk.Toplevel):
    def __init__(self, parent, item):
        super().__init__(parent)
        self.resizable(False, False)
        self.title('Edit item values')
        self.item = item
        self.new_item = None

        self.var_id = tk.BooleanVar()
        self.var_name = tk.BooleanVar()
        self.var_description = tk.BooleanVar()
        self.var_price = tk.BooleanVar()
        self.var_amount = tk.BooleanVar()

        self.label = tk.Label(self, text='Select and enter new values:').grid(row=0, column=0, padx=5, pady=5)

        vcmd = (self.register(digit_input_check), '%d', '%S')
        vcmd_dot = (self.register(digit_dot_input_check), '%d', '%S')

        self.entry_name = self.create_entry('Name', self.var_name, 1, self.item.get_name())
        self.entry_description = self.create_entry('Description', self.var_description, 2, self.item.get_description())
        self.entry_price = self.create_entry('Price', self.var_price, 3, self.item.get_price(), validatecommand=vcmd_dot)
        self.entry_amount = self.create_entry('Amount', self.var_amount, 4, self.item.get_num_of_available_items(), validatecommand=vcmd)

        ttk.Button(self, text='Submit', command=self.submit).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def create_entry(self, text, var, row, current_value, validatecommand=None):
        def submit_command(event):
            self.submit()

        ttk.Checkbutton(self, text=text, variable=var, command=lambda: self.toggle_entry(entry, var)) \
            .grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        entry = ttk.Entry(self)
        entry.insert(0, string=current_value)
        entry.configure(state='disabled')
        entry.configure(validate='key' if validatecommand is not None else None,
                          validatecommand=validatecommand)
        entry.bind('<Return>', submit_command)
        entry.grid(row=row, column=1, sticky='ew', pady=5, padx=5)

        return entry

    def toggle_entry(self, entry, var):
        if var.get():
            entry['state'] = 'normal'
        else:
            entry['state'] = 'disabled'

    def submit(self):
        try:
            if self.var_name.get():
                self.item.set_name(self.entry_name.get())
            if self.var_description.get():
                self.item.set_description(self.entry_description.get())
            if self.var_price.get():
                self.item.set_price(self.entry_price.get())
            if self.var_amount.get():
                self.item.set_num_of_available_items(self.entry_amount.get())
        except ValueError as err:
            tk.messagebox.showerror(parent = self, title='Error', message=err)
            return

        self.new_item = self.item

        self.destroy()