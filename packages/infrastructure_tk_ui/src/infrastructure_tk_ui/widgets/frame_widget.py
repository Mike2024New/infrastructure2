from infrastructure_tk_ui.parameters_class import PackParameters
from dataclasses import dataclass, field
from typing import Literal
import tkinter as tk


@dataclass
class FrameWidget:
    frame: tk.Tk | tk.Frame | tk.Toplevel
    back_color: str = 'gray'  # цвет фона подложки (можно по родительскому окну)
    border: int = 0  # толщина бордеров
    border_relief: Literal['solid', 'ridge', 'flat', 'groove', 'raised', 'sunken'] = 'solid'  # форма бордеров
    pack_parameters: PackParameters = field(default_factory=PackParameters)
    _form: tk.Frame | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        self._form = tk.Frame(
            self.frame,
            bg=self.back_color,
            bd=self.border,
            relief=self.border_relief,
        )
        self._form.pack(
            fill=self.pack_parameters.fill,
            padx=self.pack_parameters.padx,
            pady=self.pack_parameters.pady,
            expand=self.pack_parameters.expand,
        )
