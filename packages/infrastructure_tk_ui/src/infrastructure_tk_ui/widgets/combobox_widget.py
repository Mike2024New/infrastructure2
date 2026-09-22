from infrastructure_tk_ui.parameters_class import PackParameters, GridParameters, StyleParameters
import infrastructure_tk_ui.widget_helpers as widget_helpers
from dataclasses import dataclass, field
from typing import Callable
import tkinter as tk
from tkinter import ttk


@dataclass
class ComboboxWidget:
    parent: tk.Tk | tk.Frame | tk.Toplevel
    placement_strategy: PackParameters | GridParameters  # способ размещения, grid, pack
    style_parameters: StyleParameters | None = None  # параметры стилей виджета
    values: list[str] = field(default_factory=list)
    default: str = ''
    arrow_shape_color: str = 'black'  # цвет стрелки

    popdown_back_color: str | None = None  # цвет фона меню выпадающего списка
    popdown_font_color: str | None = None  # цвет шрифта меню выпадающего списка
    popdown_select_back_color: str | None = None  # цвет фона выбранного пункта меню выпадающего списка
    popdown_select_font_color: str | None = 'steelblue'  # цвет шрифта выбранного пункта меню выпадающего списка
    readonly: bool = True  # только для чтения (запретить редактирование)
    callback: Callable | None = None  # функция которая применяется к выбранному значению (опция)
    _form: ttk.Combobox | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        # стили для ttk
        self._style_name = f'Custom{id(self)}.TCombobox'  # стиль для каждого комбо уникальный
        style = ttk.Style()
        style.theme_use('clam')

        # создание виджета с привязкой имени стиля
        self._form = ttk.Combobox(
            self.parent, values=self.values,
            state='readonly' if self.readonly else 'normal',
            style=self._style_name,
        )

        # так как у ttk виджетов часто параметры специфические, карту лучше прописывать здесь
        ttk_style_map_default = {
            "fieldbackground": self.style_parameters.back_color,
            "background": self.style_parameters.back_color,
            "foreground": self.style_parameters.text_parameters.text_color,
            "arrowcolor": self.arrow_shape_color,
        }

        ttk_style_map_hover = {
            "fieldbackground": self.style_parameters.hover_back_color,
            "background": self.style_parameters.hover_back_color,
            "foreground": self.style_parameters.text_parameters.text_color,
            "arrowcolor": self.arrow_shape_color,
        }
        ttk_style_map_active = {
            "fieldbackground": self.style_parameters.active_back_color,
            "background": self.style_parameters.active_back_color,
            "foreground": self.style_parameters.text_parameters.text_color,
            "arrowcolor": self.arrow_shape_color,
        }

        # подключить стили (опционально)
        if self.style_parameters is not None:
            widget_helpers.StyleHandler(
                parent=self.parent,
                form=self._form,
                parameters=self.style_parameters,
                ttk_style_name=self._style_name,
                ttk_style_map_default=ttk_style_map_default,
                ttk_style_map_hover=ttk_style_map_hover,
                ttk_style_map_active=ttk_style_map_active,
            )

        # остается без изменений

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

        # размещение виджета (обязательно)
        widget_helpers.placement_widget_to_parent(
            widget=self._form,
            placement_strategy=self.placement_strategy,
        )

    def get_value(self) -> str:
        return self._form.get()

    def set_value(self, value: str) -> None:
        self._form.set(value)
