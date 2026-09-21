import random
from infrastructure_tk_ui import RootWidget, LabelWidget, ButtonWidget
from infrastructure_tk_ui import TextAreaWidget, ScrollableWidget, ProgressWidget
from infrastructure_tk_ui import FrameWidget
from infrastructure_tk_ui import FontParameters, PackParameters, BorderParameters

"""
Примеры с демонстрацией наиболее частых ситуаций и как работает.
Основная суть - это обертки, вся логика реализованна в датаклассах (с удобными и понятными параметрами).
Нужно просто прописать параметры, и готово формы собраны.

Список примеров:
    ex1 - создание базового окна root
    ex2 - работа с основными виджетами
    ex3 - scrollable окно с прокручиванием
    ex4 - модальное окно
    ex5 - прогресс бар 

"""


def ex1():
    """Создание главного окна, привязка событий."""
    root = RootWidget(
        title='My window',
        back_color='orange',  # если в дочерних виджетах не переопределять это поле то цвет возьмется этот
        size=(300, 200),
        offset=(1000, 400),
        resize_width=False, resize_height=False,
    )
    # все действия с виджетом через свойство form (это разделение нужно так как иногда в классе бывают методы)
    root.form.bind('<Button-1>', lambda event: print(f'Нажали на форму'))  # подвязка событий (клик мышью)
    root.form.after(1000, print, 'форма загрузилась')  # callback - функция после запуска формы
    root.form.mainloop()


def ex2():
    """
    Пример создания фрейма (области размещения на нем виджетов) и помещение на него основных виджетов
    """

    root = RootWidget(
        offset=(1200, 300),
        back_color='gray'  # если в дочерних виджетах не переопределять это поле то цвет возьмется этот
    )
    frame = FrameWidget(
        frame=root.form,  # форма на которой размещается
        # border=1,  # если нужно то включить бордер (задав толщину)
        pack_parameters=PackParameters(
            fill='both',  # для рамки лучше both (x, y)
            expand=True,  # растянуть на всю свободную и доступную область
        ),
    )
    # размещение label виджета на рамке (_label объект для обратной связи с классом производителем, form базовые методы tkinter)
    _label = LabelWidget(
        text='example',
        frame=frame.form,
        pack_parameters=PackParameters(fill='x', expand=False),
        font_parameters=FontParameters(color='black', size=14, style='bold', family='mono'),
    )
    # размещение text_area виджета на рамке (_text_area объект для обратной связи с классом производителем, form базовые методы tkinter)
    text_area = TextAreaWidget(
        frame=frame.form,
        text='Первая строка',
        size=(50, 2),  # высота в строках (задаваемых в font)
        wrap='word',
        pack_parameters=PackParameters(fill='both', expand=True),
        font_parameters=FontParameters(size=14)
    )
    # размещение button виджета на рамке (_button объект для обратной связи с классом производителем, form базовые методы tkinter)
    # связка text_area и button
    ButtonWidget(frame=frame.form, text='текст из поля', callback=lambda: print(text_area.get_text()))
    ButtonWidget(frame=frame.form, text='очистить поле', callback=lambda: text_area.clear_text())
    root.form.mainloop()


def ex3():
    """Создание scrollable прокручиваемого фрейма, когда элементов много и требуется прокрутка"""
    root = RootWidget(
        size=(400, 200),
        offset=(1200, 300),
        back_color='gray',  # если в дочерних виджетах не переопределять это поле то цвет возьмется этот по умолчанию
    )
    frame = FrameWidget(
        frame=root.form,  # форма на которой размещается
        border_parameters=BorderParameters(th=1, relief='ridge'),
        pack_parameters=PackParameters(
            fill='both',  # для рамки лучше both (x, y)
            expand=True,  # растянуть на всю свободную и доступную область
            padx=15, pady=15,
        ),
    )
    scrollable = ScrollableWidget(
        frame=frame.form,
        scrollbar=True,  # добавить полосу с прокруткой
    )
    [LabelWidget(frame=scrollable.form, text=f'label {i}') for i in range(20)]
    ButtonWidget(frame=scrollable.form, callback=lambda: print(f'Наж. кнопку'))
    root.form.mainloop()


