from tkinter import Toplevel
import tkinter as tk
import tkinter.ttk as ttk
from .digit_check import digit_input_check, digit_dot_input_check
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
import os

class ReportDialog(tk.Toplevel):

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.resizable(False, False)
        self.title('Generating Report')
        self.report_option = tk.StringVar(value='default')
        self.min_price = tk.DoubleVar()
        self.max_price = tk.DoubleVar()
        self.min_amount = tk.IntVar()
        self.max_amount = tk.IntVar()
        self.directory = None

        ttk.Radiobutton(self, text='Default report', variable=self.report_option,
                       value='default', command=self.update_entries).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(self, text='Filter by price', variable=self.report_option,
                       value='price', command=self.update_entries).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.price_frame = ttk.Frame(self)
        self.price_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.price_frame, text='Min:').grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.price_frame, text='Max:').grid(row=1, column=0, padx=5, pady=5)

        vcmd = (self.register(digit_input_check), '%d', '%S')
        vcmd_dot = (self.register(digit_dot_input_check), '%d', '%S')

        self.min_price_entry = ttk.Entry(self.price_frame, textvariable=self.min_price, state='disabled', validate='key', validatecommand=vcmd_dot)
        self.min_price_entry.grid(row=0, column=1, padx=5, pady=5)
        self.max_price_entry = ttk.Entry(self.price_frame, textvariable=self.max_price, state='disabled', validate='key', validatecommand=vcmd_dot)
        self.max_price_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Radiobutton(self, text='Filter by amount', variable=self.report_option,
                       value='amount', command=self.update_entries).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self.amount_frame = ttk.Frame(self)
        self.amount_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.amount_frame, text='Min:').grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.amount_frame, text='Max:').grid(row=1, column=0, padx=5, pady=5)

        self.min_amount_entry = ttk.Entry(self.amount_frame, textvariable=self.min_amount, state='disabled', validate='key', validatecommand=vcmd)
        self.min_amount_entry.grid(row=0, column=1, padx=5, pady=5)
        self.max_amount_entry = ttk.Entry(self.amount_frame, textvariable=self.max_amount, state='disabled', validate='key', validatecommand=vcmd)
        self.max_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=4, column=0, pady=5, padx=5, columnspan=2)

        self.submit_button = ttk.Button(self.button_frame, text='Generate', command=self.submit)
        self.submit_button.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        self.path_label = ttk.Label(self, text='Path: -')
        self.path_label.grid(row=3, column=0, columnspan=2, padx=10, pady=0, sticky=tk.W)

        def select_directory():
            self.directory = filedialog.askdirectory(parent=self, initialdir=os.getcwd())
            if self.directory is not None:
                self.path_label.configure(text=f'Path: {self.directory}')

        self.directory_button = ttk.Button(self.button_frame, text='Select output path', command=select_directory)
        self.directory_button.grid(row=0, column=0, sticky=tk.EW, padx=5, pady=5)

    def update_entries(self):
        if self.report_option.get() == 'price':
            self.min_price_entry.config(state='normal')
            self.max_price_entry.config(state='normal')
            self.min_amount_entry.config(state='disabled')
            self.max_amount_entry.config(state='disabled')
        elif self.report_option.get() == 'amount':
            self.min_price_entry.config(state='disabled')
            self.max_price_entry.config(state='disabled')
            self.min_amount_entry.config(state='normal')
            self.max_amount_entry.config(state='normal')
        else:
            self.min_price_entry.config(state='disabled')
            self.max_price_entry.config(state='disabled')
            self.min_amount_entry.config(state='disabled')
            self.max_amount_entry.config(state='disabled')

    def submit(self):
        if self.directory is None:
            messagebox.showerror(parent=self, title='Error', message='No output folder selected')
            return
        if self.report_option.get() == 'default':
            self.generate_report_default()
        elif self.report_option.get() == 'price':
            self.generate_report_by_price(self.min_price.get(), self.max_price.get())
        elif self.report_option.get() == 'amount':
            self.generate_report_by_amount(self.min_amount.get(), self.max_amount.get())
        self.destroy()

    def generate_report(self, items):
        filename = datetime.now().strftime('%d-%m-%Y %H-%M-%S') + '.txt'
        path = os.path.join(self.directory, filename)
        with open(path, 'w') as file:
            file.write('ID\tName\tDescription\tPrice\tAmount\n')
            for row in items:
                report_item = '{}\t{}\t{}\t{}\t{}\n'.format(row['ID'], row['name'], row['description'], row['price'],
                                                            row['num_of_available_items'])
                file.write(report_item)

    def generate_report_default(self):
        self.generate_report(self.db.fetch_all_items())

    def generate_report_by_price(self, min, max):
        self.generate_report(self.db.fetch_items_by_price(min, max))

    def generate_report_by_amount(self, min, max):
        self.generate_report(self.db.fetch_items_by_amount(min, max))