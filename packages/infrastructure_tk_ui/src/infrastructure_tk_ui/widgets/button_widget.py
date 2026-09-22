from infrastructure_tk_ui.parameters_class import PackParameters, GridParameters
from infrastructure_tk_ui.parameters_class import StyleParameters
import infrastructure_tk_ui.widget_helpers as widget_helpers
from dataclasses import dataclass
import tkinter as tk
from typing import Callable


@dataclass
class ButtonWidget:
    parent: tk.Tk | tk.Frame | tk.Toplevel
    placement_strategy: PackParameters | GridParameters  # способ размещения, grid, pack
    text: str = 'label'
    style_parameters: StyleParameters | None = None  # параметры стилей виджета
    callback: Callable | None = None
    _form: tk.Button | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        self._form = tk.Button(self.parent, text=self.text, command=self.callback or (lambda: None))
        self._form.configure(
            cursor='hand2',
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
