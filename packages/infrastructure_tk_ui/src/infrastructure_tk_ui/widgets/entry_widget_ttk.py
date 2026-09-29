import tkinter as tk
from tkinter import ttk


class EntryWidgetTTK:
    def __init__(self, parent: tk.Tk | tk.Frame | tk.Toplevel, editable: bool = False):
        self._form = ttk.Entry(parent)
        self.editable = editable
        self._form.configure(state='normal' if editable else 'disabled')

    @property
    def form(self):
        return self._form

    def insert_text(self, text: str) -> None:
        if self._form and text:
            if not self.editable:
                self._form.configure(state='normal')
            self._form.insert(0, text)
            if not self.editable:
                self._form.configure(state='disabled')

    def clear_text(self) -> None:
        if not self._form:
            return
        if not self.editable:
            self._form.configure(state='normal')
        self._form.delete(0, tk.END)
        if not self.editable:
            self._form.configure(state='disabled')

    def get_text(self) -> str:
        return self._form.get()
