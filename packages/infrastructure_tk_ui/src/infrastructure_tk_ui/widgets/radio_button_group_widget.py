import tkinter as tk
from tkinter import ttk


class RadiobuttonGroupTTK:
    def __init__(
            self, parent: tk.Tk | tk.Frame | tk.Toplevel, options: list[str] | None = None,
            default_value: str = ''
    ):
        """
        Создание группы радиокнопок построенных вокруг одной переменной
        :param parent: форма на которой размещаются кнопки
        :param options: список значений (например ['en','ru', 'ge']) , сколько значений столько и кнопок
        :param default_value: текущее значение по умолчанию, например 'ru', если не передавать то ни чего не выберется
        """
        self._var = tk.StringVar()
        self._widgets = []
        for option in options:
            self._widgets.append(ttk.Radiobutton(parent, text=option, variable=self._var, value=option))
        if default_value:
            self.set_value(val=default_value)

    @property
    def form(self) -> list[ttk.Radiobutton]:
        """Возвращает список радиокнопок, сгруппированных одной переменной состояния"""
        return self._widgets

    def get_value(self):
        return self._var.get()

    def set_value(self, val: str):
        self._var.set(value=val)
