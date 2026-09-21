from infrastructure_tk_ui.parameters_class import PackParameters, BorderParameters, GridParameters
from dataclasses import dataclass, field
import tkinter as tk


@dataclass
class FrameWidget:
    frame: tk.Tk | tk.Frame | tk.Toplevel
    back_color: str | None = None  # Цвет фона, подложки, если пустой то возьмется цвет родителя
    border_parameters: BorderParameters = field(default_factory=BorderParameters)  # параметры бордеров
    pack_parameters: PackParameters | None = None
    grid_parameters: GridParameters | None = None
    _form: tk.Frame | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        # взять цвет родительского окна, если не передан
        self.back_color = self.back_color if self.back_color is not None else self.frame.cget('bg')
        self._form = tk.Frame(
            self.frame,
            bg=self.back_color,
            border=self.border_parameters.th,
            relief=self.border_parameters.relief,
        )

        if all(pack is not None for pack in (self.pack_parameters, self.pack_parameters)):
            raise RuntimeError(f'Выберите что то одно из стратегий размещения')
        elif self.pack_parameters is not None:
            self._form.pack(**self.pack_parameters.get())
        elif self.grid_parameters is not None:
            # rows, colums = self.frame.grid_size()
            # if self.grid_parameters.row > rows - 1 or self.grid_parameters.col > colums - 1:
            #     raise RuntimeError(
            #         f'Указанная ячейка, находится за пределами родительского окна {rows, colums}'
            #     )
            self._form.grid(**self.grid_parameters.get())
        else:
            raise RuntimeError(
                f'Не указана стратегия размещения. '
                f'Передай либо pack_parameters, либо grid_parameters.'
            )
