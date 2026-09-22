from infrastructure_tk_ui.parameters_class import PackParameters, StyleParameters, GridParameters
import infrastructure_tk_ui.widget_helpers as widget_helpers
from dataclasses import dataclass, field
from typing import Callable
import tkinter as tk


@dataclass
class RadioGroupWidget:
    parent: tk.Tk | tk.Frame | tk.Toplevel
    options: list[str] = field(default_factory=list)
    default: str = ''
    placement_strategy: PackParameters | GridParameters = field(default_factory=PackParameters)
    style_parameters: StyleParameters | None = None
    callback: Callable | None = None
    _var: tk.StringVar | None = None
    _forms: list[tk.Radiobutton] = field(default_factory=list)

    @property
    def form(self):
        return self._forms[0] if self._forms else None

    def __post_init__(self):
        self._var = tk.StringVar(value=self.default)
        for option in self.options:
            rb = tk.Radiobutton(
                self.parent,
                text=option,
                variable=self._var,
                value=option,
            )
            if self.style_parameters is not None:
                widget_helpers.StyleHandler(
                    parent=self.parent,
                    form=rb,
                    parameters=self.style_parameters,
                )
            widget_helpers.placement_widget_to_parent(
                widget=rb,
                placement_strategy=self.placement_strategy,
            )
            self._forms.append(rb)

        if self.callback is not None:
            self._var.trace_add('write', lambda *_: self.callback(self.get_value()))  # noqa

    def get_value(self) -> str:
        return self._var.get()

    def set_value(self, value: str) -> None:
        self._var.set(value)
