from infrastructure_tk_ui.parameters_class import PackParameters, GridParameters, StyleParameters
import infrastructure_tk_ui.widget_helpers as widget_helpers
from dataclasses import dataclass
import tkinter as tk


@dataclass
class ScrollableWidget:
    parent: tk.Tk | tk.Frame | tk.Toplevel  # поле на котором будут прокручиваемые элементы
    placement_strategy: PackParameters | GridParameters  # способ размещения, grid, pack
    style_parameters: StyleParameters | None = None  # параметры стилей виджета
    _form: tk.Frame | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        """Сделать скролируемое поле"""
        # canvas, окно поддерживающее прокрутку
        canvas = tk.Canvas(self.parent)
        canvas.configure(bg='black')
        # размещение виджета (обязательно)
        widget_helpers.placement_widget_to_parent(
            widget=canvas,
            placement_strategy=self.placement_strategy,
        )

        # прокручиваемое поле
        self._form = tk.Frame(canvas)
        self._form.configure(bg='black')
        window_id = canvas.create_window((0, 0), window=self._form, anchor='nw')

        # растянуть фрейм по ширине canvas
        canvas.bind(
            '<Configure>',
            lambda event: canvas.itemconfig(window_id, width=event.width),
        )
        # обновлять scrollregion (подстройка под изменение размеров фрейма)
        self._form.bind(
            '<Configure>',
            lambda event: canvas.configure(scrollregion=canvas.bbox('all')),
        )

        # # скролл колесом
        def on_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

        canvas.bind('<Enter>', lambda e: canvas.bind_all('<MouseWheel>', on_wheel))
        canvas.bind('<Leave>', lambda e: canvas.unbind_all('<MouseWheel>'))
