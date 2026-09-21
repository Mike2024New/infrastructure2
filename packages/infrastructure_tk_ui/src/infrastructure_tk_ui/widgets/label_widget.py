from infrastructure_tk_ui.parameters_class import FontParameters, PackParameters
from dataclasses import dataclass, field
from typing import Literal
import tkinter as tk


@dataclass
class LabelWidget:
    frame: tk.Tk | tk.Frame | tk.Toplevel
    text: str = 'label'
    back_color: str | None = None  # Цвет фона, подложки, если пустой то возьмется цвет родителя
    justify: Literal['left', 'right', 'center'] = 'left'  # выравнивание текста слева, важно учитывать
    anchor: Literal['center', 'e', 'n', 'nw', 's', 'se', 'sw', 'w'] = 'nw'  # стартовая точка виджета (например север)
    font_parameters: FontParameters = field(default_factory=FontParameters)
    pack_parameters: PackParameters = field(default_factory=PackParameters)
    _form: tk.Label | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        """Размещение label на форме"""
        # взять цвет родительского окна, если не передан
        self.back_color = self.back_color if self.back_color is not None else self.frame.cget('bg')
        font_style = self.font_parameters.get()
        self._form = tk.Label(
            self.frame,
            text=self.text,
            bg=self.back_color,
            fg=font_style.color,
            font=(font_style.family, font_style.size, font_style.style),
            justify=self.justify,
            anchor=self.anchor,
        )
        self._form.pack(**self.pack_parameters.get())
