from infrastructure_tk_ui.parameters_class import PackParameters, StyleParameters, GridParameters
import infrastructure_tk_ui.widget_helpers as widget_helpers
from dataclasses import dataclass
import tkinter as tk


@dataclass
class FrameWidget:
    parent: tk.Tk | tk.Frame | tk.Toplevel
    placement_strategy: PackParameters | GridParameters  # способ размещения, grid, pack
    style_parameters: StyleParameters | None = None  # параметры стилей виджета
    grid_map: tuple[tuple[int, ...], tuple[int, ...]] | None = None  # схема сетки в % например: ((30, 60), (50, 50))
    _form: tk.Frame | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        self._form = tk.Frame(self.parent)

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

        if self.grid_map:
            # деление главного окна на ячейки (grid)
            # строки (лучше взять за правило, что все составляет часть от 100%, и делить так чтобы в сумме 100)
            rows, columns = self.grid_map

            if sum(rows) > 100 or sum(columns) > 100:
                raise RuntimeError(f'Сумма значений карты ячеек должно быть не больше 100 (для каждой оси)')

            for i, row_height in enumerate(rows):
                self._form.grid_rowconfigure(i, weight=row_height)

            # строки (лучше взять за правило, что все составляет часть от 100%, и делить так чтобы в сумме 100)
            for i, column_height in enumerate(columns):
                self._form.grid_columnconfigure(i, weight=column_height)