def ex4():
    """Простой шутливый пример посторения диалогового окна с всплывающим новым модальным окном"""
    counter = 0
    window = RootWidget(
        title='Это точно установщик?',
        offset=(1200, 300),
        back_color='orange',  # если в дочерних виджетах не переопределять это поле то цвет возьмется этот по умолчанию
        resize_width=False, resize_height=False
    )
    frame = FrameWidget(frame=window.form, border_parameters=BorderParameters(th=1, relief='ridge'))
    text_area = TextAreaWidget(frame=frame.form, size=(30, 5), editable=False)
    text_area.insert_text(text='Вы хотите установить приложение?')
    font_parameters = FontParameters(size=12, style='bold')
    pack_parameters = PackParameters(expand=True, side='left')

    def modal_window(text: str):
        """Модальное окно которое появляется при нажатии на кнопки"""
        nonlocal counter
        back_color = ('gray', 'green', 'yellow', 'red')[counter]
        mod_win = RootWidget(
            title='А я точно уверен?', offset=(1200, 300),
            back_color=back_color, parent=window.form, modal=True,  # установка свойств дочернего окна
        )
        fr = FrameWidget(
            frame=mod_win.form,
            border_parameters=BorderParameters(th=1, relief='ridge'),
            back_color=back_color
        )
        ta = TextAreaWidget(frame=fr.form, size=(30, 5), editable=False)
        ta.insert_text(text=text)
        if counter <= 2:
            text = f'Ваш уровень уверенности {counter}'
        else:
            text = f'Нет слишком не уверенно. Сброс.'
            counter = 0
        LabelWidget(frame=fr.form, text=text)
        _button = ButtonWidget(
            frame=fr.form,
            text='Попробовать чуточку увереннее',
            callback=lambda: mod_win.form.destroy(),
        )
        counter += 1

    _button1 = ButtonWidget(
        frame=frame.form, text='уверен, что не уверен',
        pack_parameters=pack_parameters, font_parameters=font_parameters,
        callback=lambda: modal_window(text='Приложение не может быть установлено, так как вы не уверены'),
    )
    _button2 = ButtonWidget(
        frame=frame.form, text='не уверен, что уверен',
        pack_parameters=pack_parameters, font_parameters=font_parameters,
        callback=lambda: modal_window(
            text='Приложение не может быть установлено, так как вы выразили сомнение в своей неуверенности'),
    )
    window.form.mainloop()


def ex5():
    """Пример работы с прогесс баром."""

    class Window:
        def __init__(self):
            self._window = RootWidget(
                title='window', offset=(1200, 300), resize_width=True, resize_height=True
            )
            self._running = True
            # построение прогресс бара. Задается рамка, за тем на ней уже размещаются виджеты
            self._progress_frame = FrameWidget(
                frame=self._window.form, border_parameters=BorderParameters(th=1, relief='ridge')
            )
            font_parameters = FontParameters(size=10)
            # можно не создавать переменую если не нужна обратная связь
            LabelWidget(
                frame=self._progress_frame.form,
                text='установка пакета', font_parameters=font_parameters,
            )  # заголовок
            self._progress = ProgressWidget(frame=self._progress_frame.form)
            ButtonWidget(
                frame=self._progress_frame.form,
                text='отмена',
                callback=self._stop,
                font_parameters=font_parameters
            )

        def _stop(self):
            self._running = False
            self._progress.close()
            self._progress_frame.form.destroy()
            self._window.form.destroy()

        def _progress_imitation(self, i=0):
            """Просто иммитация прогресс бара"""
            if not self._running:
                return
            if i > 100:
                self._stop()
                return
            self._progress.set_value(i)
            self._window.form.after(random.randint(20, 60), self._progress_imitation, i + 1)

        def start(self):
            # событие запуска прогресс бара, в данном случае через стартовый callback
            self._window.form.after(1000, self._progress_imitation)  # noqa
            self._window.form.mainloop()

    # создание и запуск класса
    window = Window()
    window.start()


if __name__ == '__main__':
    # ex1()
    # ex2()
    # ex3()
    ex4()
    # ex5()
