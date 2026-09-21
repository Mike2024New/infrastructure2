import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass, field
from infrastructure_tk_ui.parameters_class import PackParameters


@dataclass
class ProgressWidget:
    frame: tk.Tk | tk.Frame | tk.Toplevel
    back_color: str | None = None  # Цвет фона, подложки, если пустой то возьмется цвет родителя
    progress_fill_color: str = 'steelblue'  # цвет шкалы прогресса
    progress_border_color: str = 'black'  # цвет рамки вокруг шкалы прогресса
    pack_parameters: PackParameters = field(default_factory=PackParameters)  # ← для progressbar
    _form: ttk.Progressbar | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        # взять цвет родительского окна, если не передан
        self.back_color = self.back_color if self.back_color is not None else self.frame.cget('bg')
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
            self.frame,
            mode='determinate', length=400,
            style=self._style_name,
            orient='horizontal',
        )
        self._form.pack(**self.pack_parameters.get())

    def set_value(self, val: int):
        self._form['value'] = val

    def close(self):
        self._form.destroy()
