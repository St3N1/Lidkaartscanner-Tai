import tkinter as objTK
from tkinter import ttk as objTTK
import tkinter as tk
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
