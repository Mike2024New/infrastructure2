import tkinter as tk
from tkinter import ttk


class ProgressBarWidgetTTK:
    """Прогресс бар с шкалой"""

    def __init__(self, parent: tk.Tk | tk.Frame | tk.Toplevel):
        self._form = ttk.Progressbar(parent)

    @property
    def form(self):
        return self._form

    def set_value(self, val: int):
        self._form['value'] = val

    def close(self):
        self._form.destroy()
