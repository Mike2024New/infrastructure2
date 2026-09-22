from infrastructure_tk_ui.parameters_class import PackParameters, StyleParameters, GridParameters
import infrastructure_tk_ui.widget_helpers as widget_helpers
from dataclasses import dataclass
from typing import Literal
import tkinter as tk


@dataclass
class TextAreaWidget:
    parent: tk.Tk | tk.Frame | tk.Toplevel
    placement_strategy: PackParameters | GridParameters  # способ размещения, grid, pack
    text: str = 'label'
    style_parameters: StyleParameters | None = None  # параметры стилей виджета
    size: tuple[int, int] = (0, 0)  # размер окна, ширина(игнорируется если expand), и высота в строках
    wrap: Literal['word', 'none', 'char'] = 'word'
    editable: bool = True  # разрешить редактировать поле виджета?
    _form: tk.Text | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        self._form = tk.Text(self.parent)
        self._form.configure(
            width=self.size[0], height=self.size[1],
            wrap=self.wrap, state='normal' if self.editable else 'disabled',
        )

        # подключить стили (опционально)
        if self.style_parameters is not None:
            widget_helpers.StyleHandler(
                parent=self.parent,
                form=self._form,
                parameters=self.style_parameters,
            )

        # размещение виджета (обязательно)
        widget_helpers.placement_widget_to_parent(
            widget=self._form,
            placement_strategy=self.placement_strategy,
        )
        if self.text:
            self.insert_text(text=self.text)

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
