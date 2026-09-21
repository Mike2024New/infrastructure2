from infrastructure_tk_ui.parameters_class import PackParameters, FontParameters
from dataclasses import dataclass, field
from typing import Literal
import tkinter as tk


@dataclass
class TextAreaWidget:
    frame: tk.Tk | tk.Frame | tk.Toplevel
    text: str = ''
    size: tuple[int, int] = (0, 0)  # размер окна, ширина(игнорируется если expand), и высота в строках
    back_color: str | None = None  # Цвет фона, подложки, если пустой то возьмется цвет родителя
    border: int = 1  # толщина бордеров
    border_relief: Literal['solid', 'ridge', 'flat', 'groove', 'raised', 'sunken'] = 'solid'  # форма бордеров
    wrap: Literal['word', 'none', 'char'] = 'word'
    justify: Literal['left', 'right', 'center'] = 'left'  # выравнивание текста слева, важно учитывать
    anchor: Literal['center', 'e', 'n', 'nw', 's', 'se', 'sw', 'w'] = 'nw'  # стартовая точка виджета (например север)
    font_parameters: FontParameters = field(default_factory=FontParameters)
    pack_parameters: PackParameters = field(default_factory=PackParameters)
    editable: bool = True
    _form: tk.Text | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        # взять цвет родительского окна, если не передан
        self.back_color = self.back_color if self.back_color is not None else self.frame.cget('bg')
        self._form = tk.Text(self.frame)
        self._form.configure(
            width=self.size[0], height=self.size[1],
            bg=self.back_color, bd=self.border, relief=self.border_relief, fg=self.font_parameters.font_color,
            font=(self.font_parameters.font_family, self.font_parameters.font_size, self.font_parameters.font_style),
            wrap=self.wrap, state='normal' if self.editable else 'disabled',
            highlightthickness=0,  # убрать подсветку (потом можно будет вынести в параметры, пока просто убрать)
        )

        self._form.pack(**self.pack_parameters.get())

    def insert_text(self, text: str) -> None:
        if self._form and text:
            if not self.editable:
                self._form.configure(state='normal')
            self._form.insert(tk.END, text)
            self._form.see(tk.END)
            if not self.editable:
                self._form.configure(state='disabled')

    def clear_text(self) -> None:
        if not self._form:
            return
        if not self.editable:
            self._form.configure(state='normal')
        self._form.delete('1.0', tk.END)
        if not self.editable:
            self._form.configure(state='disabled')

    def get_text(self) -> str:
        return self._form.get('1.0', tk.END).rstrip('\n')
