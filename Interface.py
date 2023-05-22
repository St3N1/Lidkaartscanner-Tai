import tkinter as objTK
from tkinter import ttk as objTTK
import tkinter as tk
import customtkinter
import requests
import tkinter.ttk as ttk
from functools import partial
import datetime as objDateTime


class MyTreeview(objTTK.Treeview):
    def heading(self, column, sort_by=None, **kwargs):
        if sort_by and not hasattr(kwargs, 'command'):
            func = getattr(self, f"_sort_by_{sort_by}", None)
            if func:
                kwargs['command'] = partial(func, column, False)
        return super().heading(column, **kwargs)

    def _sort(self, column, reverse, data_type, callback):
        l = [(self.set(k, column), k) for k in self.get_children('')]
        l.sort(key=lambda t: data_type(t[0]), reverse=reverse)
        for index, (_, k) in enumerate(l):
            self.move(k, '', index)
        self.heading(column, command=partial(callback, column, not reverse))

    def _sort_by_num(self, column, reverse):
        self._sort(column, reverse, int, self._sort_by_num)

    def _sort_by_name(self, column, reverse):
        self._sort(column, reverse, str, self._sort_by_name)

    def _sort_by_date(self, column, reverse):
        def _str_to_datetime(string):
            return objDateTime.datetime.strptime(string, "%d/%m/%Y")

        self._sort(column, reverse, _str_to_datetime, self._sort_by_date)

    def _sort_by_multidecimal(self, column, reverse):
        def _multidecimal_to_str(string):
            arrString = string.split(".")
            strNum = ""
            for iValue in arrString:
                strValue = f"{int(iValue):02}"
                strNum = "".join([strNum, str(strValue)])
            strNum = "".join([strNum, "0000000"])
            return int(strNum[:8])

        self._sort(column, reverse, _multidecimal_to_str,
                   self._sort_by_multidecimal)

    def _sort_by_numcomma(self, column, reverse):
        def _numcomma_to_num(string):
            return int(string.replace(",", ""))

        self._sort(column, reverse, _numcomma_to_num, self._sort_by_numcomma)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Database viewer")
        self.resizable(False, False)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=100,
                                                 corner_radius=0)
        self.frame_left.grid(row=1, column=0, sticky="nswe")

        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(8, minsize=20)
        self.frame_left.grid_rowconfigure(11, minsize=10)

        self.menu_label = customtkinter.CTkLabel(
            self.frame_left, text="Menu", fg_color="transparent", font=("", 20))
        self.menu_label.grid(row=0, column=0, pady=50, padx=80)

        self.input_jaar = customtkinter.CTkEntry(
            self.frame_left, placeholder_text="Jaar")
        self.input_jaar.grid(row=1, column=0)

        self.button = customtkinter.CTkButton(
            self.frame_left, text="Gegevens ophalen", command=self.get_data)
        self.button.grid(row=2, column=0, pady=20)

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=1, column=1, sticky="nswe", padx=15, pady=15)

        self.add_menu_display211 = customtkinter.CTkFrame(master=self.frame_right,
                                                          corner_radius=15,
                                                          height=400,
                                                          width=600)
        self.add_menu_display211.grid(pady=15, padx=15, sticky="nws")

        columns = ['Datum', 'Voornaam', 'Achternaam']
        self.table = MyTreeview(master=self.add_menu_display211,
                                columns=columns,
                                height=17,

                                show='headings')

        arrSortType = ["date", "name", "name"]
        arrColWidth = [150, 250, 200]
        arrColAlignment = ["c", "c", "c"]

        self.table.pack()

        for iCount in range(len(columns)):
            strHdr = columns[iCount]
            self.table.heading(strHdr, text=strHdr.title(),
                               sort_by=arrSortType[iCount])
            self.table.column(columns[iCount], width=arrColWidth[iCount],
                              stretch=True, anchor=arrColAlignment[iCount])

        self.table.grid(row=0, column=0, sticky='nswe', padx=10, pady=10)
        self.table.bind('<Motion>', 'break')

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

    def get_data(self):
        self.data = requests.get(
            f"http://localhost:8000/aanwezigheidlijst/{self.input_jaar.get()}").json()
        self.add_data()

    def add_data(self):
        self.table.delete(*self.table.get_children())
        for item in self.data:
            if item != "detail":
                self.table.insert("", "end", values=(
                    item[3], item[1], item[2]))


app = App()
app.mainloop()
