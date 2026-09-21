from infrastructure_tk_ui.parameters_class import PackParameters
from dataclasses import dataclass, field
import tkinter as tk


@dataclass
class ScrollableWidget:
    frame: tk.Tk | tk.Frame | tk.Toplevel  # поле на котором будут прокручиваемые элементы
    back_color: str | None = None  # Цвет фона, подложки, если пустой то возьмется цвет родителя
    pack_parameters: PackParameters = field(default_factory=PackParameters)
    scrollbar: bool = False  # добавление скролл бара со стрелочками
    _form: tk.Frame | None = None

    @property
    def form(self):
        return self._form

    def __post_init__(self):
        """Сделать скролируемое поле"""
        # взять цвет родительского окна, если не передан
        self.back_color = self.back_color if self.back_color is not None else self.frame.cget('bg')

        # canvas, окно поддерживающее прокрутку
        canvas = tk.Canvas(self.frame)

        if self.scrollbar:
            scrollbar = tk.Scrollbar(self.frame, orient='vertical', command=canvas.yview)
            scrollbar.pack(side='right', fill='y')
            # отключить встроенный обработчик MouseWheel у Scrollbar (иначе tkinter выдает ошибку)
            scrollbar.bind('<MouseWheel>', lambda e: 'break')

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
        # обновлять scrollregion (подстройка под изменение размеров фрейма)
        self._form.bind(
            '<Configure>',
            lambda event: canvas.configure(scrollregion=canvas.bbox('all')),
        )

        # # скролл колесом
        def on_wheel(event):
            if self.scrollbar and event.widget == scrollbar:
                return
            canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

        canvas.bind('<Enter>', lambda e: canvas.bind_all('<MouseWheel>', on_wheel))
        canvas.bind('<Leave>', lambda e: canvas.unbind_all('<MouseWheel>'))
