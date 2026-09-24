import tkinter as tk
from tkinter import ttk


class ComboBoxTTK:
    def __init__(
            self, parent: tk.Tk | tk.Frame | tk.Toplevel,
            values: list[str] | None = None, default: str | None = None
    ):
        self._form = ttk.Combobox(parent, values=values or [])
        # установка значения по умолчанию
        if default:
            self._form.set(default)

    @property
    def form(self):
        return self._form

    def get_value(self) -> str:
        return self._form.get()

    def set_value(self, value: str) -> None:
        self._form.set(value)
