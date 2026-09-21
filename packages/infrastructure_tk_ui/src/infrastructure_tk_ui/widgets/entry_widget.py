from infrastructure_tk_ui.parameters_class import PackParameters, FontParameters, AnimationParameters
from dataclasses import dataclass, field
from typing import Literal
import tkinter as tk


@dataclass
class EntryWidget:
    frame: tk.Tk | tk.Frame | tk.Toplevel
    text: str = ''
    width: int = 0
    back_color: str | None = None  # Цвет фона, подложки, если пустой то возьмется цвет родителя
    select_text_back_color: str = 'steelblue'  # цвет выделенного текста
    border: int = 0  # толщина бордеров
    border_relief: Literal['solid', 'ridge', 'flat', 'groove', 'raised', 'sunken'] = 'solid'  # форма бордеров
    font_parameters: FontParameters = field(default_factory=FontParameters)  # параметры шрифта
    pack_parameters: PackParameters = field(default_factory=PackParameters)  # параметры позиционирования виджета
    animation_parameters: AnimationParameters | None = None  # параметры анимации виджета
    editable: bool = True  # разрешить редактировать поле виджета?
    _form: tk.Entry | None = None

    def __post_init__(self):
        self.back_color = self.back_color if self.back_color is not None else self.frame.cget('bg')

        font_style = self.font_parameters.get()

        self._form = tk.Entry(self.frame)
        self._form.configure(
            bg=self.back_color,
            border=self.border,
            relief=self.border_relief,
            width=self.width if self.width > 0 else 20,
            fg=font_style.color,
            font=(font_style.family, font_style.size, font_style.style),
            state='normal' if self.editable else 'disabled',
            highlightthickness=0,  # убрать подсветку (потом можно будет вынести в параметры, пока просто убрать)
            insertwidth=2, # ширина курсора
            selectbackground=self.select_text_back_color,
        )
        # подключить self.animation_parameters, если он был передан (цвета при наведении и активации)
        if self.animation_parameters is not None:
            self.animation_parameters.bind(back_color=self.back_color, frame=self._form)

        self._form.pack(**self.pack_parameters.get())
        if self.text:
            self.insert_text(text=self.text)

    @property
    def form(self):
        return self._form

    def insert_text(self, text: str) -> None:
        if self._form and text:
            if not self.editable:
                self._form.configure(state='normal')
            self._form.insert(tk.END, text)
            if not self.editable:
                self._form.configure(state='disabled')

    def clear_text(self) -> None:
        if not self._form:
            return
        if not self.editable:
            self._form.configure(state='normal')
        self._form.delete(0, tk.END)
        if not self.editable:
            self._form.configure(state='disabled')

    def get_text(self) -> str:
        return self._form.get()
