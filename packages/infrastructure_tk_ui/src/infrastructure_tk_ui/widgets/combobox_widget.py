from infrastructure_tk_ui.parameters_class import PackParameters, FontParameters, AnimationParameters
from dataclasses import dataclass, field
from typing import Callable
import tkinter as tk
from tkinter import ttk


@dataclass
class ComboboxWidget:
    frame: tk.Tk | tk.Frame | tk.Toplevel
    values: list[str] = field(default_factory=list)
    default: str = ''
    back_color: str | None = None  # Цвет фона, подложки, если пустой то возьмется цвет родителя
    arrow_shape_color: str = 'black'  # цвет стрелки
    arrow_background_color: str | None = None  # цвет фона под стрелкой
    popdown_back_color: str | None = None  # цвет фона меню выпадающего списка
    popdown_font_color: str | None = None  # цвет шрифта меню выпадающего списка
    popdown_select_back_color: str | None = None  # цвет фона выбранного пункта меню выпадающего списка
    popdown_select_font_color: str | None = 'steelblue'  # цвет шрифта выбранного пункта меню выпадающего списка
    font_parameters: FontParameters = field(default_factory=FontParameters)  # параметры шрифта
    pack_parameters: PackParameters = field(default_factory=PackParameters)  # параметры позиционирования виджета
    animation_parameters: AnimationParameters | None = None  # параметры анимации виджета
    readonly: bool = True  # только для чтения (запретить редактирование)
    callback: Callable | None = None  # функция которая применяется к выбранному значению (опция)
    _form: ttk.Combobox | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        self.back_color = self.back_color if self.back_color is not None else self.frame.cget('bg')
        self.arrow_background_color = self.arrow_background_color if self.arrow_background_color else self.back_color
        font_style = self.font_parameters.get()

        # стили для ttk
        self._style_name = f'Custom{id(self)}.TCombobox'  # стиль для каждого комбо уникальный
        style = ttk.Style()
        style.theme_use('clam')
        style.map(
            self._style_name,
            fieldbackground=[('readonly', self.back_color)],
            background=[('readonly', self.arrow_background_color)],
            foreground=[('readonly', font_style.color)],
            arrowcolor=[('readonly', self.arrow_shape_color)],
            selectbackground=[('readonly', self.back_color)],  # цвет фона выделения
            selectforeground=[('readonly', font_style.color)],  # цвет текста выделения
        )
        self._form = ttk.Combobox(self.frame, values=self.values, style=self._style_name)
        self._form.configure(
            state='readonly' if self.readonly else 'normal',
            font=(font_style.family, font_style.size, font_style.style),
        )

        # подключение изменения цвета при наведении
        if self.animation_parameters:
            self.animation_parameters.bind(
                back_color=self.back_color,
                form=self._form,
                style_ttk=(self._style_name, style),
            )

        # стили меню открытого списка combobox
        if self.popdown_back_color:
            self._form.option_add('*TCombobox*Listbox.background', self.popdown_back_color)
        if self.popdown_font_color is not None:
            self._form.option_add('*TCombobox*Listbox.foreground', self.popdown_font_color)
        if self.popdown_select_back_color is not None:
            self._form.option_add('*TCombobox*Listbox.selectBackground', self.popdown_select_back_color)
        if self.popdown_select_font_color is not None:
            self._form.option_add('*TCombobox*Listbox.selectForeground', self.popdown_select_font_color)

        # установка значения по умолчанию
        if self.default:
            self._form.set(self.default)

        # применение callback функции к выбранному элементу
        if self.callback:
            self._form.bind('<<ComboboxSelected>>', lambda e: self.callback(self.get_value()))

        self._form.pack(**self.pack_parameters.get())

    def get_value(self) -> str:
        return self._form.get()

    def set_value(self, value: str) -> None:
        self._form.set(value)
