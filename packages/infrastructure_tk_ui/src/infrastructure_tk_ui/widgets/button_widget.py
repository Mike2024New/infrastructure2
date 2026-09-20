from infrastructure_tk_ui.parameters_class import PackParameters, FontParameters
from dataclasses import dataclass, field
from typing import Literal, Callable
import tkinter as tk


@dataclass
class ButtonWidget:
    frame: tk.Tk | tk.Frame | tk.Toplevel
    text: str = 'button'
    size: tuple[int, int] = (0, 0)  # размер окна, если 0, то размер будет автоматически подогнан по содержимому
    border: int = 1  # толщина бордеров
    back_color: str = 'gray'  # цвет фона подложки (можно по родительскому окну)
    active_back_color: str = 'gray'  # цвет кнопки если нажат
    justify: Literal['left', 'right', 'center'] = 'left'  # выравнивание текста слева, важно учитывать
    anchor: Literal['center', 'e', 'n', 'nw', 's', 'se', 'sw', 'w'] = 'nw'  # стартовая точка виджета (например север)
    font_parameters: FontParameters = field(default_factory=FontParameters)
    pack_parameters: PackParameters = field(default_factory=PackParameters)
    callback: Callable | None = None
    _form: tk.Button | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        self._form = tk.Button(self.frame, command=self.callback or (lambda: None))
        self._form.configure(
            text=self.text,
            width=self.size[0], height=self.size[1],
            bd=self.border,
            bg=self.back_color,
            activebackground=self.active_back_color,
            fg=self.font_parameters.font_color,
            font=(self.font_parameters.font_family, self.font_parameters.font_size, self.font_parameters.font_style),
            justify=self.justify,
            anchor=self.anchor,
            highlightthickness=0,  # убрать подсветку (потом можно будет вынести в параметры, пока просто убрать)
        )
        self._form.pack(**self.pack_parameters.get())
