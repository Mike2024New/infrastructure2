import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from infrastructure_tk_ui.parameters_class import PackParameters, GridParameters
import infrastructure_tk_ui.widget_helpers as widget_helpers


@dataclass
class ProgressWidget:
    parent: tk.Tk | tk.Frame | tk.Toplevel
    placement_strategy: PackParameters | GridParameters  # способ размещения, grid, pack
    back_color: str | None = None  # Цвет фона, подложки, если пустой то возьмется цвет родителя
    progress_fill_color: str = 'steelblue'  # цвет шкалы прогресса
    progress_border_color: str = 'black'  # цвет рамки вокруг шкалы прогресса
    _form: ttk.Progressbar | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        # взять цвет родительского окна, если не передан
        self.back_color = self.back_color if self.back_color is not None else self.parent.cget('bg')
        self._style_name = f'Custom{id(self)}.Horizontal.TProgressbar'  # стиль для каждого прогресс бара уникален
        style = ttk.Style()
        style.theme_use('clam')

        style.configure(
            self._style_name,  # у стиля свое имя
            troughcolor=self.back_color,  # Цвет фона (пустой части)
            background=self.progress_fill_color,  # Цвет заполненной части (полосы)
            bordercolor=self.progress_border_color,  # Цвет границы
        )

        self._form = ttk.Progressbar(
            self.parent,
            mode='determinate', length=400,
            style=self._style_name,
            orient='horizontal',
        )

        # размещение виджета (обязательно)
        widget_helpers.placement_widget_to_parent(
            widget=self._form,
            placement_strategy=self.placement_strategy,
        )

    def set_value(self, val: int):
        self._form['value'] = val

    def close(self):
        self._form.destroy()
