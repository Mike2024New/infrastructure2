from tkinter import ttk
from infrastructure_tk_ui import RootWidget, CheckboxWidgetTTK, RadiobuttonGroupTTK
from infrastructure_tk_ui.examples.ex0 import StyleManager

"""
Примеры построения основных виджетов, встроенными tkinter методами, и классами расширителями, а также применение стилей
Стили определены в ex0
"""


def ex1():
    """Создание checkbox-галочки выбора и кнопки для отслеживания состояния"""
    padx, pady = 3, 3
    root = RootWidget()
    # ВАЖНО! Активацию стилей делать только после создания root окна (иначе будет появляться второе окно)
    # активация стилей, их можно отключить при необходимости (флаги disable)
    style_manager = StyleManager(root=root.form)
    styles, styles_ttk = style_manager.set_style(tk_disable=False, ttk_disable=False, options_disable=False)
    root.form.configure(padx=padx, pady=pady, **styles.root)
    # создание чекбоксов - через вспомогательный класс, базовые методы (например configure и другие) доступны через .form (escape hatch)
    check_box = CheckboxWidgetTTK(parent=root.form, text='Добавить опцию', active=False)
    check_box.form.configure(style=styles_ttk.checkbutton)
    check_box.form.pack(expand=True, fill='x', anchor='center')

    # создание кнопок - обычным способом
    ttk.Button(
        root.form, text='cb1', command=lambda: print(check_box.get()), style=styles_ttk.button,
    ).pack(expand=True, fill='x', anchor='center', padx=padx)
    root.form.mainloop()


def ex2():
    """Пример создания простого диалогового окна label и две кнопки"""
    padx, pady = 3, 3
    root = RootWidget()
    # ВАЖНО! Активацию стилей делать только после создания root окна (иначе будет появляться второе окно)
    # активация стилей, их можно отключить при необходимости (флаги disable)
    style_manager = StyleManager(root=root.form)
    styles, styles_ttk = style_manager.set_style(tk_disable=False, ttk_disable=False, options_disable=False)
    root.form.configure(padx=5, pady=5, **styles.root)
    ttk.Label(text=f'Установить обновление?', style=styles_ttk.label).pack(
        fill='x', expand=True, padx=padx, pady=pady * 3)
    ttk.Button(text=f'Да', command=lambda: root.form.destroy()).pack(
        fill='x', expand=True, side='left', padx=padx, pady=pady)
    ttk.Button(text=f'Нет', command=lambda: root.form.destroy()).pack(
        fill='x', expand=True, side='left', padx=padx, pady=pady)
    root.form.mainloop()


def ex3():
    """Создание модального окна и обработка нажатия в нем"""
    padx, pady = 3, 3
    root = RootWidget()
    # ВАЖНО! Активацию стилей делать только после создания root окна (иначе будет появляться второе окно)
    # активация стилей, их можно отключить при необходимости (флаги disable)
    style_manager = StyleManager(root=root.form)
    styles, styles_ttk = style_manager.set_style(tk_disable=False, ttk_disable=False, options_disable=False)
    root.form.configure(padx=padx, pady=pady, **styles.root)

    def create_modal():
        """создается внешнее модальное окно, и кнопка которая закрывает его"""
        modal = RootWidget(parent=root.form, modal=True)
        ttk.Button(modal.form, text=f'close', command=lambda: modal.form.destroy()).pack()

    ttk.Button(text=f'Открыть', command=lambda: create_modal(), style=styles_ttk.button).pack(
        fill='x', expand=True, side='left', padx=padx, pady=pady)
    root.form.mainloop()


def ex4():
    """RadioButton группа кнопок"""
    padx, pady = 3, 3
    root = RootWidget()
    # ВАЖНО! Активацию стилей делать только после создания root окна (иначе будет появляться второе окно)
    # активация стилей, их можно отключить при необходимости (флаги disable)
    style_manager = StyleManager(root=root.form)
    styles, styles_ttk = style_manager.set_style(tk_disable=False, ttk_disable=False, options_disable=False)
    root.form.configure(padx=5, pady=5)
    root.form.configure(padx=padx, pady=pady, **styles.root)

    radio_buttons = RadiobuttonGroupTTK(parent=root.form, options=['en', 'ru', 'ge'], default_value='ru')
    for form in radio_buttons.form:
        form.configure(style=styles_ttk.radiobutton)
        form.pack()
    ttk.Button(text='get value', command=lambda: print(radio_buttons.get_value())).pack()
    root.form.mainloop()


def ex5():
    """Создание текстового поля (text area)"""
    padx, pady = 3, 3
    root = RootWidget()
    # ВАЖНО! Активацию стилей делать только после создания root окна (иначе будет появляться второе окно)
    # активация стилей, их можно отключить при необходимости (флаги disable)
    style_manager = StyleManager(root=root.form)
    styles, styles_ttk = style_manager.set_style(tk_disable=False, ttk_disable=False, options_disable=False)
    root.form.configure(padx=5, pady=5)
    root.form.configure(padx=padx, pady=pady, **styles.root)

    from tkinter.scrolledtext import ScrolledText

    text = ScrolledText(root.form, wrap='word', height=10, width=40)
    text.configure(**styles.textarea)
    text.pack(fill='both', expand=True)
    root.form.mainloop()


if __name__ == '__main__':
    # ex1()
    ex2()
    # ex3()
    # ex4()
    # ex5()
