from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from infrastructure_tk_ui import RootWidget, CheckboxWidgetTTK, RadiobuttonGroupTTK
from infrastructure_tk_ui import StyleManager
# стили можно определить и свои (например если планируется несколько слоев виджетов), а можно взять и стандартные как в импортах ниже
from infrastructure_tk_ui import get_standart_styles
from infrastructure_tk_ui import themes_standart as themes

"""
Примеры построения основных виджетов, встроенными tkinter методами, и классами расширителями, а также применение стилей
Стили определены в ex0
"""


def ex1():
    """Создание checkbox-галочки выбора и кнопки для отслеживания состояния"""
    padx, pady = 3, 3
    # сперва создать root окно (tk.Tk())
    root = RootWidget()
    # привязать стили
    style_manager = StyleManager(
        themes=[get_standart_styles(themes.Dracula)],
        disabled_tk=False, disabled_ttk=False, disabled_options=False,
        bypass=False,  # если нужно отключить стили полностью то использовать bypass
    )
    # создание размещение элементов (всё стандартными способами tkinter)
    root.form.configure(padx=padx, pady=pady)
    # создание чекбоксов - через вспомогательный класс, базовые методы (например configure и другие) доступны через .form (escape hatch)
    check_box = CheckboxWidgetTTK(parent=root.form, text='Добавить опцию', active=False)
    check_box.form.pack(expand=True, fill='x', anchor='center')
    button = ttk.Button(root.form, text='cb1', command=lambda: print(check_box.get()))
    button.pack(expand=True, fill='x', anchor='center', padx=padx)

    # применение стилей выбранной темы
    style_manager.apply(container=root.form)
    # отрисовка формы
    root.form.mainloop()


def ex2():
    """Пример создания простого диалогового окна label и две кнопки"""
    padx, pady = 3, 3
    # сперва создать root окно (tk.Tk())
    root = RootWidget()
    # привязать стили
    style_manager = StyleManager(
        themes=[get_standart_styles(themes.LightBeige)],
        disabled_tk=False, disabled_ttk=False, disabled_options=False,
        bypass=False,  # если нужно отключить стили полностью то использовать bypass
    )
    # создание размещение элементов (всё стандартными способами tkinter)
    root.form.configure(padx=padx, pady=pady)
    lbl = ttk.Label(text=f'Установить обновление?')
    lbl.pack(fill='x', expand=True, padx=padx, pady=pady * 3)

    ttk.Button(text=f'Да', command=lambda: root.form.destroy()).pack(
        fill='x', expand=True, side='left', padx=padx, pady=pady)
    ttk.Button(text=f'Нет', command=lambda: root.form.destroy()).pack(
        fill='x', expand=True, side='left', padx=padx, pady=pady)

    # применение стилей выбранной темы
    style_manager.apply(container=root.form)
    # после применения стилей можно при необходимости для конкретных элементов переопределить свойства
    lbl.configure(font=('mono', 14))
    # отрисовка формы
    root.form.mainloop()


def ex3():
    """Создание модального окна и обработка нажатия в нем"""
    padx, pady = 3, 3
    # сперва создать root окно (tk.Tk())
    root = RootWidget()
    # привязать стили
    style_manager = StyleManager(
        themes=[get_standart_styles(themes.LightGreen)],
        disabled_tk=False, disabled_ttk=False, disabled_options=False,
        bypass=False,  # если нужно отключить стили полностью то использовать bypass
    )

    # создание размещение элементов (всё стандартными способами tkinter)
    root.form.configure(padx=padx, pady=pady)

    def create_modal():
        """создается внешнее модальное окно, и кнопка которая закрывает его"""
        modal = RootWidget(parent=root.form, modal=True)
        ttk.Button(modal.form, text=f'close', command=lambda: modal.form.destroy()).pack()

    btn = ttk.Button(text=f'Открыть', command=lambda: create_modal())
    btn.pack(fill='x', expand=True, side='left', padx=padx, pady=pady)

    # применение стилей выбранной темы
    style_manager.apply(container=root.form)
    # отрисовка формы
    root.form.mainloop()


def ex4():
    """RadioButton группа кнопок"""
    padx, pady = 3, 3
    # сперва создать root окно (tk.Tk())
    root = RootWidget()
    # привязать стили
    style_manager = StyleManager(
        themes=[get_standart_styles(themes.DarkRed)],
        disabled_tk=False, disabled_ttk=False, disabled_options=False,
        bypass=False,  # если нужно отключить стили полностью то использовать bypass
    )

    # создание размещение элементов (всё стандартными способами tkinter)
    root.form.configure(padx=padx, pady=pady)

    radio_buttons = RadiobuttonGroupTTK(parent=root.form, options=['en', 'ru', 'ge'], default_value='ru')
    for form in radio_buttons.form:
        form.pack()
    btn = ttk.Button(text='get value', command=lambda: print(radio_buttons.get_value()))
    btn.pack()

    # применение стилей выбранной темы
    style_manager.apply(container=root.form)
    # отрисовка формы
    root.form.mainloop()


def ex5():
    """Создание текстового поля (text area)"""
    padx, pady = 10, 10
    # сперва создать root окно (tk.Tk())
    root = RootWidget()
    # привязать стили
    style_manager = StyleManager(
        themes=[get_standart_styles(themes.Nord)],
        disabled_tk=False, disabled_ttk=False, disabled_options=False,
        bypass=False,  # если нужно отключить стили полностью то использовать bypass
    )

    # создание размещение элементов (всё стандартными способами tkinter)
    root.form.configure(padx=padx, pady=pady)

    text = ScrolledText(root.form, wrap='word', height=10, width=40)
    text.pack(fill='both', expand=True)

    # применение стилей выбранной темы
    style_manager.apply(container=root.form)
    # отрисовка формы
    root.form.mainloop()


if __name__ == '__main__':
    ex1()
    # ex2()
    # ex3()
    # ex4()
    # ex5()
