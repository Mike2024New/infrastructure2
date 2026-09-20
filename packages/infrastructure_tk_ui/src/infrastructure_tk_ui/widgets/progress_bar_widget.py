from typing import Literal
import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass, field
from infrastructure_tk_ui.widgets.frame_widget import FrameWidget
from infrastructure_tk_ui.widgets.label_widget import LabelWidget
from infrastructure_tk_ui.parameters_class import FontParameters, PackParameters


@dataclass
class ProgressWidget:
    frame: tk.Tk | tk.Frame | tk.Toplevel
    back_color: str = 'gray'
    border: int = 0
    border_relief: Literal['solid', 'ridge', 'flat', 'groove', 'raised', 'sunken'] = 'solid'
    label_text: str = 'lbl'
    font_parameters: FontParameters = field(default_factory=FontParameters)
    pack_parameters: PackParameters = field(default_factory=PackParameters)  # ← для progressbar
    outer_pack_parameters: PackParameters = field(
        default_factory=lambda: PackParameters(expand=True, fill='both')
    )  # для самого ProgressWidget
    _form: FrameWidget | None = None
    _progress: ttk.Progressbar | None = None

    @property
    def form(self):
        return self._form.form

    def __post_init__(self):
        self._form = FrameWidget(
            frame=self.frame,
            back_color=self.back_color,
            border=self.border,
            border_relief=self.border_relief,
            pack_parameters=self.outer_pack_parameters,
        )
        if self.label_text:
            LabelWidget(
                frame=self._form.form,
                text=self.label_text,
                font_parameters=self.font_parameters,
            )
        self._progress = ttk.Progressbar(self._form.form, mode='determinate', length=400)
        self._progress.pack(**self.pack_parameters.get())

    def set_value(self, val: int):
        self._progress['value'] = val

    def close(self):
        self._form.form.destroy()
