from infrastructure_tk_ui.parameters_class import PackParameters, FontParameters, AnimationParameters, BorderParameters
from dataclasses import dataclass, field
from typing import Literal
import tkinter as tk


@dataclass
class TextAreaWidget:
    frame: tk.Tk | tk.Frame | tk.Toplevel
    text: str = ''
    size: tuple[int, int] = (0, 0)  # размер окна, ширина(игнорируется если expand), и высота в строках
    back_color: str | None = None  # Цвет фона, подложки, если пустой то возьмется цвет родителя
    wrap: Literal['word', 'none', 'char'] = 'word'
    border_parameters: BorderParameters = field(default_factory=BorderParameters)  # параметры бордеров
    font_parameters: FontParameters = field(default_factory=FontParameters)  # параметры шрифта
    pack_parameters: PackParameters = field(default_factory=PackParameters)  # параметры позиционирования виджета
    animation_parameters: AnimationParameters | None = None  # параметры анимации виджета
    editable: bool = True  # разрешить редактировать поле виджета?
    _form: tk.Text | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        # взять цвет родительского окна, если не передан
        self.back_color = self.back_color if self.back_color is not None else self.frame.cget('bg')
        font_style = self.font_parameters.get()

        self._form = tk.Text(self.frame)
        self._form.configure(
            bg=self.back_color,
            border=self.border_parameters.th,
            relief=self.border_parameters.relief,
            width=self.size[0], height=self.size[1],
            fg=font_style.color,
            font=(font_style.family, font_style.size, font_style.style),
            wrap=self.wrap, state='normal' if self.editable else 'disabled',
            highlightthickness=0,  # убрать подсветку (потом можно будет вынести в параметры, пока просто убрать)
            insertwidth=2,  # ширина курсора
            selectbackground=self.font_parameters.select_text_back_color,
        )
        # подключить self.animation_parameters, если он был передан (цвета при наведении и активации)
        if self.animation_parameters is not None:
            self.animation_parameters.bind(back_color=self.back_color, form=self._form)

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
