from infrastructure_tk_ui.parameters_class import PackParameters
from infrastructure_tk_ui.widgets.frame_widget import FrameWidget
from dataclasses import dataclass, field
from typing import Literal
import tkinter as tk


@dataclass
class ScrollableWidget:
    frame: tk.Tk | tk.Frame | tk.Toplevel  # поле на котором будут прокручиваемые элементы
    back_color: str = 'gray'  # цвет фона подложки (можно по родительскому окну)
    border: int = 0  # толщина бордеров
    border_relief: Literal['solid', 'ridge', 'flat', 'groove', 'raised', 'sunken'] = 'solid'  # форма бордеров
    pack_parameters: PackParameters = field(default_factory=PackParameters)
    scrollbar: bool = False  # добавление скролл бара со стрелочками
    _form: tk.Frame | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        """Сделать скролируемое поле"""

        self._scroll_container = FrameWidget(
            frame=self.frame,
            back_color=self.back_color,
            border=self.border,
            border_relief=self.border_relief,
            pack_parameters=PackParameters(expand=True, fill='both'),
        )
        canvas = tk.Canvas(self._scroll_container.form)
        if self.scrollbar:
            scrollbar = tk.Scrollbar(self._scroll_container.form, orient='vertical', command=canvas.yview)
            scrollbar.pack(side='right', fill='y')
        canvas.configure(
            bg=self.back_color,
            bd=0,  # рамку рисует внешний FrameWidget
            highlightthickness=0,  # убрать подсветку (потом можно будет вынести в параметры, пока просто убрать)
        )
        canvas.pack(**self.pack_parameters.get())
        self._form = tk.Frame(canvas)  # прокручиваемое поле
        self._form.configure(bg=self.back_color, bd=0)
        window_id = canvas.create_window((0, 0), window=self._form, anchor='nw')

        # растянуть фрейм по ширине canvas
        canvas.bind(
            '<Configure>',
            lambda event: canvas.itemconfig(window_id, width=event.width),
        )
        # обновлять scrollregion при изменении размеров фрейма
        self._form.bind(
            '<Configure>',
            lambda event: canvas.configure(scrollregion=canvas.bbox('all')),
        )
        # скролл колесом
        canvas.bind_all(
            '<MouseWheel>',
            lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units'),
        )
