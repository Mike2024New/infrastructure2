import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass, field
from infrastructure_tk_ui.parameters_class import FontParameters, PackParameters


@dataclass
class ProgressWidget:
    frame: tk.Tk | tk.Frame | tk.Toplevel
    back_color: str | None = None  # Цвет фона, подложки, если пустой то возьмется цвет родителя
    progress_fill_color: str = 'steelblue'  # цвет шкалы прогресса
    progress_border_color: str = 'black'  # цвет рамки вокруг шкалы прогресса
    font_parameters: FontParameters = field(default_factory=FontParameters)
    pack_parameters: PackParameters = field(default_factory=PackParameters)  # ← для progressbar
    _form: ttk.Progressbar | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        # взять цвет родительского окна, если не передан
        self.back_color = self.back_color if self.back_color is not None else self.frame.cget('bg')
        style = ttk.Style()
        style.theme_use('clam')

        style.configure(
            "Custom.Horizontal.TProgressbar",  # Даём стилю своё имя
            troughcolor=self.back_color,  # Цвет фона (пустой части)
            background=self.progress_fill_color,  # Цвет заполненной части (полосы)
            bordercolor=self.progress_border_color,  # Цвет границы
        )

        self._form = ttk.Progressbar(
            self.frame,
            mode='determinate', length=400,
            style='Custom.Horizontal.TProgressbar',
            orient='horizontal',
        )
        self._form.pack(**self.pack_parameters.get())

    def set_value(self, val: int):
        self._form['value'] = val

    def close(self):
        self._form.destroy()