import tkinter as tk
from dataclasses import dataclass, field
from infrastructure_tk_ui import BorderParameters


@dataclass
class RootWidget:
    title: str = 'window'  # заголовок окна
    size: tuple[int, int] = (0, 0)  # размер окна, если 0, то размер будет автоматически подогнан по содержимому
    offset: tuple[int, int] = (0, 0)  # смещение верхнего левого угла окна относительно верхнего левого угла экрана
    back_color: str = 'white'  # фоновый цвет
    grid_map: tuple[tuple[int, ...], tuple[int, ...]] | None = None  # схема сетки в % например: ((30, 60), (50, 50))
    border_parameters: BorderParameters = field(default_factory=BorderParameters)  # параметры бордеров
    resize_width: bool = False  # можно растягивать по x?
    resize_height: bool = False  # можно растягивать по y?
    parent: tk.Tk | tk.Toplevel | None = None  # Если окно вторичное, поверх основного -> передать его
    modal: bool = False  # блокировать родительское окно? (параметр не актуален если не передан parent)
    _form: tk.Tk | tk.Toplevel | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        geometry = ''
        if self.size[0] > 0 and self.size[1] > 0:
            geometry = f"{self.size[0]}x{self.size[1]}"

        geometry += f"+{self.offset[0]}+{self.offset[1]}"

        # определение статуса окна - основное или вторичное. Модальное или нет
        if self.parent is not None:  # окно дочернее
            self._form = tk.Toplevel(self.parent)
            if self.modal:  # является модальным?
                self._form.transient(self.parent)  # окно всегда поверх родителя
                self._form.grab_set()
        else:  # обычное главное окно
            self._form = tk.Tk()

        self._form.title(self.title)
        self._form.resizable(width=self.resize_width, height=self.resize_height)
        self._form.geometry(geometry)
        self._form.configure(
            bg=self.back_color,
            border=self.border_parameters.th,
            relief=self.border_parameters.relief,
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
