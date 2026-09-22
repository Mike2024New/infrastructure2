from infrastructure_tk_ui.parameters_class import PackParameters, StyleParameters, GridParameters
import infrastructure_tk_ui.widget_helpers as widget_helpers
from dataclasses import dataclass
from typing import Callable
import tkinter as tk


@dataclass
class CheckBoxWidget:
    parent: tk.Tk | tk.Frame | tk.Toplevel
    placement_strategy: PackParameters | GridParameters  # способ размещения, grid, pack
    text: str = 'checkbox'
    style_parameters: StyleParameters | None = None  # параметры стилей виджета
    callback: Callable | None = None
    _form: tk.Checkbutton | None = None
    _is_active: tk.BooleanVar = False

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        self._form = tk.Checkbutton(self.parent)
        self._is_active = tk.BooleanVar()
        self._form.configure(
            text=self.text,
            variable=self._is_active,
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

    def get_value(self):
        return self._is_active.get()

    def set_value(self, val: bool):
        self._is_active.set(value=val)
