import tkinter as tk
from tkinter import ttk


class CheckboxWidgetTTK:
    def __init__(self, parent: tk.Tk | tk.Frame | tk.Toplevel, text: str = '', active: bool = False):
        """
        Построение чекбокса
        :param parent: родительский элемент
        :param text: текст выборов
        :param active: сделать галочку предустановленной?
        """
        self._var = tk.BooleanVar()
        self._form = ttk.Checkbutton(
            parent, text=text, variable=self._var,
            onvalue=True, offvalue=False,  # onvalue, offvalue - это значения которые вернет checkbox, обычно True/False
        )
        self._form.state(['!alternate'])
        if active:
            self.set(value=True)

    @property
    def form(self):
        """Возвращает объект ttk с доступными свойствами, например grid, pack, configure и другими"""
        return self._form

    def get(self) -> bool:
        return self._var.get()

    def set(self, value: bool) -> None:
        self._var.set(value)
